# Scout report: existing Copilot branches

Read-only investigation of three Copilot-authored branches to see whether canon-editor Phase 3 would duplicate work already done. Findings inform the Phase 2-3 design.

## Summary

| Branch | PR | What it actually does | Overlap with canon |
|---|---|---|---|
| `copilot/mycelial-visualization-organization` | [#5](https://github.com/warrenghaad/HTML-CSS-JS-Static-1/pull/5) draft | Canvas visualization: 4 domains × 7 spores + Supabase/Notion integration nodes | **Canvas chassis reusable as a graph view over the vault** — not a canon-editor itself |
| `copilot/organize-llm-output-for-obsidian` | (none) | "Review Workbench" — hand-triage UI with status vocab, validation issues, TOC extraction, JSON placement-map output | **≈ 50 % of Phase 3 already exists** — missing YAML frontmatter, Drive ingestion, writeback |
| `copilot/research-workflow-diagram-implementation` | (none) | "Repo File Catalog" backend — 3 JSON APIs classifying files into stack layers | **No overlap** — different problem (codebase introspection) |

## Details

### `copilot/mycelial-visualization-organization`

Files: `pages/mycelial-network.html`, `scripts/mycelial-network.js` (23.7 KB IIFE), `styles/mycelial-network.css`.

Data model is a static in-JS object literal (`DOMAINS`, `INTEGRATIONS`, `SPORE_LABELS`, `SPORE_DESCRIPTIONS`). No load seam, no exports, no fetch. Cross-domain edges hardcoded.

**Reusable (~60 % of the file):** `draw()`, `drawEdges()`, `drawMycelialEdge()`, `drawDashedEdge()`, `worldToScreen`/`screenToWorld`, `nodeAtScreen`, pan/zoom/drag/wheel handlers, tooltip, animation loop. All operate on generic `{nodes, edges}` arrays.

**Needs rewriting to plug in an Obsidian graph:** `buildGraph()` (positions are hand-assigned, no force layout), `drawNodes()` (switch on `type === 'domain'|'spore'|'integration'`), `openPanel()` (reaches into module-scope `DOMAINS`).

### `copilot/organize-llm-output-for-obsidian`

Files: `pages/review-workbench.html`, `scripts/review-workbench.js`, `styles/review-workbench.css`, `data/review-metadata.json`. Empty scaffolding: `data/obsidian-ready/`, `data/future-tocs/`, `data/placement-maps/`.

What it does: open a `.md` file (or one of three baked-in samples), edit in a `<textarea>`, assign a Status, set a target vault path, attach Validation Issues with likelihood/critical/blocking flags, auto-derive status via policy, generate a Provisional TOC from headings, emit a JSON "placement-map" note.

**Status vocabulary** (canonical — adopt as-is for canon frontmatter):

- `Inbox`
- `Active Review`
- `Canon`
- `Provisional Canon`
- `Canon Candidate`
- `Fragment`
- `Conflict`
- `Superseded`
- `Archive`
- `Build-System`
- `Lesson`
- `Obsidian Ready`

**Auto-derive policy:**
- All issues resolved → `Canon`
- Unresolved non-critical issues + likelihood ≥ 0.7 → `Provisional Canon` with 14-day review-due date
- Critical blocking issue → forces `Active Review`

**Placement-map JSON schema (`placement-map/v0.2`):** `schema`, `generated_at`, `document`, `status`, `future_destination`, `review_notes`, `detected_headings`, `validation_policy`, `validation_summary`, `unresolved_questions`, `issues`, `validation_queue`.

**Missing pieces:**
- No YAML frontmatter emission (Save writes raw textarea contents unchanged).
- No writeback to disk (persistence is `localStorage` only, per `review-metadata.json`).
- No Drive fetch — you have to open a local `.md` yourself.
- No parser for LLM chat exports.

### `copilot/research-workflow-diagram-implementation`

Despite the name, adds three JSON APIs to `server.py` classifying repo files into stack layers (`backend`/`frontend`/`experimental`/`future-react`). No frontend, no diagram data structure. Complementary to (not overlapping with) the other two branches.

Endpoints:
- `GET /api/catalog/files/summary`
- `GET /api/catalog/files?extension=&type=&layer=&q=&python_only=`
- `GET /api/catalog/stack`

## Recommendation: pivot Phase 3

Instead of building `canon-editor/` fresh in React:

1. **Phase 2 extraction** emits Markdown whose YAML frontmatter matches review-workbench's placement-map schema — same field names (`status`, `future_destination`, `validation_summary`, `unresolved_questions`, `issues`, `validation_queue`) so review-workbench opens vault files without translation.
2. **Phase 3** extends review-workbench (rebased onto `canon-preservation`) with:
   - Drive-fetch button that pulls a backend HTML by ID from `CATALOG.md`
   - YAML-frontmatter injection on Save (JSON placement-map → frontmatter + Markdown body)
   - Writeback to `canon/vault/` instead of `localStorage`-only
3. **Phase 4 (bonus)** wires the mycelial canvas to render `canon/vault/` as a graph (nodes = files, edges = wiki-links + shared tags). Reuses ≈60 % of `mycelial-network.js`; `buildGraph` gets replaced with a markdown-parse step.

This avoids duplicating work already done, keeps the tool count small (one editor + one graph view), and lets prior review-workbench state carry forward.
