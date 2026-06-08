# codex-image — example

A peaceful fantasy world on a sunny day, generated with this skill.

## Prompt

> A serene fantasy countryside basking in bright midday sun, rolling emerald
> hills strewn with wildflowers, a sparkling river crossed by a small arched
> stone bridge, a cozy village of thatched cottages with smoking chimneys, a
> graceful fairytale castle on a distant gentle hill, soft cumulus clouds and a
> couple of whimsical airships drifting by, warm golden sunlight with gentle god
> rays, lush vibrant greens accented by soft pastels, painterly storybook
> concept-art style, wide cinematic composition, cheerful and tranquil mood.
> Avoid: text, watermark, logos, darkness, storms, menacing elements.

Built with the skill's scaffold — **scene/backdrop → subject → details →
constraints** — and a trailing `Avoid:` clause to suppress unwanted elements.

## Command

```bash
"${CLAUDE_PLUGIN_ROOT}/claude-skills/codex-image/codex-image.sh" "<prompt above>" peaceful-fantasy.png
```

## Result

![Peaceful sunny fantasy world](peaceful-fantasy.png)
