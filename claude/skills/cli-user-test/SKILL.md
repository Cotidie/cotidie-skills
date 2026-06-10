---
name: cli-user-test
description: Use when a program (CLI tool, REPL/TUI, backend server, script, or library) is built and unit-tested and you need to validate it as a real user would, by driving it through the terminal with varied and adversarial inputs and reporting what works, breaks, or behaves unexpectedly. Triggers include "act as a user", "test this for me", "drive it yourself", smoke test, dogfood, manual/exploratory testing, verifying before a live run, or confirming an assembled feature end to end.
trigger: /cli-user-test
---

# CLI User Test

## Overview

Drive the built program the way a real user would, with your own inputs, and report
findings. Unit tests check units in isolation; this checks the **assembled product**
against real and hostile inputs. Bugs hide in the seams between units, in config and
credentials, and in edge inputs no fixture covered.

A target consumes **inputs** (args, files, stdin, requests, REPL commands) and produces
**outputs and side effects** (stdout, exit code, files, HTTP responses, DB writes).

Core principle: **find the failures the test suite couldn't, then report before fixing.**

## When to use

- A feature/iteration is implemented and its unit tests pass, but nobody has *run it*.
- Before declaring work done, or before an expensive/irreversible live run.
- User says "act as a user", "test this", "try it yourself", "smoke test", "dogfood".

Not for: writing the unit tests themselves (TDD), or reviewing code statically.

## The process

### 1. Read the run guide — required input

Start from a provided "how to run" guide (README, usage doc, `--help`, CLAUDE.md run
section). From it, determine: the entrypoint and how to invoke it, required
config/credentials, external services, and what correct output looks like.

**Gate:** if you cannot determine how to run the program from the docs (no run guide, or
it's ambiguous/incomplete), **STOP and ask the user to write or update the doc** before
testing. Do not guess the run command, invent flags, or reverse-engineer the invocation
from source — a wrong guess produces misleading "bugs," and asking for the doc improves
the project. (Reading source to understand *expected behavior* is fine; guessing *how to
launch it* is not.)

### 2. Generate varied interactions

Build a battery of runs, tiered by cost — cheapest first:

1. **Free:** help, arg/route parsing, offline paths, edge inputs (see table).
2. **Cheap real:** the smallest live invocation.
3. **Scale / irreversible:** last, only after small runs are clean.

- **Substitute expensive/unavailable externals at the seam.** Missing key, paid service,
  GPU, real DB, an input file you don't have — replace it where the code takes the
  dependency (inject a fake, point at a temp/in-memory instance, craft a minimal real
  input) so the *full program still runs end to end*.
- **Push edges on purpose** (table below). Boundaries are where it breaks.
- **Watch non-functional behavior:** latency, resource use, work volume, nondeterminism,
  concurrency, leaked processes/handles, partial writes on interrupt.

### 3. Report

In tiers, and **don't fix silently**:
- ✅ **Works correctly** — what ran as expected, with the observed behavior.
- 🔴 **Issues** — bugs with severity + a one-line repro. Separate *config blockers* (bad
  key, wrong port/model) from *code bugs*.
- 🛠 **Suggestions / fixes** — concrete fix direction per issue. Offer to apply; apply only
  trivial fixes, and only if asked.

## Driving by target shape

| Shape | How to drive it |
|-------|-----------------|
| One-shot CLI | run with args / files / piped stdin; check stdout, exit code, files written |
| Interactive REPL / TUI | pipe or script a command sequence; test quit, bad command, multiline |
| Backend server / daemon | start it; curl health + endpoints (valid + malformed); check clean shutdown, concurrent requests |
| Library (no CLI) | write a tiny driver script that calls the public API |

## Edge inputs to try

| Category | Examples |
|----------|----------|
| Missing / empty | absent file, empty file, empty string, no args, empty request body |
| Malformed | wrong type/format, corrupt file, invalid JSON, bad flags, bad route |
| Boundary | 0, 1, max, oversized input, very long string, deeply nested |
| Exotic values | floats/precision, unicode/emoji, negatives, NaN/inf, complex, huge numbers |
| Failure modes | input that errors, hangs/timeouts, divide-by-zero, resource exhaustion |
| State / idempotency | run twice, same output target, concurrent runs, Ctrl-C mid-run (partial writes?) |
| Config / auth | missing/invalid credentials, wrong endpoint/port/model id, missing config file |

## Common mistakes

- **Guessing how to run it.** No run doc → ask for one; don't invent the command (step 1).
- **Only the happy path.** That's what unit tests already cover. Spend time on edges.
- **Blaming code for a config failure.** A 401/missing-key/port-in-use is usually config,
  not a bug. Confirm the code surfaced it cleanly; report the config separately.
- **`pkill -f <pattern>` that also matches your own new process** → it kills itself
  instantly (exit 137/144). Use a unique pattern or a captured PID.
- **Trusting exit 0.** Check actual output/side effects, not just the return code.
  Block-buffered stdout flushes at the end — a "stuck" run may just be buffering.
- **Leaving a server/daemon running.** Always stop what you started; check for zombies.
- **Fixing while testing.** You lose the finding and conflate cause. Report first.

## Context this skill depends on

- **A run guide** (README/usage/`--help`/run section) — the required starting input. If
  absent or unclear, ask the user to provide it (step 1 gate).
- **How to run it** (interpreter, build step, venv, working dir, how to start/stop a server).
- **Config/credential locations** (`.env`, env vars, config files) and which paths need them.
- **External dependencies it calls** (APIs, models, DBs, hardware) and their cost.
- **A seam to substitute** those externals (an injected dependency, a temp instance, a mock).
- **Expected behavior / ground truth** to judge output against.

## Dependencies

- A terminal (Bash) and the project's installed runtime + deps (plus a build/start step
  if it's a server or compiled tool).
- Optionally valid credentials for the live path; otherwise stub the external call.
- Any sample inputs or fixtures the project ships, reusable as test inputs.
