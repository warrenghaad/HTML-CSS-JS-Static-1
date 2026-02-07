# Geo-Arts Curriculum System

## Overview
A learning-focused project management documentation space that serves as both a tutorial for web development (HTML/CSS/JS) and a visual diagram of the Geo-Arts educational curriculum backend system.

**Created:** February 4, 2026  
**Updated:** February 5, 2026  
**Status:** Complete end-goal example with lessons

## Purpose
This project has two goals:
1. **End Goal Example**: A fully developed visual diagram showing the complete curriculum system workflow
2. **Learning Resource**: Step-by-step lessons teaching HTML, CSS, and JavaScript concepts

## Project Structure

```
.
├── index.html                    - System architecture diagram (home page)
├── pages/
│   ├── governance.html           - Governance & Context engine
│   ├── knowledge-graph.html      - Knowledge Graph Engine
│   ├── rwi-system.html           - RWI (Research/Writing/Image) System
│   ├── lesson-builder.html       - Lesson Builder engine
│   ├── teacher-student.html      - Teacher/Student facing interface
│   └── lessons.html              - Web development lessons
├── styles/
│   └── main.css                  - Shared stylesheet (1800+ lines)
├── scripts/
│   └── main.js                   - Shared JavaScript
└── replit.md                     - This documentation
```

## The 5 Engine Cards

| Card | Purpose | Description |
|------|---------|-------------|
| **Governance & Context** | SSOTs, Presets, Standards | Provides overarching context, program info, 6+ knowledge graph presets/views |
| **Knowledge Graph Engine** | Ingestion, Ontology, Tagging | 3D research graph, 30GB+ PDF ingestion, wiki node generation |
| **RWI System** | Research, Writing, Images | Content drafting, image sourcing, Gemini/OpenAI API integration |
| **Lesson Builder** | Canvas, Sections, Distillation | Drag-drop wiki canvas, lesson section assembly, eTextbook deliverables |
| **Teacher/Student** | Deliverables, Progress | Final presentations, eTextbook viewer, performance analytics |

## Data Flow (Color-Coded)

```
Governance (Cyan - overarching context)
        ↓
Knowledge Graph → (Blue) → RWI System → (Green) → Lesson Builder → (Purple) → Teacher/Student
        ↑                                                                           ↓
        └────────────────────── (Orange - Performance Feedback Loop) ───────────────┘
```

## Key System Features

### Knowledge Graph Presets (6 Views)
1. **Geometric Elements** - Original research on geometric fundamentals
2. **Lesson Structure** - Geometric research → lesson creation
3. **Standards & Curriculum** - Current mappings, cognitive domains
4. **Child Development** - Cognitive domains & developmental stages
5. **Student Performance** - Domains, standards, performance data
6. **Standards Creation** - Building new standards from research

### Visual-First Curriculum Philosophy
- Story told with pictures, captioned by text
- Every piece of content must have an image
- Images sourced via search, or generated via:
  - Gemini API (short videos, diagrams)
  - OpenAI API (long videos, myths)

### RWI System API Points
- `GET /api/images/search` - Search existing images
- `POST /api/gemini/generate` - Generate short videos/images
- `POST /api/openai/generate` - Generate long videos/complex content

### eTextbook Distillation
- Complete lessons → Distillation process → Deliverables
- Outputs: eTextbook chapters, presentation slides, worksheets, rubrics

## Web Development Lessons (8 Lessons)

| Lesson | Topic | Level |
|--------|-------|-------|
| 1 | HTML Structure: Building Cards | Beginner |
| 2 | CSS Flexbox: Arranging Cards in Rows | Beginner |
| 3 | CSS Variables: Theme Colors | Intermediate |
| 4 | JavaScript Events: Theme Toggle | Intermediate |
| 5 | CSS Transitions: Smooth Animations | Beginner |
| 6 | JavaScript DOM: Finding and Changing Elements | Intermediate |
| 7 | Responsive Design: Mobile-Friendly Layouts | Intermediate |
| 8 | Multi-Page Apps: Navigation with Links | Beginner |

## Technical Implementation

### CSS Techniques Used
- CSS custom properties (`:root` variables) for theming
- CSS Grid for 4-column engine layout
- Flexbox for card contents
- Health status indicators with colored dots and shadows
- Smooth transitions on hover
- Media queries for responsive design
- Dark/light theme support

### JavaScript Features
- Theme toggle with localStorage persistence
- Flow arrow highlighting on card hover
- Health status update functions (ready for backend)
- DOM manipulation examples

## Document Editor & Versioning

The Governance page includes an in-page pop-out editor for the System Functionality Document:
- Click "Edit This Document" to open the editor modal
- Edit content in a full-screen text area
- Save with version notes — every save creates a new version
- Browse version history in the sidebar
- View or restore any previous version

### API Endpoints
- `GET /api/documents/<doc_key>` - Load a document
- `PUT /api/documents/<doc_key>` - Save document (creates new version)
- `GET /api/documents/<doc_key>/versions` - List all versions
- `GET /api/documents/<doc_key>/versions/<n>` - Get specific version
- `POST /api/documents/<doc_key>/versions/<n>/restore` - Restore a version

### Database Tables
- `documents` - Current document state (doc_key, title, content)
- `document_versions` - Version history (version_number, content, save_note, timestamp)

## User Preferences

- **Visual-first curriculum**: All content must have images
- **Multi-page app structure**: Separate HTML files, not SPA
- **Learning-focused**: Code serves as tutorial material
- **In-page editing**: Documents should be editable with versioning

## Running the Project

The project uses a Flask backend server:
```bash
python server.py
```

Access at `http://localhost:5000`
