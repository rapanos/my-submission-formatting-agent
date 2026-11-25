# Session Log: 2026-11-24 -- Add /respond-to-reviewers skill

**Status:** COMPLETED

## Objective
Add peer-review revision support (point-by-point response letter, approved manuscript edits, highlighted docx) consistent with the repo's quality gates. Merges pedrohcgs `respond-to-referees` and Aperivue medsci `revise` (both MIT).

Plan: `quality_reports/plans/2026-11-24_respond-to-reviewers-skill.md`

## Design Decisions

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| Author approves every manuscript edit; edits live only in `revisions/[j]/R[n]/manuscript_revised.md` | letter-only; auto-edit | Keeps "never alter scientific content" as a bounded, auditable exception |
| Clean + yellow-highlighted docx | true tracked changes | Achievable with pandoc pipeline; tracked changes needs Word Compare |
| Vendor `check_response_claims.py` (MIT, stdlib) | rewrite | Deterministic, tested upstream |
| `revisions/` gitignored | committed | Reviewer reports are confidential, like manuscripts/ and outputs/ |

## Incremental Work Log

- Push of local work to fork `rapanos` done (remote `rapanos`, main tracks it).
- Plan approved; implementation started.
- Pandoc 3.14 renders `[..]{.mark}` spans as yellow highlight in docx, so python-docx post-processing is not needed.
- Fabricated-claim and unapproved-edit deductions raised from 15 to 25: at 15 a fabricated claim still passed the commit gate (85).
- Found a pre-existing problem: PyYAML is not installed, so `--journal` checks were skipped without saying why. The scorer now prints the real reason.

## Verification Results

| Check | Result | Status |
|-------|--------|--------|
| check_response_claims on fixture (exact quotes) | OK, exit 0 | PASS |
| check_response_claims with fabricated quote | 1 major, exit 1 | PASS |
| export --revisions clean / highlight | 0 / 7 highlight runs, no marker text in docx | PASS |
| unclosed REVISION marker | export refuses, exit 1 | PASS |
| --rubric response: fixture / fabricated / missing+unapproved | 100 / 75 / 60 | PASS |
| Regression: export of outputs/geoheritage/working.md old vs new | document.xml identical | PASS |
| Regression: --rubric manuscript score unchanged | 100 = 100 | PASS |

## Open Questions / Blockers

- [ ] `pip install pyyaml` so journal word-cap checks run
- [ ] The real Geoheritage decision letter is needed to run R1

**Status:** COMPLETED (implementation); awaiting real reviewer comments
