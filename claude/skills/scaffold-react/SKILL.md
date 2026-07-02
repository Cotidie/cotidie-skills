---
name: scaffold-react
description: "Create new React web projects or refactor existing React apps using the bundled React scaffold conventions: route-level lazy loading, page/component folder structure, Redux/SWR/Axios data flow, Formik/Yup forms, styled-components/CSS styling, Storybook, Jest/React Testing Library, ESLint/Prettier, and incremental migration guidance. Use when asked to scaffold a React app, align a React codebase to this architecture, or refactor an existing React project."
trigger: /scaffold-react
---

# Scaffold React

## Core Workflow

1. Inspect the target project before changing files.
   - If the repo has `.codegraph/`, use CodeGraph first to locate React entrypoints, stores, routes, API clients, and tests.
   - Read repository agent instructions and package/config files next (`AGENTS.md`, `CLAUDE.md`, `package.json`, Vite/CRA config, TypeScript config).
   - Preserve the existing toolchain unless the user explicitly asks to replace it.

2. Load `references/react-scaffold-rules.md` before architecture work.
   - Use it for folder layout, provider boundaries, routing, state/data rules, styling, testing, Storybook, and validation commands.

3. For a new CRA-style JavaScript app, use the bundled template:
   ```sh
   python scripts/create_from_template.py \
     --name my-react-app \
     --dest /path/to/my-react-app
   ```
   Run this command from the `scaffold-react` skill directory, or pass the full path to the script after locating the installed skill.
   Then run dependency install and verification from the new project directory.

4. For an existing app, refactor incrementally.
   - Map current routes, reusable components, global state, API helpers, styling, and tests to the scaffold conventions.
   - Move one slice or route at a time, update imports, run focused checks, then continue.
   - Do not copy CRA files into a Vite/Next/TypeScript app wholesale. Translate the architecture to the target project's stack.

## Resource Map

- `references/react-scaffold-rules.md`: bundled React scaffold conventions and migration rules.
- `assets/cra-template/`: bundled CRA-style template without `.git`, `node_modules`, lockfiles, build output, or coverage.
- `scripts/create_from_template.py`: deterministic copier for new CRA-style projects.

## Existing Project Targets

For any existing React project, treat this as a refactor target, not a new scaffold target.

- Use CodeGraph first when the repo is indexed.
- Follow the target repo's instructions (`AGENTS.md`, `CLAUDE.md`, story files, design docs, or equivalent).
- Keep the target project's current toolchain unless the user explicitly asks to replace it.
- Adapt the scaffold concepts to the existing folders, tests, generated files, and design-system rules.
