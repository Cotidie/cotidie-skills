---
name: pr-writer
description: Draft a PR or MR title and body from the branch diff, commits, or a summary. Use when asked for PR/MR text, a PR title/description/body, or a reviewer-facing change summary.
trigger: /pr-writer
---

# PR Writer

## Scope

Write only the PR title and PR body. Do not review code, propose fixes, or add implementation details unless they are needed to explain the change clearly.

Assume the reader is a junior developer or a teammate from another team. Prefer impact over file lists. Use plain English, short bullets, and a practical tone.

## Inputs

Use whatever context is available:

- User-provided summary, diff, commits, issue, screenshots, or release notes.
- Current branch diff or commit list when the user asks for the current branch. Gather it
  yourself with `git diff <base>...HEAD` and `git log <base>..HEAD --oneline` (default base
  to the repo's main branch), or `gh pr diff` when a PR already exists.
- Attached screenshot only as context for what screenshot might be useful; do not describe unrelated visual details.

If important context is missing, ask one concise clarification question via `AskUserQuestion`. Otherwise, make a reasonable draft.

## Title

Use this format:

```text
Type: Pascal Case Title
```

Examples:

```text
Feat: Add Factorial Analysis Report
Fix: Prevent Missing Loss Metrics
Refactor: Simplify Student Training Stats
Docs: Add Project README
```

Choose a type that matches the change: `Feat`, `Fix`, `Refactor`, `Docs`, `Test`, `Chore`, or another common PR prefix if clearly better.

Keep the title short, specific, and action-oriented.

## Body Structure

Use sections selectively. Omit sections that do not apply.

```markdown
## Context

Why this change exists. Keep this to no more than 3 lines.

## Changes

- High-level change.
  - Optional supporting detail.
- High-level change.

## Refactoring

- Meaningful internal restructuring, only if relevant.

## How to run

`command`

## Screenshot

Suggested screenshot: the most useful view to show the result.

## Notes

- Small caveat or trivial detail.
- Small caveat or trivial detail.
```

## Section Guidance

### Context

Explain the motivation, not the implementation. Keep it short.

### Changes

Use concise bullets like a teammate-facing changelog. Good bullets describe what changed and why it matters.

Use at most 6 main (top-level) bullets. Pick only the most important changes; fold or drop the rest. Indented sub-bullets are allowed for supporting detail and do not count toward the 6.

Example style:

```markdown
- Added a WiFi demo flow for connecting and sending sample data.
  - Handles reconnect and a simple retry on failure.
- Added a small server endpoint for receiving device messages.
- Added setup notes for running the demo locally.
```

### Refactoring

Include only for meaningful restructuring. Avoid mentioning every renamed helper or moved line.

### How to run

Include commands only when useful. Prefer tested commands, scripts, or manual verification steps.

### Screenshot

Include only when visual output matters. If no screenshot is attached, suggest the best one to add.

Examples:

```markdown
Suggested screenshot: the generated analysis report showing the embedded figures.
```

```markdown
Suggested screenshot: the dashboard after applying the new filter.
```

### Notes

Use for small caveats only. No more than 2 bullets. Omit if there are no caveats.

## Output

Return the PR title first, then the body.

```markdown
Title: Feat: Add Factorial Analysis Report

## Context

...
```

Output the text only. Do not create or push the PR unless the user explicitly asks; if they
do, use `gh pr create` with the drafted title and body.
