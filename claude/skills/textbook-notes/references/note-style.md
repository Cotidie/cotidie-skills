# Note writing rules

## Language

Target: a first-year engineering undergraduate follows every paragraph on
the first read. Plain sentences, standard terminology, exact math. Simple
structure is not baby talk: never dumb down the terms, only the syntax.

- Body in plain English by default; Korean only when the user asks.
- Use the field's standard terms (pseudo-machine, starvation, blocking).
  Gloss each once in plain words at first use, then use the term alone.
  Do not invent cute synonyms like "fake machine".
- Prefer common words for everything that is not a term of art: use, not
  utilize; enough, not sufficient; about, not approximately.
- One idea per sentence. No nested clauses: split them.
- Sentences under ~20 words. Paragraphs under 3 sentences.
- Active voice ("the buffer empties", not "the buffer is emptied").
- Cut filler: "basically", "in order to", "note that", "it is important".
- Never use an em-dash.
- Every symbol gets a plain-words name at first use ("r_u(i), the
  probability the upstream pseudo-machine is repaired in one step").
- Say "probability", not "chance", for defined quantities.
- Teach by example. After an abstract statement, give one tiny concrete
  case with numbers when possible.
- Read-aloud test: if you would stumble or re-read a sentence, break it up.
- Do not paraphrase the book's long paragraphs. Say the point in one or
  two short sentences and let the math carry the rest.
- Prefer bullet points over prose. Any sentence listing two or more items,
  causes, cases, or observations becomes a list. Any paragraph that is
  really an enumeration ("first... also... finally") becomes a list.
- Bullets are fragments, not essays: one line each when possible, no
  trailing sub-clauses. Use numbered lists only when order matters.

## Structure

- H1 chapter title, H2 sections, H3 subsections, H4 for mini-headers
  (plain bold, no decoration).
- Open each H2 section with a `::: goal` callout when the section solves a
  stated problem.
- Sections not yet distilled contain exactly: `_Not distilled yet._`

## Math

- Reproduce every load-bearing equation in display math, keeping the
  book's equation numbers in trailing tags like `\tag{4.4}`.
- Right after each equation, add one short sentence saying what it means
  in plain words. Skip it only when the surrounding prose already does.
- When the book jumps between two equations, restore the intermediate
  algebra inside a `::: gap` callout. Say explicitly it is not in the book.
- Prefer aligned derivations (`\begin{aligned}`) over prose descriptions
  of algebra. Let the math talk; keep the prose around it short.
- Break wide equations into two or more `\begin{aligned}` lines instead of
  letting them scroll horizontally. Rough limit: if a display equation
  would not fit in about 80 characters of LaTeX terms, split it at an
  operator (=, +) with `\\` and align.

## Callouts

- `goal`: the problem the chapter/section answers.
- `definition`: definitions and theorems, close to the book's wording.
- `warning`: traps, common misreadings, conditions that silently matter.
- `tip`: intuition, physical meaning, engineering rules of thumb.
- `qa`: one or more per section. Ask the question a reader should test
  themselves with, then answer it fully.
- `gap`: restored derivations or bridging logic missing from the book.
- `summary`: 1-2 lines stating what the reader must remember. It closes
  what `goal` opened: goal asks the section's question up front, summary
  states the answer at the end. Never let one restate the other.
  Renders as a quiet section footer (top hairline + small uppercase
  label), not a box, so it does not add callout fatigue.
  - Add it only to H2 sections with substantial technical content
    (derivations, equation sets, results).
  - Skip it for short orientation sections (exercise lists, notation,
    reference pointers) and whenever it would only repeat the goal.
  - One chapter-level block at the very end, titled "Chapter takeaway".
  - Never on H3 subsections. Never precede it with a `---` rule; its own
    top border is the separator.
- Open questions you cannot resolve: add a `::: qa` with the question and
  the line "Open question, ask to revise." so the revise mode finds them.
- Avoid two adjacent callouts of the same type; interleave prose.

## Figures

- Schematics and structure diagrams (transfer lines, buffers, block
  diagrams): redraw as SVG into `figures/chNN/`. Match note colors: ink
  strokes, cream fills, one brand accent max.
- Mermaid only for flowcharts/algorithms where boxes-and-arrows semantics
  fit; otherwise SVG.
- Data plots and simulation results: crop from the source PDF.
  `pdftoppm -png -r 200 -f <pdfpage> -l <pdfpage> book.pdf /tmp/page`
  then crop with Python PIL and save to `figures/chNN/fig-N-M.png`.
  Verify every crop by Reading the output image.
- Illustrative/decorative images (rare): codex-image skill or a web
  download are acceptable fallbacks.
- Every figure gets a caption: `<figure>` markdown image + italic caption
  line, numbered like the book (Figure 4.1) so revise requests can refer
  to them.
- Pair figures two per row with `<div class="fig-row">` around two
  `<figure>` blocks, ONLY when both hold:
  - They form a comparison series: same plot type and axes, varied
    parameter (N = 4 vs N = 8), or before/after.
  - Each stays legible at half width: portrait or square aspect, no dense
    small labels. Wide landscape plots with label clutter stay full width.
- Never pair figures discussed in separate, distant paragraphs.
  Maximum two per row.

## Faithfulness

- The note is a study companion, not a paraphrase dump: compress
  repetitive prose, keep all definitions, all equations, all conditions.
- Keep the book's notation exactly. Do not invent new symbols.
- Cite the source page range in the header table.
