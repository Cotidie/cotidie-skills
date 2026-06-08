---
name: iteration-roadmap
description: "Break a project, feature, or design into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. Use when the user wants to plan iterations, make a roadmap, phase work into milestones/releases/MVPs, sequence work, or deliver a big build incrementally (even from a finished design doc). Use it BEFORE per-iteration detailed planning."
---

# Iteration Roadmap

Turn a project, feature, or design into an **adaptive roadmap of vertical, user-testable
iterations**. Each iteration ships something the user can actually run and judge; their
feedback then revises the iterations you haven't detailed yet.

This skill is a **macro-sequencing layer**. It sits between intent and detailed planning:

- **Up:** if the input is just a vague idea, do a product-discovery / brainstorming pass
  (or research) first — you cannot honestly slice scope you haven't pinned down.
- **Down:** each iteration, when you actually start it, gets its own detailed plan via a
  dedicated planning pass. This skill produces the roadmap, not the line-by-line plan.

The reason this skill exists: left to default behavior, models produce **infrastructure-
ordered** plans (build the indexer, then the sync, then the API, then finally something
usable) and **over-specify the far future** from assumptions that feedback will overturn.
Both waste effort and hide risk. This skill forces vertical slices and just-in-time detail.

## Step 0 — Classify input maturity (do this first; it decides everything)

You cannot slice what isn't decided. Before anything, read the input and branch. The
failure mode to avoid is **fabricating decisions** to fill a roadmap the user can't yet
support.

| Input you were given | What to do |
| --- | --- |
| **Vague idea / goal only** ("I want semantic search someday") | **Interview to lift it to sliceable** (see below). Roadmap only after. Do a product-discovery / brainstorming pass *instead* only if it's genuine product-discovery — you can't yet say what it is, why, or for whom even after asking. |
| **Spec / requirements, no architecture** | Extract constraints, then surface the **open technical decisions** as questions (see Step 4) before slicing. Mark anything still unknown as `OPEN` — never quietly choose for far iterations. |
| **Locked design doc / decisions already made** | Re-slice directly. Preserve every locked decision unless there's a clear reason to revisit — name the reason if you do. |

If unsure which bucket you're in, you're probably in the middle one: ask.

### Interview to reach sliceable maturity

