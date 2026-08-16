# Figures

How he uses visuals, and how to produce them.

- [What the corpus does](#what-the-corpus-does)
- [Decision ladder](#decision-ladder)
- [Sourcing an existing figure](#sourcing-an-existing-figure)
  - [From the source PDF](#from-the-source-pdf)
  - [From the web](#from-the-web)
- [codex-image](#codex-image)
  - [House style](#house-style)
  - [Scaffolds by figure type](#scaffolds-by-figure-type)
- [matplotlib](#matplotlib)
- [mermaid and SVG](#mermaid-and-svg)
- [Placement, naming, storage](#placement-naming-storage)

## What the corpus does

Measured over 147 files:

| Fact | Number |
|---|---|
| Files containing at least one figure | 61 of 147 (41%) |
| Figures in the figure-dense notes | 4 to 8 |
| Figures placed directly under a heading | 111 of 129 |
| Figures followed by prose | 94 |
| Figures followed by a list, code block, or table | 34 |
| Image lines ending in two trailing spaces | 116 of 129 |
| Alt text that is a short label rather than a sentence | 129 of 129 |

The pattern is consistent: **heading → figure → prose**. The figure states the mechanism
spatially, and the paragraph under it states the rule the figure cannot say in words. He almost
never describes what the picture shows, because the picture already showed it.

Provenance is the other half of the picture. Most of his figures were not drawn by him:

| Where the figure came from | Number |
|---|---|
| Saved into a repo-local `.images/` folder | 59 |
| Re-uploaded to a host he controls (imgur, GitHub) | 48 |
| Hotlinked straight to a third-party site | 22 |

Two things follow. **Borrowing is the default move** — programiz for algorithm matrices,
rabbitmq.com and cloudamqp for broker diagrams, geeksforgeeks and medium for data structures,
researchgate for consistent hashing. And **he keeps a copy**: 107 of 129 figures live somewhere he
controls rather than on a stranger's server. Do the same, since hotlinks rot. His own OSI note
contains a figure URL that got mangled into the surrounding prose and now renders as broken text.

Attribution is loose in his corpus — only 7 figures have a `| See:` line nearby. Add one anyway
when a figure came from a specific doc or post. It costs a line, it uses the `| See:` form he
already writes for sources, and the point is being able to find the original again later.

Seven figure types recur.

| Type | Examples from his notes |
|---|---|
| Architecture / component map | ROS master registry, Docker client-daemon-registry, RabbitMQ broker, PostgreSQL architecture |
| Layered stack | OSI 7 layers, Docker image layers, host vs container virtualization |
| Flow / traversal trace | packet travelling A→R1→R2→B, query execution phases, Node event loop, recursive CTE |
| Algorithm state | Kruskal, union-find, segment tree, level-order traversal, DP recurrence table, topological sort |
| Comparison / taxonomy | numeric types, character types, switch vs router, three-way vs four-way handshake |
| Data plot | loss function, logistic regression, polynomial fit, gradient descent surface |
| Screenshot | pgAdmin, Node debugger, RabbitMQ management web, app screenshots |

## Decision ladder

Work down this list and stop at the first match.

**1. Does the figure need real numbers?**
Loss curve, complexity growth, benchmark result, distribution, decision boundary → **matplotlib**.
A generated illustration cannot plot true data. A plausible-looking but fabricated curve in a
study note is worse than no curve, because he will later trust it.

**2. Is it a screenshot of a real UI or real terminal output?**
Take or ask for the real thing. Do not generate a fake UI. If neither is available, drop the
figure and use a fenced code block of the real output instead.

**3. Does a good figure already exist? → source it.**
Check in this order, and stop as soon as one fits:

- **The source the note is summarising.** If you are writing up a paper, a slide deck, a lecture
  PDF, or a specific doc page, its own figures are first choice. They are the exact diagrams the
  argument was built on, they cost nothing, and they arrive instantly.
- **Official documentation** for the tool or protocol. His RabbitMQ note pulls straight from
  rabbitmq.com.
- **A canonical third-party diagram** that is genuinely well known for this concept — the
  programiz Floyd-Warshall matrices, the standard sliding-window picture.

**4. No good existing figure → codex-image.** Covers types 1-5 above: mechanism, architecture,
layered model, data flow, memory layout, algorithm state, comparison, taxonomy.

Steps 3 and 4 are peers, not a strict ranking. Sourcing is the cheaper probe, so spend one search
or one `pdfimages` run before generating — codex-image is a slow call against a rate-limited
quota, and a note needing five figures burns real time. But **do not settle for an approximate
match.** codex-image output is usually higher quality and lets you control exactly what the figure
emphasises. Generate instead of sourcing when the candidates are watermarked, low-resolution,
cluttered with unrelated detail, in the wrong language, or only roughly about your point. A
borrowed figure that nearly fits teaches the wrong mechanism, which is the one outcome worse than
having no figure.

One more tiebreaker: if you are already generating several figures for a note, generating the
rest keeps the set stylistically coherent. If you are mostly sourcing, do not fight the visual
mismatch between sources — his corpus mixes freely and it reads fine.

**5. Exception: trivially simple structure → mermaid or SVG.** A linear flow of five nodes or
fewer, a three-message sequence, a two-table ER. Generating a raster for these wastes a call and
the code-native version stays editable. If you find yourself writing more than about a dozen
mermaid nodes, that is a sign the figure wanted to be an illustration — go back to codex-image.

## Sourcing an existing figure

Always save a copy into the note's `.images/` folder rather than referencing a remote URL, then
`Read` the saved file to confirm it is the figure you meant and not an error page, a placeholder,
or the wrong panel.

### From the source PDF

`pdfimages` and `pdftoppm` (poppler) are installed.

```bash
# 1. see what images the PDF holds, with page numbers and pixel sizes
pdfimages -list paper.pdf | head -40

# 2. extract the embedded images from pages 3 to 5 as PNG
pdfimages -png -f 3 -l 5 paper.pdf .images/fig

# 3. when a "figure" is really vector art plus text labels, pdfimages misses it.
#    render the whole page instead, then crop.
pdftoppm -png -r 150 -f 4 -l 4 paper.pdf .images/page4
```

Step 3 is the common case for papers and slides: diagrams drawn in vector form have no embedded
raster to extract, so render the page and crop the region with Pillow.

```python
from PIL import Image
im = Image.open(".images/page4-4.png")
im.crop((left, top, right, bottom)).save(".images/architecture.png")
```

Discard extracted images that turn out to be logos, page furniture, or one-pixel spacers —
`pdfimages -list` sizes make these obvious before you look.

### From the web

```bash
curl -sL -o .images/consistent-hashing.png "<url>"
file .images/consistent-hashing.png     # confirm it is really a PNG/JPEG, not an HTML error page
```

Then `Read` it. Prefer a direct image URL from the official docs over a screenshot of a page.
If the image is behind a viewer or only exists inside a rendered page, it is usually faster to
generate the figure than to fight for it.

## codex-image

Invoke the bundled `codex-image` skill (`cotidie:codex-image` in Claude Code) and run its
wrapper:

```bash
"<codex-image-skill-dir>/codex-image.sh" "<prompt>" <dest.png>
```

Then `Read` the printed path and confirm it shows what you intend before referencing it. Iterate
with one targeted change if it misses.

**If the wrapper prints nothing and no file appears, do not regenerate.** The call can exit 0
after `image_gen` succeeded but before the copy step, which strands a finished PNG. Look for it
first:

```bash
ls -t ~/.codex/generated_images/*/ | head        # newest run directory
cp ~/.codex/generated_images/<run-id>/exec-*.png .images/<slug>.png
```

Regenerating costs another slow call against the quota and returns a different image, so a note
that lost one figure this way ends up stylistically inconsistent with the rest of its set.

Two things govern prompt quality here. First, prompt order is **scene/backdrop → subject →
details → constraints**, and any text that must appear in the image is quoted verbatim. Second,
image generation garbles dense text: **cap in-image labels at about six short ones.** This is not
a limitation to work around, it is the same division of labour his notes already use — the figure
shows the shape, the bullets under it name the parts precisely.

### House style

Reuse one style clause across every figure in the same note, so the set looks like it belongs
together. A serviceable default for technical notes:

> Clean flat technical illustration, light neutral background, limited palette of two accent
> colours plus grey, thin confident strokes, generous whitespace, no drop shadows, no gradients,
> no photorealism, labels in a plain sans-serif.

Adjust the accent colours per note, keep everything else fixed.

### Scaffolds by figure type

**Architecture / component map**

> Clean flat technical illustration on a light neutral background. A central rounded box labelled
> "Broker" with two boxes on its left labelled "Producer" and two on its right labelled
> "Consumer". Arrows flow left to right through the centre box. Inside the centre box, two
> smaller stacked shapes labelled "Exchange" and "Queue". Thin strokes, one blue accent, grey
> supporting elements, generous whitespace, no shadows, no gradients, plain sans-serif labels.

**Layered stack**

> Clean flat technical illustration on a light neutral background. Seven horizontal bars stacked
> vertically, widest at the bottom and equal width throughout, each a slightly different tint of
> a single blue. Labels from top to bottom: "Application", "Presentation", "Session",
> "Transport", "Network", "Data Link", "Physical". A thin downward arrow along the left edge.
> Thin strokes, generous whitespace, no shadows, plain sans-serif labels.

**Flow / traversal trace**

> Clean flat technical illustration on a light neutral background. A horizontal path with four
> nodes left to right labelled "A", "R1", "R2", "B", connected by arrows. Above each arrow a
> small rectangle representing a packet, made of two stacked segments tinted differently. The
> packet gains a segment between "A" and "R1" and loses it between "R1" and "R2". Thin strokes,
> one orange accent, grey supporting elements, no shadows, plain sans-serif labels.

**Algorithm state**

Show two or three moments side by side rather than one static picture, so the reader sees the
transition. That is what makes an algorithm figure earn its place.

> Clean flat technical illustration on a light neutral background. Three small undirected graphs
> arranged left to right, each with the same five circular nodes in the same positions, separated
> by thin vertical divider lines. In the first, no edges are highlighted. In the second, one edge
> is thick and green. In the third, three edges are thick and green forming a tree. Small captions
> beneath each panel: "start", "step 1", "step 3". Thin strokes, grey unselected edges, generous
> whitespace, no shadows, plain sans-serif labels.

**Comparison / taxonomy**

> Clean flat technical illustration on a light neutral background, split into two equal halves by
> a thin vertical line. Left half titled "Host virtualization": a stack of four bars labelled
> from bottom "Hardware", "Host OS", "Hypervisor", "Guest OS", with three small app boxes on top.
> Right half titled "Container virtualization": a stack of three bars labelled from bottom
> "Hardware", "Host OS", "Container engine", with three small app boxes on top. Same widths and
> alignment across both halves so the missing layer is obvious. Thin strokes, one accent colour,
> no shadows, plain sans-serif labels.

The alignment instruction is what makes this type work. The comparison lands because the two
halves are drawn to the same grid, not because a caption says they differ.

## matplotlib

matplotlib 3.11 is available. Keep plots plain: no seaborn styling, no titles that repeat the
heading above the figure, axis labels with units, and `dpi=150` so the PNG stays readable when
scaled.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(xs, ys)
ax.set_xlabel("iteration")
ax.set_ylabel("cost J(w,b)")
fig.tight_layout()
fig.savefig(".images/gradient-descent-cost.png", dpi=150)
```

If the numbers are illustrative rather than measured, say so in the sentence under the figure.
Do not let a synthetic curve pass as a result.

## mermaid and SVG

`mmdc` is not installed, so a mermaid fence cannot be rasterised locally. The fence still renders
on GitHub, in Notion, and in Artifacts, so it is fine when the note lives in one of those. When
the destination needs an actual image file, use codex-image or matplotlib instead.

Hand-written SVG is worth it only for figures that are both simple and precise: a table layout, a
memory diagram with exact byte offsets, a grid. If you write SVG, set an explicit `viewBox`,
avoid external fonts, and keep it under roughly 40 lines or it stops being the cheap option.

## Placement, naming, storage

Store figures in a `.images/` folder beside the note, matching his repo convention (59 of his
local figure references live under `.images/`).

```
network/
  03 UDP and TCP.md
  .images/
    tcp-handshake.png
    congestion-window.png
```

The image line itself:

```markdown
### Congestion Control
![congestion-window](.images/congestion-window.png)  
 Congestion control is about preventing packet loss when travelling between routers, as routers
 would drop packets exceeding MTU or when their buffer lacks space.
```

Four details in that snippet, all measured from the corpus:

- The figure sits **directly under the heading it explains**, before any prose. 111 of 129 figures
  do this. Putting one under the H1 title instead makes it belong to no section, so the first real
  section ends up text-only while the file still looks illustrated. When a figure should open the
  note, put it under `## Overview`.
- The note never mentions how the figure was made. Generation scripts live beside the images in
  the same folder and are committed, but no note in 147 files references one.
- Alt text is a **short lowercase or kebab-case label naming the concept** (`congestion-window`,
  `query-phases`, `recursive-cte`, `union-find`), never empty and never a sentence. Use the same
  slug for the filename.
- The line ends with **two trailing spaces**, which is a markdown hard break and is what keeps
  the following paragraph tight against the image.

In Notion notes the caption goes inside the alt text wrapped in angle brackets instead:

```markdown
![< UDP: 프로세스가 하나의 소켓을 유지, TCP: 여러 개의 소켓을 유지 >](url)
```
