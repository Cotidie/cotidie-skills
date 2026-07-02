# React Scaffold Rules

Distilled from the bundled CRA-style scaffold template and generalized for new React projects and existing React refactors.

## Source Scaffold Profile

- Toolchain: Create React App (`react-scripts`), React 18, JavaScript.
- Routing: `react-router-dom` v6.
- Global state: Redux Toolkit `configureStore` with traditional reducers/actions.
- Server/cache: Axios instance plus SWR fetcher and `mutate` after writes.
- Forms: Formik with Yup validation.
- Styling: styled-components for reusable components; colocated CSS for pages/global app styles.
- UI docs: Storybook 7 with CRA preset.
- Tests: Jest and React Testing Library with `@testing-library/jest-dom`.
- Code quality: ESLint, Prettier, husky/lint-staged.

## Folder Layout

Use this shape for new apps, or as a migration target for existing apps:

```text
src/
  App.js
  index.js
  setupTests.js
  action/
    ActionTypes.js
    AppActions.js
  reducers/
    AppReducer.js
    index.js
  store/
    index.js
  utils/
    axiosInstance.js
    fetcher.js
  pages/
    Home/
      Home.js
      Home.css
    About/
      About.js
      About.css
  components/
    Button/
      Button.js
      Button.stories.js
    ComponentName/
      ComponentName.js
      ComponentName.test.js
      ComponentName.stories.js
```

Conventions:

- Put route-level screens in `src/pages/<PageName>/`.
- Put reusable UI and form controls in `src/components/<ComponentName>/`.
- Keep component-specific styled-components in the component file for small components, or in `<ComponentName>Styled.js` when styles are substantial or shared across sibling elements.
- Put global store creation under `src/store/`, root reducer composition under `src/reducers/`, and action constants/creators under `src/action/` when following the source scaffold exactly.
- For TypeScript or modern Redux projects, prefer target-stack conventions such as slices, typed hooks, and `.tsx` files while keeping the same architectural boundaries.

## App Boundary

The scaffold puts cross-cutting providers at the app/root boundary:

- `index.js`: create React root, wrap `<App />` in Redux `<Provider store={store}>`, and enable `React.StrictMode`.
- `App.js`: wrap routes with `BrowserRouter`, top-level navigation, `SWRConfig`, `ErrorBoundary`, and `Suspense`.
- Route components are lazy loaded with `React.lazy`.
- `Suspense` fallback should be simple and non-blocking.
- Use an `ErrorBoundary` around lazy/data-driven route content.

Example provider order from the scaffold:

```jsx
<Provider store={store}>
  <React.StrictMode>
    <App />
  </React.StrictMode>
</Provider>
```

```jsx
<Router>
  <Navbar />
  <SWRConfig value={{ refreshInterval: 3000 }}>
    <ErrorBoundary>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>{/* lazy route elements */}</Routes>
      </Suspense>
    </ErrorBoundary>
  </SWRConfig>
</Router>
```

Adjust provider order only when the target app has a clear dependency reason.

## Routing And Pages

- Use `react-router-dom` v6 `Routes`/`Route`.
- Lazy import page components from `src/pages`.
- Keep page-specific document metadata in the page when SEO matters; the source scaffold uses `react-helmet`.
- Keep nav links in a reusable `Navbar` component using router `Link`/`NavLink`.

## State Management

- The scaffold uses Redux Toolkit `configureStore` but traditional `ActionTypes`, action creators, and reducers.
- Keep root reducer composition centralized in `src/reducers/index.js`.
- Keep the store exported from `src/store/index.js`.
- Use `useSelector` and `useDispatch` inside pages/components.
- For new TypeScript refactors, adapt to typed Redux hooks or an existing state library rather than forcing legacy action/reducer files.

## API And Cache