A vague goal doesn't need a full design before you can slice it — it needs just enough to
name a first runnable slice and the headline value. Ask the **smallest set** that gets you
there (batch related questions into one turn where you can; don't interrogate). Target:

- **Who + what + why** — who uses this, what they do with it, the one outcome that makes it
  worth building. (If this stays fuzzy after asking → that's the product-discovery signal:
  do a discovery / brainstorming pass instead of forcing a roadmap.)
- **Must-have vs nice-to-have** — what the *first usable version* must do, and what is
  explicitly deferred. This is what seeds iteration 1 vs later slices.
- **Any fixed points** — decisions or constraints the user already holds (stack they must
  use, privacy/cost/deadline limits, environment). Don't invent these; ask.
- **Where output lives** — file/location for the roadmap.

Stop interviewing the moment you can write iteration 1's *user-facing value* in one
concrete sentence. More questions past that point is over-scoping, not diligence — the
roadmap's feedback loop is designed to surface the rest. Then proceed to Step 1.

## Step 1 — Extract the fixed points

Pull out, explicitly, before slicing:

- **Locked decisions** (stack, models, storage, protocols) — these constrain ordering.
- **Hard constraints** (privacy, cost, latency, deadlines, environment).
- **Headline user value** — the one sentence describing why the project exists. This is
  your compass for "is each slice actually valuable?"

## Step 2 — Find the MVP vertical slice (iteration 1)

Iteration 1 is the **smallest thing the user can run end-to-end and form an opinion on.**
Not "the database layer." Something they can invoke. It is allowed to be embarrassingly
limited (one-shot, manual refresh, no polish) as long as it produces real output on real
input. If you can't describe how the user would try iteration 1 by hand, it isn't a slice
yet — cut deeper.

## Step 3 — Order the remaining slices

Sequence by **risk-reduction + dependency**, not by architectural tidiness:

- Front-load the iterations that **validate the riskiest assumption** (usually output
  quality / "does this even work?"). Validate in the cheapest, most debuggable surface
  first — a CLI or script beats a server beats a distributed system.
- A later iteration may depend on an earlier one's mechanism, but should still add **its
  own** user-visible capability. If a proposed iteration has no user-facing value, it's
  infrastructure — fold it into the slice that needs it.

## Step 4 — Surface the shape-changing forks (and only those)

Some decisions change the **shape** of the roadmap (which iterations exist, in what
order). Examples: "CLI-first or service-first?", "containerize from day one or last?".
Put these — at most 1–3 — to the user before writing, because guessing wrong rewrites the
whole sequence. Do **not** ask about choices that only affect one iteration's internals;
those get decided when that iteration is detailed.

## Step 5 — Write the iterations

Detail the **first 2–3** iterations fully. Keep the rest deliberately light — a goal and a
one-line value statement is enough — and say plainly that they'll be re-planned from
feedback. Resist filling them in; that detail is a liability, not diligence.

Each detailed iteration carries all eight fields. They exist to force the iteration to be
genuinely shippable and testable, not a relabeled infra phase:

- **Goal** — what this iteration proves or enables.
- **User-facing value** — what the user can *do* after it. If you can't write this in one
  concrete sentence, the iteration isn't vertical.
- **Features introduced** — only the *new* capabilities. No carryover.
- **Deliverables** — files, commands, tools, docs, behavior that should exist.
- **Testable conditions** — concrete checks that prove it works.
- **User test flow** — how the user manually tries it.
- **Feedback to collect** — what you need to learn before detailing later iterations.
  This is what makes the roadmap *adaptive*; without it each ship teaches nothing.
- **Risks / open decisions** — include only if they affect sequencing.

## Step 6 — Save the artifact and set up the loop

Write the roadmap to a durable file the user chose (default: alongside the source design,
with a numeric prefix if that folder is numbered — e.g. `01-<topic>-iteration-roadmap.md`).
Use frontmatter, link back to the source design, and include a short overview table
(iteration → user-facing slice) above the detailed entries so it scans fast.

State the loop explicitly at the top: **after each iteration the user tests it directly and
gives feedback; that feedback revises the remaining iterations before they're detailed.**
When you return to detail iteration N+1, fold in what was learned — don't just execute the
stale outline.

## Anti-pattern checklist (scan the draft against this before saving)

- ❌ An iteration with no one-sentence user-facing value → it's infrastructure; fold it in.
- ❌ Iteration 1 the user can't run by hand → slice deeper.
- ❌ Far iterations detailed as heavily as near ones → strip them back to a goal.
- ❌ A technical decision invented to fill a gap → mark `OPEN` or ask instead.
- ❌ Ordering that mirrors the architecture diagram (data → logic → UI) → re-order by
  risk and user value.
- ❌ Forks that change roadmap shape decided silently → put them to the user.

## Quick reference: roadmap file skeleton

```markdown
---
type: plan
status: draft
created: <date>
source_plan: "[[<source design>]]"
---

# Iteration Roadmap — <project>

## Context
Why this roadmap, what input it came from, the confirmed sequencing decisions,
and the feedback→revise loop.

## Overview
| # | Iteration | User-facing slice |
|---|-----------|-------------------|
| 1 | ...       | what they can do  |

## Iteration 1 — <name>
- **Goal:** …
- **User-facing value:** …
- **Features introduced:** …
- **Deliverables:** …
- **Testable conditions:** …
- **User test flow:** …
- **Feedback to collect:** …
- **Risks / open decisions:** …

## Iteration 2 — <name>
(detailed)

## Iteration 3+ — <name>
(light: goal + one-line value; "re-planned from feedback")
```
