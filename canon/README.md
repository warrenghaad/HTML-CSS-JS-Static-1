# canon/

Index + extracted knowledge for the Trivius / Mesopotamia backend.

## Purpose

The backend has lived in a rolling series of large `index-v5.html` files on Google Drive — big, self-contained HTML documents that carry the whole system's state (canvases, workflows, presets, personas, Q&A). Every rewrite has risked losing structure that was baked into those files.

This directory is the **catalog and structured extraction** of that material — the raw HTMLs stay in Drive (which is authoritative), and everything here is what we've indexed, extracted, and cross-referenced from them.

## Layout

```
canon/
├── README.md                   ← you are here
├── backend-history/
│   └── CATALOG.md              ← index of Drive-hosted backend HTMLs by ID
├── inventory.json              ← (Phase 1) structured map of every entity across all backend HTMLs
└── vault/                      ← (Phase 2) Obsidian-compatible Markdown, one file per entity
    ├── canvases/
    ├── workflows/
    ├── presets/
    ├── personas/
    └── qa/
```

A sibling `canon-editor/` (Phase 3) is a React viewer that reads `canon/vault/**/*.md` and renders it as a browsable, cross-linked tree.

## Workflow

1. **A new backend HTML appears in Drive.** Add a row to `backend-history/CATALOG.md` with its Drive ID, date, size, and one-line description. Do NOT copy the raw HTML into this repo — Drive is canonical.
2. **Run Phase 1 (inventory).** A scout re-fetches each catalogued HTML, parses out the section structure and entities, and updates `inventory.json`.
3. **Run Phase 2 (extract).** For entities that don't yet have a Markdown file in `vault/`, generate one with YAML frontmatter linking back to the source Drive ID.
4. **Edit in Obsidian.** Point Obsidian at `canon/vault/` (or copy it into your existing vault). Edits get committed here through the git-connect.
5. **View through canon-editor.** The React app reads the vault at runtime and renders it with search, tags, and cross-links.

## Non-goals

- **Not a Drive backup.** We don't copy raw HTMLs into the repo. If Drive loses a file, restore from Drive's version history, not from here.
- **Not the app.** Nothing in `canon/` runs at app runtime for end users. It powers `canon-editor/`, which is a separate authoring surface for the team.
