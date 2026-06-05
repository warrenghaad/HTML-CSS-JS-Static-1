# Phase 1 — Scout

Direct prompt for the scout if you want to run a single phase.

---

Use the `scout-euclid` subagent.

**Goal:** Produce a complete inventory of every artifact under the EUCLID
source that could plausibly inform a component library, classified by
kind. Read-only. No judgment about what's needed — just classify.

**Sources, in priority order:**

1. Mac filesystem (Filesystem MCP) — **canonical**. Start at
   `/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/`. Recurse into:
   - `GE SECTION OR MAPPING/`
   - `CONTENT MANAGEMENT SYSTEM/IMAGE SPEC AND PRODUCTION/`
   - `LESSON SECTION DESIGN/`
2. Figma libraries available to the authenticated user. Use
   `get_libraries` against the most recently opened EUCLID Figma file
   (ask the user for the file URL if no obvious one exists).
3. Drive — fallback only when a referenced asset is missing locally.

**Notion is in development and not yet canonical.** It may be used for
draft context only and must not override local canonical files.

**Classification taxonomy** (each artifact gets exactly one):

- `design.figma-node` — a Figma frame/component reachable via fileKey + nodeId
- `design.figma-library-component` — a published library component
- `design.image-spec` — raster/vector spec for an illustration
- `design.layout-spec` — page-level layout description
- `content.lesson-section` — a lesson-section markdown / doc
- `content.image-asset` — PNG/SVG/PSD ready for production
- `content.copy` — microcopy or body text
- `meta.mapping` — a GE SECTION OR MAPPING file (relationship graph)
- `unknown` — cannot classify; include the path so a human can label it

**Output:** write `out/scout-report.json` matching
`templates/component-spec.schema.json#/definitions/scoutReport`. For
each entry record at minimum: `path`, `kind`, `sizeBytes`, `mtime`,
and a 1-line `summary`.

**Stop conditions:**
- If you find fewer than 5 artifacts under the EUCLID root, stop and
  ask the user to verify the path — the directory may not be mounted.
- If a single subtree exceeds 5,000 entries, sample (every Nth file)
  and flag the truncation in the report's `meta.truncated` field.

Report back with the file count by kind and the top 10 largest files.
