# Geo-Arts System Console

## Overview
A static HTML dashboard for the Geo-Arts educational curriculum system. This console serves as:
- **SSOT Holder** - Single Source of Truth documentation library
- **System Auditor** - Analyzes project status and identifies gaps
- **Checklist Generator** - Creates actionable tasks
- **Job JSON + CLI Generator** - Produces payloads for automation

**Created:** February 4, 2026
**Status:** Static console deployed

## Project Structure

```
.
├── index.html            - Main console (single-file application)
├── style.css             - Not used (styles embedded in HTML)
├── script.js             - Not used (scripts embedded in HTML)
├── replit.md             - Project documentation
└── attached_assets/      - Original source files
```

## Console Features

### 1. Theme Modes
- **Face (Light)** - Clean light theme for presentations
- **Builder (Blue)** - Dark blue theme for development work
- **Research (Dark)** - Dark theme for extended reading

### 2. Tab Panels
- **Overview** - Canonical truth rules and usage instructions
- **SSOT Library** - Embedded documentation files (expandable)
- **Auditor + Checklist** - Paste status JSON, analyze gaps
- **Job JSON + CLI** - Generate automation payloads
- **Flight Crew To-Do** - Local task list (localStorage)

### 3. Embedded SSOT Documents
- SSOT-000_MASTER_TAXONOMY.md/.json - Core taxonomy definitions
- PATCH_SSOT_002_014.md - Alignment patches
- SECTION_TAG_PRESETS.json - Section tagging rules
- SYSTEM_PROMPT_CARWASH.md - Agent system prompt
- EXAMPLE_section_pack_shamash_circle_A1.json - Sample data
- SSOT-000_TERMS_TABLE.md - Quick reference

## Key Concepts (Taxonomy)

| Term | Meaning | Used For |
|------|---------|----------|
| GE | Geometric Element | Core throughline |
| GEA | Atomic (primitives) | Point, line, circle, etc. |
| GEM | Molecular (composites) | Rosettes, grids, patterns |
| GEK | Conceptual (math+science) | Day B content |
| GEpHR | Metaphor (meaning) | Day A content |
| GEU | Ubiquitous flag | Cross-cultural elements |

## Day A / Day B Structure

**Day A (GEpHR - Metaphor Track):**
- A1: Myth Definition
- A2: Metaphor Visualization
- A3: Mythic Iconography
- A4: Material Culture + Ritual
- A5: Decomposition
- A6: Art Activity
- A7: Bridge Prompt

**Day B (GEK - Function Track):**
- B1: Bridge Answer
- B2: Math Concept
- B3: Science Effect
- B4: STEM Timeline
- B5: Case Study
- B6: Deconstruction
- B7: Build/Design Challenge
- B8: Synthesis

## How to Use the Console

1. **View Documentation**: Click "SSOT Library" tab, expand any document
2. **Audit a Project**: Paste status JSON into Auditor, click "Analyze"
3. **Generate Jobs**: After analysis, click "Generate Jobs" for automation
4. **Track Tasks**: Use "Flight Crew To-Do" for persistent task tracking

## Web Design Learning Points

### HTML Structure
- Single-page application pattern
- Semantic HTML (header, main, aside, section)
- Details/summary for collapsible content
- Data attributes for JavaScript binding

### CSS Techniques
- CSS custom properties (variables) for theming
- Flexbox and Grid layouts
- Backdrop blur for glassmorphism
- Media queries for responsiveness
- Transitions and animations

### JavaScript Patterns
- Tab switching with classList
- localStorage for persistent data
- JSON parsing and display
- Event delegation
- Dynamic DOM manipulation

## Backend Integration (Future)

The console currently works offline. To connect to Supabase:
1. Add Supabase client library
2. Replace localStorage with database calls
3. Add authentication
4. Implement real-time status sync

## User Preferences

- Building educational curriculum tools
- Focus on Kanban/Scrum project management
- Learning web development fundamentals
- Has extensive backend (Supabase) to connect later
- Needs documentation for Geo-Arts system
