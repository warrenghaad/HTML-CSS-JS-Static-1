# SSOT-010: IMAGE ACQUISITION + INTEGRATION
version: 5.0.0
generated_at: 2026-02-02

# SSOT-010: IMAGE ACQUISITION & TAGGING INTEGRATION

## Architecture Overview

```
[Sources]                    [Download]              [Tag]                [Store]
Met API ─────────┐
Smithsonian ─────┼──► image_downloader.py ──► auto_tagger.py ──► SQLite + Files
Wiki Commons ────┤                                                    │
CDLI ────────────┘                                                    ▼
                                                              [Query/Use]
                                                           curriculum_builder
```

---

## Database Schema (from Image_extraction)

Already defined in project. Key tables:

```sql
images (id, item_id, path, mime, width, height, hash, alt_text, caption)
rights (image_id, license_code, attribution_text, deriv_permitted)
image_features (image_id, elements_json, symmetry_json, tiling_type)
```

**Addition for GE taxonomy:**

```sql
CREATE TABLE image_ge_tags (
  image_id TEXT REFERENCES images(id),
  ge_type TEXT CHECK(ge_type IN ('GEA','GEM','GEK','GEU')),
  ge_element TEXT,
  confidence REAL,
  source TEXT CHECK(source IN ('auto','manual')),
  PRIMARY KEY (image_id, ge_type, ge_element)
);

CREATE TABLE image_civ_tags (
  image_id TEXT REFERENCES images(id),
  civilization TEXT,
  period TEXT,
  PRIMARY KEY (image_id, civilization)
);

CREATE TABLE image_deity_links (
  image_id TEXT REFERENCES images(id),
  deity_id TEXT,
  relationship TEXT DEFAULT 'depicts_symbol',
  PRIMARY KEY (image_id, deity_id)
);
```

---

## Sources & Rate Limits

| Source | API | Rate | License | Focus |
|--------|-----|------|---------|-------|
| Met Museum | REST, no auth | 80/sec | CC0 | Islamic, Egyptian, Greek |
| Smithsonian | REST, API key | 1000/day | CC0 | Diverse |
| Wiki Commons | REST | 50/sec | Varies | All |
| CDLI | Bulk | N/A | Edu use | Cuneiform |
| Yale Babylon | Manual | N/A | Edu use | Tablets |

---

## File Structure

```
/images/
  /raw/                    # Original downloads
    /{source}/
      /{civilization}/
        {id}_{title}.{ext}
  /processed/              # Resized, annotated
    /lesson/               # Lesson-ready
    /thumb/                # Thumbnails
  /metadata/
    manifest.json          # All images
    rights_log.csv         # License tracking
```

---

## Naming Convention

`{source}_{civ}_{period}_{ge_primary}_{id}.{ext}`

Examples:
- `met_meso_urIII_GEM-rosette_12345.jpg`
- `wiki_egypt_newkingdom_GEA-triangle_pyramid01.jpg`
- `smith_islamic_abbasid_GEK-2Don3D_bowl789.jpg`

---

## Integration Points

1. **Download** → writes to `/raw/`, creates `images` + `rights` rows
2. **Auto-tag** → reads image, writes `image_ge_tags` rows
3. **Manual review** → updates confidence, adds tags
4. **Curriculum builder** → queries by GE tags, civ, period

---

## Quick Start Commands

```bash
# Download from Met (Islamic geometric)
python image_downloader.py --source met --dept 14 --query "geometric" --limit 100

# Download from Met (Egyptian)
python image_downloader.py --source met --dept 10 --query "pyramid" --limit 50

# Auto-tag downloaded images
python auto_tagger.py --dir ./images/raw/met/

# Export for lesson
python export_lesson_images.py --lesson W1L1 --output ./lessons/w1l1/images/
```

---

## VERSION

| Date | Change |
|------|--------|
| 2024-12-29 | Created. Integration of GE taxonomy with image pipeline. |