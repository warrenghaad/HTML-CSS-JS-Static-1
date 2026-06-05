# MCP Setup

The kit assumes Claude Code on your Mac with the following MCP servers
configured. Copy `.mcp.json.example` to the repo root as `.mcp.json` and
edit the env vars.

**Note:** Notion is **in development** and **not yet canonical** in this
kit. If connected, treat Notion only as draft context and never as source
of truth over the local Mac files.

## Required (the canonical source + design context)

### 1. Filesystem MCP — reads `/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID`

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem \
  "/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID"
```

The trailing path is the **only** directory the server is allowed to
read — a sandbox boundary. Add more paths as additional positional args
if scout needs them (e.g. the GE SECTION OR MAPPING and IMAGE SPEC AND
PRODUCTION subdirectories).

### 2. Figma MCP (official) — design context, libraries, Code Connect

Claude Code's built-in Figma integration is already configured for this
session (`smajeed3@gmail.com`, Trivius org dev seat). On your Mac:

```bash
claude mcp add figma --transport http -- https://mcp.figma.com
# follow the OAuth flow; pick the Trivius org for design-system access
```

## Optional satellites

### Google Drive MCP — fallback for assets / specs not yet on the Mac

```bash
claude mcp add gdrive -- npx -y @modelcontextprotocol/server-gdrive
# requires GOOGLE_APPLICATION_CREDENTIALS pointing at a service-account JSON
```

Use only when a referenced asset is missing locally. The Mac filesystem
stays canonical.

### Adobe Express MCP — image ops, asset search, vectorize, background removal

```bash
claude mcp add adobe-express --transport http -- https://express.adobe.com/mcp
```

Useful for the IMAGE SPEC AND PRODUCTION pipeline: `image_remove_background`,
`image_vectorize`, `asset_search`, `image_generative_expand`.

### Adobe Experience Manager (AEM) MCP — if EUCLID assets land in AEM

```bash
claude mcp add aem --transport http -- https://aem.adobe.com/mcp
# scopes: read-api, lookup-api-spec
```

### GitHub MCP — already wired in Claude Code; no extra setup

### shadcn registry — not an MCP, just the CLI; foreman invokes it

```bash
# inside the target React project (not necessarily this repo):
npx shadcn@latest init
# foreman runs `npx shadcn@latest add <component>` per sourcing-matrix entry
```

### Perplexity MCP (research) — only for the sourcer's last-resort path

```bash
claude mcp add perplexity -- npx -y perplexity-mcp-server
# requires PERPLEXITY_API_KEY
```

### Gemini / Google AI MCP

```bash
claude mcp add gemini -- npx -y @google/gemini-mcp-server
# requires GEMINI_API_KEY
```

## Verification

Inside Claude Code:

```
/mcp
```

should list every server above as `connected`. If `filesystem` shows
`connection refused`, check the path quoting — the EUCLID path has
spaces and a hyphen.

## Permissions to allowlist

Add these to `.claude/settings.local.json` to avoid prompts during agent
runs (review carefully — these grant broad read on the EUCLID dir and
limited write on `src/`):

```json
{
  "permissions": {
    "allow": [
      "Read(/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/**)",
      "Bash(npx shadcn@latest add:*)",
      "Bash(npx shadcn@latest init)",
      "Write(src/components/**)",
      "Write(src/styles/tokens.css)",
      "Write(out/**)"
    ]
  }
}
```
