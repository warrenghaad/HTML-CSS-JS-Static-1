# MCP Setup

The kit assumes Claude Code on your Mac with the following MCP servers
configured. Copy `.mcp.json.example` to the repo root as `.mcp.json` and
edit the env vars.

**Notion status:** the user has reorganized Notion (as of the
`canon-preservation` branch) and it is now a **supported optional
satellite**. It is still not the source of truth over local Mac files
or the canon in this repo, but it is safe to consult.

## Required (the canonical source + design context)

### 1. Filesystem MCP — reads the mounted EUCLID volume

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem \
  "/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID"
```

The canonical EUCLID directory lives on a mounted secondary volume
(`Macintosh HD-1`). If Finder doesn't show that volume, mount it before
starting Claude Code — the filesystem MCP fails fast if the path
doesn't resolve.

The trailing path is the **only** directory the server is allowed to
read — a sandbox boundary. Add more paths as additional positional args
if scout needs them (e.g. the `GE SECTION OR MAPPING` and `IMAGE SPEC AND
PRODUCTION` subdirectories already live under EUCLID, so the single
path covers them).

### 2. Figma MCP (hosted) — design context, libraries, Code Connect

Claude Code's built-in Figma integration is already configured for this
session (`smajeed3@gmail.com`, Trivius org dev seat). On your Mac:

```bash
claude mcp add figma --transport http -- https://mcp.figma.com
# follow the OAuth flow; pick the Trivius org for design-system access
```

### 3. Figma Dev Mode MCP (local) — pulls designs open in the desktop app

When the **Figma desktop app** is running with **Dev Mode MCP** enabled
(Preferences → Dev Mode → "Enable local MCP server"), it exposes an HTTP
MCP endpoint at `http://127.0.0.1:3845/mcp` that Claude Code can call to
read the currently-open file and selection.

```bash
claude mcp add figma-local --transport http -- http://127.0.0.1:3845/mcp
```

**When to use `figma-local` vs the hosted `figma`:**

- **hosted `figma`** — headless access to any file in the Trivius org by
  file key; use for scheduled scripts, CI, or when the desktop app isn't
  running.
- **local `figma-local`** — zero-latency access to the currently-open
  file and selection; use during interactive design-to-code work,
  especially for pulling a specific frame you're staring at into the
  canon-editor pipeline. See `canon/GRAPH-PIPELINE.md`.

Both can coexist — tools have distinct prefixes (`mcp__figma__*` vs
`mcp__figma-local__*`).

### 4. Notion MCP — reference organization (post-reorg)

```bash
claude mcp add notion --transport http -- https://mcp.notion.com/mcp
# OAuth into the workspace that owns the reorganized structure
```

Safe to consult for cross-referencing structure. Never source of truth
over local files or the repo's `canon/`.

## Optional satellites

### Google Drive MCP — fallback for assets / specs not on the Mac

```bash
claude mcp add gdrive -- npx -y @modelcontextprotocol/server-gdrive
# requires GOOGLE_APPLICATION_CREDENTIALS pointing at a service-account JSON
```

Use only when a referenced asset is missing locally. Also the source
for the backend HTMLs catalogued in `canon/backend-history/CATALOG.md`.

### Adobe Express MCP — image ops, asset search, vectorize, background removal

```bash
claude mcp add adobe-express --transport http -- https://express.adobe.com/mcp
```

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

should list every server above as `connected`. Common gotchas:

- `filesystem` shows `connection refused` → the `Macintosh HD-1` volume
  isn't mounted. Mount it, restart Claude Code.
- `figma-local` shows `connection refused` → the Figma desktop app isn't
  running, or Dev Mode MCP isn't enabled in Preferences.
- `notion` shows `unauthorized` → re-run the OAuth flow via
  `claude mcp` or in claude.ai connector settings.

## Permissions to allowlist

Add these to `.claude/settings.local.json` to avoid prompts during agent
runs (review carefully — these grant broad read on the EUCLID dir and
limited write on `src/` and `canon/`):

```json
{
  "permissions": {
    "allow": [
      "Read(/Volumes/Macintosh HD-1/Users/warrenghaad/PANTTEARRA - DOCUMENTS/EUCLID/**)",
      "Bash(npx shadcn@latest add:*)",
      "Bash(npx shadcn@latest init)",
      "Write(src/components/**)",
      "Write(src/styles/tokens.css)",
      "Write(out/**)",
      "Write(canon/vault/**)"
    ]
  }
}
```
