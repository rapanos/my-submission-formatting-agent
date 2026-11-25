#!/usr/bin/env python3
"""
Export formatted markdown to docx using pandoc + reference template.

Usage:
    python scripts/export_docx.py outputs/journal/manuscript_formatted.md outputs/journal/manuscript_formatted.docx
    python scripts/export_docx.py outputs/journal/working.md outputs/journal/manuscript_formatted.docx --reference templates/reference.docx

    # Peer-review revision (/respond-to-reviewers): clean or yellow-highlighted
    python scripts/export_docx.py revisions/journal/R1/manuscript_revised.md revisions/journal/R1/manuscript_revised.docx --revisions clean
    python scripts/export_docx.py revisions/journal/R1/manuscript_revised.md revisions/journal/R1/manuscript_revised_highlighted.docx --revisions highlight
"""

import os
import re
import sys
import subprocess
import argparse
import tempfile
from pathlib import Path

try:
    import pypandoc as _pypandoc
    _PANDOC_BIN = _pypandoc.get_pandoc_path()
except Exception:
    _PANDOC_BIN = 'pandoc'


DEFAULT_REFERENCE = Path('templates/reference.docx')


DEFAULT_CSL_DIR = Path('templates/csl')


# ------------------------------------------------------------------------------
# Revision markers (used by /respond-to-reviewers)
#   inline:  ... <!-- REVISION R1-2 -->new text<!-- END REVISION --> ...
#   block:   <!-- REVISION R1-2 -->        (own line)
#            paragraph(s)
#            <!-- END REVISION -->         (own line)
# ------------------------------------------------------------------------------

REV_OPEN = re.compile(r'<!--\s*REVISION\s+([A-Za-z0-9.\-]+)\s*-->')
REV_CLOSE = re.compile(r'<!--\s*END REVISION\s*-->')
REV_INLINE = re.compile(r'<!--\s*REVISION\s+[A-Za-z0-9.\-]+\s*-->(.*?)<!--\s*END REVISION\s*-->')
# Line prefixes kept outside the highlight span: headings, list items, blockquotes
_PREFIX = re.compile(r'^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s*)*)(.*?)(\s*)$')
# Lines that must not be wrapped in a span
_NO_WRAP = re.compile(r'^\s*(\||\$\$|```|~~~|!\[|\[\^|<!--|:::|-{3,}\s*$|={3,}\s*$|\\begin|\\end)')


class RevisionMarkerError(ValueError):
    pass


def _check_markers(text: str) -> int:
    """Validate that revision markers are balanced and not nested. Returns count."""
    depth, count = 0, 0
    tokens = sorted(
        [(m.start(), 'open', m.group(1)) for m in REV_OPEN.finditer(text)]
        + [(m.start(), 'close', None) for m in REV_CLOSE.finditer(text)]
    )
    for pos, kind, rid in tokens:
        line = text.count('\n', 0, pos) + 1
        if kind == 'open':
            if depth:
                raise RevisionMarkerError(f'line {line}: nested REVISION marker ({rid})')
            depth, count = 1, count + 1
        else:
            if not depth:
                raise RevisionMarkerError(f'line {line}: END REVISION without opening marker')
            depth = 0
    if depth:
        raise RevisionMarkerError('unclosed REVISION marker at end of file')
    return count


def _mark_line(line: str) -> str:
    if not line.strip() or _NO_WRAP.match(line):
        return line
    m = _PREFIX.match(line)
    prefix, body, trail = m.group(1), m.group(2), m.group(3)
    if not body:
        return line
    return f'{prefix}[{body}]{{.mark}}{trail}'


def apply_revision_markers(text: str, mode: str) -> str:
    """mode='clean': drop markers. mode='highlight': wrap marked text in [..]{.mark}
    (pandoc renders .mark spans as yellow highlight in docx)."""
    _check_markers(text)
    if mode == 'clean':
        text = REV_OPEN.sub('', text)
        return REV_CLOSE.sub('', text)

    # Inline markers first (open and close on the same line)
    def _inline(m):
        inner = m.group(1)
        return f'[{inner}]{{.mark}}' if inner.strip() else inner
    out_lines, inside = [], False
    for line in text.split('\n'):
        line = REV_INLINE.sub(_inline, line)
        has_open, has_close = bool(REV_OPEN.search(line)), bool(REV_CLOSE.search(line))
        if has_open and not inside:
            before, after = REV_OPEN.split(line, maxsplit=1)[0], REV_OPEN.split(line, maxsplit=1)[2]
            inside = True
            if before.strip():
                out_lines.append(before.rstrip())
            line = after
            if not line.strip():
                continue
        if inside and has_close:
            before, after = REV_CLOSE.split(line, maxsplit=1)
            if before.strip():
                out_lines.append(_mark_line(before))
            inside = False
            if after.strip():
                out_lines.append(after)
            continue
        out_lines.append(_mark_line(line) if inside else line)
    return '\n'.join(out_lines)


