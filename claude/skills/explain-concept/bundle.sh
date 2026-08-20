#!/usr/bin/env sh
# 세 파일을 하나로 이어 붙인다. Codex, 웹 챗 등 스킬 로더가 없는 곳에 붙여 넣을 때 쓴다.
# 사용법:  ./bundle.sh > /tmp/explain-concept.md
d=$(cd "$(dirname "$0")" && pwd)
cat "$d/SKILL.md"
printf '\n\n---\n\n# 부록 A. references/design-principles.md\n\n'
cat "$d/references/design-principles.md"
printf '\n\n---\n\n# 부록 B. references/patterns.md\n\n'
cat "$d/references/patterns.md"
