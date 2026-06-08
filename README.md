# cotidie-skills

Custom agent skills, split by host. The `claude/` plugin serves Claude Code and
the `codex/` plugin serves Codex. Both ship under the `cotidie` plugin name, so
skills invoke as `cotidie:<skill>` in Claude Code and `$cotidie:<skill>` in
Codex.

## Skills

### Claude Code (`claude/`)

| Skill | Description | Example |
|-------|-------------|---------|
| [cotidie:iteration-roadmap](claude/skills/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. | - |
| [cotidie:pr-writer](claude/skills/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. | - |
| [cotidie:codex-image](claude/skills/codex-image) | Generate or edit raster images via the Codex CLI's `image_gen` tool (no `OPENAI_API_KEY`). | [prompt + result](claude/skills/codex-image/example) |
| [cotidie:create-class-diagram](claude/skills/create-class-diagram) | Create lean, monochrome UML class diagrams as uncompressed `.drawio` XML (written to the working directory), emphasizing OOP structure, SOLID, and dependency flow. | - |
| [cotidie:modify-class-diagram](claude/skills/modify-class-diagram) | Conservatively update an existing on-disk `.drawio` class diagram to match a codebase, preserving IDs, layout, and style. | - |

### Codex (`codex/`)

| Skill | Description |
|-------|-------------|
| [cotidie:iteration-roadmap](codex/skills/iteration-roadmap) | Codex-safe port of the roadmap skill (no `trigger`/`AskUserQuestion`/superpowers refs). |
| [cotidie:pr-writer](codex/skills/pr-writer) | Codex-safe port of the PR writer (no `trigger`/`AskUserQuestion`/`gh` refs). |
| [cotidie:create-class-diagram](codex/skills/create-class-diagram) | Codex-safe port for creating lean, monochrome UML class diagrams as uncompressed `.drawio` XML. |
| [cotidie:modify-class-diagram](codex/skills/modify-class-diagram) | Codex-safe port for conservatively updating an existing `.drawio` class diagram against a codebase. |

## Layout

```
.claude-plugin/
  marketplace.json        # Claude Code marketplace manifest (points at ./claude)
.agents/plugins/
  marketplace.json        # Codex marketplace manifest (points at ./codex)
claude/
  .claude-plugin/
    plugin.json           # Claude Code plugin manifest (skills: ./skills/)
  skills/
    iteration-roadmap/
    pr-writer/
    codex-image/          # Claude Code only
    create-class-diagram/
    modify-class-diagram/
codex/
  .codex-plugin/
    plugin.json           # Codex plugin manifest (skills: ./skills/)
  skills/
    iteration-roadmap/    # Codex-safe port
    pr-writer/            # Codex-safe port
    create-class-diagram/ # Codex-safe port
    modify-class-diagram/ # Codex-safe port
```

Each skill is a folder containing a `SKILL.md` (YAML frontmatter with `name` +
`description`, followed by markdown instructions) plus any supporting scripts or
reference files. Claude and Codex keep separate skill copies so each can carry
host-specific instructions. Claude-bundled scripts reference their location via
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
claude plugin details cotidie   # lists the 5 bundled skills
```

Skills load on the next session as `cotidie:codex-image`,
`cotidie:create-class-diagram`, `cotidie:iteration-roadmap`,
`cotidie:modify-class-diagram`, and `cotidie:pr-writer`.

### Codex CLI (plugin)

This repo includes a local Codex marketplace at `.agents/plugins/marketplace.json`.
From this repo, restart Codex and open the plugin browser:

```text
/plugins
```

Install and enable `cotidie` from the `Cotidie Skills` marketplace. The bundled
Codex skills then invoke as:

```text
$cotidie:iteration-roadmap
$cotidie:pr-writer
$cotidie:create-class-diagram
$cotidie:modify-class-diagram
```

For local authoring without the plugin namespace, you can still symlink a
source skill folder into `~/.codex/skills/`, but that exposes it as
`$<skill-name>` instead of `$cotidie:<skill>`.
