# Figma Librarian — Discovery synthesis

**Status:** unreviewed synthesis by an autonomous agent. Do not treat as authoritative until the human has confirmed each claim.

**Date:** 2026-09-09
**Sources:**
- Replit app `3275bb41-8f6f-45e7-97a4-48fbe699f64a` (workspace title: *Tiered Wireframe Library*)
- Notion page `329410ee-31e9-816d-9a6c-e9d518b084d2` — "EUCLID — Figma Specification & Transition Guide"
- Notion page `330410ee-31e9-8144-a9df-cd1896e4786c` — "Agent Directions: Improving Sections + Image Production Planning"
- Notion page `329410ee-31e9-8130-aa7a-c2bad7ff026a` — "EUCLID Registry + Figma Layer Hub"
- Notion page `328410ee-31e9-814b-bd80-e0ed9c3881f2` — "Design System (Component Library)" (glossary row, page body empty)
- Notion page `336410ee-31e9-8124-8bd0-efe87aeb4325` — "Three-Lane Production Plan"

---

## 1. What the Replit app currently is

**Identity mismatch, first.** The Replit workspace is titled *Tiered Wireframe Library*, not "Figma Librarian". Its own README calls the agent "the Librarian" and describes a hub-and-spoke system that takes a plain-language need statement and emits a validated diagram plan; it is the closest thing in the Replit account to the object called "the Figma Librarian" in this brief. Everything below reads that mapping as intentional.

**Stack.** A pnpm workspace (`pnpm-workspace.yaml`) running TypeScript 5.9 on Node with `concurrently` orchestrating four dev processes:

- `lib/*` (deterministic librarian package and shared API contract packages)
- `artifacts/api-server` — Express + Pino + Zod-validated `/api/librarian/*` routes
- `artifacts/wireframe-library` — Vite/React web UI (uses Tailwind v4, wouter, TanStack Query, shadcn-style `components.json`)
- `artifacts/mockup-sandbox` — React reference renders (the "source of truth" when a manifest component has `figmaNodeId: null`)

Supply-chain hardening: `pnpm` `minimumReleaseAge: 1440` (24h) with an allowlist for `@replit/*`.

**Repository layout.**

```
docs/wireframe-library/     SPEC.md v0.2.0, manifest.json (+schema), source-catalog.json, FIGMA-AUDIT.md, FIGMA-INTAKE.md
lib/wireframe-librarian/    src/{types.ts, librarian.ts, validate.ts, index.ts, librarian.test.ts}
lib/api-spec/               openapi.yaml + orval.config.ts (typed client generation)
lib/api-zod/                Zod request/response schemas shared by API + UI
lib/api-client-react/       React client generated from api-spec
lib/db/                     (present, contents not read)
artifacts/api-server/src/   app.ts, index.ts, routes/{index,health,librarian}.ts, lib/{manifest,llmExtract,promotion,logger}.ts (+ tests)
artifacts/wireframe-library/ Vite/React SPA; components.json for shadcn UI
artifacts/mockup-sandbox/   React reference sheets (TierLadder, GrowthAxes, KnowledgeGraphExample, WorkflowExample)
scripts/                    figma-intake.js, publish/preflight for GitHub, tests
.agents/{memory,skills}/    (present, contents not read)
```

**Entry points.** `artifacts/api-server/src/index.ts` boots the Express app on `PORT`; the app mounts a single `/api` router that composes `health` + `librarian`.

**Existing schemas** (TypeScript, in `lib/wireframe-librarian/src/types.ts` — full shapes captured in §3):

- `AxisCoords {a1..a5:number}` and constant `AXIS_IDS`
- `ManifestComponent`, `ManifestTokens`, `Manifest`, `Composition`, `CompositionSlot`
- `SourceCatalog`, `SourceCatalogEntry`, `SourceAsset`, `SourceTemplateCandidate`, `SourceMapping`, `SourceCoverage`, `SourceMetadata`
- `VisualLanguageDefinition`, `ComponentFamilyDefinition`
- `PlanRequest`, `DiagramPlan`, `Placement`, `PlacementContent`, `DraftPlacement`
- `StructuredNode`, `StructuredEdge`, `StructuredGroup`
- `ValidationIssue`, `ValidationReport`
- Type unions: `VisualLanguage` = `knowledge-graph | uml | database | mui-ui | flowchart | workflow | information-architecture | mind-map`; `DiagramFamily` = `knowledge-graph | workflow`; `AtomicLevel` = `molecule | organism | template`; `CompositionFamily` = `tier1 | knowledge-graph | workflow | cross-family`; `SourceCapability` = `graph-primitive | graph-template | data-surface | ui-building-block | reference-only`

