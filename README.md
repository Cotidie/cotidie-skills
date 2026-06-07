# cotidie-skills

Custom agent skills, organized per platform.

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

## Claude ↔ Codex portability

The `SKILL.md` format is shared (same agentskills.io spec; `name` + `description`
frontmatter). To port a skill between `claude/` and `codex/`:

1. **Fix hardcoded paths** — `~/.claude/skills/...` → `~/.codex/skills/...`, or
   make paths `$HOME`-relative.
2. **Map tool names** if the body references Claude-specific tools:

   | Claude | Codex |
   |--------|-------|
   | `Task` (subagent) | `spawn_agent` / `wait_agent` / `close_agent` |
   | `TodoWrite` | `update_plan` |
   | `Skill` | loads natively — just follow instructions |
   | `Read` / `Write` / `Edit` / `Bash` | native file & shell tools |

3. **Subagent skills** need `multi_agent = true` under `[features]` in
   `~/.codex/config.toml`.

Prose-only skills usually port with no edits beyond placement.
