# Graph pipeline: Figma Dev Mode → canon-editor

How a graph visualization designed in Figma becomes the interactive
canon graph view.

## The endpoint

When the **Figma desktop app** runs with **Dev Mode MCP** enabled, it
serves an HTTP MCP endpoint at:

```
http://127.0.0.1:3845/mcp
```

This endpoint is `127.0.0.1` — only reachable from the Mac running
Figma. Remote Claude Code sessions (like this repo's cloud sessions)
cannot reach it. That's fine — the pipeline runs locally.

## Enable it once (Mac, one-time)

1. Open the Figma desktop app.
2. Preferences → Dev Mode → toggle **Enable local MCP server**.
3. Confirm the endpoint responds:
   ```bash
   curl -sS http://127.0.0.1:3845/mcp | head
   ```
   You should get an MCP handshake response (not a 404).
4. Register with Claude Code (already in `.mcp.json.example` as
   `figma-local`):
   ```bash
   claude mcp add figma-local --transport http -- http://127.0.0.1:3845/mcp
   ```
5. Inside Claude Code, `/mcp` should show `figma-local: connected`.

## The pipeline

```
  Figma desktop            127.0.0.1:3845/mcp             local Claude Code
  (Dev Mode on)   ─────────────────────────────▶   (this repo)
                                                                 │
                                                                 ▼
                                                     mcp__figma-local__
                                                     get_design_context
                                                     get_screenshot
                                                     get_variable_defs
                                                                 │
                                                                 ▼
                                                        canon-editor/
                                                        graph view (React)
```

1. **Select the graph frame in Figma.** Whatever frame you have selected
   is what `get_design_context` returns.
2. **In Claude Code, ask for the canon graph view.** The foreman calls
   `mcp__figma-local__get_design_context` (React + Tailwind reference
   output) and `mcp__figma-local__get_variable_defs` (design tokens).
3. **Output lands at `canon-editor/`.** Following the review-workbench
   pivot (see `scout-report.md`), the graph view is a companion to the
   markdown editor, both reading from `canon/vault/`. Nodes = files
   (parsed frontmatter), edges = wiki-links + shared tags.
4. **Iterate.** Edit the Figma frame, re-select, re-ask. Design tokens
   flow into `src/styles/tokens.css`; layout flows into the React
   component.

## What lives where

| Layer | Source | Consumed by |
|---|---|---|
| Visual design (frame, colors, spacing) | Figma file (Dev Mode) | `figma-local` MCP → foreman → React |
| Design tokens (color / radii / type) | Figma variables | `get_variable_defs` → `src/styles/tokens.css` |
| Node data (what to draw) | `canon/vault/**/*.md` frontmatter | canon-editor at runtime |
| Edge data | wiki-links in `canon/vault/**/*.md` bodies | canon-editor at runtime |
| Graph layout positions | `canon/graph-positions.json` (user-editable) | canon-editor + persists on drag |

This keeps the visual design in Figma (where it belongs), the semantic
data in Markdown (where it can be edited without Figma), and the
interactive state in a small JSON file (that survives a redesign).

## Related design source: the mycelial visualization

The already-shipped `pages/mycelial-network.html` +
`scripts/mycelial-network.js` on branch
`copilot/mycelial-visualization-organization` (PR #5) is a
canvas-based graph engine with ~60 % of the render/interaction code
reusable as-is. See `canon/scout-report.md` for the reusability
analysis. Two viable moves:

- **Fold into canon-editor.** Adapt `mycelial-network.js` as the graph
  view; drop `buildGraph` and replace with a markdown-parser that walks
  `canon/vault/`.
- **Design fresh in Figma.** Use `figma-local` to pull a new design from
  the currently-open Figma frame; regenerate as React. Recommended if
  the Figma design at 127.0.0.1:3845 is what you want the graph view to
  look like.

The two are not mutually exclusive — the Figma design informs the
visual language; the mycelial canvas code provides the working pan /
zoom / hit-test primitives if you don't want to rewrite them.

## Non-obvious notes

- **The endpoint moves with Figma.** If the desktop app quits, the
  endpoint dies. Restart the app to bring it back.
- **Port 3845 is Figma's default** but can be changed in Preferences.
  If you change it, update `.mcp.json.example` in this repo.
- **Multiple designers, one endpoint.** Only the Mac running Figma
  serves this endpoint. Teammates on other Macs need their own Figma +
  Dev Mode.
- **Selection state is the API contract.** If nothing is selected,
  `get_design_context` returns nothing useful — always select the frame
  first.
