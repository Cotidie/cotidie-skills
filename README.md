# cotidie-skills

Custom agent skills. Claude Code skills ship as the `cotidie` plugin (skills
invoke as `cotidie:<skill>`); Codex skills stay as loose skill folders.

## Skills

### Claude (`cotidie` plugin)

| Skill | Description | Example |
|-------|-------------|---------|
| [cotidie:codex-image](plugins/cotidie/skills/codex-image) | Generate or edit raster images via the Codex CLI's `image_gen` tool (no `OPENAI_API_KEY`). | [prompt + result](plugins/cotidie/skills/codex-image/example) |
| [cotidie:iteration-roadmap](plugins/cotidie/skills/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. | - |
| [cotidie:pr-writer](plugins/cotidie/skills/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. | - |

### Codex

| Skill | Description | Example |
|-------|-------------|---------|
| [iteration-roadmap](codex/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. (Codex port: no `trigger`/`AskUserQuestion`/superpowers refs.) | - |
| [pr-writer](codex/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. (Codex port: no `trigger`/`AskUserQuestion`/`gh` refs.) | - |

## Layout

```
.claude-plugin/
  marketplace.json        # marketplace manifest (points at plugins/cotidie)
plugins/cotidie/
  .claude-plugin/
    plugin.json           # plugin manifest
  skills/                 # auto-discovered Claude Code skills
    codex-image/
    iteration-roadmap/
    pr-writer/
codex/                    # Codex CLI skills → install to ~/.codex/skills/
```

Each skill is a folder containing a `SKILL.md` (YAML frontmatter with `name` +
`description`, followed by markdown instructions) plus any supporting scripts or
reference files. Bundled scripts reference their location via
`${CLAUDE_PLUGIN_ROOT}`.

## Installing

### Claude Code (plugin)

Add this repo as a marketplace, then install the plugin. From the terminal:

```bash
claude plugin marketplace add Cotidie/cotidie-skills
claude plugin install cotidie@cotidie-skills
```

Or in-session via slash commands:

```
/plugin marketplace add Cotidie/cotidie-skills
/plugin install cotidie@cotidie-skills
```

For local development against a checkout, point the marketplace at the path
instead (edits stay live; run `claude plugin marketplace update cotidie-skills`
after pulling changes):

```bash
claude plugin marketplace add /absolute/path/to/cotidie-skills
claude plugin install cotidie@cotidie-skills
```

Verify and inspect:

```bash
claude plugin list              # cotidie@cotidie-skills → enabled
claude plugin details cotidie   # lists the 3 bundled skills
```

Skills load on the next session as `cotidie:codex-image`,
`cotidie:iteration-roadmap`, and `cotidie:pr-writer`.

### Codex CLI

Symlink (so edits stay live) or copy the skill folder:

```bash
ln -s "$PWD/codex/my-skill" ~/.codex/skills/my-skill
```
