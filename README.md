# cotidie-skills

Custom agent skills for Claude Code and Codex, in one plugin named `cotidie`.

- `claude/` serves Claude Code, `codex/` serves Codex.
- Invoke as `cotidie:<skill>` in Claude Code, `$cotidie:<skill>` in Codex.
- Install steps live in [INSTALL.md](INSTALL.md). Point an agent at it and the
whole environment rebuilds itself.

## Skills


| Skill                  | Description                                                                   | Claude                                  | Codex                                  |
| ---------------------- | ----------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------- |
| `pr-writer`            | Draft a PR or MR title and body from a branch diff, commits, or summary.      | [✅](claude/skills/pr-writer)            | [✅](codex/skills/pr-writer)            |
| `textbook-notes`       | Distill math-heavy textbook chapters into study notes with offline HTML.      | [✅](claude/skills/textbook-notes)       | [✅](codex/skills/textbook-notes)       |
| `summary-paper`        | Read a paper with PACES into a Markdown or HTML summary with figures.        | [✅](claude/skills/summary-paper)        | [✅](codex/skills/summary-paper)        |
| `scaffold-react`       | Create or refactor React apps to the bundled scaffold conventions.            | [✅](claude/skills/scaffold-react)       | [✅](codex/skills/scaffold-react)       |
| `create-class-diagram` | Create UML class diagrams in uncompressed `.drawio` XML format.               | [✅](claude/skills/create-class-diagram) | [✅](codex/skills/create-class-diagram) |
| `extract-slide-design` | Reverse-engineer slides or report PDFs into a reusable `DESIGN.md`.           | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap`    | Break a project into small, vertical, user-testable iterations.               | [✅](claude/skills/iteration-roadmap)    | [✅](codex/skills/iteration-roadmap)    |
| `refactor-slim`        | Slim a codebase, then fix function, interface, file, and module boundaries.   | [✅](claude/skills/refactor-slim)        | [✅](codex/skills/refactor-slim)        |


## Third party skills

Upstream projects, not authored here. Each installs from its own repo; see
[INSTALL.md](INSTALL.md#2-third-party-skills).


| Skill                 | Description                                                          | Upstream                                                                                      | Claude  | Codex   |
| --------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------- | ------- |
| `humanizer`           | Remove signs of AI-generated writing from text.                      | [blader/humanizer](https://github.com/blader/humanizer)                                       | install | install |
| `i-have-adhd`         | Shape answers for an ADHD reader: next action first, numbered steps. | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)                                   | install | install |
| `karpathy-guidelines` | Keep coding work simple, surgical, explicit, and verifiable.         | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | install | install |


Both `humanizer` and `i-have-adhd` can run on every answer instead of on
request. See [User-scope defaults](INSTALL.md#3-user-scope-defaults).

## Contributing

- Mirror a new skill to both hosts unless one host cannot support it.
- Bump the plugin `version` in `claude/.claude-plugin/plugin.json` and
`codex/.codex-plugin/plugin.json` on every skill change. Minor for adding or
removing a skill, patch for a fix.
- Reflect the change in the skills table above.

