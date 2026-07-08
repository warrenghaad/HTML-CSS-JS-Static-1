# Backend HTML catalog

Authoritative source: Google Drive. This file is an **index by Drive ID** — do not copy raw HTMLs into the repo.

Extraction status:
- `pending` — catalogued, not yet processed by Phase 1
- `inventoried` — Phase 1 has produced an entry in `../inventory.json`
- `extracted` — Phase 2 has generated Markdown in `../vault/`

## Files

| Drive ID | Filename | Approx. modified | Approx. size | Notes | Status |
|---|---|---|---|---|---|
| `1Lmpndt7pEBZf5kKamsJPWJUOkl0I0hT-` | `index-v5.html` (Project Euclid) | 2026-02-13 | ~67 KB | Primary backend variant. Full canvas + workflow structure with embedded Project Euclid framing. | `pending` |
| `1bkWWrLN_lypUxMUYfccTYtx0R284-BR0` | `index-v5.html` (S50K variant) | 2026-02-18 | ~25 KB | Slimmer variant tuned around the S50K system + workflow hub layout. | `pending` |
| `1qdsEaAZl289L-wzkXRc2c0SARYZB1AIb` | `Copy of index-v5.backup-pre-static-map-20260217_174759.html` | 2026-02-17 17:47 | ~67 KB | Snapshot taken immediately before the static-map refactor. | `pending` |
| `17j1Ehmpsl4kZL5k8GT6Ky5zheO9BGumY` | `index-v5.backup-pre-system-workflow-reorg-20260217_203907.html` | 2026-02-17 20:39 | ~18 KB | Snapshot taken before the system + workflow reorganization. | `pending` |

## Also relevant

SSOT (single source of truth) reference material already committed to the repo lives at `attached_assets/`:

- `SSOT_Personas.md` — the persona set
- `SSOT_Framework_-Trivius-Learn-System.md` — Trivius framework overview
- `SSOT_Adventure_Realms.md` — realms catalog
- `SSOT_Blender-Cinematic.md` — cinematic reference
- `SSOT-Adventure_Sample.md` — sample adventure spec

These are treated as **inputs to the vault**, not part of the backend HTML history. Phase 2 references them by relative path from the extracted Markdown.

## Adding a new backend HTML

1. Upload to Drive (any location — path is not what matters, the file ID is).
2. Add a row to the table above with the ID.
3. Set status to `pending` and open a PR — that's the trigger for Phase 1 to re-run.

Any row whose approximate metadata is unverified should be re-checked by Phase 1's scout, which re-queries Drive by ID and updates this table with the ground-truth values.
