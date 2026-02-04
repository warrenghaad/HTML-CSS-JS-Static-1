# Geo-Arts System Console - Multi-Agent Pipeline

## Overview
A multi-page web application documenting a multi-agent workflow pipeline. This is NOT a single-page app—each engine has its own dedicated page.

**Created:** February 4, 2026
**Status:** Multi-page structure complete

## Project Structure

```
.
├── index.html              - Home dashboard with 5 engine cards
├── pages/
│   ├── snapshot.html       - Snapshot Engine page
│   ├── diff.html           - Diff Engine page
│   ├── ag-func.html        - Ag_Func Engine page
│   ├── ag-mess.html        - Ag_Mess Engine page
│   └── ag-html.html        - Ag_Html Engine page
├── styles/
│   └── main.css            - Shared stylesheet
├── scripts/
│   └── main.js             - Shared JavaScript
└── replit.md               - This documentation
```

## The 5 Engines

| Engine | Purpose | Health |
|--------|---------|--------|
| **Snapshot** | Captures backend state at checkpoints | Healthy |
| **Diff** | Compares current vs desired state | Has errors |
| **Ag_Func** | Function agents write files & wait | Warning |
| **Ag_Mess** | Messenger reads files, updates status | Healthy |
| **Ag_Html** | Tests functionality, writes results | Healthy |

## Workflow Connections (Arrow Colors)

- **Blue** - Snapshot Flow (Snapshot → Diff, Ag_Html → Snapshot loop)
- **Green** - Diff → Ag_Func
- **Purple** - Ag_Func → Ag_Mess
- **Orange** - Ag_Mess → Ag_Html

## Agent Pipeline Workflow

```
1. SNAPSHOT: Capture backend state
       ↓ (blue)
2. DIFF: Compare current vs desired, chunk into tasks
       ↓ (green)
3. AG_FUNC: Write files, generate status report, WAIT
       ↓ (purple)
4. AG_MESS: Read new files, write status updates (NEW files only)
       ↓ (orange)
5. AG_HTML: Read status, run tests, write results
       ↓
   SPLIT:
   ├── PASS: New snapshot → Next task
   └── FAIL: Debug loop → Back to Ag_Func
```

## Key Rules

### Ag_Func Rules
- FORBIDDEN: Claiming completion immediately after write
- Must wait for validation from Ag_Mess + Ag_Html
- Status remains "pending_validation" until test passes

### Ag_Mess Rules
- Only writes NEW files (never overwrites)
- File naming: `status_{task_id}_{timestamp}.json`

### Task Chunking Rules
- Each chunk ≤ context window size minus memory reserve
- Each chunk has defined input/output for testing
- Chunks are self-contained

## Web Design Concepts Demonstrated

### Multi-Page vs Single-Page
- **MPA (Multi-Page App)**: Each page is a separate HTML file
- Links use `href="pages/engine.html"` (full page navigation)
- Shared CSS/JS files across pages
- Browser handles navigation (no JavaScript routing)

### CSS Techniques
- CSS custom properties for theming
- Grid layout for dashboard
- Flexbox for card rows
- Health status indicators with colored dots
- Responsive design with media queries

### JavaScript Features
- Theme toggle with localStorage
- Hover effects on cards
- Health status updates (prepared for real data)

## Next Steps

1. Add detailed functionality lists to each engine page
2. Create the snapshot/diff JSON schema
3. Build actual agent scripts
4. Connect to Supabase backend

## User Requirements (From Conversation)

- Multi-page app (NOT single-page)
- 5 engine cards with health status
- Colored workflow arrows between engines
- Each tool has input/output for testing
- Ag_Func cannot claim completion immediately
- Ag_Mess only writes NEW files
- Pipeline split at Ag_Html (pass/fail branching)
