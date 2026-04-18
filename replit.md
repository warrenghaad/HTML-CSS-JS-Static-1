# Geo-Arts Curriculum System

## Overview
The Geo-Arts Curriculum System is a dual-purpose project: it serves as a comprehensive visual diagram of an educational curriculum backend and a step-by-step tutorial for web development using HTML, CSS, and JavaScript. Its primary goal is to demonstrate a fully developed curriculum system workflow while simultaneously providing learning resources for aspiring web developers. The project envisions streamlining curriculum development, enhancing learning experiences through visual content, and providing robust tools for content creation, management, and delivery within an educational framework.

## User Preferences

- **Visual-first curriculum**: All content must have images
- **Multi-page app structure**: Separate HTML files, not SPA
- **Learning-focused**: Code serves as tutorial material
- **In-page editing**: Documents should be editable with versioning
- **Sandbox workflow**: Experiment in playground, get AI review before promoting

## System Architecture

The system is built around five core "Engines": Governance & Context, Knowledge Graph, RWI (Research/Writing/Image) System, Lesson Builder, and Teacher/Student Interface. These engines manage the curriculum workflow from foundational context and knowledge ingestion to lesson assembly and final delivery.

**UI/UX Decisions:**
- A visual-first philosophy dictates that all content is image-centric, with images sourced or AI-generated.
- The UI uses CSS custom properties for theming, CSS Grid for layout, and Flexbox for component arrangement.
- Responsive design with media queries ensures adaptability across devices.
- Dark/light theme support is included.

**Technical Implementations:**
- **Core Structure**: The application uses a multi-page architecture with distinct HTML files for different sections (e.g., `index.html`, `pages/governance.html`, `pages/production-dashboard.html`).
- **Styling**: `main.css` provides comprehensive styling, including health status indicators, smooth transitions, and thematic elements.
- **Interactivity**: `main.js` handles client-side logic such as theme toggling with `localStorage` persistence, flow arrow highlighting, and DOM manipulation.
- **Document Editor**: An in-page editor with versioning capabilities allows for editing system documentation, tracking changes, and restoring previous versions.
- **Code Playground**: A sandbox environment (`pages/playground.html`) enables users to write and preview HTML/CSS, with an option for AI review.
- **Production Dashboard**: Tracks the 48 Mesopotamia lesson production workflow, including overall progress, team performance, and lesson pipeline status.
- **Variable Management**: A "Variables Spreadsheet" (`pages/variables-spreadsheet.html`) allows for inline editing and management of lesson-specific variables with auto-save functionality.
- **Asset Management**: The "Asset Manager" (`pages/asset-manager.html`) tracks visual assets, supporting CRUD operations and status tracking.
- **Content Pipeline**: The "Content Pipeline" (`pages/content-pipeline.html`) manages content drafts (Myths, Math, Visual Stories, Activities) through various stages.
- **Lesson Assembly**: Tracks the readiness of components for each lesson using a checklist system.
- **QA Review**: Facilitates quality assurance checks across different categories for each lesson.
- **Database Schema**: Key database tables include `documents`, `document_versions`, `playground_drafts`, `production_lessons`, `production_teams`, `production_tasks`, `production_assets`, `content_items`, `assembly_checklists`, and `qa_reviews`.

## Day B Geometry Curriculum System

The Day B system delivers 24 geometry lessons (8 geometric elements x 3 grade levels) with 192 total sections following the ECD (Element + Carrier + Dimension) framework.

### Element Sequence (SSOT-004)
| Week | Element | Deity | Core Property |
|------|---------|-------|---------------|
| 1 | Circle | Shamash | Equidistance |
| 2 | 8-Pointed Star | Ishtar | Radial symmetry (8-fold) |
| 3 | Triangle | Enlil | Structural rigidity |
| 4 | Square/Rectangle | Nabu | Right-angle regularity |
| 5 | Spiral | Tiamat | Progressive expansion |
| 6 | Arc/Curve | Anu | Continuous directional change |
| 7 | Hexagon | Nisaba | Optimal packing |
| 8 | Pyramid | Marduk | Convergent stability |

### Section Structure (B1-B8)
- B1: Bridge Review (connects to Day A)
- B2: Math Proof
- B3: STEM History
- B4: Cultural Connection
- B5: Cumulative Synthesis (references B2+B3+B4 from ALL prior elements)
- B6: Engineering Activity
- B7: Advanced Application
- B8: Reflection/Assessment

### MAGIC Drivers
M=Math, A=Aesthetics, G=Geometry (emergent center), I=Ideology, C=Culture

### Grade Differentiation
- Grade 3: Concrete language, hands-on tasks
- Grade 4: Connecting concepts, applied measurement
- Grade 5: Abstract reasoning, mathematical proofs

### Day B Database Tables
- `day_b_elements` - 8 geometric elements with deity pairings
- `day_b_lessons` - 24 lessons (element x grade)
- `day_b_sections` - 192 sections with JSONB ECD fields and B5 cumulative references

### Day B API Endpoints
- `GET /api/dayb/stats` - Aggregated statistics
- `GET /api/dayb/elements` - All 8 elements
- `GET /api/dayb/lessons` - Lessons with optional grade filter
- `GET /api/dayb/lessons/<id>/sections` - B1-B8 sections for a lesson
- `PUT /api/dayb/sections/<id>` - Update section content/status
- `GET /api/dayb/b5-chain/<lesson_id>` - Cumulative B5 prior element data

### Kanban Process Tracker
- 3 grade-specific boards (Grade 3: 78 cards, Grade 4: 91 cards, Grade 5: 38 cards)
- 6 workflow columns: Intake, Chunk, Artifact QA, Assets, Build, QA
- Drag-and-drop with localStorage persistence
- Per-card checklists and filtering by week/day/search

### Integrated Tools
- **Myth Catalog**: Interactive Mesopotamian mythology reference with grade/shape/category filters
- **Image Manager**: Museum API sourcing tool (Met, Yale, British Museum, Wikimedia, Smithsonian, CDLI)
- **Lesson Shell Demo**: Sidebar navigation with hash-based routing for rendered lesson content
- **Drive Ingester** (`pages/ingester.html`): Pulls structured lesson content from a Google Drive folder (expects subfolders named `G{grade}-W{week}-Day{A|B}` containing `sections.json`) and reconciles them against `day_b_sections`. Per-section, per-field side-by-side diff with selective apply / reject / reset. Backed by `gdrive_helper.py` + `/api/ingest/*` endpoints and the `ingest_candidates` table. Uses the Replit Google Drive integration (OAuth handled via the connectors proxy at `${REPLIT_CONNECTORS_HOSTNAME}`). Note: only Day B has DB lessons today, so Day A candidates show as "no DB match" until a Day A schema is added.

## External Dependencies

- **Gemini API**: Used for generating short videos and diagrams.
- **OpenAI API**: Integrated for generating longer videos, complex content, and AI review in the Playground.
- **Flask**: Python microframework used for the backend server (`server.py`) to handle API requests and serve HTML content.