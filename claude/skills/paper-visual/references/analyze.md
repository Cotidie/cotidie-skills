# Pass 1: Analyze

Goal: an accurate, complete draft and a handoff for passes 2 and 3. Shape comes later.

## 1. Full text

| Input | Action |
|---|---|
| arXiv URL | Scrape `arxiv.org/abs/<id>` and `arxiv.org/html/<id>` with firecrawl. Download the PDF into the paper folder for figure crops |
| PDF | Read it with the Read tool, 20 pages per call, until the appendix is done |
| Pasted text | Use all of it. Say that figure crops are impossible without the PDF |

Check before moving on: abstract, method, experiments, and appendix are all read. A scanned PDF with no text layer stops the pass; report it.

## 2. Code

Find the repository link in the paper (footnote, end of the introduction, or the abstract page). Otherwise search GitHub with the title and first author.

Clone into the session scratchpad, never into the repo: `git clone --depth 1 <url> <scratchpad>/paper-code`. Read the README, then the core source and config files. Never run its scripts or install its dependencies.

| Status | Action | In the note |
|---|---|---|
| Released | Map at least two method parts to `file:line` | A code block of at most 30 lines with its path, under the matching H3 |
| Pending | Check the README and releases | The status and repository link in the metadata |
| None | Search for unofficial implementations | `공개 코드 없음` in the metadata. An unofficial one gets a link tagged 비공식 and is never evidence |

With no code, the pseudocode, equations, and setup tables are the evidence. Implementation details the paper omits (hyperparameters, preprocessing, seeds, run length) go to 한계 as `재현 정보 누락`.

## 3. Analysis

Work these out before writing. Do not show the process.

1. **Contributions:** one to three, one sentence each.
2. **Mechanism per contribution:** input, processing, output, and why it beats the baseline.
3. **Strongest evidence:** the single most convincing experiment, and why.
4. **Weaknesses:** name the design choice and the condition under which it distorts the result. Tag each one `저자 인정` with a locator (Section, page, or quote) or `추론` (reader-inferred). An absence claim names the sections checked.
5. **Simulation-evaluated papers:** check that the layout, fleet size, arrival distribution, warm-up and run length, and seeds are stated; that baselines were tuned; that tail metrics appear beside means. Each missing item is a weakness.

## 4. Draft and handoff

Write `paper-visual.ko.md` from `assets/template.md`. Keep every contribution, every load-bearing equation, and every main result number.

Write `figures/paper-visual/handoff.md` with:

- Notation conflicts and open doubts, each with a page or section.
- Candidate visuals: the claim in one line each. Mark each contribution's core mechanism.
- Paper figures to crop: Fig number, page, and the claim it supports.
