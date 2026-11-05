---
name: paper-visual
description: 'Use when the user wants one research paper (arXiv URL or PDF) turned into a visual study page with ManimGX animations and generated figures, saved as one offline HTML file. Korean triggers - 논문 시각화, 논문 애니메이션으로 정리, 논문 HTML 정리, 논문 그림으로 이해, paper-visual. Not for a chat-only explanation (paper-forge), a blog-style shareable article (paper-analyzer), a multi-paper comparison (deep-research three-way-scan), or textbook chapters (textbook-notes).'
---

# paper-visual

Turn one paper into a study page read like a newspaper: short sentence, equation, picture. The analysis follows paper-analyzer rounds 1 to 3. Writing rules, visuals, and the build reuse textbook-notes. The note is in Korean with technical terms in English.

`<tn>` below means the textbook-notes skill directory: the `textbook-notes` folder next to this skill's folder in the same plugin (`<this skill's directory>/../textbook-notes`). Read the named `<tn>` file when its pass starts.

## Passes

Run all three passes without stopping. Ask for review only at the end.

| Pass | Job | Contract |
|---|---|---|
| 1 Analyze | Full text, code, analysis, draft note, handoff | `references/analyze.md` |
| 2 Reshape | Hierarchy, cuts, folds, visuals list | `<tn>/references/pass-2-reshape.md` and `<tn>/references/reading-rules.md`, with the overrides below |
| 3 Visuals | Animations, figures, paper figure crops, build | `<tn>/references/pass-3-visuals.md`, with the overrides below |

All passes run in the main session.

## Layout

```
02-papers/NN-<Short-Name>/
  <paper>.pdf
  paper-visual.ko.md
  figures/paper-visual/   handoff.md (during passes), image_prompts.py, anim-N.{py,mp4,png}, paper-fig-N.png
  build/paper-visual.ko.html
```

- When the PDF already sits in a `02-papers/NN-*` folder, use that folder.
- Otherwise create `NN-<Short-Name>` with the next free number and save the PDF there. For an arXiv URL, download `arxiv.org/pdf/<id>`.
- When the working tree has no `02-papers/`, ask once where the folder goes.

## Overrides

These replace the `Structure` section of `reading-rules.md`:

- H1 is the paper title, followed by the metadata table from `assets/template.md`.
- H2 order is fixed: 문제, 핵심 아이디어, 방법, 실험, 한계, 관련 연구, 요약. Under 방법, give each contribution its own H3.
- 문제, 방법, and 실험 open with `goal` and close with `summary`.
- Keep the paper's equation numbers (`\tag{3}`). Cite its Fig, Table, and Section numbers.
- One `::: symbols` block, at the end of 방법.

These adjust `pass-3-visuals.md`:

- Read `<skill-dir>` as `<tn>` (for `anim_kit.py` and `make_images.py`) and `figures/chNN/` as `figures/paper-visual/`. Name animations `anim-N` by their H3 order.
- Animations: at most one per contribution, three per paper. Only 방법 gets them.
- Experiment results come from the paper itself. Crop the figure from the PDF (`pdftoppm -r 200 -f P -l P -png <paper>.pdf figures/paper-visual/page`, then crop with Pillow), or download it from the arXiv HTML page. The caption keeps the paper's number: "그림 3 (논문 Fig. 4): <claim>".
- An orientation figure goes after the H1 `goal`. Crop the paper's overview figure when it is clear. Otherwise generate a pipeline schematic with the image model.

## Related work

- Default: fill 관련 연구 from the paper's own related-work section and reference list. No search.
- Only when the user asks for 3W ("3W 포함", "관련 연구 검색", "three-way scan"): find 3 to 5 other papers on the same problem with the paper-search MCP or a web search, with this paper as the seed. Summarize each as WHY/HOW/WHAT and write the cross-paper synthesis, under 800 words. Render the result as one table (논문, WHY, HOW, WHAT) and one paragraph on where this paper sits. Title the section `관련 연구 (3W 스캔, <date>)`.

## Build

From the paper folder:

```
node <tn>/scripts/render.mjs paper-visual.ko.md
```

When `<tn>/scripts/node_modules` is missing, run `cd <tn>/scripts && npm install` first. The build inlines images and videos, so the HTML opens offline. Keep each video under 2 MB.

## Revise

The user asks about a part they do not understand, or requests a change.

1. Answer in chat first.
2. Patch the note: fix the wording, or add a `::: qa` block with the question and answer.
3. Rebuild.

## Finish

1. Delete `handoff.md`. Build with no KaTeX errors.
2. Commit the paper folder.
3. Report the HTML path, the code status, and the image count (each image is billed).

## Common mistakes

| Mistake | Fix |
|---|---|
| Redrawing an experiment plot with matplotlib or the image model | Crop the paper's figure |
| Running cloned code or installing its dependencies | Read it only |
| A weakness with no locator and no `reader-inferred` tag | Add one of the two, per `references/analyze.md` |
| Using an unofficial implementation as evidence | Link it as 비공식 in the metadata only |
