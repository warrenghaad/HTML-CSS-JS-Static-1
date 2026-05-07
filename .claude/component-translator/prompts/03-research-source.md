# Phase 3 — Research & source

Direct prompt for the sourcer.

---

Use the `component-sourcer` subagent.

**Goal:** For every entry in `out/component-spec.json`, decide *where the
implementation comes from*. Cite each decision.

**Input:** `out/component-spec.json` (primary). You may consult Figma
libraries, the shadcn registry (via web), Adobe stock catalog, and — only
as a last resort — Perplexity / Gemini.

**Source-priority ladder** (try in order, stop at first match):

1. **`figma-library`** — Run `search_design_system` against the Trivius
   org libraries. If a published component matches `name` (or close
   semantic match) AND has a Code Connect mapping, use it. Record the
   `libraryKey` and `codeConnectSrc`.
2. **`shadcn`** — If the spec name maps to a shadcn primitive
   (Button, Dialog, Tabs, Accordion, Sheet, Popover, Tooltip, etc.),
   use `npx shadcn@latest add <name>`. Verify the name exists at
   `https://ui.shadcn.com/docs/components/<name>`.
3. **`figma-node`** — If Figma has a designed node but no library/Code
   Connect mapping, record `fileKey` + `nodeId` so the foreman can call
   `get_design_context` later.
4. **`adobe-asset`** — For media-heavy components (lesson illustrations,
   hero imagery), search Adobe Stock via `asset_search`. Record the
   asset ID and license requirements.
5. **`hand-build-from-spec`** — Spec describes the component but no
   Figma node exists yet. Foreman writes from the EUCLID text spec.
6. **`research-then-build`** (last resort) — Use Perplexity / Gemini to
   find prior art. Cite at least two URLs. Foreman writes from the
   research synthesis.

**For each spec entry, produce a `sourcingDecision`:**

- `componentName`
- `source` (one of the six labels above)
- `details` (libraryKey, shadcn name, fileKey+nodeId, asset ID, etc.)
- `rationale` (1–2 sentences: why this source)
- `citations` (URLs / Figma links / Notion page IDs)
- `confidence` (`high` | `medium` | `low`)
- `risks` (e.g. "shadcn Tabs doesn't expose programmatic focus we'll need")

**Outputs:**
- `out/sourcing-matrix.json` (machine-readable)
- `out/sourcing-matrix.md` (human-readable, see
  `templates/sourcing-matrix.example.md` for format)

**Stop after writing both files.** The foreman will not proceed until
the user explicitly approves the matrix.

Report: count by source; list every `low` confidence row for human review.
