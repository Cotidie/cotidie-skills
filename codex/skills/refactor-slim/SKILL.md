---
name: refactor-slim
description: Use when asked to refactor, clean up, simplify, slim, or restructure a codebase or module ("리팩토링", "정리", "단순화", "구조 개선", "모듈 분리", "파일 분리/통합", "가드레일 걷어내기", "불필요한 코드 삭제"), or when code shows defensive clutter (broad try/except, None/isinstance guards on internal calls, hand-written utilities a library covers, pass-through classes, magic values, unreferenced functions, tests that pin trivia) or structural trouble (functions doing several jobs, wide or leaky interfaces, files holding unrelated things, one concept scattered over many files, modules importing each other in a circle).
---

# Refactor Slim

## Overview

Two responsibilities, with two different goals:

1. **Slimming**: remove what the product does not need. Default to deletion. Every guard, fallback, layer, constant, and test has to earn its place; "it might be used" or "it is the current behavior" does not earn it.
2. **Structure**: put what remains in the right units. The goal is clear boundaries between functions, interfaces, files, and modules. Line count is not the measure here: a structural change that adds lines is fine when each unit ends up with one job and one reason to change.

Behavior the product needs stays the same in both.

**Violating the letter of these rules is violating the spirit.**

## Order

Slim first (passes 1, 2, 4, 5, 6), then structure (pass 3). Structuring code you are about to delete wastes the work. Record each change in one line as you go.

## Slimming passes

| Pass | Look for | Do |
|---|---|---|
| 1. Guardrails | `if x is None: raise`, `isinstance` coercion, empty-input early returns, caps like `[:500]`, checks on values your own code produces | Delete unless the value crosses a trust boundary (HTTP input, file on disk, user text) |
| 2. Libraries | Hand-written slugify, retry, date/path/URL parsing, validation, CLI parsing, caching | Search for the maintained library (latest version), replace, keep only glue |
| 4. Conditionals and exceptions | `except Exception` that logs and returns `None`/default, nested try, if/else ladders, duplicated default dicts | Let errors raise to one handler at the edge (route, CLI main). Replace ladders with a table, `f"{n:02d}"`, `dict.get`, pydantic defaults |
| 5. Hardcoding | Ports, hosts, paths, limits, labels inside logic | Move to settings/config if a user could change it; delete if nothing needs it; a named constant only when it carries meaning |
| 6. Dead code and tests | No reference in the repo (grep, `vulture`, `knip`, `ts-prune`), "used by v0/legacy" comments, tests of deleted guards, tests of private helpers, tests that restate the implementation | Delete. Tests stay only for behavior a user or caller sees |

## Pass 3: Structure

Work from the smallest unit to the largest. At each level both directions are open: split what holds two things, merge what was cut apart for no reason.

| Level | Split when | Merge or inline when | Target |
|---|---|---|---|
| Function / method | It does several jobs in sequence, mixes levels (parsing next to business rules next to I/O), takes flag arguments that select a behavior, or needs a comment per block | A helper is called once and its name says no more than its body; two functions differ by one argument | One job per function, named by what it gives the caller. A reader follows the top-level function without opening the helpers |
| Interface (signatures, class surface, protocol, API) | A class serves two kinds of caller; a parameter list carries values that travel together (make them one object); callers reach through an object into its internals | An interface has one implementation and no test fake; a service only delegates; a manager wraps one call | The smallest surface callers need. Dependencies passed in, internals hidden, the same idea spelled the same way everywhere |
| File | It holds unrelated things, or you scroll past one concept to reach another | One concept is spread over several small files that always change together; a file exists for one tiny type or constant | One concept per file. The file name tells what is inside |
| Module / package | It has two areas with separate callers; a change in one area forces edits in the other | Two modules import each other, or one is only ever used by the other | Dependencies point one way (no cycles), lower layers know nothing of upper ones, and a feature lives in one place |

How to decide, when unsure:

- **Follow the reasons to change.** Things that change together belong together; things that change for different reasons belong apart.
- **Follow the callers.** Structure serves whoever reads and calls the code. A boundary no caller benefits from is a layer to inline.
- **Move, do not rewrite.** A structural change relocates and renames code. Logic changes go in a separate change, so the diff stays reviewable.
- **Update every caller in the same change.** No re-export shims, no aliases for the old name, no "kept for compatibility" inside one repo.

### Not short-coding

Structure work never aims at fewer characters or lines. Do not:

- Fold clear statements into dense one-liners, nested comprehensions, chained ternaries, or walrus tricks
- Shorten names (`cfg`, `mgr`, `tmp2`) or drop a variable whose name explained a step
- Merge unrelated things because the result is shorter
- Replace a readable loop with a clever expression

If a change makes the code shorter but harder to follow, revert it. If it makes the code longer but each unit clearer, keep it.

## Rules that settle the usual arguments

- **"External callers might use it."** The repo is the evidence. No reference and no public package export means delete. Git history keeps it.
- **"Changing the error behavior changes the public contract."** Swallowing errors into `None` is a bug the contract hid. Raise; map the exception once at the boundary. Update the callers in the same change.
- **"Keep it as a named constant."** Moving `8180` into `PORT = 8180` inside the same module is not a fix. Pass 5 decides: config, meaning, or delete.
- **"Splitting adds lines, and this skill is about less code."** Slimming is about less code. Structure is about boundaries. A split that gives each unit one job stands even when the total grows.
- **"A smaller file count is simpler."** Count concepts per file, not files. Merge only what changes together.
- **Behavior the product needs stays.** Bugs you find are reported separately, not fixed silently in the same change.
- **Never add a test for code you could delete instead.**

## Red flags - stop and reconsider

- Writing a test for a function nothing calls
- "Kept because the comment says..."
- "Kept to preserve the current (swallowing) behavior"
- Re-implementing a regex/loop a library already ships
- A class whose methods each call one other object's method
- Judging a structural change by its line count
- A function you can only name with "and" (`load_and_validate_and_save`)
- A new file or module named `utils`, `helpers`, `common`, or `misc`
- A refactor that leaves the old name behind as an alias

## Verification

1. Full test suite green (the project's own command, not one file).
2. Dead-code tool clean, or each remaining hit explained as a false positive.
3. Slimming: `git diff --stat` shows net deletion; if it grew, name what the growth buys.
4. Structure: no import cycles (`pydeps`, `madge`, `import-linter`, or the project's own layer test), every moved name has no reference to its old location, and each split or merge is stated as "X now owns Y".
5. Commit only the touched files. Slimming and structure go in separate commits when both are large.

## Report

1. Slimming table: pass, file:line, change.
2. Structure table: level (function, interface, file, module), before, after, the reason to change that drove it.
3. "Kept": each item with the trust boundary or user-visible behavior that justifies it.
4. "Bugs found, not fixed".
5. Net line count for slimming. For structure, give the unit counts instead (functions, files, modules before and after).
