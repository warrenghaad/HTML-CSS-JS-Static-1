# Project Management Documentation Site

## Overview
A static HTML documentation site for a desktop project management application. This read-only reference guide covers Kanban and Scrum project management features.

**Created:** February 4, 2026
**Status:** Static documentation site complete

## Project Structure

```
.
├── index.html    - Main HTML documentation with all sections
├── style.css     - Professional styling for documentation
├── script.js     - Navigation between sections
└── replit.md     - Project documentation
```

## Documentation Sections

1. **Overview** - Introduction to the app's features
2. **Kanban Board** - Visual workflow management, columns, cards, WIP limits
3. **Scrum Framework** - Roles, events, ceremonies
4. **Product Backlog** - User stories, story points, prioritization
5. **Sprint Planning** - Sprint configuration and workflow
6. **Reports & Metrics** - Burndown charts, velocity, cycle time

## Features

### Static Documentation
- Clean, professional layout with sidebar navigation
- No backend required - pure HTML/CSS/JS
- Responsive design for desktop and mobile
- Smooth section transitions

### Content Covered
- Kanban board columns and card features
- Scrum roles (Product Owner, Scrum Master, Dev Team)
- Scrum events (Planning, Standups, Review, Retrospective)
- User story format and story points
- Sprint workflow steps
- Key project metrics and reports

## Web Hosting

Served using Python's built-in HTTP server:
- **Command**: `python -m http.server 5000`
- **Port**: 5000

## How to Modify

### Adding New Sections
1. Add a navigation link in the sidebar `<nav>` section
2. Create a new `<section id="your-id" class="content-section">` in main
3. Fill in your documentation content

### Changing Styles
- Edit `style.css` to modify colors, fonts, spacing
- Main color scheme uses blues (#1a365d, #2b6cb0)

## User Preferences

- Learning web design basics
- Building documentation for a desktop app
- Focus on Kanban and Scrum project management features
- Static/read-only content preferred
