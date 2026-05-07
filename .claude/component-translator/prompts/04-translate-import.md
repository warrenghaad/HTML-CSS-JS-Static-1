# Phase 4 — Translate & import

Direct prompt for the foreman in writing mode.

---

Use the `foreman-translator` subagent.

**Pre-flight (block until satisfied):**
- `out/sourcing-matrix.md` exists and the user has approved it.
- The target React project is initialized; `package.json` includes
  `react`, `tailwindcss`, and either has shadcn configured or will
  accept `npx shadcn@latest init`.
- `src/styles/tokens.css` either does not exist or is safe to overwrite.

**Execution order:**

1. **Tokens first.** Pick a representative Figma file (the one used
   during sourcing). Call `get_variable_defs` for color, spacing,
   typography, and radii collections. Emit `src/styles/tokens.css`
   as CSS custom properties on `:root` (and `.dark` if a dark mode
   variable mode exists). Components must reference these tokens.

2. **shadcn entries.** For each `source: shadcn` row, run
   `npx shadcn@latest add <name>`. After install, open the file and
   replace any literal colors with `var(--token-name)` from
   `tokens.css`.

3. **figma-library entries.** If Code Connect maps to an existing
   codebase component, no new code — just import it. If the mapping
   points to a path that doesn't exist yet, fall back to `figma-node`.

4. **figma-node entries.** Call `get_design_context(fileKey, nodeId)`.
   Adapt the React+Tailwind reference output to the project's
   conventions:
   - Use the project's path aliases (`@/components/ui/...`).
   - Replace inline styles with token references.
   - Convert any absolutely-positioned children to flex/grid where
     the screenshot allows.
   Write to `src/components/<kind>/<Name>.tsx`.

5. **adobe-asset entries.** Use the Adobe MCP to license/download the
   asset, place under `public/assets/`, then write the React wrapper
   that consumes it.

6. **hand-build / research-then-build entries.** Write the component
   from the spec + screenshot + (for research case) the cited prior
   art. Add a TODO comment with a link to the EUCLID source.

7. **Gate.** Run the project's typecheck and lint:
   - `npm run typecheck`
   - `npm run lint`
   Phase fails if either fails. Don't "fix" by suppressing rules; fix
   the underlying issue or revert the offending component.

8. **Storybook (if present).** For every new component, generate a
   `<Name>.stories.tsx` with one story per variant declared in the
   component spec.

**Output report:**
- Components written (path, source, lines)
- Components skipped + reason
- Token file diff summary
- Typecheck / lint result
- Suggested next step (e.g. "add Storybook", "wire to a page")