**Existing routes** (all under `/api`):

- `GET /health` (from `routes/health.ts`, not opened)
- `GET /librarian/manifest`
- `GET /librarian/catalog`
- `GET /librarian/catalog/assets?sourceId=…&offset=&limit=`
- `GET /librarian/compositions?level=molecule|organism|template`
- `POST /librarian/compositions/promote` (same-workspace-origin gated; requires `assertManifestWriteAllowed`)
- `POST /librarian/plan`
- `POST /librarian/refine` (LLM-only; 503 without one)
- `POST /librarian/validate`

**Pipeline (as it stands, in code).** `need → classifyVisualLanguage → LLM extract (via `AI_INTEGRATIONS_OPENAI_*` proxy or `OPENAI_API_KEY`, else deterministic keyword extractor) → buildPlan (spend emphasis one axis-step at a time) → validatePlan → return`. All emphasis-spending, tier logic, hue/size budgets and "no double-encoding" rules live in `librarian.ts` + `validate.ts`. The LLM never picks a component ID; kinds are coerced to sets derived from the librarian's own selection tables in `llmExtract.ts`.

**Figma integration status** (from `docs/wireframe-library/FIGMA-INTAKE.md`, dated 2026-08-24): `scripts/figma-intake.js` reads registered `figmaSources`, catalogues everything as `SourceAsset` records, but only assigns a renderer role when an exact pre-approved `fileKey:nodeId` mapping exists. 26 of 28 manifest roles have verified Figma node references; `prim.node.round` and `kg.class` remain React-reference fallbacks. Primary FigJam source is *Visual Logic Primitives* (`nOEamjKEXw6oXF9Clp8PGD`).

---

## 2. What the Notion plan says the librarian should be

**Critical framing observation.** Four of the five Notion pages are about **EUCLID**, a K-12 curriculum/pedagogy project (Mesopotamia pilot, Grade 3), and describe Figma as the **nervous system** in a Brain (Notion + Sami) → Nervous System (Figma) → Hands (CapCut) pipeline for producing lessons. They do not describe the Replit "Tiered Wireframe Library" architecture directly. The **fifth** page — "Design System (Component Library)" — is a one-row glossary entry whose body is blank; it only names the concept ("15 section-specific visual templates in Figma that can be instantiated across all 48 lessons"). See §5 for the reconciliation this forces.

**Synthesized purpose (from Notion).** Figma is *not* the source of truth. It is the visual delivery shell that turns brain-decided section content into a template-rendered artboard, which CapCut then animates. Every content decision (deity, element, MAGIC weights, GECD readings, image requirements) lives upstream in Notion databases.

**Component library structure** (from *EUCLID — Figma Specification & Transition Guide*):

- **Master frame** 1440×900; nav rail 52px, top bar 48px, footer 32px, content 1388×820.
- **Color tokens (Figma variables):** `night #0D1B2A`, `lapis #1B3A5C`, `gold #C8A84E`, `clay #E8D5B7`, `parchment #FAF6EE`, `brown #3D2B1F`, plus three register tokens (`register-metaphor #5B7FA5`, `register-function #6B8F5B`, `register-both #8B6BAF`) and three power accents (`power-gold #D4A843`, `power-blue #4A7FB5`, `power-rose #B5647A`).
- **Typography:** Georgia/Newsreader (deity/body), JetBrains Mono (labels), Inter (UI), Courier/JetBrains Mono (math).
- **15 section templates** as Figma component sets, each with a distinct screen archetype: A1 Cinematic, A2 Character Sheet, A3 Lore Codex, A4 Collection Gallery, A5 Tutorial, A6 Workshop, A7 Split Reveal, B1 Recap, B2 Whiteboard, B3 Transformation, B4 Schematic, B5 Tech Tree, B6 Blueprint, B7 Build Guide, B8 Superimposition. Each has enumerated `Figma variant properties` (e.g. A1: `beat` 1–5, `act` I/II/III).
- **Shared components (must be built first):** Power Badge (identical instance across A2/A3/A4/B8 for "visual schema transfer"), Nav Rail (52px, 15 items), Star8 SVG (variants by size + color), Section Header Bar (48px).
- **Transition specifications** organized as within-register (A→A, B→B), register transitions (A6→A7 the "PIVOT", A7→B1, B7→B8), and special transitions (THE PIVOT, THE CIRCUIT, Lesson complete) with named durations/easings.

