# cotidie-skills

Custom agent skills split by host: `claude/` serves Claude Code, `codex/` serves
Codex. Both ship under the `cotidie` plugin name.

## Version bump rule

Bump the plugin `version` on every change that adds, removes, or modifies a
skill. Two files hold it and must stay in sync:

- `claude/.claude-plugin/plugin.json`
- `codex/.codex-plugin/plugin.json`

Semver:

- Add or remove a skill, or a user-facing feature → **minor** (`0.2.0` → `0.3.0`).
- Fix or tweak an existing skill → **patch** (`0.2.0` → `0.2.1`).

A stale version does not block `claude plugin marketplace update` (git sources
pull the branch regardless), but it leaves `plugin list`/`details` showing the
wrong version and hides what changed. Always bump.

## Keeping hosts in sync

A skill added to one host should usually be mirrored to the other. Reflect every
skill change in the README support table.
