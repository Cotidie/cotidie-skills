# cotidie-skills

Custom agent skills, split by host. The `claude/` plugin serves Claude Code and
the `codex/` plugin serves Codex. Both ship under the `cotidie` plugin name, so
skills invoke as `cotidie:<skill>` in Claude Code and `$cotidie:<skill>` in
Codex.

## Skills

Use `cotidie:<skill>` in Claude Code and `$cotidie:<skill>` in Codex for supported
hosts.

### Cotidie Skills

| Skill | Description | Claude | Codex |
|-------|-------------|--------|-------|
| `cli-user-test` | Validate a built, unit-tested program as a real user would from the terminal. | [✅](claude/skills/cli-user-test) | [✅](codex/skills/cli-user-test) |
| `codex-image` | Generate or edit raster images through the Codex CLI image tool. | [✅](claude/skills/codex-image) | ❌ |
| `create-class-diagram` | Create UML class diagrams in uncompressed `.drawio` XML format. | [✅](claude/skills/create-class-diagram) | [✅](codex/skills/create-class-diagram) |
| `extract-slide-design` | Reverse-engineer slide images, deck screenshots, or report PDFs into a reusable `DESIGN.md`. | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap` | Break a project or feature into small, vertical, user-testable iterations. | [✅](claude/skills/iteration-roadmap) | [✅](codex/skills/iteration-roadmap) |
| `modify-class-diagram` | Update an existing `.drawio` UML class diagram to match a target codebase. | [✅](claude/skills/modify-class-diagram) | [✅](codex/skills/modify-class-diagram) |
| `pr-writer` | Draft a PR or MR title and body from a branch diff, commits, or summary. | [✅](claude/skills/pr-writer) | [✅](codex/skills/pr-writer) |
| `scaffold-react` | Create new React apps or refactor existing React apps to the bundled scaffold conventions. | [✅](claude/skills/scaffold-react) | [✅](codex/skills/scaffold-react) |

### Vendored Skills

These skills are snapshots of upstream open source projects. The recorded version
identifies the upstream release or commit currently vendored here.

| Skill | Description | Recorded version | Claude | Codex |
|-------|-------------|------------------|--------|-------|
| [`humanizer`](https://github.com/blader/humanizer) | Remove signs of AI-generated writing from text. | [`v2.8.1`](https://github.com/blader/humanizer/tree/199e69420669768b2768d368d1286474e38c00f5) | [✅](claude/skills/humanizer) | [✅](codex/skills/humanizer) |
| [`karpathy-guidelines`](https://github.com/forrestchang/andrej-karpathy-skills) | Keep coding work simple, surgical, explicit, and verifiable. | [`64723a4`](https://github.com/forrestchang/andrej-karpathy-skills/commit/64723a49ea6117894304eb491f0d32a60570bf45) | [✅](claude/skills/karpathy-guidelines) | [✅](codex/skills/karpathy-guidelines) |

## Installing

### Claude Code (plugin)

```bash
claude plugin marketplace add Cotidie/cotidie-skills
claude plugin install cotidie@cotidie-skills
```

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
$cotidie:karpathy-guidelines
$cotidie:pr-writer
$cotidie:create-class-diagram
$cotidie:modify-class-diagram
$cotidie:extract-slide-design
$cotidie:scaffold-react
$cotidie:humanizer
```

For local authoring without the plugin namespace, you can still symlink a
source skill folder into `~/.codex/skills/`, but that exposes it as
`$<skill-name>` instead of `$cotidie:<skill>`.
