# Plan: Geoheritage R1 revision for GEOH-D-26-00196 ("GeoparkCraft…")

## Context
The Geoheritage review came back as **major revision**, with one reviewer and 28 comments: 3 general and 25 line-by-line or about figures. Inputs:
- the reviewer report `C:\Users\earap\Downloads\Review_Rapanos_and_Valdati-2026.docx`
- the submitted PDF `C:\Users\earap\Downloads\GEOH-D-26-00196.pdf`, with line numbers the reviewer cites as page/line

We run the new `/respond-to-reviewers` workflow (`.claude/skills/respond-to-reviewers/SKILL.md`, rule `.claude/rules/revision-handling.md`) to produce the revised manuscript, the response letter, the cover letter and the docx files.

**User decisions:**
- Baseline R0 is `outputs/geoheritage/manuscript_formatted_v2.md`. It must first be checked against the PDF.
- Cultural heritage: **change the title** rather than add a section.
- Facts only the author knows are collected through a **Portuguese questionnaire**.
- Figures: the author redraws them from a checklist. Claude handles captions, numbering, placement and the letter.

## Step 1: Set up `revisions/geoheritage/R1/` (gitignored)
- `decision_letter.md`: the reviewer docx converted with `scripts/ingest.py`, verbatim.
- `manuscript_R0.md`: a copy of `manuscript_formatted_v2.md`. First diff its prose against the PDF text (`pdftotext`, or by reading pages); report any mismatch before going on.
- `manuscript_revised.md`: a copy of R0.

## Step 2: Comment matrix (GATE 1: user confirms)
Proposed numbering and classification. Page/line refer to the submitted PDF.

| ID | Type | Topic | Proposed handling |
|---|---|---|---|
| R1-1 | MAJ | Objective limited to MAB; reframe as a generic workflow with MAB as the case study (also L22-39, p2 L40-42) | Rewrite the objective in the abstract and the last Intro paragraph, and change the **title**. Text drafted by Claude. |
| R1-2a | MAJ | Map of all fieldwork observations (also p5 L38) | **Figure by author**; Claude adds the caption, the in-text call and a renumbered figure |
| R1-2b | MAJ | Scale: block = ? m, vertical exaggeration, how defined, 1 m DEM vs block, coarser DEMs? | New Methods paragraph from **questionnaire** answers; numbers tagged `[AUTHOR: VERIFY NUMBER]` |
| R1-2c | MAJ | Section on how people and institutions access the world | New subsection 2.2.4 "Deployment and access", from the questionnaire |
| R1-3 | MAJ | Title says cultural heritage, but the text barely covers it | Change the title (user decision); in the letter, point to the existing cultural elements (historian NPC, Sect. 4.5) |
| R1-4 | MIN | p1 L22-39: make the abstract objective clearer | Covered with R1-1 |
| R1-5 | MIN | p1 L54-59: add Ghiraldi 2014, Lemaire 2026, Pasquaré Mariotto & Bonali 2021, Perotti 2020 | Add citations and reference entries (DOIs supplied by reviewer) |
| R1-6 | MIN | p1 L58-59: "serious games" → "educational video games" | Adopt "educational (didactic) video games". **Author may prefer to keep the established term**, so confirm at the gate |
| R1-7 | MIN | p2 L9: cite Lemaire 2026 for virtual geotrips | Add citation |
| R1-8 | MIN | p2 L40-42: objective sentence | Covered with R1-1 |
| R1-9 | MIN | p2 L44: references for the geopark and geosites | Candidates already in the list: Rapanos et al. 2022, dos Santos 2021; plus any geopark dossier from the author (questionnaire) |
| R1-10 | MAJ | Intro lacks a study-area description and geological context | New "Study area" paragraph drafted from facts already in the paper (Rio do Rasto and Botucatu Fms, relief compartments, Fenda da Raia), **verified by the author** |
| R1-11 | MIN | p5 L16: state the CRS once | Edit: say once at the start of 2.1.1, remove the other mentions |
| R1-12 | MIN | p5 L23: cite the DEM provider (SDS/SC) | Reference details from the questionnaire |
| R1-13 | MIN | p6 L19: rewrite "This stage utilized…" | Direct edit |
| R1-14 | MIN | p6 L28: why WorldPainter | Questionnaire |
| R1-15 | MAJ | p6 L28: justify the 656×656 grid ("optimize navigation"?) | Questionnaire (performance, area extent) |
| R1-16 | MIN | p6 L44: why Forge | Questionnaire |
| R1-17 | MIN | p6 L45: define MODs at first use | Direct edit: "modifications (mods), user-created add-ons that…" |
| R1-18 | MIN | p7 L32: don't spell out DEM again | Direct edit |
| R1-19 | MAJ | p7 L32-34: why features are absent from the DEM; how they were modelled by hand | Questionnaire (size vs resolution, field measurements, photos) |
| R1-20 | MIN | p7 L37-46: detail the vegetation classes; field vs in-game photo figure | Text from the questionnaire (CONAMA classes) + optional figure by the author |
| R1-21 | MIN | p8 L56: justify structures; give a panel letter per item, in order | Edit the list with figure panels. The **author maps items to panels**, because Fig. 4 panels don't match the list |
| R1-22 | MIN | p13 L32: add "exploration" | Direct edit |
| R1-23 | MIN | Fig. 1: English legend, north arrow and scale inside the map, zoom inset, "Rapanos and Valdati (2021)" | Figure by author; caption fixed by Claude. **Note:** the reference list has *Rapanos, Valdati, Gomes (2022)*, not 2021, so the author must resolve the mismatch |
| R1-24 | MIN | Fig. 2: text says 3 stages, figure shows 2; remove the grey box | Change the text to the two stages that match sections 2.1 and 2.2; the author removes the box |
| R1-25 | MIN | Fig. 3: enlarge a–c, full page, fuller caption | Figure by author; expanded caption drafted by Claude |
| R1-26 | MIN | Fig. 5: show an NPC conversation (e.g. panel g) | Screenshot by author; caption updated |
| R1-27 | MIN | Fig. 6 belongs in Methods | Move it into 2.2. **Also fix:** its caption reads "Figure 5. GeoparkCraft cover", a duplicate number, so renumber all figures |

