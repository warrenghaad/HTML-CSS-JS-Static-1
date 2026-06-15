# Component Translator

A multi-agent kit that turns **EUCLID** design source material (local Mac
files, Figma, Adobe, Drive, AEM) into a working **React + shadcn/ui +
Tailwind** component library. Claude Code is the foreman; specialized
subagents do the legwork.

## The four agents

| Agent | Role | Reads from | Writes |
|---|---|---|---|
| **scout-euclid** | Inventory the raw source material; classify every artifact | Mac filesystem (canonical), Figma, Drive, AEM | `out/scout-report.json` |
| **component-analyzer** | Infer the component set the project actually needs and the variants/states each requires | scout report | `out/component-spec.json` |
| **component-sourcer** | Decide *where each component comes from* (shadcn registry, Figma library, Adobe asset, Gemini/Perplexity research, hand-build) | component spec + Figma libraries + web | `out/sourcing-matrix.md` + `out/sourcing-matrix.json` |
| **foreman-translator** | Execute imports, translate Figma nodes to code, write components, wire shared tokens, gate on tests | sourcing matrix | `src/components/**`, `src/styles/tokens.css` |

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the full data flow.

## Source-of-truth rule

The canonical EUCLID path is:

```
/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/
```

This lives on a mounted secondary volume (`Macintosh HD-1`). Every other
source (Figma, Drive, Adobe, AEM) is a satellite — read-only context the
agents may consult to fill in designs or assets, never to override the
local files.

Notion is **not** used by this kit. Even if EUCLID-named pages exist in
Notion, they are out of scope and not consulted by any agent.

## Why this shape

The four agents enforce a separation of concerns that breaks down without
them:

- **Scout** has a *wide read surface* but no judgment — just classify.
- **Analyzer** has *no read surface* outside the scout report — forced to
  reason about what's actually needed instead of pattern-matching what exists.
- **Sourcer** has *web + Figma* and is the only agent allowed to recommend
  external dependencies. It must justify each choice with a citation.
- **Foreman** has *write* permission. Nothing else does.

This prevents the most common failure mode: an agent that scouts, infers,
and writes in one pass tends to import whatever it saw first instead of what
the project needs.

## Quickstart on your Mac

Assumed working directory:
`/Users/samimajeed-air/Projects/Trivius - Euclid/HTML-CSS-JS-Static-1`

```bash
cd "/Users/samimajeed-air/Projects/Trivius - Euclid/HTML-CSS-JS-Static-1"
git fetch origin claude/figma-component-translator-7KlxS
git checkout claude/figma-component-translator-7KlxS

# Verify the EUCLID volume is mounted
ls "/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID"

# Wire MCP servers (see MCP-SETUP.md for prereqs)
cp .claude/component-translator/.mcp.json.example .mcp.json

# Open Claude Code in this repo
claude
```

Inside Claude Code:

```
/mcp        # confirm filesystem + figma show 'connected'
/agents     # confirm the 4 subagents are discovered
```

Then paste `.claude/component-translator/prompts/00-foreman-bootstrap.md`
for a full end-to-end run, or `prompts/01-scout.md` to start with just
the inventory phase.

## Layout

```
.claude/
  agents/                        ← auto-discovered subagents (Claude Code reads these)
    scout-euclid.md
    component-analyzer.md
    component-sourcer.md
    foreman-translator.md
  component-translator/
    README.md                    ← you are here
    ARCHITECTURE.md              ← data flow + diagrams
    MCP-SETUP.md                 ← install/auth notes per MCP server
    CLAUDE.md                    ← local guidance for Claude Code in this dir
    .mcp.json.example            ← ready-to-edit MCP config
    prompts/
      00-foreman-bootstrap.md    ← single-shot end-to-end prompt
      01-scout.md                ← phase 1: inventory
      02-analyze.md              ← phase 2: component spec
      03-research-source.md      ← phase 3: sourcing matrix
      04-translate-import.md     ← phase 4: code generation
    templates/
      component-spec.schema.json ← JSON Schema for the analyzer's output
      sourcing-matrix.example.md ← worked example of phase-3 output
```

## What the kit assumes about your environment

- macOS, user `samimajeed-air`, Claude Code installed.
- The volume `Macintosh HD-1` is mounted (visible in `/Volumes/`).
- Read access to `/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/`
  — the canonical source of truth.
- A target React+Tailwind+shadcn project. If you're keeping this repo as a
  static-HTML site, generated components should land in a sibling project;
  the foreman prompt asks you to confirm the destination on first run.
