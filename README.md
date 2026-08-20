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
| `explain-concept` | Research a concept from primary sources and organize it into a self-contained study document. | [✅](claude/skills/explain-concept) | [✅](codex/skills/explain-concept) |
| `extract-slide-design` | Reverse-engineer slide images, deck screenshots, or report PDFs into a reusable `DESIGN.md`. | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap` | Break a project or feature into small, vertical, user-testable iterations. | [✅](claude/skills/iteration-roadmap) | [✅](codex/skills/iteration-roadmap) |
| `modify-class-diagram` | Update an existing `.drawio` UML class diagram to match a target codebase. | [✅](claude/skills/modify-class-diagram) | [✅](codex/skills/modify-class-diagram) |
| `pr-writer` | Draft a PR or MR title and body from a branch diff, commits, or summary. | [✅](claude/skills/pr-writer) | [✅](codex/skills/pr-writer) |
| `scaffold-react` | Create new React apps or refactor existing React apps to the bundled scaffold conventions. | [✅](claude/skills/scaffold-react) | [✅](codex/skills/scaffold-react) |
| `textbook-notes` | Distill math-heavy textbook chapter PDFs into Notion-style study notes with offline HTML output. | [✅](claude/skills/textbook-notes) | [✅](codex/skills/textbook-notes) |
| `write-like-me` | Write figure-first knowledge notes in Cotidie's documented voice. | [✅](claude/skills/write-like-me) | [✅](codex/skills/write-like-me) |

### Vendored Skills

These skills are snapshots of upstream open source projects. The recorded version
identifies the upstream release or commit currently vendored here.

| Skill | Description | Recorded version | Claude | Codex |
|-------|-------------|------------------|--------|-------|
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
$cotidie:explain-concept
$cotidie:scaffold-react
$cotidie:textbook-notes
$cotidie:write-like-me
```

For local authoring without the plugin namespace, you can still symlink a
source skill folder into `~/.codex/skills/`, but that exposes it as
`$<skill-name>` instead of `$cotidie:<skill>`.

## Third Party Installation

Skills and plugins this repo deliberately does not bundle, because someone else
maintains them. Run these on a new machine to finish the setup. The bundled
`write-like-me` skill calls `humanizer` in its final editing pass, so install it
if you use that skill.

### humanizer

Strips signs of AI writing. Upstream: [blader/humanizer](https://github.com/blader/humanizer) (MIT).

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

Update later with `git -C ~/.claude/skills/humanizer pull`. For Codex, clone into
`~/.codex/skills/humanizer` instead.

To apply it to every answer instead of on request, add this block to
`~/.claude/CLAUDE.md`:

```markdown
# prose: humanizer (always on)
Apply the humanizer rules to every piece of prose you write: chat replies, commit
messages, READMEs, docs, PR bodies. Full skill at `~/.claude/skills/humanizer/SKILL.md`;
load it with the Skill tool for long-form drafting or editing passes.
```

### i-have-adhd

Shapes every answer so it can be acted on: next action first, numbered steps,
one concrete next step at the end. Upstream:
[ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd).

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

That installs it as an on-demand `/i-have-adhd` command. To make it the default
for every session:

```bash
touch ~/.claude/.i-have-adhd-always
```

A `SessionStart` hook loads the full ruleset whenever the flag file exists. Say
`stop adhd mode` to disable it for the current session, or `rm
~/.claude/.i-have-adhd-always` to go back to on-demand.
