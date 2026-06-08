---
name: pr-writer
description: Draft concise pull request titles and bodies only. Use when the user asks for a PR title, PR description, PR body, GitHub PR text, merge request text, or wants a high-level summary of the current branch/diff/commits for teammates, junior developers, reviewers, or non-specialist readers.
---

# PR Writer

## Scope

Write only the PR title and PR body. Do not review code, propose fixes, or add implementation details unless they are needed to explain the change clearly.

Assume the reader is a junior developer or a teammate from another team. Prefer impact over file lists. Use plain English, short bullets, and a practical tone.

## Inputs

Use whatever context is available:

- User-provided summary, diff, commits, issue, screenshots, or release notes.
- Current branch diff or commit list when the user asks for the current branch.
- Attached screenshot only as context for what screenshot might be useful; do not describe unrelated visual details.

If important context is missing, ask one concise clarification question. Otherwise, make a reasonable draft.

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

Example style:

```markdown
- Added a WiFi demo flow for connecting and sending sample data.
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
