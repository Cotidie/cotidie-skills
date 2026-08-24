# INSTALL

Instructions for an agent setting up a machine. Goal: after running these
sections, Claude Code and Codex expose the same skills as the author's own
setup.

Run sections in order. Skip a host that is not installed. Every section ends
with a verification command; run it before moving on.

## 1. This repo's plugin

Ships as `cotidie` on both hosts. Skills invoke as `cotidie:<skill>` in Claude
Code and `$cotidie:<skill>` in Codex.

### Claude Code

```bash
claude plugin marketplace add Cotidie/cotidie-skills
claude plugin install cotidie@cotidie-skills
```

Verify: `claude plugin list` lists `cotidie@cotidie-skills`.

### Codex

```bash
codex plugin marketplace add Cotidie/cotidie-skills
codex plugin add cotidie@cotidie-skills
```

Verify: `codex plugin list` shows `cotidie@cotidie-skills` as `installed, enabled`.

### Updating later

- Claude Code: `claude plugin marketplace update cotidie-skills`
- Codex: `codex plugin marketplace upgrade cotidie-skills`, then
  `codex plugin remove cotidie && codex plugin add cotidie@cotidie-skills`

## 2. Single-host skills

Most skills ship for both hosts. The README table marks the exceptions with
`❌`. Today that is `codex-image`, which ships for Claude Code only.

To use a single-host skill on the other host, copy the skill directory into
that host's user skills directory:

- into Claude Code: `~/.claude/skills/<name>`
- into Codex: `~/.codex/skills/<name>`

```bash
git clone https://github.com/Cotidie/cotidie-skills.git /tmp/cotidie-skills
mkdir -p ~/.codex/skills
cp -r /tmp/cotidie-skills/claude/skills/codex-image ~/.codex/skills/codex-image
```

An imported skill sits outside the plugin, so it invokes as `$codex-image`
rather than `$cotidie:codex-image`. It also does not update with the plugin;
re-copy it after a plugin update.

Verify: the skill directory exists and holds a `SKILL.md`.

## 3. Third-party skills

Maintained elsewhere, deliberately not vendored here.

### humanizer

Removes signs of AI writing. Upstream: <https://github.com/blader/humanizer> (MIT).
The bundled `write-like-me` skill calls it in its final editing pass.

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer

# Codex, same skill, separate copy
mkdir -p ~/.codex/skills
git clone https://github.com/blader/humanizer.git ~/.codex/skills/humanizer
```

Update with `git -C ~/.claude/skills/humanizer pull`.

Verify: `~/.claude/skills/humanizer/SKILL.md` exists.

### i-have-adhd

Shapes answers for an ADHD reader. Upstream: <https://github.com/ayghri/i-have-adhd>.

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd

codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Verify: `claude plugin list` and `codex plugin list` both show it.

## 4. User-scope defaults

Sections 1 to 3 leave every skill on demand. This section makes two of them
apply to every answer.

### i-have-adhd, always on

Claude Code reads a flag file at session start:

```bash
touch ~/.claude/.i-have-adhd-always
```

The `SessionStart` hook loads the ruleset whenever that file exists. `stop adhd
mode` disables it for one session; delete the file to go back to on demand.

Codex has no equivalent hook. Invoke `$i-have-adhd` explicitly, or paste the
rules into `~/.codex/AGENTS.md`.

### humanizer, always on

No flag file. Add the block below to the user-scope instruction file, which is
`~/.claude/CLAUDE.md` for Claude Code and `~/.codex/AGENTS.md` for Codex.
Append it; do not overwrite a file that already has content.

```markdown
# prose: humanizer (always on)
Apply the humanizer rules to every piece of prose you write: chat replies, commit
messages, READMEs, docs, PR bodies. Full skill at `~/.claude/skills/humanizer/SKILL.md`;
load it with the Skill tool for long-form drafting or editing passes.
```

Point the path at `~/.codex/skills/humanizer/SKILL.md` in the Codex copy.

Verify: the block appears once in the file.

## 5. Final check

```bash
claude plugin list
codex plugin list
ls ~/.claude/skills ~/.codex/skills
ls ~/.claude/.i-have-adhd-always
```

Expected: `cotidie` and `i-have-adhd` installed on both hosts, `humanizer`
present in both skills directories, and the ADHD flag file in place.