**Agent role** (from *Agent Directions*):

- **Section-improvement agent workflow (Part 1):** Read Canon page → read Section × SRQ × MAGIC × GECD × Content/Image page → pick one element → run SRQ per section → check structural constraints (B2 math ↔ B6 invention, etc.) → check cross-day parallels (A2↔B2, A4↔B5, A5↔B6, A6↔B7) → identify weakness → rewrite with evidence.
- **Image production agent workflow (Part 2):** Read section canon → check cell library → list images (type/cells consumed/cells to create/delegation target) → sequence per Phase 2 order → write production prompts.
- **Six image types** (MUS/SCN/DGM/CON/MOT/OVR) and **five cell categories** (DEI, SET, FIG, OBJ, GEO) with ID formats `DEI.[civ].[deity].[pose]`, `SET.[civ].[location]`, `FIG.[civ].[role].[pose]`, `OBJ.[civ].[object]`, `GEO.[element].[view]`.
- **Delegation architecture:** Gemini (3D/motion/realism), DALL-E/Codex (myth/portraits), Claude (museum sourcing metadata — *not* image gen), Perplexity (research).

**Data flows / boundaries** (from *Three-Lane Production Plan* and *Agent Directions Part 3*):

- **Three lanes running in parallel.** Lane 1 = Rapid Pilot Production (teacher deliverables now). Lane 2 = Visual Primitive Library (the "Henry Ford assembly line" of reusable cells). Lane 3 = Mesopotamia-specific need drives which primitives get built first.
- **Explicit hierarchy:** Notion/DB + Sami = brain; Figma = nervous system (orchestrate + arrange + template); CapCut = hands. Figma does NOT hold content, does not decide sequence, does not render final motion.
- **Pipeline:** Notion decides section needs → research agent sources/generates images → cell library stores → Figma lays out shell → CapCutAPI assembles → Sami finalizes → export.

**Registry contract** (from *EUCLID Registry + Figma Layer Hub*):

- **Seven-layer stack:** Raw Source Files → Reconciliation Intake → Subject Categories → Comparison Taxonomy → Review Board → Registry Records → Downstream Surfaces (of which Figma is one).
- **Rule:** raw files are evidence; the registry stores approved records only; a file does not become truth by itself.
- **Databases referenced:** `EUCLID — Source Artifacts`, `EUCLID — Fragments`, plus a FigJam layer map (cross-reference not chased per guardrail).
- **Notion AI integration pattern** (from Figma Specification page): the *Content Template* field in each Section Template row directs Notion AI to fill `[DEITY]`, `[ELEMENT]`, `[POWER]` slots per row of the *Deities & Elements* database.

**Rules across all Notion pages:** one panel at a time; all words in images real; animate the connectors between sections; animate metaphor in Day B; primitive library reusable across civilizations; CapCut Pro is the primary production tool.

---

## 3. Named entities & schemas already defined

