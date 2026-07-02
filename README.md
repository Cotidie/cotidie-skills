# cotidie-skills

Custom agent skills, split by host. The `claude/` plugin serves Claude Code and
the `codex/` plugin serves Codex. Both ship under the `cotidie` plugin name, so
skills invoke as `cotidie:<skill>` in Claude Code and `$cotidie:<skill>` in
Codex.

## Skills

Use `cotidie:<skill>` in Claude Code and `$cotidie:<skill>` in Codex for supported
hosts.

| Skill | Description | Claude | Codex |
|-------|-------------|--------|-------|
| `cli-user-test` | Validate a built, unit-tested program as a real user would from the terminal. | [✅](claude/skills/cli-user-test) | [✅](codex/skills/cli-user-test) |
| `codex-image` | Generate or edit raster images through the Codex CLI image tool. | [✅](claude/skills/codex-image) | ❌ |
| `create-class-diagram` | Create UML class diagrams in uncompressed `.drawio` XML format. | [✅](claude/skills/create-class-diagram) | [✅](codex/skills/create-class-diagram) |
| `extract-slide-design` | Reverse-engineer slide images, deck screenshots, or report PDFs into a reusable `DESIGN.md`. | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap` | Break a project or feature into small, vertical, user-testable iterations. | [✅](claude/skills/iteration-roadmap) | [✅](codex/skills/iteration-roadmap) |
| `modify-class-diagram` | Update an existing `.drawio` UML class diagram to match a target codebase. | [✅](claude/skills/modify-class-diagram) | [✅](codex/skills/modify-class-diagram) |
| `pr-writer` | Draft a PR or MR title and body from a branch diff, commits, or summary. | [✅](claude/skills/pr-writer) | [✅](codex/skills/pr-writer) |
| `scaffold-react` | Create new React apps or refactor existing React apps to the bundled scaffold conventions. | ❌ | [✅](codex/skills/scaffold-react) |

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
    cli-user-test/
    extract-slide-design/
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
    cli-user-test/        # Codex-safe port
    extract-slide-design/ # Codex-safe port
    scaffold-react/       # Codex-safe React scaffold workflow
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
claude plugin details cotidie   # lists the 7 bundled skills
```

Skills load on the next session as `cotidie:cli-user-test`,
`cotidie:codex-image`, `cotidie:create-class-diagram`,
`cotidie:extract-slide-design`, `cotidie:iteration-roadmap`,
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
$cotidie:cli-user-test
$cotidie:iteration-roadmap
$cotidie:pr-writer
$cotidie:create-class-diagram
$cotidie:modify-class-diagram
$cotidie:extract-slide-design
$cotidie:scaffold-react
```

For local authoring without the plugin namespace, you can still symlink a
source skill folder into `~/.codex/skills/`, but that exposes it as
`$<skill-name>` instead of `$cotidie:<skill>`.
