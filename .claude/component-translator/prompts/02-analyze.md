# Phase 2 — Analyze

Direct prompt for the analyzer.

---

Use the `component-analyzer` subagent.

**Goal:** Determine the *minimum sufficient component set* the React +
shadcn/ui + Tailwind project needs to render every artifact in the scout
report. Reason from the report — do **not** call any external MCP.

**Input:** `out/scout-report.json` only.

**Method:**

1. Group scout entries by what they imply about the UI:
   - `content.lesson-section` → needs a lesson template, a section block,
     a step block, probably a rich-text renderer
   - `design.layout-spec` → needs page templates
   - `design.image-spec` → needs media containers (responsive image,
     figure with caption, gallery)
   - `design.figma-library-component` → needs a 1:1 component (could be
     shadcn-equivalent or hand-build, sourcer decides later)
   - `meta.mapping` → needs navigation / breadcrumb / section map components

2. For each implied component, write a `componentSpec` entry with:
   - `name` (PascalCase)
   - `kind` (`atom` | `molecule` | `organism` | `template`)
   - `purpose` (one sentence: what it renders, for which artifacts)
   - `props` (likely prop signature inferred from the artifacts)
   - `variants` (size / state / theme variants implied by the artifacts)
   - `dependsOn` (other components it composes)
   - `evidenceRefs` (paths from the scout report that justify this entry)

3. Deduplicate aggressively. If two artifacts imply the same component,
   merge them and union their evidenceRefs.

4. Sort by atom → molecule → organism → template, then alphabetical.

**Output:** `out/component-spec.json` matching
`templates/component-spec.schema.json#/definitions/componentSpecArray`.

**Stop conditions:**
- If you produce > 80 specs in one pass, stop. Ask the user whether to
  scope down (e.g. just LESSON SECTION DESIGN first) or to split the
  output by EUCLID subtree.
- If you produce < 5 specs, the scout report was probably empty — verify.

Report: count by kind; top 5 organisms by composition depth.
