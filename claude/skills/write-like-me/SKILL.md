---
name: write-like-me
description: |
  Write or rewrite knowledge notes in Wonseok's (Cotidie's) documented voice, with figures.
  Use this whenever the user asks to write up, organize, document, or summarize something they
  have learned or studied — study notes, technical reference notes, concept explanations,
  README/문서 정리, 개념 정리, 지식 정리, "이거 정리해줘", "노트로 만들어줘" — or says
  "write like me" / "내 스타일로 써줘" / "/write-like-me". Also use it when reviewing or
  rewriting a note the user already drafted so it matches their voice. Every note this skill
  produces is figure-first: rather than shipping a wall of text it pulls diagrams out of the
  source PDF or official docs and generates the rest with codex-image, then runs stop-slop +
  humanizer as a final pass. Prefer this skill over writing a plain markdown summary yourself,
  even when the user does not mention style or figures.
trigger: /write-like-me
---

# write-like-me

Write knowledge notes that read as if Wonseok wrote them, and that are worth re-reading months
later because the figures carry the mechanism.

The voice specification lives in `references/voice-dna.md`. It was reverse-engineered from 147
Markdown files (2022-2026) and the Notion `Class` databases, with frequency counts. **Read it
before writing.** Everything below assumes it.

## What this skill is for

Organising knowledge he has just learned: a protocol, an algorithm, a tool, a paper, a library,
a lecture. The output is a reference note his future self will look things up in, not an essay
and not a tutorial for strangers.

The single biggest failure mode is **shipping text-only**. A note with no figure has failed even
if every sentence is perfectly in voice. His own notes average 4-8 figures in the dense ones, and
111 of 129 figures in the corpus sit directly under a heading with the prose below them. The
figure carries the mechanism; the prose carries the rule.

## Workflow

### 1. Read the voice spec

Read `references/voice-dna.md` in full. Do not work from memory of it. The parts that most often
get lost: definition-first opener, one leading space before body paragraphs, no conclusion,
zero first-person opinion, `단,` as the Korean paragraph pivot.

### 2. Pick the language and the format

Language follows the subject, matching his corpus: English for protocols, algorithms, tools,
infrastructure. Korean for project write-ups, problem approaches, and lecture-derived concept
notes. If the user wrote to you in Korean about an English-language technology, ask which they
want rather than guessing — the two registers are genuinely different (해라체 normative vs.
impersonal-instructional) and switching mid-note is the most obvious tell.

Then pick a skeleton from `assets/note-template.md`: reference note, problem note, or project
note.

### 3. Plan the figures before writing prose

This ordering matters. If you draft the text first you will rationalise that it "explains itself"
and ship a text-only note. Instead, list the H2 sections, then for each one name the figure that
would let a reader skip the paragraph entirely.

**Budget: at least one figure per substantive H2, minimum 3 per note.** A section that resists a
figure is usually a section that is really a list, so make it a table instead.

The budget counts figures **under the H2 they explain**. A figure parked under the H1 title is
decoration: it satisfies no section and leaves the first real section text-only. If a figure
would open the note, it belongs under `## Overview` instead, which is where the corpus puts it.

Read `references/figures.md` for the decision ladder, the codex-image prompt scaffolds, the
sourcing commands, and the placement rules. The short version:

| Content | Tool |
|---|---|
| Real numeric data (loss curve, complexity growth, benchmark, distribution) | matplotlib → PNG |
| A figure the source already contains, or a canonical diagram that already exists | **source it** (extract from the PDF, save from official docs) |
| Anything conceptual with no good existing figure: mechanism, architecture, layered model, packet/data flow, memory layout, algorithm state, comparison, taxonomy | **codex-image** |
| Trivially simple structure only: ≤5-node linear flow, tiny sequence, tiny ER | mermaid fence or hand-written SVG |

