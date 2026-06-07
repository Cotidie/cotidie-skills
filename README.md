# cotidie-skills

Custom agent skills, organized per platform.

## Skills

### Claude

| Skill | Description | Example |
|-------|-------------|---------|
| [codex-image](claude/codex-image) | Generate or edit raster/bitmap images via the Codex CLI's built-in `image_gen` tool (no `OPENAI_API_KEY` needed). | [prompt + result](claude/codex-image/example) |
| [iteration-roadmap](claude/iteration-roadmap) | Break a project, feature, or design into an adaptive roadmap of small, vertical, user-testable iterations — detailed near-term, flexible far-term, revised after each ship. | — |

### Codex

_None yet._

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