- Put the configured Axios client in `src/utils/axiosInstance.js`.
- Put the SWR fetcher in `src/utils/fetcher.js`.
- Prefer environment-derived `baseURL` in real projects; the scaffold's hard-coded JSONPlaceholder URL is only a placeholder.
- Keep auth/error response interceptors in the Axios instance.
- Use SWR keys that match the fetcher's URL convention.
- After writes, trigger revalidation with `mutate(key)` for affected reads.
- Avoid mixing raw `fetch` and Axios in production code unless there is a deliberate boundary; the scaffold demonstrates both, but the reusable rule is to centralize API behavior.

## Forms

- Use Formik for form state and submission.
- Use Yup for validation schema.
- Reuse labeled input components.
- Validate on blur for user-facing forms when possible; avoid noisy validation on every keystroke unless the product needs it.
- Keep labels connected with `htmlFor`/`id` so React Testing Library can query by label.

## Styling

- Prettier settings from the scaffold:
  - single quotes
  - no semicolons
  - 2-space indentation
  - trailing commas
  - print width 80
- Use styled-components for reusable UI primitives and structured component styles.
- Use colocated page CSS for page-level layout when the target app already uses CSS.
- Keep cards and modals modest: radius around 8px, no unnecessary nested cards.
- When refactoring an existing design system, preserve tokens and generated CSS rules instead of introducing raw colors/spacing.

## Storybook

- Add `.stories.js`/`.stories.tsx` for reusable components that have visual states.
- Keep stories near the component.
- Use Storybook config to load `../src/**/*.stories.@(js|jsx|mjs|ts|tsx)` and MDX if present.
- For portable Storybook static assets, prefer `staticDirs: ['../public']`; avoid Windows-only path separators.

## Tests

- Keep `setupTests.js` importing `@testing-library/jest-dom`.
- Test reusable controls and forms with React Testing Library.
- Prefer user-visible queries (`getByRole`, `getByLabelText`, `getByText`).
- Cover at least:
  - component rendering
  - event callbacks
  - validation/error display
  - successful form submission
- Snapshot tests may exist, but do not rely on snapshots alone for behavior.

## Import Paths

- The source scaffold uses `jsconfig.json` with `baseUrl: "src"` so imports can use `components/Button/Button`, `action/AppActions`, and `reducers/index`.
- In TypeScript/Vite projects, preserve or add equivalent aliases through `tsconfig` and bundler config only if the app already supports them or the migration is broad enough to justify it.
- Update tests, stories, and barrel exports when moving components.

## New Project Checklist

1. Copy the template with `scripts/create_from_template.py`.
2. Install dependencies.
3. Replace placeholder package name, API base URL, routes, metadata, and example JSONPlaceholder calls.
4. Decide whether to keep CRA. If the user wants Vite/TypeScript, create the project with that stack and port the rules, not the CRA files.
5. Run `npm run lint`, `npm test`, `npm run build`, and `npm run storybook` or `npm run build-storybook` as appropriate.

## Existing Project Refactor Checklist

1. Read repo instructions and detect stack.
2. If `.codegraph/` exists, use CodeGraph before grep/find/manual file reads.
3. Inventory current structure: entrypoint, app shell, routes, global state, API clients, reusable components, tests, Storybook, styling/tokens.
4. Choose one migration slice:
   - app providers
   - route/page folder organization
   - component colocation
   - API/SWR/fetcher centralization
   - form extraction
   - tests/stories
5. Preserve behavior and public contracts.
6. Run focused checks for the touched slice, then broader checks.

## Existing Project Notes

Do not assume an existing target is a CRA app. Many targets may use Vite, Next.js, TypeScript, generated API clients, generated design tokens, or domain-specific folder boundaries.

When applying this skill to an existing codebase:

- Use CodeGraph first when available.
- Work from the frontend package directory when the repo is a monorepo.
- Keep generated API types generated; do not hand-author generated files.
- Preserve generated design-token flows and project design-system rules.
- Adapt the scaffold's boundaries without flattening established domain folders.
- Run the checks documented by the target repo for changed areas.