**Sourcing and codex-image are peers, and sourcing is the cheaper probe.** Borrowing is as native
to his practice as generating: 70 of his 129 figures came from outside, and when a note summarises
a specific paper, slide deck, or doc, that source's own figure is the exact one the argument was
built on. It is also free and instant, where codex-image costs a slow call against a rate-limited
quota.

So look first, generate second. Spend one search or one `pdfimages` run before reaching for
codex-image. But do not settle: codex-image output is usually higher quality and stylistically
consistent, so if the candidates are watermarked, low-resolution, cluttered, or only
approximately about your point, generate instead. A borrowed figure that nearly fits teaches the
wrong mechanism.

Reach for matplotlib whenever real numbers exist, because neither sourcing nor generation can
plot *your* data. Reach for mermaid/SVG only when the figure is so simple that producing a raster
would be silly.

### 4. Write the note

Follow the voice spec. While drafting, the four things that most reliably break the illusion:

- **A conclusion.** He never writes one. The note ends on the last technical item or on a
  `## Questions` / `## Errors` section.
- **A hook.** First body sentence defines the title noun. Nothing precedes it.
- **First-person opinion.** `I think`, `생각한다`, `느낀다` appear zero times in 147 files. Views
  arrive as `should` / `해야 한다` / `advisable` attached to a technical object.
- **Explaining motivation.** He documents how a thing works, never why you would want it.
- **Housekeeping about the note itself.** No "reproduce with `make_fig.py`", no "the figure below
  was generated with", no "this section needs expanding". The note exists to carry the concept,
  the explanation, and the understanding. How the artifact was built is metadata about the
  document, not about the subject, and it breaks the reading the moment a reader hits it. His
  corpus keeps figure-generation scripts on disk beside the images and mentions them **zero**
  times in 147 files. Do the same: commit the script, say nothing about it.

Put the explanation load into commented code blocks and figure captions rather than paragraphs.
His English paragraphs median 20 words; if a paragraph is running long, the content belongs in a
list, a table, or a code comment.

#### Nested bullets carry the reasoning

Bullets are the primary medium, not the fallback: 1,576 reasoning bullets against 738 prose
sentences, and 77% of files nest at least one level. A long paragraph is usually a list that has
not been broken up yet.

How heavily depends on the format, so aim at the right one rather than the corpus average:

| Format | Bullets : prose | Children as share of bullets |
|---|---|---|
| Reference note | 1.4 : 1 | 25% |
| Project note | 1.8 : 1 | 33% |
| Problem note | 3.5 : 1 | 35% |

The structure is a claim and what follows from it:

- **Level 1 is the claim, the step, or the term.** The thing that would survive on its own.
  - **Level 2 is what derives from it.** The reason the parent is legal, the other branch, the
    constraint it imposes, or the concrete instantiation.

**Stop at two levels.** A grandchild, meaning two indents, appears four times in 147 files and
**zero times in 566 reference-note bullets**. Treat it as unavailable. If content wants a third
level, the top-level item was really a heading: promote it to `###` and restart the list beneath.

A completely flat list is a signal rather than a style. It usually means the reasoning got left
behind in prose, or dropped.

Not everything becomes a bullet. Prose still carries the definition-first opener and any argument
whose force depends on one sentence following another. Convert what enumerates: chains of cause,
sets of cases, sequences of steps, property lists.

The two parent shapes that dominate:

```markdown
3. **A** tries to attach L2 header with SMAC and DMAC.
   - DIP is not in the same subnet. DMAC should be the Default Gateway
   - MAC for the Default Gateway is unknown, send ARP request to Swtich.

- **Durable**: durable queues/exchanges will recreate messages when broker/node restarts
  - **Persistency**: Message's ability to be restored in a disk (should work with durable queues)
```

A numbered step takes children that say *why the step is legal*. A bold term takes children that
say *what the term implies*. Both let the top level read as a clean skim while the detail stays
one indent away, which is the whole point: the reader should be able to follow the shape of the
argument from the level-1 items alone.

