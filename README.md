# cotidie-skills

Custom agent skills. Claude Code and Codex both ship skills through the
`cotidie` plugin namespace, so skills invoke as `cotidie:<skill>` in Claude
Code and `$cotidie:<skill>` in Codex.

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
| [cotidie:iteration-roadmap](codex/iteration-roadmap) | Break a project or feature into an adaptive roadmap of small, vertical, user-testable iterations: detailed near-term, flexible later, revised after each ship. (Codex port: no `trigger`/`AskUserQuestion`/superpowers refs.) | - |
| [cotidie:pr-writer](codex/pr-writer) | Draft a PR/MR title and body from the branch diff, commits, or a summary. (Codex port: no `trigger`/`AskUserQuestion`/`gh` refs.) | - |

## Layout

```
.agents/plugins/
  marketplace.json        # Codex marketplace manifest (points at codex/plugins/cotidie)
.claude-plugin/
  marketplace.json        # marketplace manifest (points at plugins/cotidie)
codex/
  iteration-roadmap/      # Codex-safe source skill
  pr-writer/              # Codex-safe source skill
  plugins/cotidie/
    .codex-plugin/
      plugin.json         # Codex plugin manifest
    skills/               # Codex plugin skill links
      iteration-roadmap -> ../../../iteration-roadmap
      pr-writer -> ../../../pr-writer
plugins/cotidie/
  .claude-plugin/
    plugin.json           # Claude Code plugin manifest
  skills/                 # auto-discovered Claude Code skills
    codex-image/
    iteration-roadmap/
    pr-writer/
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
```

For local authoring without the plugin namespace, you can still symlink a
source skill folder into `~/.codex/skills/`, but that exposes it as
`$<skill-name>` instead of `$cotidie:<skill>`.
