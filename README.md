[![DOI](https://zenodo.org/badge/1165646565.svg)](https://doi.org/10.5281/zenodo.19026694)

# Manuscript Submission Formatting Agent

*在 Vibe Research 时代，让 Agent 处理投稿格式，而让研究者专注于科学问题。*

A structured Claude Code workflow to reformat research manuscripts for any journal's submission requirements — without altering scientific content, created by **朱晨 | 遗传社科研究** https://zhuchencau.wordpress.com/cv 
Special thanks to Pedro H. C. Sant'Anna for the claude-code-my-workflow repository, which inspired this workflow. 

Designed for Claude Code; scripts and guidelines are usable standalone with any LLM.


## 中文简介

该Agent解决的是科研流程中一个无聊且耗时的问题：**投稿格式整理（submission formatting）**。

在学术论文投稿过程中，不同期刊往往有各自复杂且细碎的格式要求，例如：

- 是否需要 **结构化摘要（structured abstract）**
- 各章节的 **顺序与标题规范**
- **引用格式**（author–year / Vancouver / superscript 等）
- 是否必须包含 **Key Messages / Declarations / Ethics / Data availability**
- 不同的 **字数限制与标题样式**

当论文被拒稿后转投新期刊时，研究者通常需要花费 **数小时甚至更久** 来重新整理稿件格式——而这些工作 **并不会增加任何新的学术价值**。

**Manuscript Submission Formatting Agent** 的目标就是自动完成这一过程。

该工具基于 **Claude Code 工作流**，能够：

- 自动解析目标期刊的 **Author Guidelines**
- 分析论文结构并进行 **章节重排**
- 自动补充 **期刊要求但缺失的投稿部分**
- 调整 **引用格式、标题格式与章节结构**
- 输出 **符合期刊投稿要求的 Word 手稿**

整个系统遵循一个核心原则：

> **只调整格式，不改变科研内容。**

该工具 **不会修改论文中的数据、结果或结论**。  

## 输入 / 输出

**输入**

- 原始论文文件  
  - `.docx`
    或
  - `.tex`
  - `.pdf`
  - `.bib`
- 目标期刊名称或 Author Guidelines URL

**输出**

- 符合投稿格式的 `.docx` 手稿
- Markdown 版本（便于版本控制与编辑）
- 投稿要求 **合规检查表（compliance checklist）**
- **格式修改报告（formatting report）**

**Last Updated:** 2026-03-15

---

## The problem

Every journal has different formatting requirements: structured abstracts, specific section ordering, heading styles, citation formats, word limits, required declarations. Reformatting a manuscript for a new journal — or after a rejection — is tedious, error-prone, and takes hours of work that adds zero scientific value.

## The solution

Give this agent your manuscript and a journal's author guidelines URL. It parses the requirements, restructures your paper to comply, auto-drafts any missing required sections (clearly marked for your review), and delivers a submission-ready `.docx` with a compliance report.

**What it never does:**
- Alter your scientific content (numbers, results, citations, conclusions)
- Silently add text — all auto-drafted sections are visibly marked `<!-- DRAFT: requires author review -->`
- Cut content to meet word limits — those are flagged as warnings for you to decide

> **Privacy:** `manuscripts/` and `outputs/` are gitignored. Your manuscripts never leave your machine or get pushed to GitHub.

## 隐私与数据安全

你的论文 **不会离开本地电脑**。

在本仓库中：


manuscripts/

outputs/


两个目录都被 `.gitignore` 忽略，因此：

- 不会被上传到 GitHub
- 不会进入远程仓库
- 所有处理均在 **本地完成**
---

## Quick start

### 1. Clone and open

```bash
git clone https://github.com/maxwell2732/my-submission-formatting-agent.git
cd my-submission-formatting-agent
claude
```

### 2. Set up a journal (one-time per journal)

```
/parse-guidelines ije https://academic.oup.com/ije/pages/general_instructions
```

This fetches the author guidelines and saves structured requirements to `guidelines/ije.yml`.

> **Tip:** If the journal's website blocks automated access (403 error), paste the guidelines text when prompted — the agent will extract requirements from the pasted content instead.

### 3. Format your manuscript

Drop your manuscript into `manuscripts/`, then:

```
/format-manuscript manuscripts/my_paper.docx ije
```

The agent will ingest your manuscript, analyse its structure, reformat it to comply with the journal's requirements, and deliver:

| Output file | What it is |
|-------------|-----------|
| `outputs/ije/manuscript_formatted.docx` | Submission-ready Word document |
| `outputs/ije/manuscript_formatted.md` | Markdown version (for version control and editing) |
| `outputs/ije/compliance_checklist.md` | PASS/WARN/FAIL for every journal requirement |
| `outputs/ije/formatting_report.md` | Summary of every change made + required author actions |

### 4. Review and submit

Open the formatting report, complete any DRAFT sections, address warnings, and submit.

---

## What it handles

The formatting pipeline (`/format-manuscript`) runs 11 steps automatically:

1. **Ingest** — converts .docx, .tex, or .pdf to normalised markdown via pandoc
2. **Analyse structure** — identifies sections, detects IMRaD structure, compares against journal requirements
3. **Reorder sections** — moves sections to match the journal's required order
4. **Rename headings** — applies the journal's heading naming convention and case style
5. **Restructure abstract** — converts to the journal's required structured format (e.g., Background/Methods/Results/Conclusions)
6. **Draft missing sections** — synthesises content for required sections that are absent (Key Messages, Declarations, etc.)
7. **Convert citations** — adjusts citation format (e.g., author-year to Vancouver superscript)
8. **Export** — produces `.docx` using a reference template and `.md` for version control
9. **Compliance check** — PASS/WARN/FAIL checklist for every journal requirement
10. **Quality score** — 0-100 compliance score (80 = acceptable, 90 = delivery-ready)
11. **Proofread** — grammar, typos, consistency, draft marker integrity

---

## Supported input formats

| Format | Quality | Notes |
|--------|---------|-------|
| `.tex` (LaTeX) | Best | Preserves structure, equations, citations |
| `.docx` (Word) | Good | Standard manuscript format |
| `.pdf` | Acceptable | Lossy conversion — review output carefully |

### MathType / OMML equation support

LaTeX math in your manuscript (`$...$`, `$$...$$`, `\begin{equation}`) is automatically converted to native Word (OOXML/MathType-compatible) equations in the exported `.docx`. This uses pandoc's `--mathml` flag, enabled by default.

- Equations render as editable Word equations, not images
- Compatible with MathType and Word's built-in equation editor
- To disable (e.g., if you prefer image-based math): pass `--no-mathml` to the export script

The ingest script also supports a `--bibliography` flag to override the `.bib` file path when the source `.tex` references a different filename than what's on disk.


---

## All commands

| Command | What it does |
|---------|-------------|
| `/parse-guidelines [name] [URL]` | Extract journal requirements → `guidelines/[name].yml` |
| `/format-manuscript [file] [journal]` | Full formatting pipeline |
| `/validate-compliance [file] [journal]` | Standalone compliance check on any formatted file |
| `/generate-report [journal]` | Generate formatting report with before/after diff |
| `/respond-to-reviewers [letter] [journal] [round]` | Peer-review revision: response letter, approved edits, highlighted docx |
| `/proofread [file]` | Grammar, typos, draft marker check |
| `/review-paper [file]` | Substantive manuscript review (argument, methods, referee objections) |
| `/validate-bib` | Cross-reference citations against bibliography |
| `/devils-advocate` | Challenge formatting decisions |
| `/commit [msg]` | Stage, commit, push |

---

## Responding to reviewers

After peer review, `/respond-to-reviewers` turns the decision letter into a complete revision package. It follows the same rules as formatting: nothing scientific changes without the author's approval.

1. **Parse and classify.** Every comment gets an ID (`E-1`, `R1-1`, `R1-3a`), a type (MAJ / MIN / REB) and a triage category. **You confirm the classifications** before anything else happens.
2. **Propose, then approve.** For each comment the agent proposes an exact old → new edit, or a rationale for deferring or disagreeing. Requests for new data, analyses or figures are marked `BLOCKED — author must supply`; numbers are never invented.
3. **Apply approved edits only.** Approved edits go into `revisions/[journal]/R1/manuscript_revised.md`, wrapped in `<!-- REVISION R1-2 -->` markers. The original manuscript and the version the reviewers saw stay untouched.
4. **Draft the letters.** You get a point-by-point response, a cover letter (R1) and a change log, all marked DRAFT.
5. **Verify.** `check_response_claims.py` confirms that every text quoted as "now reads…" exists in the revised manuscript. A separate `claim-verifier` agent, which never sees the draft letter, checks every claimed change.
6. **Export and score.** Outputs are a clean `.docx`, a `.docx` with the changes highlighted in yellow, and a `--rubric response` score that must reach 80/90.

```
/respond-to-reviewers revisions/geoheritage/R1/decision_letter.md geoheritage R1
```

`revisions/` is gitignored, because reviewer reports are confidential.

> **PT:** Depois da revisão por pares, `/respond-to-reviewers` organiza e classifica os comentários e propõe as mudanças para você aprovar. Só aplica as aprovadas, numa cópia marcada. Depois escreve a carta de resposta ponto a ponto, confere cada afirmação da carta contra o manuscrito e gera o .docx limpo e o .docx com as mudanças em amarelo.

The workflow is adapted from [Aperivue/medsci-skills `revise`](https://github.com/Aperivue/medsci-skills) and [pedrohcgs/claude-code-my-workflow `respond-to-referees`](https://github.com/pedrohcgs/claude-code-my-workflow), both MIT (see `scripts/THIRD_PARTY_LICENSES.md`).

---

## What's included

<details>
<summary><strong>8 agents, 13 skills, 13 rules, 4 hooks</strong> (click to expand)</summary>

### Agents (`.claude/agents/`)

| Agent | What it does |
|-------|-------------|
| `manuscript-analyzer` | Section inventory, IMRaD detection, gap analysis vs. journal requirements |
| `guidelines-extractor` | URL or pasted text → structured `guidelines/[journal].yml` |
| `section-drafter` | Synthesises missing required sections from existing manuscript content (always marks DRAFT) |
| `compliance-checker` | PASS/WARN/FAIL checklist for every journal requirement |
| `proofreader` | Grammar, typos, draft marker integrity, formatting artifacts |
| `verifier` | Checks output files exist, are valid, and quality score passes |
| `claim-verifier` | Fresh-context check that every change a response letter claims is really in the revised manuscript |
| `domain-reviewer` | **Template** — customise for your field's substance review |

### Rules (`.claude/rules/`)

**Always-on:**

| Rule | What it enforces |
|------|-----------------|
| `plan-first-workflow` | Plan mode for non-trivial tasks + context preservation |
| `orchestrator-protocol` | Contractor mode: implement → verify → review → fix → score |
| `session-logging` | Post-plan, incremental, and end-of-session logs |
| `meta-governance` | What belongs in the repo vs. gitignored |

**Path-scoped** (load only when working on matching files):

| Rule | Triggers on | What it enforces |
|------|------------|-----------------|
| `manuscript-handling` | `manuscripts/`, `outputs/` | Ingest pipeline, content integrity, draft markers |
| `journal-compliance` | `guidelines/`, `outputs/` | Section order, abstract structure, heading style |
| `output-generation` | `outputs/` | pandoc export, formatting report requirements |
| `quality-gates` | `outputs/` | 80/90/95 scoring thresholds, manuscript rubric |
| `proofreading-protocol` | `outputs/`, `manuscripts/` | Propose-first, then apply with approval |
| `pdf-processing` | `master_supporting_docs/` | Safe large PDF handling |
| `revision-handling` | `revisions/` | Approved, marker-wrapped edits only; never invent numbers or references |

### Templates (`templates/`)

| Template | What it does |
|----------|-------------|
| `reference.docx` | Pandoc reference document for docx export |
| `journal-requirements.yml` | Annotated schema for journal YAML files |
| `formatting-report.md` | Report template for formatting outputs |
| `session-log.md` | Structured session logging format |
| `quality-report.md` | Merge-time quality report format |
| `requirements-spec.md` | MUST/SHOULD/MAY requirements framework |
| `comment-matrix.md` | Reviewer comment tracker: ID, type, coverage, approval |
| `response-to-reviewers.md` | Point-by-point response letter skeleton |
| `revision-cover-letter.md` | Cover letter to the editor (R1) |
| `revision-change-log.md` | One row per approved manuscript change |
| `references/r2r_voice.md` | Response-letter voice guide (avoids AI-sounding letters) |

</details>

---

## File layout

```
my-submission-formatting-agent/
├── manuscripts/          # Drop input manuscripts here (gitignored)
├── guidelines/           # Journal requirements YAML (one per journal)
├── outputs/              # Formatted outputs (gitignored)
│   └── [journal-name]/
│       ├── working.md                  # Normalised markdown (from ingest)
│       ├── manuscript_formatted.md     # Formatted output
│       ├── manuscript_formatted.docx   # Formatted Word document
│       ├── compliance_checklist.md     # PASS/WARN/FAIL per requirement
│       └── formatting_report.md        # Full change summary
├── revisions/            # Peer-review rounds (gitignored)
│   └── [journal-name]/R1/
│       ├── decision_letter.md          # Reviewer comments (verbatim)
│       ├── comment_matrix.md           # Classification + approvals
│       ├── manuscript_revised.md       # Approved edits in REVISION markers
│       ├── response_to_reviewers.md    # Point-by-point letter
│       └── manuscript_revised_highlighted.docx
├── scripts/
│   ├── ingest.py          # Manuscript → markdown (pandoc wrapper)
│   ├── export_docx.py     # Markdown → docx (pandoc wrapper; --revisions clean|highlight)
│   ├── quality_score.py   # Scoring (--rubric manuscript | response)
│   └── check_response_claims.py  # Response-letter claims vs revised manuscript
├── templates/             # Reference docs and report templates
└── .claude/               # Rules, skills, agents, hooks
```

---

## Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Everything | `npm install -g @anthropic-ai/claude-code` |
| [pandoc](https://pandoc.org) | Ingest + export | [pandoc.org/installing.html](https://pandoc.org/installing.html) |
| Python 3.8+ | Quality scoring | [python.org](https://www.python.org/) |
| pyyaml | Guidelines-aware scoring | `pip install pyyaml` |

---

## Author ｜ 作者

**Chen Zhu 朱晨** ｜ China Agricultural University 中国农业大学


## License

MIT License. Use freely for research or any academic purpose.
