---
name: codex-image
description: Create or edit a raster/bitmap image (photo, illustration, infographic, UI mockup, texture, sprite, cover art) via the installed Codex CLI. NOT for diagrams, flowcharts, wireframes, icons, or logos; use mermaid/SVG for those.
---

# codex-image

## Overview

Claude has no native image generation. The `codex` CLI does, via its built-in
`image_gen` tool (uses the user's Codex auth — **no `OPENAI_API_KEY` needed**).
Drive it from Bash, then collect the PNG it writes.

## When to use

- New raster asset: photo, illustration, concept art, hero/cover, infographic,
  product/UI mockup, texture, sprite.
- Editing an existing image (background swap, object removal, style transfer).

## When NOT to use

- **Diagrams, flowcharts, architecture diagrams, sequence/ER diagrams** → mermaid.
- Wireframes, icons, logos, simple shapes → SVG / HTML / CSS.
- Anything that should be deterministic code-native output.

## Quick procedure

Use the wrapper — it runs Codex, locates the PNG, and prints the final path:

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/codex-image/codex-image.sh" "<prompt>" [dest.png]
```

- Omit `dest.png` → prints the source path under `~/.codex/generated_images/`.
- Give `dest.png` → copies there and prints it (use a versioned name like
  `hero-v2.png`; never overwrite an existing asset unless asked).

Then **verify**: `Read` the printed path to confirm the image matches intent
before using it. Iterate with one targeted change if needed.

## Prompt scaffold

Order: **scene/backdrop → subject → details → constraints**. Quote any in-image
text verbatim. Keep it tight; only add detail that materially helps.

```
A <style/medium> <subject>, <composition/framing>, <lighting/mood>,
<color palette>. Text (verbatim): "<exact text>". Constraints: <must-keep>;
Avoid: <no logos, no watermark, ...>.
```

## How it works (manual fallback if the script breaks)

The built-in tool does NOT return a path. Resolve it from the session id:

1. Run: `codex exec --sandbox workspace-write --skip-git-repo-check "<prompt>" < /dev/null`
2. Grep the output header for `session id: <id>`.
3. PNG lands at `~/.codex/generated_images/<id>/ig_*.png` (one per generated image).

Three flags are mandatory — each fixes a real failure:

| Flag / piece | Without it |
| --- | --- |
| `--skip-git-repo-check` | "Not inside a trusted directory" refusal |
| `< /dev/null` | hangs: "Reading additional input from stdin" |
| `--sandbox workspace-write` | can't write output |

Prompt must say **"use the built-in image_gen tool only — no code, no CLI
fallback"**, else Codex may write a Python/SVG script instead, or fall to the
CLI path that needs `OPENAI_API_KEY`.

## Common mistakes

- Expecting `codex exec` to print the file path — it won't. Use the session id.
- Running in a non-git / untrusted dir without `--skip-git-repo-check`.
- Using this for diagrams — wrong tool; use mermaid/SVG.
- Overwriting an existing asset — write a `-v2` sibling instead.
- Transparent background: built-in tool can't do true alpha. Generate on a flat
  `#00ff00` chroma-key bg, then remove with
  `~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py`. True native
  transparency needs the CLI fallback (`gpt-image-1.5` + `OPENAI_API_KEY`) — ask
  the user first.
