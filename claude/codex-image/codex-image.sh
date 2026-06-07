#!/usr/bin/env bash
# codex-image.sh — generate a raster image via Codex's built-in image_gen tool.
#
# Usage: codex-image.sh "<prompt>" [dest.png]
#   - No dest: prints the source PNG path under ~/.codex/generated_images/<sid>/
#   - With dest: copies there (mkdir -p) and prints the dest path.
#
# Uses the user's Codex auth (no OPENAI_API_KEY). Built-in tool only — no CLI
# fallback, no codegen. The built-in tool does not return a path, so we resolve
# it from the session id printed in the exec header.
set -euo pipefail

prompt="${1:?usage: codex-image.sh \"<prompt>\" [dest.png]}"
dest="${2:-}"

instruction="Use your built-in image_gen tool to generate: ${prompt}
Use the built-in image_gen tool only — no code, no CLI fallback. Do not ask clarifying questions; proceed with reasonable defaults."

# 2>&1: the session-id header may go to stderr; we need it in the captured text.
out="$(codex exec --sandbox workspace-write --skip-git-repo-check "$instruction" < /dev/null 2>&1)" || {
  printf '%s\n' "$out" >&2
  echo "ERROR: codex exec failed" >&2
  exit 1
}

sid="$(printf '%s\n' "$out" | grep -oiE 'session id: [0-9a-fA-F-]+' | head -1 | awk '{print $NF}')"
if [ -z "$sid" ]; then
  printf '%s\n' "$out" >&2
  echo "ERROR: could not parse session id from codex output" >&2
  exit 1
fi

dir="${CODEX_HOME:-$HOME/.codex}/generated_images/$sid"

# The file may land a moment after exec returns; poll briefly.
png=""
for _ in 1 2 3 4 5 6; do
  png="$(ls -t "$dir"/*.png 2>/dev/null | head -1 || true)"
  [ -n "$png" ] && break
  sleep 1
done
if [ -z "$png" ]; then
  echo "ERROR: no PNG found in $dir" >&2
  echo "--- codex output ---" >&2
  printf '%s\n' "$out" >&2
  exit 1
fi

if [ -n "$dest" ]; then
  mkdir -p "$(dirname "$dest")"
  cp "$png" "$dest"
  printf '%s\n' "$dest"
else
  printf '%s\n' "$png"
fi
