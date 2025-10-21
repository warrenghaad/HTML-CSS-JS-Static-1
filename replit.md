# Interactive E-Textbook Project

## Overview
This is a simple interactive e-textbook website designed to help learn the basics of web design, hosting, and creating interactive elements. The project is aimed at providing educational material for teachers and students.

**Created:** October 21, 2025
**Status:** Basic structure complete and running

## Project Structure

```
.
├── index.html    - Main HTML file with textbook content
├── style.css     - Stylesheet for layout and design
├── script.js     - JavaScript for interactive features
└── replit.md     - This documentation file
```

## Features Implemented

### Basic Web Design Elements
- Clean, responsive HTML structure
- Navigation menu with multiple sections (Home, Chapter 1, Chapter 2, Resources)
- Styled header and footer
- CSS styling with gradients, colors, and layouts

### Interactive Features
- **Section Navigation**: Click navigation links to switch between different chapters
- **Collapsible Content**: Toggle buttons to show/hide content
- **Interactive Quiz**: Sample quiz with instant feedback
- **Responsive Design**: Works on both desktop and mobile devices

### Educational Content
- Introduction to HTML
- Introduction to CSS
- JavaScript basics
- Sample interactive quiz
- Resources section for teachers and students

## How to Use

The website is automatically hosted using Python's built-in HTTP server on port 5000. The server runs continuously when the Repl is active.

### For Students
- Navigate through chapters using the top menu
- Click "toggle" buttons to reveal additional content
- Try the interactive quiz in Chapter 2
- All interactions happen in the browser without needing to reload

### For Teachers
- The Resources section contains placeholders for teacher materials
- Content can be easily expanded by editing the HTML file
- New chapters can be added by following the existing pattern

## Web Hosting

The site is served using Python's HTTP server:
- **Command**: `python -m http.server 5000`
- **Port**: 5000 (required for Replit webview)
- **Access**: Click the webview pane or use the Replit-provided URL

## Learning Paths

### What You Can Learn from This Project

1. **HTML Basics**
   - Document structure
   - Semantic elements (header, nav, main, footer)
   - Links and navigation
   - Content organization

2. **CSS Styling**
   - Layout with flexbox
   - Colors and gradients
   - Responsive design with media queries
   - Animations and transitions
   - Shadow effects

3. **JavaScript Interactivity**
   - Event listeners
   - DOM manipulation
   - Functions
   - Conditional logic
   - Class toggling for show/hide effects

4. **Web Hosting**
   - How web servers work
   - Serving static files
   - Port configuration

## Next Steps to Expand

- Add more chapters and lessons
- Create additional interactive elements (drag-and-drop, flashcards)
- Add video embeds or image galleries
- Create a progress tracking system
- Implement user accounts (requires backend)
- Add printable worksheets
- Create assessment tools and gradebooks

## Troubleshooting

### Website not loading?
- Check that the Web Server workflow is running
- Ensure it's running on port 5000
- Refresh the browser/webview

### Changes not appearing?
- Save your files
- Hard refresh the browser (Ctrl+Shift+R or Cmd+Shift+R)
- Clear browser cache if needed

### Navigation not working?
- Check browser console for JavaScript errors (F12)
- Ensure script.js is properly linked in index.html

## Files Description

**index.html** - Contains all the page structure and content. This is where you add new chapters, sections, and text.

**style.css** - Controls all visual aspects including colors, fonts, spacing, and animations. Modify this to change the look and feel.

**script.js** - Handles all interactive behaviors like navigation switching, content toggling, and quiz functionality.

## User Preferences

None specified yet.
