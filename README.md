# cotidie-skills

Custom agent skills, organized per platform.

## Skills

### Claude

| Skill | Description | Example |
|-------|-------------|---------|
| [codex-image](claude/codex-image) | Generate or edit raster images via the Codex CLI's `image_gen` tool (no `OPENAI_API_KEY`). | [prompt + result](claude/codex-image/example) |
| [iteration-roadmap](claude/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. | — |
| [pr-writer](claude/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. | — |

### Codex

| Skill | Description | Example |
|-------|-------------|---------|
| [iteration-roadmap](codex/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. (Codex port: no `trigger`/`AskUserQuestion`/superpowers refs.) | — |
| [pr-writer](codex/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. (Codex port: no `trigger`/`AskUserQuestion`/`gh` refs.) | — |

## Layout

```
claude/    # Skills for Claude Code  → install to ~/.claude/skills/
codex/     # Skills for Codex CLI    → install to ~/.codex/skills/
```

Each skill is a folder containing a `SKILL.md` (YAML frontmatter with `name` +
`description`, followed by markdown instructions) plus any supporting scripts or
reference files.

```
claude/
  my-skill/
    SKILL.md
    helper.sh        # optional supporting files
```

## Installing a skill

Symlink (so edits in the repo stay live) or copy the skill folder into the
platform's skills directory:

```bash
# Claude Code
ln -s "$PWD/claude/my-skill" ~/.claude/skills/my-skill

# Codex CLI
ln -s "$PWD/codex/my-skill" ~/.codex/skills/my-skill
```