def export_docx(
    source: Path,
    output: Path,
    reference_doc: Path = DEFAULT_REFERENCE,
    mathml: bool = True,
    bibliography: 'Path | None' = None,
    csl: 'Path | None' = None,
    revisions: 'str | None' = None,
) -> bool:
    """Convert markdown to docx using pandoc. Returns success bool.

    revisions: None (default, file passed to pandoc unchanged), 'clean' (strip
    revision markers) or 'highlight' (yellow-highlight text inside markers).
    """
    if not source.exists():
        print(f"Error: Source file not found: {source}", file=sys.stderr)
        return False

    tmp_path = None
    pandoc_source = source
    if revisions:
        text = source.read_text(encoding='utf-8')
        try:
            n = _check_markers(text)
            text = apply_revision_markers(text, revisions)
        except RevisionMarkerError as e:
            print(f"Error: revision markers in {source}: {e}", file=sys.stderr)
            return False
        fd, tmp = tempfile.mkstemp(suffix='.md', prefix='revision_')
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(text)
        tmp_path = Path(tmp)
        pandoc_source = tmp_path
        print(f"Revisions: {revisions} ({n} marked change(s))")
    try:
        return _run_pandoc(source, pandoc_source, output, reference_doc, mathml,
                           bibliography, csl)
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)


def _run_pandoc(source: Path, pandoc_source: Path, output: Path, reference_doc: Path,
                mathml: bool, bibliography, csl) -> bool:

    if not reference_doc.exists():
        print(f"Warning: Reference doc not found at {reference_doc}.", file=sys.stderr)
        print("To create a default reference: pandoc --print-default-data-file reference.docx > templates/reference.docx", file=sys.stderr)
        print("Proceeding without reference doc (pandoc default styles will be used).", file=sys.stderr)
        ref_args = []
    else:
        ref_args = ['--reference-doc', str(reference_doc)]

    # Create output directory if needed
    output.parent.mkdir(parents=True, exist_ok=True)

    # Use --mathml so LaTeX math converts to native OOXML equations in .docx
    math_args = ['--mathml'] if mathml else []

    # Citation processing: --citeproc resolves [@key] citations using a .bib + .csl
    cite_args = []
    if bibliography:
        if not bibliography.exists():
            print(f"Warning: Bibliography file not found: {bibliography}", file=sys.stderr)
        else:
            cite_args.extend(['--citeproc', '--bibliography', str(bibliography)])
            if csl:
                if not csl.exists():
                    print(f"Warning: CSL file not found: {csl}", file=sys.stderr)
                else:
                    cite_args.extend(['--csl', str(csl)])
                    print(f"Citation style: {csl.stem}")

    cmd = [
        _PANDOC_BIN,
        '--from', 'markdown',
        '--to', 'docx',
        *ref_args,
        *math_args,
        *cite_args,
        '--output', str(output),
    ]
    if pandoc_source != source:
        # temp copy lives elsewhere: keep image paths resolving as before
        cmd.append('--resource-path=' + os.pathsep.join(['.', str(source.parent)]))
    cmd.append(str(pandoc_source))

    print(f"Exporting: {source}")
    print(f"Output: {output}")
    if ref_args:
        print(f"Reference: {reference_doc}")
    if cite_args:
        print(f"Bibliography: {bibliography}")
        print("Citations: will be resolved via citeproc")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"Error: pandoc failed:\n{result.stderr or result.stdout}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("Error: pandoc timed out (>120s)", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: pandoc not found. Install pandoc: https://pandoc.org/installing.html", file=sys.stderr)
        return False

    if output.exists():
        size_kb = output.stat().st_size / 1024
        print(f"Success: {output.name} ({size_kb:.1f} KB)")
        if mathml:
            print("MathML: enabled (LaTeX math -> native OOXML equations)")
        if size_kb < 5:
            print("Warning: Output file is very small — check for conversion issues.", file=sys.stderr)
        return True
    else:
        print("Error: Output file was not created.", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert formatted markdown to docx via pandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/export_docx.py outputs/lancet/manuscript_formatted.md outputs/lancet/manuscript_formatted.docx
  python scripts/export_docx.py outputs/nejm/working.md outputs/nejm/out.docx --reference templates/custom.docx

Setup (first time):
  pandoc --print-default-data-file reference.docx > templates/reference.docx

The reference.docx defines heading styles, fonts, and margins for the output.
Customize it in Word, then save to templates/reference.docx.
        """
    )
    parser.add_argument('source', type=Path, help='Input markdown file')
    parser.add_argument('output', type=Path, help='Output docx file')
    parser.add_argument(
        '--reference', type=Path, default=DEFAULT_REFERENCE,
        help=f'Reference docx template (default: {DEFAULT_REFERENCE})'
    )
    parser.add_argument(
        '--no-mathml', action='store_true', default=False,
        help='Disable MathML conversion (LaTeX math stays as images/text instead of native OOXML)'
    )
    parser.add_argument(
        '--bibliography', type=Path, default=None,
        help='Path to .bib file — enables --citeproc to resolve [@key] citations'
    )
    parser.add_argument(
        '--csl', type=Path, default=None,
        help='Path to .csl citation style file (e.g. templates/csl/pnas.csl). '
             'Without this, pandoc uses its default Chicago author-date style.'
    )

    parser.add_argument(
        '--revisions', choices=['clean', 'highlight'], default=None,
        help='Handle <!-- REVISION id --> ... <!-- END REVISION --> markers '
             '(from /respond-to-reviewers): "clean" strips them, "highlight" '
             'renders the marked text with yellow highlight.'
    )

    args = parser.parse_args()
    success = export_docx(
        args.source, args.output, args.reference,
        mathml=not args.no_mathml,
        bibliography=args.bibliography,
        csl=args.csl,
        revisions=args.revisions,
    )
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
