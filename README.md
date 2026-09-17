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
| `explain-concept`      | Research a concept from primary sources into a self-contained study document. | [✅](claude/skills/explain-concept)      | [✅](codex/skills/explain-concept)      |
| `summary-paper`        | Read a paper with PACES into a Markdown or HTML summary with figures.        | [✅](claude/skills/summary-paper)        | [✅](codex/skills/summary-paper)        |
| `scaffold-react`       | Create or refactor React apps to the bundled scaffold conventions.            | [✅](claude/skills/scaffold-react)       | [✅](codex/skills/scaffold-react)       |
| `cli-user-test`        | Validate a built, unit-tested program as a real user would from the terminal. | [✅](claude/skills/cli-user-test)        | [✅](codex/skills/cli-user-test)        |
| `create-class-diagram` | Create UML class diagrams in uncompressed `.drawio` XML format.               | [✅](claude/skills/create-class-diagram) | [✅](codex/skills/create-class-diagram) |
| `extract-slide-design` | Reverse-engineer slides or report PDFs into a reusable `DESIGN.md`.           | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap`    | Break a project into small, vertical, user-testable iterations.               | [✅](claude/skills/iteration-roadmap)    | [✅](codex/skills/iteration-roadmap)    |
| `modify-class-diagram` | Update an existing `.drawio` class diagram to match a codebase.               | [✅](claude/skills/modify-class-diagram) | [✅](codex/skills/modify-class-diagram) |
| `write-like-me`        | Write figure-first knowledge notes in Cotidie's documented voice.             | [✅](claude/skills/write-like-me)        | [✅](codex/skills/write-like-me)        |


## Third party skills

Upstream projects, not authored here. `karpathy-guidelines` ships as a pinned
snapshot. The other two install separately and are covered in
[INSTALL.md](INSTALL.md#3-third-party-skills).


| Skill                 | Description                                                          | Upstream                                                                                                            | Claude                                 | Codex                                 |
| --------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------- |
| `humanizer`           | Remove signs of AI-generated writing from text.                      | [blader/humanizer](https://github.com/blader/humanizer)                                                             | install                                | install                               |
| `i-have-adhd`         | Shape answers for an ADHD reader: next action first, numbered steps. | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)                                                         | install                                | install                               |
| `karpathy-guidelines` | Keep coding work simple, surgical, explicit, and verifiable.         | [`64723a4`](https://github.com/forrestchang/andrej-karpathy-skills/commit/64723a49ea6117894304eb491f0d32a60570bf45) | [✅](claude/skills/karpathy-guidelines) | [✅](codex/skills/karpathy-guidelines) |


Both `humanizer` and `i-have-adhd` can run on every answer instead of on
request. See [User-scope defaults](INSTALL.md#4-user-scope-defaults).

## Contributing

- Mirror a new skill to both hosts unless one host cannot support it.
- Bump the plugin `version` in `claude/.claude-plugin/plugin.json` and
`codex/.codex-plugin/plugin.json` on every skill change. Minor for adding or
removing a skill, patch for a fix.
- Reflect the change in the skills table above.

