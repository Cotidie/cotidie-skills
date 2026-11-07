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
| `summary-paper`        | Read a paper with PACES into a Markdown or HTML summary with figures.        | [✅](claude/skills/summary-paper)        | [✅](codex/skills/summary-paper)        |
| `paper-visual`         | Turn one paper into a visual study page with animations and offline HTML.     | [✅](claude/skills/paper-visual)         | [✅](codex/skills/paper-visual)         |
| `scaffold-react`       | Create or refactor React apps to the bundled scaffold conventions.            | [✅](claude/skills/scaffold-react)       | [✅](codex/skills/scaffold-react)       |
| `create-class-diagram` | Create UML class diagrams in uncompressed `.drawio` XML format.               | [✅](claude/skills/create-class-diagram) | [✅](codex/skills/create-class-diagram) |
| `extract-slide-design` | Reverse-engineer slides or report PDFs into a reusable `DESIGN.md`.           | [✅](claude/skills/extract-slide-design) | [✅](codex/skills/extract-slide-design) |
| `iteration-roadmap`    | Break a project into small, vertical, user-testable iterations.               | [✅](claude/skills/iteration-roadmap)    | [✅](codex/skills/iteration-roadmap)    |
| `refactor-slim`        | Slim a codebase, then fix function, interface, file, and module boundaries.   | [✅](claude/skills/refactor-slim)        | [✅](codex/skills/refactor-slim)        |


## Third party skills and MCP servers

Upstream projects, not authored here, grouped by when they help. Anthropic's
built-in and official skills are left out. Install steps for `humanizer`,
`i-have-adhd`, and `karpathy-guidelines` live in
[INSTALL.md](INSTALL.md#2-third-party-skills); the others install from their
upstream README.

### 1. Coding

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `superpowers` | plugin, 15 skills | Brainstorm, plan, test first, debug, review, and finish a branch. | [obra/superpowers](https://github.com/obra/superpowers) |
| `mattpocock skills` | 29 skills | Design deep modules, grill a plan, write specs and tickets, TDD, diagnose bugs. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `karpathy-guidelines` | plugin | Keep coding work simple, surgical, explicit, and verifiable. | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) |
| `chrome-devtools-mcp` | plugin, 7 skills + MCP | Debug pages in Chrome: performance, memory leaks, accessibility, cookies. | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| `GitNexus` | 12 skills + MCP | Index a repo as a code graph to explore, trace impact, refactor, and review. | [abhigyanpatwari/GitNexus](https://github.com/abhigyanpatwari/GitNexus) |
| `context7` | MCP | Fetch current library docs and code examples. | [upstash/context7](https://github.com/upstash/context7) |

### 2. Research

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `academic-research-skills` | plugin, 8 skills | Plan, write, review, and revise papers; deep research and citation checks. | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |
| `scholar-megasearch` | 2 skills | Search arXiv, Semantic Scholar, and other databases at once and merge the results. | [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) |
| `paper-forge` | skill | Explain one paper in chat: the authors' reasoning, the method, critique, follow-up ideas. Upstream has no license, so the adapted copy stays local. | [FeijiangHan/PaperForge](https://github.com/FeijiangHan/PaperForge) |
| `paper-craft-skills` | 3 skills | Turn a paper into an HTML article, method figures, or a slide deck. | [zsyggg/paper-craft-skills](https://github.com/zsyggg/paper-craft-skills) |
| `scientific-agent-skills` | 4 skills | Statistics, critical appraisal, scientific figures, Hugging Face Transformers. | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) |
| `paper-search-mcp` | MCP | Search and download papers from arXiv, PubMed, Semantic Scholar, and more. | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) |
| `asta` | MCP, hosted | Query Ai2's scientific literature graph. | [Ai2 Asta](https://allenai.org/asta/resources/mcp) |
| `zotero-mcp` | MCP | Search, read, and annotate the Zotero library. | [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) |
| `matlab` | MCP | Run and test MATLAB code in the local MATLAB. | [matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server) |

### 3. Writing

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `stop-slop` | skill | Remove AI writing patterns from prose. | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) |
| `humanizer` | skill | Remove signs of AI-generated writing from text. | [blader/humanizer](https://github.com/blader/humanizer) |
| `markitdown-mcp` | MCP | Convert PDF, Office, and other files to Markdown. | [trsdn/markitdown-mcp](https://github.com/trsdn/markitdown-mcp) |
| `notion` | MCP, hosted | Read and write Notion pages and databases. | [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) |

### 4. Visuals and slides

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `frontend-slides` | plugin | Build animated HTML slide decks, or convert PPTX to web. | [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) |
| `diagram-design` | plugin, 7 skills | Draw and export diagrams; import draw.io, Excalidraw, and Mermaid. | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) |
| `manimgx` | skill | Author and render math and 3D animations with ManimGX. | [academa-labs/manimgx](https://github.com/academa-labs/manimgx) |
| `shaders` | skill + MCP | Build WebGPU visual effects with the Shaders component library. | [shader-effects-inc/shaders](https://github.com/shader-effects-inc/shaders) |
| `openrouter-images` | skill | Generate and edit images through OpenRouter's Image API. | [OpenRouterTeam/skills](https://github.com/OpenRouterTeam/skills) |
| `impeccable` | plugin, skill + hook, per project | Steer, critique, and audit web UI design, and flag AI design slop. | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |

`textbook-notes` and `paper-visual` call `manimgx` and `openrouter-images` for
their animations and figures.

Install `impeccable` per web project, never globally. Its design hook scans
every HTML, CSS, and JS edit wherever it is enabled, including the HTML that
`textbook-notes` and `paper-visual` write. From the web project's root:

```bash
claude plugin marketplace add pbakaus/impeccable   # once per machine
claude plugin install impeccable@impeccable --scope local
```

### 5. Web and daily life

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `firecrawl` | MCP, hosted | Search the web and scrape pages to Markdown. | [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) |
| `playwright` | MCP | Drive a browser for tests and automation. | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) |
| `browseros-neo` | skill + MCP | Work in BrowserOS neo, a local browser signed into the user's accounts. | [browseros-ai/BrowserOS](https://github.com/browseros-ai/BrowserOS) |
| `k-skill` | 3 skills | Book SRT trains, look up Korail timetables, compare prices on Danawa. | [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) |

### 6. Agent operations

| Name | Kind | Use | Upstream |
| --- | --- | --- | --- |
| `claude-mem` | plugin, 30 skills + MCP | Keep memory and work state across sessions, and search past work. | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) |
| `orca` | 3 skills | Run Orca worker agents and worktrees, and drive app windows. | [stablyai/orca](https://github.com/stablyai/orca) |
| `codex` | plugin, 5 skills | Hand a task or a second opinion to Codex from Claude Code. | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) |
| `claude-dashboard` | plugin, 4 skills | Show usage limits of AI CLIs in the status line. | [uppinote20/claude-dashboard](https://github.com/uppinote20/claude-dashboard) |
| `i-have-adhd` | plugin | Shape answers for an ADHD reader: next action first, numbered steps. | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) |


Both `humanizer` and `i-have-adhd` can run on every answer instead of on
request. See [User-scope defaults](INSTALL.md#3-user-scope-defaults).

## Contributing

- Mirror a new skill to both hosts unless one host cannot support it.
- Bump the plugin `version` in `claude/.claude-plugin/plugin.json` and
`codex/.codex-plugin/plugin.json` on every skill change. Minor for adding or
removing a skill, patch for a fix.
- Reflect the change in the skills table above.
- Add or drop a third-party row when an upstream skill or MCP server is installed
or removed.

