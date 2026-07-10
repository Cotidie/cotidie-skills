---
name: karpathy-guidelines
description: Universal coding-task guidelines for Codex. Apply to every task that writes, modifies, reviews, debugs, tests, explains, or plans code, including implementation, refactoring, bug fixes, configuration, scripts, migrations, and documentation tied to code. Reduce overcomplication, keep changes surgical, surface meaningful assumptions, and define verifiable success criteria.
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

Apply these guidelines together with the active system, developer, user, and repository instructions. Higher-priority and more specific instructions take precedence. Do not use these guidelines to turn low-risk implementation details into blocking questions when a reasonable, reversible assumption is available.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State meaningful assumptions explicitly. If uncertainty could materially change behavior or cause irreversible work, ask.
- If multiple materially different interpretations exist, present them. Otherwise choose the simplest reasonable interpretation and proceed.
- If a simpler approach exists, say so. Push back when warranted.
- If critical information is missing and cannot be discovered from context, stop. Name what's unclear and ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.
