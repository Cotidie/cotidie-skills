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
- Heading titles are the book's titles, verbatim: same numbering, same
  words, same capitalization. Never paraphrase, shorten, retitle, or
  translate them. This holds in translated notes too: body in the target
  language, headings in the book's language. H1 format:
  `Ch.N - <exact book chapter title>`.
- H4 mini-headers that exist in the book (run-in or paragraph-lead
  headers) also keep the book's exact wording. Only headers you invent
  for structure the book lacks get your own title, still written in the
  book's language so the heading hierarchy stays uniform.
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

A callout box is an instruction to the reader, not decoration. Box a
block only when one of these holds; otherwise write prose:

- The reader will come back to it later (reference) → lavender.
- The reader may skip it on a first read (enrichment) → teal or ochre.
- The reader must not miss it (trap) → coral.

Two things never get a box:

- Definitions and theorems. They belong in the body prose; they are the
  note's core content, not an aside. Never re-define in a box what the
  body already defines.
- Plain restatements of book content in easier words. Making the book
  easy IS the body's job.

Box types, by color:

- Lavender, deeper into the book than the body goes:
  - `gap`: anything the book skips over that the reader needs: restored
    derivations and proofs, bridging algebra between two equations,
    logical jumps and missed connections between statements, and
    verification checks ("why 4(k-1) equations"). Say explicitly what
    is not in the book.
- Teal, beyond the book:
  - `insight`: content that needs knowledge from outside the chapter:
    applications, links to other chapters or fields, practice notes.
    Name the outside source ("this is Gauss-Seidel relaxation") and mark
    it as not from the book.
- Ochre, creative:
  - `qa`: a novel question with a full answer. Only questions whose
    answer is not already plain in the body; delete routine
    comprehension checks or fold them into prose. Counting/verification
    questions are `gap`, not `qa`.
  - Open questions you cannot resolve: a `qa` ending with the line
    "Open question, ask to revise." so revise mode finds them.
- Coral, signal:
  - `warning`: traps, common misreadings, conditions that silently
    matter. The only must-read box. Keep it rare: a few per chapter.

Quiet structural bookends (no box, do not count toward box rules):

- `goal`: the problem the chapter/section answers, right under the
  heading. Renders as a quiet opener (small uppercase label + bottom
  hairline).
- `summary`: 1-2 lines stating what the reader must remember. It closes
  what `goal` opened: goal asks the section's question up front, summary
  states the answer at the end. Never let one restate the other.
  Renders as a quiet footer (top hairline + small uppercase label).
  - Add it only to H2 sections with substantial technical content
    (derivations, equation sets, results).
  - Skip it for short orientation sections (exercise lists, notation,
    reference pointers) and whenever it would only repeat the goal.
  - One chapter-level block at the very end, titled "Chapter takeaway".
  - Never on H3 subsections. Never precede it with a `---` rule; its own
    top border is the separator.

Budget and spacing:

- `insight` + `qa` combined: at most 2 per H2 section. They are content
  you add, so they are rationed; `gap` count follows what the book
  skips.
- Never three boxes in a row. Two in a row only when their colors
  differ. Prefer prose between boxes.

## Figures

### When a figure is missing

A figure is warranted exactly when the body makes a claim the reader
would otherwise have to simulate in their head. After drafting a
section, sweep the text for these triggers; each hit is a figure
candidate:

The triggers are domain-general; examples span math and CS on purpose.

- Shape claim: any shape adjective about a function, curve, or data
  ("U-shaped", "heavy-tailed", "step", "plateaus", "straight line on
  log-log") → plot the object.
- Evolution over a variable: "converges to", "approaches as n grows",
  loss over training steps, quality over iterations → plot the family
  at several stages with the limit or target overlaid.
- Comparison or trade-off: "thicker/faster/larger than", "one shrinks
  as the other grows" (α vs β, bias-variance, precision-recall,
  throughput-latency) → plot both on the same axes.
- Geometry claim: regions and boundaries (support, integration region,
  decision boundary), projections, embedding-space intuition → draw
  the space with the operation's direction marked.
- Structure and dataflow: components with something flowing between
  them, described in prose ("the input passes through ... then ...").
  Architectures (Transformer block), pipelines, protocol stacks,
  memory layouts, pointer structures → block diagram; label the flow
  (tensor shapes, packets, gradients).
- Execution trace: prose narrating an algorithm's state changing step
  by step (DP table filling, sort partitioning, attention pattern over
  a sentence) → snapshot sequence of the state at 2-3 steps.
- Relation web: three or more concepts tied by transformations,
  limits, or implications, spread across sections → one orientation
  diagram per chapter at most.
- Empirical artifact: claims about what a trained model or a real
  system actually produces (attention maps, generated samples,
  saliency maps, profiler output). Never redraw these; crop the
  original from the book or cited paper, or download it (see source
  table below).
- Physical object or apparatus: photo or schematic.

Kill criteria, mirror of the callout rules: no figure for what a
formula already shows at a glance, none purely decorative, and if the
caption cannot cite the specific claim it illustrates, cut the figure.
Rough budget: 1-2 per H2, plus the chapter orientation diagram.

Tables use the same logic: three or more objects sharing two or more
attributes discussed in prose (distributions × mean/variance/mgf,
models × benchmark scores, algorithms × time/space complexity) →
comparison table instead of running text.

### Where it goes

- Directly AFTER the first claim it illustrates: after the display
  equation, theorem, or sentence that makes the shape/limit/comparison
  claim, before the next concept starts. Never ahead of the claim.
- Exception: a chapter orientation diagram goes right after the
  chapter goal, before the first H2.
- Never inside a bullet list; place it after the list closes.
- If a callout discusses the figure's content, the figure goes before
  that callout, so the callout can refer to it.
- Caption restates the claim, not the picture: "점프 크기가 P(X=x)다",
  not "cdf의 그래프이다".

### Figure sources

Pick the source per figure by figure TYPE, not by a fixed priority
order. Rule: whoever produces the most faithful image wins.

- Figure exists in the book, or in a paper the book cites → crop it
  from that PDF:
  `pdftoppm -png -r 200 -f <pdfpage> -l <pdfpage> book.pdf /tmp/page`
  then crop with Python PIL into `figures/chNN/fig-N-M.png`.
  Empirical artifacts (attention maps, generated samples, benchmark
  plots) are ALWAYS crops or downloads, never redraws: their value is
  being the real output.
- Curve or plot computable from a formula, toy data, or a small
  runnable example (pdf shapes, power functions, convergence plots,
  complexity curves, a toy attention heatmap) → generate with
  matplotlib, styled to the note palette (transparent background, ink
  and brand-accent lines, no top/right spines), saved as SVG.
- Nodes-and-arrows structure (block diagrams, architectures,
  pipelines, memory layouts, family trees, implication maps) and
  execution-trace snapshots → hand-author SVG (ink strokes, cream
  fills, one accent). Mermaid only when flowchart semantics fit.
- Photographs, real-world objects, 3D renderings, software-output
  examples, and canonical images a redraw would degrade (a Galton
  board photo, a famous historical chart) → download from the web,
  directly and without hesitation; it is a first-class source, not a
  fallback. Save into `figures/chNN/`, note the source domain in the
  caption. Notes are for personal study; licensing is not a gate.
- Illustrative art with no factual content → codex-image skill.

Books with no figures at all (common for lecture notes): generate your
own where a picture carries real explanatory weight, still capped by
restraint (a few per chapter, each tied to a specific claim in the
body). Verify every produced or downloaded image by Reading it.
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