| Entity | Defined in | Fields / shape | Referenced by |
|---|---|---|---|
| `AxisCoords` | Replit `lib/wireframe-librarian/src/types.ts` | `{a1,a2,a3,a4,a5: number}` (each 0–4) | Every plan, placement, manifest component |
| `ManifestComponent` | Replit `types.ts` | `{id, family, tier, shape, axes, maxAxes, figmaNodeId, fileKey?, sourceMetadata?, capabilityTags?, mappingStatus?, visualLanguages?, semanticRoles?}` | `Manifest.components`, `buildPlan`, `validatePlan` |
| `Manifest` | Replit `types.ts` + `docs/wireframe-library/manifest.json` | `{name, version, tokens, components, visualLanguages?, componentFamilies?, compositions?, sourceCatalog?}` | Every API route; UI browser |
| `ManifestTokens` | Replit `types.ts` | `{ink, paper, accent, palette:string[], tintSteps:number[], sizeScale:{widths,aspect,ratio}, strokeScale:number[], dashVocabulary}` | Renderer, hue budget check |
| `Composition` | Replit `types.ts` | `{id, atomicLevel: molecule\|organism\|template, label, description?, family, visualLanguages?, slots: CompositionSlot[], sourceMetadata?, capabilityTags?}` | `/librarian/compositions`, promotion |
| `CompositionSlot` | Replit `types.ts` | `{componentId, role, position:{x,y}, axes?: Partial<AxisCoords>}` | Composition slot integrity check |
| `SourceCatalog` (+ Entry/Asset/Mapping/Coverage) | Replit `types.ts` + `docs/wireframe-library/source-catalog.json` | Full source inventory, capability classes, mapping status | `/librarian/catalog*` routes; Figma intake |
| `PlanRequest` | Replit `types.ts` | `{need, family?, visualLanguage?, compositionIds?, nodes?, edges?, groups?, view?: overview\|detail}` | `POST /librarian/plan`, `/refine` |
| `DiagramPlan` | Replit `types.ts` | `{need, title, family, visualLanguage?, compositionIds?, axisMeanings, tier1Draft, placements, notes}` | Plan / validate / render |
| `Placement` / `PlacementContent` | Replit `types.ts` | `{id, componentId, axes, content:{label?,typeTag?,className?,properties?,hueIndex?,from?,to?,parent?,role?,focal?}}` | Renderer; validator |
| `StructuredNode` / `StructuredEdge` / `StructuredGroup` | Replit `types.ts` | See LLM extractor schema | LLM contract; `buildPlan` input |
| `VisualLanguageDefinition` | Replit `types.ts` + `librarian.ts` (`VISUAL_LANGUAGE_DEFINITIONS`) | `{id, label, description, cues:string[], baseFamily, semanticRoles:string[], componentFamilies:string[]}` | Classification; validator (`visual-language`, `semantic-role` rules) |
| `ComponentFamilyDefinition` | Replit `types.ts` | `{id, label, visualLanguages, semanticRoles}` | Validator cross-check |
| Section Template (15) | Notion "EUCLID — Figma Specification" §Section Component Specs | Per-section: `layout`, structural parts, `Figma variant property` (e.g. A1 `beat` 1–5, `act` I/II/III); A2 `power-expanded`; A3 `artifact-selected`, `power-filter`; A7 `split-position`; etc. | Notion Deities & Elements DB rows; CapCut assembly |
| Deities & Elements row | Notion Figma Specification §Notion AI Integration Pattern | Deity, element, powers, carriers, invention (fields not fully listed on the page examined) | Section Template `Content Template` slots |
| Cell library asset | Notion *Agent Directions* Part 2 §Five Cell Categories | `DEI.[civ].[deity].[pose]`, `SET.[civ].[location]`, `FIG.[civ].[role].[pose]`, `OBJ.[civ].[object]`, `GEO.[element].[view]` | Every Phase-2 image production plan |
| Image type | Notion *Agent Directions* Part 2 §Six Image Types | `MUS / SCN / DGM / CON / MOT / OVR` + source + reuse-potential | Image production planning |
| Registry Record | Notion *Registry + Figma Layer Hub* | Approved definitions/relationships/canonical entities (fields not enumerated in the page examined) | Downstream Surfaces (incl. Figma) |
| Section Template (row in a Notion table) | Notion *Registry + Figma Layer Hub* (indirect, via `EUCLID — Source Artifacts` + `EUCLID — Fragments` DBs) | Fields not defined on this page — DB schema not opened per guardrail | Notion AI content generation |
| Design System (Component Library) glossary term | Notion `328410ee…` | Term only; `What Sami Built = "The plan to create 15 section-specific visual templates in Figma that can be instantiated across all 48 lessons"` — page body blank | Referenced by name only |

---

## 4. Named contracts / APIs / boundaries

