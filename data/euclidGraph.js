export const nodes = [
  { id: 'lesson-system', label: 'EUCLID Lesson System', type: 'system', layer: 'root', summary: 'The whole curriculum production map: canon, lesson instances, research, writing, images, design, and QA.' },

  { id: 'research-system', label: 'Research System', type: 'system', layer: 'production', summary: 'Sources, museum artifacts, evidence notes, and scholarly claims that fuel writing.' },
  { id: 'writing-system', label: 'Writing System', type: 'system', layer: 'production', summary: 'SSOT drafts, student-facing copy, teacher scripts, concept handoff language, and slide text.' },
  { id: 'image-system', label: 'Image System', type: 'system', layer: 'production', summary: 'Image briefs, found-image searches, museum assets, generated prompts, and diagram requests.' },
  { id: 'design-system', label: 'Design System', type: 'system', layer: 'production', summary: 'Screen archetypes, Figma frames, visual layouts, diagrams, and final assembly.' },
  { id: 'qa-system', label: 'QA Compiler', type: 'system', layer: 'production', summary: 'Tag validation, Day A / Day B boundary checks, handoff checks, and production readiness.' },

  { id: 'A1', label: 'A1 Myth', type: 'section', day: 'A', register: 'Metaphor', screen: 'Cinematic', summary: 'The element appears as a story power that solves a mythic problem.' },
  { id: 'A2', label: 'A2 Symbolic Role', type: 'section', day: 'A', register: 'Metaphor', screen: 'Character Sheet', summary: 'The myth power becomes a symbolic statement and visual rhetoric lens.' },
  { id: 'A3', label: 'A3 Artifact Visualization', type: 'section', day: 'A', register: 'Metaphor', screen: 'Lore Codex', summary: 'The symbolic meaning becomes visible in artifacts and iconography.' },
  { id: 'A4', label: 'A4 Material Culture', type: 'section', day: 'A', register: 'Metaphor', screen: 'Collection Gallery', summary: 'The artifact pattern expands into a wider cultural ecosystem.' },
  { id: 'A5', label: 'A5 Visual Toolbelt', type: 'section', day: 'A', register: 'Metaphor', screen: 'Tutorial', summary: 'The cultural visual pattern becomes teachable art technique and decomposition.' },
  { id: 'A6', label: 'A6 Create Artifact', type: 'section', day: 'A', register: 'Metaphor', screen: 'Workshop', summary: 'Students embody the visual rhetoric through making.' },
  { id: 'A7', label: 'A7 Bridge / Exit', type: 'section', day: 'A', register: 'Both', screen: 'Split Reveal', summary: 'A dual-register object asks what the same geometry means and does.' },

  { id: 'B1', label: 'B1 Bridge Review', type: 'section', day: 'B', register: 'Both', screen: 'Recap', summary: 'The Day A object is reframed as a function question.' },
  { id: 'B2', label: 'B2 Math Proof', type: 'section', day: 'B', register: 'Function', screen: 'Whiteboard', summary: 'The function question becomes grade-scaled geometry and proof.' },
  { id: 'B3', label: 'B3 Transformation', type: 'section', day: 'B', register: 'Function', screen: 'Transformation', summary: 'The formal geometry becomes an operation: rotate, reflect, scale, tile, transform.' },
  { id: 'B4', label: 'B4 Mechanics', type: 'section', day: 'B', register: 'Function', screen: 'Schematic', summary: 'The operation becomes physical mechanism: force, load, flow, light, material, or motion.' },
  { id: 'B5', label: 'B5 STEM History', type: 'section', day: 'B', register: 'Function', screen: 'Tech Tree', summary: 'The mechanism appears across inventions and historical deployments.' },
  { id: 'B6', label: 'B6 Invention Moment', type: 'section', day: 'B', register: 'Function', screen: 'Blueprint', summary: 'One invention expands into a case study with decomposition and implicit science.' },
  { id: 'B7', label: 'B7 Build Activity', type: 'section', day: 'B', register: 'Function', screen: 'Build Guide', summary: 'Students prototype and test the functional principle.' },
  { id: 'B8', label: 'B8 Synthesis', type: 'section', day: 'B', register: 'Both', screen: 'Superimposition', summary: 'Meaning and function are held together without collapsing one into the other.' }
];

export const edges = [/* unchanged */];

export const handoffOrder = ['A1','A2','A3','A4','A5','A6','A7','B1','B2','B3','B4','B5','B6','B7','B8'];