### Images the author supplied (2026-11-24)
- **New figure "Field vs in-game comparison"** answers R1-20 (the reviewer asked for field and in-game photos) and gives visual evidence for R1-19 (hand-modelled features) and R1-2b (scale and exaggeration). Sources: `...\grafica\plate_corew\comparacao1.png` (ruiniform pinnacles) and `comparacao2.png` (sandstone escarpment).
  - Place it in Results 3.1, after the paragraph on features absent from the DEM.
  - Combine into one 4-panel plate: a/b escarpment, c/d pinnacles.
  - The caption must explain the block choice (Botucatu Fm as Red Sandstone, a symbolic colour). The facts it needs (photo source/date, location, in-game coordinates) go in the questionnaire.
- **NPC dialogue** answers R1-26. Sources: `...\screenshots\2023-03-11_11.33.51.png` (start of the conversation) and `11.33.30.png` (continuation), both with Jairo at the observation deck.
  - Replace panel **g** of Fig. 5, as the reviewer suggested.
  - Build one panel with the two crops stacked in chronological order, and drop the player line that appears twice.
  - The dialogue is in Portuguese, so the caption gives an English translation.
  - Because the dialogue panel replaces Eduardo's g, the "Eduardo (Geologist)" entry in the text's NPC list needs a decision: keep it in the text without a picture, or move it to another panel.

Extra issues found during the read, outside the reviewer's comments and to be flagged to the author:
- the duplicate "Figure 5" label
- the Fig. 1 citation does not match the reference list
- the Salazar-Del-Pozo 2025 entry says "Land 15:43", but its DOI is a *Geosciences* one

## Step 3: Author questionnaire (Portuguese)
`revisions/geoheritage/R1/questionario_autor.md`: one short, objective question per item (R1-2b, 2c, 9, 12, 14, 15, 16, 19, 20, 21, 23 and the extra issues), each naming the comment it answers. Example questions:
- "Quantos metros equivale 1 bloco (horizontal)?"
- "Qual exagero vertical (×)?"
- "Por que WorldPainter e não Terra++/WorldMachine?"

Edits that don't depend on answers go ahead in parallel.

## Step 4: Proposals and approval (GATE 2)
In `comment_matrix.md`, give each item its exact old → new text in English, in the manuscript's register. Present them in batches, in this order:
1. direct edits
2. the objective/title reframe
3. the new paragraphs from questionnaire answers
4. figure captions and numbering

The user approves YES / NO / EDITED. Scientific-content edits are tagged `[AUTHOR REVIEW REQUIRED]`.

## Step 5: Apply, draft, verify, export (per the skill)
- Apply approved edits in `manuscript_revised.md` inside `<!-- REVISION R1-n -->` markers. Add the new references to the reference list in the existing Springer author-year style.
- Write `response_to_reviewers.md` (English; voice guide `templates/references/r2r_voice.md`), `cover_letter.md` and `change_log.md`.
- Write `figure_checklist.md` (Portuguese) with exact instructions per figure: what to change, and the new number and caption.
- Verify:
  - `python scripts/check_response_claims.py … --strict`
  - the `claim-verifier` agent (fresh context, without the letter)
  - `python scripts/quality_score.py …response_to_reviewers.md --rubric response`, which must reach ≥ 90
  - `--rubric manuscript --journal geoheritage` on the revised manuscript (`pip install pyyaml` first, with the user's OK, so the word-cap check runs)
- Export with `scripts/export_docx.py`: `manuscript_revised.docx` (`--revisions clean`), `manuscript_revised_highlighted.docx` (`--revisions highlight`), and `response_to_reviewers.docx`.

## Verification
- R0 matches the PDF text, with no unexplained differences.
- Every one of the 28 matrix IDs has a letter block; the score is ≥ 90; check_response_claims reports 0 major findings; the verifier reports 0 FAIL.
- Open the highlighted docx and confirm only the approved changes are yellow.
- Final message lists the remaining BLOCKED items: figures, plus any unanswered questionnaire items.
- Session log in `quality_reports/session_logs/2026-11-24_geoheritage-R1.md`.