Children are fragments, not paragraphs. They inherit the parent's subject and drop it, the way
`if not, merge two nodes` and `package name must be **'main'**` do.

### 5. Run the filters

Apply **stop-slop** then **humanizer**, in that order, as a final editing pass over the prose.
Invoke them with the Skill tool. When calling humanizer, pass `references/voice-dna.md` as its
Voice Calibration sample so it tunes toward his register instead of a generic human one.

Both skills are negative filters: they say what to strip. The voice spec is the positive
specification: it says what to write. **When they disagree, the voice spec wins**, because those
skills are tuned for persuasive prose and this is reference documentation. The collisions are
predictable, so resolve them this way rather than rediscovering them each time:

| Filter says | Here | Why |
|---|---|---|
| stop-slop: kill all adverbs, no -ly words | Keep adverbs that carry technical precision (`exponentially increase`, `explicitly requeued`, `dynamically fills up`). Kill only emphasis adverbs (`really`, `simply`, `genuinely`). | `slowly increase the size` states a rate. Deleting it deletes information. |
| stop-slop: no Wh- sentence starters | Applies to body prose only. `## Questions` entries are literally `**\| How does X work?**` in his corpus. | The Wh- ban exists to stop rhetorical throat-clearing. A parked open question is not that. |
| stop-slop: two items beat three, vary rhythm, no stacked fragments | Applies to prose only. Bullet lists, spec lists, and tables routinely run 4-7 parallel items and should stay parallel. | Rhythm rules protect paragraphs. A property list is a data structure. |
| stop-slop: put the reader in the room, "you" beats "people" | His register is impersonal. `you` appears only inside procedures. | Voice spec wins. |
| humanizer: add personality and soul, give it a pulse | Skip this section entirely for solo notes. His solo writing has zero emotional register by measurement, and that absence *is* the voice. | Injecting warmth here is the single most damaging thing either filter can do. |

Everything else in both skills applies as written and reinforces the voice: no em dashes, no
hedges, no promotional language, no negative parallelisms, no rule-of-three, active voice, no
vague attributions.

### 6. Verify before handing over

Check these, because they are cheap to check and expensive to get wrong:

1. Every figure file actually exists at the path referenced, and you have `Read` it to confirm it
   shows what the caption claims. A broken or wrong figure is worse than none, and this applies
   doubly to sourced figures, where it is easy to save an error page or the wrong panel.
2. Sourced figures are saved into `.images/`, not hotlinked to someone else's server.
3. No substantive H2 is text-only. Count figures per H2, not per file, so a title figure cannot
   mask an empty first section.
4. No housekeeping: grep the note for `reproduce`, `regenerate`, `script`, `.py`. A hit outside a
   code block is almost always commentary about the document rather than about the subject.
5. No em dash anywhere.
6. The note does not conclude.
7. Image lines end with two trailing spaces.

Then tell the user where the note and the `.images/` folder are.

## Bundled resources

- `references/voice-dna.md` — the full voice specification. Read first, every time.
- `references/figures.md` — figure decision ladder, codex-image prompt scaffolds by figure type,
  matplotlib and mermaid/SVG guidance, placement and naming rules.
- `assets/note-template.md` — the three skeletons (reference note, problem note, project note).

## Notes on the environment

- `codex-image`: invoke the bundled `codex-image` skill (`cotidie:codex-image` in Claude Code)
  and follow its wrapper procedure. Read the printed path afterwards to verify the result.
- `pdfimages` and `pdftoppm` (poppler) are installed for pulling figures out of a source PDF.
  Pillow 12.2 handles cropping, `curl` handles saving from the web.
- matplotlib 3.11 is available for data plots.
- `mmdc` is not installed, so mermaid cannot be rasterised locally. A ```mermaid fence still
  renders on GitHub, in Notion, and in Artifacts. If the destination needs a real image file,
  use codex-image or matplotlib instead.
