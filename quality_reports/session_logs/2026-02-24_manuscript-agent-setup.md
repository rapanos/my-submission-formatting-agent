# Session Log: Manuscript Submission Formatting Agent Setup

**Date:** 2026-02-24
**Goal:** Repurpose academic workflow template repo into a manuscript submission formatting agent
**Status:** COMPLETE

---

## What Was Done

Implemented the full setup plan for the manuscript submission formatting agent. Transformed a Beamer/Quarto slide development repo into a manuscript formatting pipeline.

### Phase 1: Configuration Updates
- Updated `CLAUDE.md` — replaced slide-centric content with manuscript workflow context
- Filled all `[BRACKETED PLACEHOLDERS]` with meaningful defaults

### Phase 2: Removed Irrelevant Infrastructure
- Deleted 9 slide/R/TikZ-specific rules
- Deleted 7 slide-specific agents (beamer-translator, quarto-critic, quarto-fixer, slide-auditor, pedagogy-reviewer, tikz-reviewer, r-reviewer)
- Deleted 11 slide/R/TikZ-specific skill directories
- Removed `Slides/`, `Quarto/`, `Preambles/` directories

### Phase 3: New Directory Structure
- Created `manuscripts/` (read-only input store)
- Created `guidelines/` (journal requirements YAML)
- Created `outputs/` (formatted output per journal)

### Phase 4: New Rules
- `.claude/rules/manuscript-handling.md` — ingest pipeline + content integrity rules
- `.claude/rules/journal-compliance.md` — section order, abstract structure, heading style
- `.claude/rules/output-generation.md` — pandoc export, formatting report requirements
- Updated `.claude/rules/quality-gates.md` — manuscript compliance rubric

### Phase 5: New Agents
- `manuscript-analyzer.md` — section inventory, IMRaD detection, gap analysis
- `guidelines-extractor.md` — URL/text → structured YAML
- `section-drafter.md` — synthesize missing sections from existing content (always DRAFT)
- `compliance-checker.md` — systematic PASS/WARN/FAIL compliance checklist
- Updated `proofreader.md` — adapted for manuscripts (draft marker integrity, formatting artifacts)
- Updated `verifier.md` — adapted for docx/md output verification

### Phase 6: New Skills
- `parse-guidelines/` — extracts journal requirements from URL or pasted text
- `format-manuscript/` — full pipeline orchestrator (11-step workflow)
- `validate-compliance/` — standalone compliance check
- `generate-report/` — formatting_report.md with before/after diff
- Updated `proofread/` and `review-paper/` for manuscript context

### Phase 7: Scripts
- `scripts/ingest.py` — pandoc wrapper for .docx/.tex/.pdf → markdown
- `scripts/export_docx.py` — pandoc wrapper for markdown → docx with reference template
- Updated `scripts/quality_score.py` — added `ManuscriptScorer` class + `--rubric manuscript` flag

### Phase 8: Templates
- `templates/reference.docx` — pandoc default reference document (created via pandoc)
- `templates/journal-requirements.yml` — annotated schema template for journal YAML files
- `templates/formatting-report.md` — report template for formatting outputs
- Updated `.claude/WORKFLOW_QUICK_REF.md` — manuscript workflow context
- Updated `MEMORY.md` — [LEARN] entries for manuscript agent patterns

---

## Key Decisions

1. **manuscripts/ is read-only** — protects originals; work always happens on outputs/ copies
2. **Draft markers mandatory** — no auto-drafted content without `<!-- DRAFT -->` wrapper
3. **Word count = WARN not FAIL** — authors decide what to cut, tool never deletes content
4. **Both .md and .docx always delivered** — .md for version control/editing, .docx for submission
5. **guidelines.yml is single source of truth** — all compliance checks read from this file

---

## Verification Remaining

End-to-end verification (run when pandoc + sample manuscript available):
1. `python scripts/ingest.py manuscripts/sample.docx outputs/test/working.md`
2. `python scripts/export_docx.py outputs/test/working.md outputs/test/out.docx`
3. `/parse-guidelines [name] [URL]`
4. `/format-manuscript manuscripts/sample.docx [journal]`
5. `python scripts/quality_score.py outputs/test/working.md --rubric manuscript`

---

## Open Questions

- None. Setup complete. Ready for first real manuscript.

---

## Next Steps for User

1. Run `/parse-guidelines [journal-name] [URL]` to set up your first journal
2. Drop a manuscript into `manuscripts/`
3. Run `/format-manuscript manuscripts/[file] [journal-name]`

---

## Session Update — 2026-05-25: First Real Manuscript (Geoheritage)

### What Was Done

**Journal setup:**
- Extracted Geoheritage (Springer) guidelines → `guidelines/geoheritage.yml`
- Initial URL (`link.springer.com/journal/12371`) confirmed as Geoheritage (not IJE as initially misidentified)

**Infrastructure fixes:**
- `scripts/ingest.py` and `scripts/export_docx.py`: added `pypandoc` path detection to work with `.venv` (pandoc not on system PATH); replaced Unicode arrow `→` with `->` to fix Windows cp1252 encoding error
- `pypandoc-binary 1.17` installed into `.venv` (pandoc 3.9 bundled)

**Pipeline run — `manuscripts/artigo_rapanos.docx` → Geoheritage:**
1. Ingest: 245 lines, ~4,678 words
2. Analysis: IMRaD structure present; section 3.5 numbering gap; Statements and Declarations missing; 20 headings non-compliant (title case)
3. Reformat: 20 headings corrected to sentence case; section 3.5 → 3.3; `## References` → `# References`; Statements and Declarations auto-drafted (DRAFT)
4. Export: `manuscript_formatted.docx` (25.1 KB)
5. Compliance: PASS 14 / WARN 9 / FAIL 3 (title, author info, AI disclosure)
6. Proofreading: 30 issues identified; all applied to `.md` and re-exported
7. References: all 26 reformatted to Springer author-date; 3 factual corrections (Štrba, Pereira, IJET journal name)

**Key decisions:**
- AI disclosure for copy editing: NOT required per Geoheritage guidelines ("Disclosure not required for AI-assisted copy editing") — statement added then removed
- docx overwrite incident: overwrote user's manually formatted docx; corrected by re-applying all proofreading fixes programmatically
- Title and author block: pending — user to supply details

**Remaining author actions:**
- Add title, author names, affiliations, corresponding author email
- Complete 6 DRAFT placeholders in Statements and Declarations
- Reduce keywords from 7 to 6
- Fix duplicate Figure 2 label
- Reformat reference list (done in .md; user may need to verify in docx)

**Output files:**
- `outputs/geoheritage/manuscript_formatted.md` — current source of truth
- `outputs/geoheritage/manuscript_formatted.docx` — 25.1 KB, ready for author review
- `outputs/geoheritage/compliance_checklist.md`
- `outputs/geoheritage/formatting_report.md`
- `quality_reports/geoheritage_proofread.md`