| Contract | Defined in | Shape |
|---|---|---|
| `GET /api/librarian/manifest` | Replit `routes/librarian.ts` | Returns full `Manifest` |
| `GET /api/librarian/catalog` | Replit `routes/librarian.ts` | Returns `manifest.sourceCatalog` or `null` |
| `GET /api/librarian/catalog/assets` | Replit `routes/librarian.ts` | Query `sourceId, offset (≥0), limit (1–200)`; returns `{items, total, offset, limit}` |
| `GET /api/librarian/compositions` | Replit `routes/librarian.ts` | Query `?level=molecule\|organism\|template`; body validated by `CompositionsResponse` (Zod) |
| `POST /api/librarian/compositions/promote` | Replit `routes/librarian.ts` | Body: `PromoteDiagramPlanBody` (Zod); requires same-workspace `Origin` header + `assertManifestWriteAllowed`; only valid plans; returns `PromoteDiagramPlanResponse` |
| `POST /api/librarian/plan` | Replit `routes/librarian.ts` | Body: `CreateDiagramPlanBody` (Zod ≈ `PlanRequest`); returns `CreateDiagramPlanResponse = {plan, validation}`; LLM fallback surfaces `503 {llmError:true}` when configured but failing |
| `POST /api/librarian/refine` | Replit `routes/librarian.ts` | Body: `RefineDiagramPlanBody`; LLM-only (503 without); returns `{plan, validation}` |
| `POST /api/librarian/validate` | Replit `routes/librarian.ts` | Body: `ValidateDiagramPlanBody`; returns `ValidationReport` |
| LLM extraction contract | Replit `lib/llmExtract.ts` `buildSystemPrompt()` | JSON schema for `{family, nodes[], edges[], groups[]}`; allowed `kind` sets derived from `KG_NODE_COMPONENT / WF_NODE_COMPONENT / KG_EDGE_COMPONENT / WF_EDGE_COMPONENT` |
| Manifest write authorization | Replit `lib/promotion.ts` (referenced) | `assertManifestWriteAllowed()` gate + same-origin check |
| Figma intake protocol | Replit `docs/wireframe-library/FIGMA-INTAKE.md` + `SPEC.md §7` | Only exact `fileKey:nodeId` mappings become renderer roles; everything else stays `unmatched` in `SourceAsset` |
| OpenAPI spec | Replit `lib/api-spec/openapi.yaml` (present, not opened) | Source of `lib/api-zod` and `lib/api-client-react` (orval config in `lib/api-spec/orval.config.ts`) |
| Brain / Nervous System / Hands pipeline | Notion *Agent Directions* Part 3 | Notion + Sami (decide) → research agent (source/generate) → cell library (store) → Figma (orchestrate + arrange + template) → CapCutAPI (assemble draft) → Sami (finalize) → export |
| Notion AI content generation | Notion *Figma Specification* §Notion AI Integration Pattern | Reads (Section Template `Content Template`) + (Deity row accumulated data) + (previous sections' outputs); fills `[DEITY]`, `[ELEMENT]`, `[POWER]` slots; human approves before Figma/image pipelines |
| Registry access rule | Notion *Registry + Figma Layer Hub* §Important Boundary | Board = review; Registry = approved; raw folders + single files never become truth by themselves |
| Three-lane parallelism | Notion *Three-Lane Production Plan* | Lane 1 deliverables now; Lane 2 primitive library; Lane 3 Mesopotamia drives priority — Lanes 2/3 serve Lane 1 |
| Delegation targets | Notion *Agent Directions* Part 2 §Image Delegation Architecture | Gemini / DALL-E / Claude (metadata only) / Perplexity per image type |
| CapCut boundary | Notion *Agent Directions* Part 3 §What CapCut does NOT do | No lesson-flow orchestration, no template design, no vector overlays; consumes Figma-exported PNGs |

---

## 5. Gap analysis

**The largest finding is a category mismatch between the two source sets.**

The Replit app is a generic *tiered wireframe / knowledge-graph / workflow* librarian aimed at LLM-driven diagram generation across eight visual languages. Its vocabulary is UML/DB/flowchart/mind-map/etc. The Notion pages, in contrast, describe **EUCLID**, a domain-specific curriculum production system whose Figma layer is a set of **15 pedagogically-named section templates** (Cinematic, Character Sheet, Lore Codex, …) driven by a Notion content database and consumed by CapCut. Nowhere in the five Notion pages examined is the Replit app named, and nowhere in the Replit repo are the EUCLID sections, deity data, or CapCut pipeline referenced.

The rest of the gap analysis follows from that.

**In Replit but not in Notion:**

- The `AxisCoords` / tiered emphasis model (A1 shape, A2 color, A3 size, A4 stroke, A5 label; `max(axes) ≤ tier`).
- The eight-language `VisualLanguage` set and `visualLanguageDefinitions` cues.
- The `SourceCatalog` intake pipeline (capability classes, mapping status, provenance).
- The `/api/librarian/plan` + `/refine` + `/validate` + `/compositions/promote` contract.
- The LLM-owns-structure / deterministic-owns-axes split.
- The `Composition` / atomic-level (molecule/organism/template) vocabulary.
- The Figma primitive library actually wired up (Visual Logic Primitives FigJam file, 26/28 roles verified).

**In Notion but not in Replit:**

- The 15 EUCLID section templates and their variant-property enumerations.
- The Brain → Nervous System → Hands hierarchy and CapCutAPI hand-off.
- The five cell categories (`DEI/SET/FIG/OBJ/GEO`) and the six image types (`MUS/SCN/DGM/CON/MOT/OVR`).
- The Notion-AI Content Template pattern and the *Deities & Elements* instantiation model.
- The register palette (`metaphor/function/both`) and pedagogical color tokens (`night/lapis/gold/clay/parchment/brown` + power accents).
- The seven-layer registry stack (raw → reconciliation → subject → taxonomy → review board → registry → downstream).
- The transition specification (within-register, register-transitions, special transitions including "THE PIVOT" and "THE CIRCUIT").
- The three-lane production model.

**Conflicts / open tensions:**

- **Domain scope.** Replit's SPEC §1 explicitly names `knowledge-graph, uml, database, mui-ui, flowchart, workflow, information-architecture, mind-map` as its supported vocabularies — none of which is EUCLID's *section templates* family. The Replit `manifest.json`'s `sourceCatalog` capability classes are `graph-primitive / graph-template / data-surface / ui-building-block / reference-only`; the EUCLID templates would need a new capability class or a wholly separate manifest.
- **Figma's role.** Notion says Figma "does NOT decide anything" and "does NOT hold content". Replit's manifest, by contrast, treats Figma files as the *canonical source* for approved renderer roles (via `figmaNodeId + fileKey` mappings), while React sheets are only fallback. These two "sources of truth" are compatible if the Notion pipeline is upstream of Replit's manifest (Notion drives *which* templates exist; Figma is where they are stored; Replit indexes them), but this is not stated anywhere in either source.
- **Templates vs. compositions.** Notion "template" = a Figma component set with named variants (e.g. A5 Tutorial). Replit "template" = a `Composition` at `atomicLevel: "template"` with named slots. Same word, different granularity — one is a whole 1440×900 artboard, the other is a slot arrangement of primitives.
- **LLM's job.** Notion agent directions have an LLM read the Canon page and *rewrite section content grounded in historical evidence*. Replit's LLM only extracts a `{nodes, edges, groups}` structure and is deliberately walled off from component IDs. A single "Figma Librarian" agent that has to do both is not sketched in either source.
- **The glossary page (`328410ee…`) is essentially empty** — only the property row exists, with a one-sentence "What It Is" and "What Sami Built" description; the page body is blank. It cannot serve as authoritative canon on its own.

---

## 6. Reconciliation notes for the plan-in-progress

*The 18-step, 5-phase plan lives in the chat; I don't have its text, so notes below are keyed by the phase names the brief refers to. Where I lack the exact step wording, the note is scoped to what any step in that phase should almost certainly account for. Confirm before acting.*

- **Phase A — Confirm project identity / scope.** The Replit `Tiered Wireframe Library` is the Figma Librarian in name only until the human confirms. The five Notion pages examined here describe EUCLID, a specific application; nothing in them talks about a general-purpose wireframe librarian. Before proceeding, decide: is the Librarian meant to be (i) EUCLID-specific, (ii) a generic diagram engine that EUCLID happens to consume, or (iii) an intermediate abstraction across both? The current code answers (ii); the current Notion answers (i). Every downstream phase depends on which one wins.
- **Phase B — Outline JSON / semantic input schema.** Do not author fresh. Extend, don't invent. `PlanRequest / StructuredNode / StructuredEdge / StructuredGroup` in `lib/wireframe-librarian/src/types.ts` and the LLM contract in `buildSystemPrompt()` (`llmExtract.ts`) already fix the input shape end-to-end. `CreateDiagramPlanBody` in `lib/api-zod` (not opened) is the wire schema. Any new "outline" schema should be a superset or a mapping onto these, not a replacement.
- **Phase B — Component/manifest schema.** Already fully defined. `Manifest`, `ManifestComponent`, `Composition`, `SourceCatalog` and the JSON Schema at `docs/wireframe-library/manifest.schema.json` are the current authority. If EUCLID section templates need to land here, the reduction is "add 15 template-family `Composition`s + a `section-template` capability class"; the expansion is a *separate* manifest with different atomic vocabulary.
- **Phase B — Rules / validator.** Do not rewrite. `validatePlan` already enforces axis range, `max-axes`, hue budget (≤5), size spread (≤2 steps), one-hero (≤1 Tier-4), no-double-encoding, edge-endpoint integrity, visual-language and semantic-role compatibility. New rules should be added here.
- **Phase C — Figma output / renderer.** Partially built. The Replit ships React reference renders (`mockup-sandbox`) and a web UI (`wireframe-library`); it does *not* ship a Figma plugin (README calls it a future spoke). The 15 EUCLID section templates named in Notion have Figma variant properties enumerated, which is the exact shape a Figma-plugin renderer would consume — those specs reduce Phase C scope. There is no CapCutAPI code in the Replit; if the Librarian is expected to feed CapCut, that is entirely greenfield.
- **Phase C — Figma intake.** Already built. `scripts/figma-intake.js` + `FIGMA-INTAKE.md`. Any "let the Librarian read Figma" step should reuse this rather than duplicate it.
- **Phase D — Agent instructions.** Notion *Agent Directions* Part 1 (section-improvement) and Part 2 (image production) are ready-made agent playbooks and should be adopted verbatim if the Librarian ever handles EUCLID content. Do not author new agent workflows for those two responsibilities.
- **Phase D — Rules of engagement / boundaries.** The Brain/Nervous-System/Hands split in *Agent Directions* Part 3 is a hard boundary. Any plan step that has "Librarian generates content" invalidates it — the Librarian composes the shell, Notion+Sami owns content.
- **Phase E — Ship / integrate.** Depends entirely on Phase A. If the Librarian stays generic, the integration point is a small Notion connector that translates section-template rows into Librarian `Composition`s. If it becomes EUCLID-specific, the register palette and 15 section templates need to live in `manifest.json` and the eight generic `visualLanguages` need re-scoping.

---

## 7. Open questions for the human

1. Is the Replit "Tiered Wireframe Library" repo the intended body of the "Figma Librarian", or is that name reserved for a not-yet-existing service? If reserved, where does the tiered-library code fit relative to it?
2. Should the Librarian be domain-agnostic (its current SPEC v0.2.0), EUCLID-specific (the Notion frame), or a two-layer architecture (generic engine + EUCLID-flavored manifest / compositions)?
3. Does the Librarian ever author content, or is it strictly the "nervous system" (compose, arrange, template) with Notion+Sami owning every content decision?
4. Are the 15 EUCLID section templates to be modeled as `Composition`s of atomic level `template` inside the existing `manifest.json`, or in a separate EUCLID-specific manifest?
5. Should the register colors + power accents + Georgia/Newsreader/JetBrains-Mono type stack replace or coexist with the current `tokens` block (`ink #1A1D23`, palette `[#2563EB, #D97706, …]`)?
6. Does "output to Figma" mean (a) a Figma plugin that consumes `DiagramPlan` JSON, (b) the Figma REST API writing frames from `figmaNodeId`, or (c) both? The README lists both as future work but does not choose.
7. Should the CapCutAPI step live inside the Librarian repo, or in a separate spoke that consumes Librarian output?
8. Who has write access to `manifest.json` in production — the `assertManifestWriteAllowed` gate is coded but its policy source is not in the files examined; is the promotion flow meant to be human-only, human-approved-agent, or open to the Librarian agent itself?

---

## 8. Recommended next 3 concrete actions

1. **Get a human ruling on question 1 and 2 (identity + scope) before any schema work.** Tool: a synchronous conversation, or a short Notion page in the *Claude Teamspace — EUCLID Canon* that answers the two questions in one paragraph each. Every Phase B/C decision hinges on this.
2. **Read the two Notion pages this discovery deliberately did not chase** (per the one-hop guardrail): the *Canon page* under *Claude Teamspace — EUCLID Canon* and the *Section × SRQ × MAGIC × GECD × Content/Image page*, plus the two Notion databases already surfaced in *Registry + Figma Layer Hub* (`EUCLID — Source Artifacts` and `EUCLID — Fragments`). Tool: `notion-fetch` for the two pages, `notion-query-data-sources` for the two databases. This will confirm or falsify the "EUCLID and the tiered library are different projects" reading in §5.
3. **Read the Replit `docs/wireframe-library/manifest.json` in full and the two API-contract packages (`lib/api-spec/openapi.yaml`, `lib/api-zod/`) that Phase B would extend.** Tool: `mcp__Replit__read_app_file` for each. Nothing new should be authored until the current wire schema is on the page — the discovery already caught that Phase B risks re-authoring types that already exist.
