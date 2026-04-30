export const nodes = [
  { id: 'lesson-system', label: 'EUCLID Lesson System', type: 'system', layer: 'root', summary: 'The whole curriculum production map: canon, lesson instances, research, writing, images, design, and QA.' },

  { id: 'research-system', label: 'Research System', type: 'system', layer: 'production', summary: 'Sources, museum artifacts, evidence notes, and scholarly claims that fuel writing.' },
  { id: 'writing-system', label: 'Writing System', type: 'system', layer: 'production', summary: 'SSOT drafts, student-facing copy, teacher scripts, concept handoff language, and slide text.' },
  { id: 'image-system', label: 'Image System', type: 'system', layer: 'production', summary: 'Image briefs, found-image searches, museum assets, generated prompts, and diagram requests.' },
  { id: 'design-system', label: 'Design System', type: 'system', layer: 'production', summary: 'Screen archetypes, Figma frames, visual layouts, diagrams, and final assembly.' },
  { id: 'qa-system', label: 'QA Compiler', type: 'system', layer: 'production', summary: 'Tag validation, Day A / Day B boundary checks, handoff checks, and production readiness.' },

  { id: 'A1', label: 'A1 Myth', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Cinematic', summary: 'The element appears as a story power that solves a mythic problem.' },
  { id: 'A2', label: 'A2 Symbolic Role', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Character Sheet', summary: 'The myth power becomes a symbolic statement and visual rhetoric lens.' },
  { id: 'A3', label: 'A3 Artifact Visualization', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Lore Codex', summary: 'The symbolic meaning becomes visible in artifacts and iconography.' },
  { id: 'A4', label: 'A4 Material Culture', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Collection Gallery', summary: 'The artifact pattern expands into a wider cultural ecosystem.' },
  { id: 'A5', label: 'A5 Visual Toolbelt', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Tutorial', summary: 'The cultural visual pattern becomes teachable art technique and decomposition.' },
  { id: 'A6', label: 'A6 Create Artifact', type: 'section', day: 'A', mode: 'GEA', register: 'Metaphor', screen: 'Workshop', summary: 'Students embody the visual rhetoric through making.' },
  { id: 'A7', label: 'A7 Bridge / Exit', type: 'section', day: 'A', mode: 'GEA', register: 'Both', screen: 'Split Reveal', summary: 'A dual-register object asks what the same geometry means and does.' },

  { id: 'B1', label: 'B1 Bridge Review', type: 'section', day: 'B', mode: 'GEF', register: 'Both', screen: 'Recap', summary: 'The Day A object is reframed as a function question.' },
  { id: 'B2', label: 'B2 Math Proof', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Whiteboard', summary: 'The function question becomes grade-scaled geometry and proof.' },
  { id: 'B3', label: 'B3 Transformation', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Transformation', summary: 'The formal geometry becomes an operation: rotate, reflect, scale, tile, transform.' },
  { id: 'B4', label: 'B4 Mechanics', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Schematic', summary: 'The operation becomes physical mechanism: force, load, flow, light, material, or motion.' },
  { id: 'B5', label: 'B5 STEM History', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Tech Tree', summary: 'The mechanism appears across inventions and historical deployments.' },
  { id: 'B6', label: 'B6 Invention Moment', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Blueprint', summary: 'One invention expands into a case study with decomposition and implicit science.' },
  { id: 'B7', label: 'B7 Build Activity', type: 'section', day: 'B', mode: 'GEF', register: 'Function', screen: 'Build Guide', summary: 'Students prototype and test the functional principle.' },
  { id: 'B8', label: 'B8 Synthesis', type: 'section', day: 'B', mode: 'GEF', register: 'Both', screen: 'Superimposition', summary: 'Meaning and function are held together without collapsing one into the other.' }
];

export const edges = [
  { source: 'lesson-system', target: 'A1', type: 'contains', label: 'starts' },
  { source: 'lesson-system', target: 'research-system', type: 'contains', label: 'has system' },
  { source: 'lesson-system', target: 'writing-system', type: 'contains', label: 'has system' },
  { source: 'lesson-system', target: 'image-system', type: 'contains', label: 'has system' },
  { source: 'lesson-system', target: 'design-system', type: 'contains', label: 'has system' },
  { source: 'lesson-system', target: 'qa-system', type: 'contains', label: 'has system' },

  { source: 'A1', target: 'A2', type: 'concept_handoff', label: 'Myth-to-Meaning', summary: 'The element first appears as a story power, then becomes the symbolic role students can name.' },
  { source: 'A2', target: 'A3', type: 'concept_handoff', label: 'Meaning-to-Artifact', summary: 'The symbolic power becomes visible in artifacts, deity symbols, and iconographic choices.' },
  { source: 'A3', target: 'A4', type: 'concept_handoff', label: 'Artifact-to-Culture', summary: 'One artifact becomes a broader pattern across ritual, institution, domestic life, and material culture.' },
  { source: 'A4', target: 'A5', type: 'concept_handoff', label: 'Culture-to-Technique', summary: 'Cultural examples become a teachable visual toolbelt: motif, composition, and technique.' },
  { source: 'A5', target: 'A6', type: 'concept_handoff', label: 'Technique-to-Practice', summary: 'The visual toolbelt becomes student making, practice, and creative application.' },
  { source: 'A6', target: 'A7', type: 'concept_handoff', label: 'Practice-to-Reflection', summary: 'Student work becomes the reflection bridge toward an object with both meaning and function.' },
  { source: 'A7', target: 'B1', type: 'concept_handoff', label: 'Register Shift', summary: 'The same object shifts from what the geometry means to what the geometry does.' },
  { source: 'B1', target: 'B2', type: 'concept_handoff', label: 'Intuition-to-Definition', summary: 'The functional question becomes formal geometry, vocabulary, representation, and proof.' },
  { source: 'B2', target: 'B3', type: 'concept_handoff', label: 'Definition-to-Operation', summary: 'Defined geometry becomes transformation: what changes, what stays invariant, and what new capability appears.' },
  { source: 'B3', target: 'B4', type: 'concept_handoff', label: 'Operation-to-Mechanism', summary: 'Transformation reveals physical consequence through mechanics, materials, flow, light, or motion.' },
  { source: 'B4', target: 'B5', type: 'concept_handoff', label: 'Mechanism-to-History', summary: 'Mechanism becomes historical deployment across tools, inventions, and scientific problem solving.' },
  { source: 'B5', target: 'B6', type: 'concept_handoff', label: 'History-to-Case Study', summary: 'One timeline invention is expanded into its parts, constraints, science, and functional geometry.' },
  { source: 'B6', target: 'B7', type: 'concept_handoff', label: 'Case Study-to-Prototype', summary: 'The invention logic becomes a student build, test, and iteration activity.' },
  { source: 'B7', target: 'B8', type: 'concept_handoff', label: 'Prototype-to-Synthesis', summary: 'Built function returns to the shared geometry and joins Day A meaning with Day B function.' },

  { source: 'research-system', target: 'writing-system', type: 'supports', label: 'evidence supports writing' },
  { source: 'writing-system', target: 'design-system', type: 'produces', label: 'copy becomes layout' },
  { source: 'image-system', target: 'design-system', type: 'supports', label: 'assets support layout' },
  { source: 'qa-system', target: 'writing-system', type: 'checks', label: 'checks scope and tags' },
  { source: 'qa-system', target: 'design-system', type: 'checks', label: 'checks readiness' },

  { source: 'A3', target: 'research-system', type: 'requires', label: 'museum artifacts' },
  { source: 'A4', target: 'research-system', type: 'requires', label: 'material culture' },
  { source: 'B4', target: 'research-system', type: 'requires', label: 'science mechanism' },
  { source: 'B5', target: 'research-system', type: 'requires', label: 'invention history' },
  { source: 'A1', target: 'writing-system', type: 'produces', label: 'myth script' },
  { source: 'A5', target: 'image-system', type: 'requires', label: 'step images' },
  { source: 'B4', target: 'image-system', type: 'requires', label: 'schematic diagram' },
  { source: 'B8', target: 'design-system', type: 'produces', label: 'synthesis screen' }
];

export const handoffOrder = ['A1','A2','A3','A4','A5','A6','A7','B1','B2','B3','B4','B5','B6','B7','B8'];
