# Architecture

## Data flow

```
  Mac filesystem (canonical)              Figma libraries     Drive (assets)    AEM / Adobe
  /Volumes/Macintosh HD-1/Users/          (Pro + Trivius)     (satellite)       (assets)
  warrenghaad/PANTTEARRA - DOCUMENTS/         │                    │                  │
  EUCLID/                                     │                    │                  │
        │                                     │                    │                  │
        └───────────────┬───────────────────┴──────────────────┘
                          ▼
               ┌───────────────────────┐
               │   scout-euclid       │   classifies every artifact
               │   (read-only)        │   no judgment, no imports
               └───────────┬──────────┘
                           ▼
                  out/scout-report.json
                           │
                           ▼
               ┌─────────────────────┐
               │ component-analyzer   │   what does the product need?
               │ (no external reads)  │   forced to reason from report
               └───────────┬──────────┘
                           ▼
                 out/component-spec.json
                           │
                           ▼
               ┌─────────────────────┐
               │ component-sourcer    │   for each spec entry: where?
               │ (Figma + web)        │   shadcn / Figma / Adobe / build
               └───────────┬──────────┘
                           ▼
                 out/sourcing-matrix.json
                           │
                           ▼
               ┌─────────────────────┐
               │ foreman-translator   │   the only agent with write
               │ (write + bash)       │   runs shadcn add, get_design_context, etc.
               └───────────┬──────────┘
                           ▼
                  src/components/**
                  src/styles/tokens.css
```

## Why this shape

**Read/write separation.** Only the foreman writes code. The other three
produce structured artifacts (`scout-report.json`, `component-spec.json`,
`sourcing-matrix.json`) that are reviewable, diffable, and replayable.

**Source-of-truth chain.** Each agent's only input is the previous agent's
structured output, *not* the raw sources. This means you can edit
`component-spec.json` by hand to override the analyzer, and the sourcer
and foreman will still work.

**Replay.** Because every stage emits a JSON artifact, you can:
- Re-run sourcing without re-running scouting (cheap iteration).
- Re-run translation against a tweaked sourcing matrix (cheaper iteration).
- Diff `component-spec.json` over time to see how requirements drift.

## Sources used by the kit

- **Mac filesystem at `/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/`**
  — canonical. The scout always reads from here first.
- **Figma (Pro + Trivius org)** — design components, variables,
  Code Connect mappings.
- **Drive** — satellite for image assets and any spec docs that didn't
  make it to the Mac. Read-only fallback.
- **Adobe Express / Stock** — licensed media assets.
- **AEM** — only if EUCLID assets land there.
- **shadcn registry** — component installs via `npx shadcn@latest add`.
- **Perplexity / Gemini** — last-resort research path for the sourcer.

Notion is **not** consulted. The user has flagged Notion content as
disorganized and not canonical.

## Source-priority rules

The sourcer follows a strict order when picking an origin for each component:

1. **Existing Figma library component** — if there's already a Figma
   component with a Code Connect mapping, use it. Free wins.
2. **shadcn/ui registry** — if shadcn has it, install it via
   `npx shadcn@latest add <name>`. Don't reinvent.
3. **Adobe Stock / AEM asset** — for media-heavy components (hero
   imagery, lesson illustrations) the Adobe MCP can search and license.
4. **Hand-build from Figma node** — if Figma has a designed node but no
   library mapping, foreman calls `get_design_context` and writes code.
5. **Hand-build from EUCLID spec** — if Figma has nothing, the spec in
   the EUCLID directories is the brief and the foreman writes from
   description.
6. **Research first** — only if every prior path fails, the sourcer is
   permitted to use Perplexity/Gemini to find prior art, and must cite
   sources in the matrix.

## Token strategy

All color/spacing/typography decisions land in `src/styles/tokens.css` as
CSS custom properties, sourced from Figma variables via
`get_variable_defs`. Components reference tokens — never literal hex
values. This lets a single Figma variable change ripple through the whole
library without code edits.
