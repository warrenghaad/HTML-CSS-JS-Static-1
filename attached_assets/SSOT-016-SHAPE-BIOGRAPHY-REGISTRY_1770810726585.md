# SSOT-016: SHAPE BIOGRAPHY REGISTRY
version: 5.0.0
generated_at: 2026-02-02

# SSOT-016: SHAPE BIOGRAPHY REGISTRY

## Overview

The Shape Biography Registry is the **canonical spine** for curriculum generation. Each geometric element has a biography that:
1. Defines its core properties and scientific effects
2. Maps to Mesopotamian history and artifact evidence
3. Connects to the RWI (Research-Writing-Image) system
4. Integrates with the tagging ontology (SSOT-003)
5. Provides image requirements for each slot
6. Links to graph node structure for lesson routing

---

## SCHEMA VERSION

```yaml
schema_version: SB_CANON_V1
```

---

## SLOT STRUCTURE (DAY A ↔ DAY B PARALLEL)

Each Shape Biography has **8 canonical slots** that map to Day A (Metaphor) and Day B (Function):

| Slot | Label | Day A Focus (Lens A) | Day B Focus (Lens B) |
|------|-------|---------------------|---------------------|
| 1 | Establish meaning vs structure | MYTHIC_ORIGIN | INVENTION_MECHANISM |
| 2 | Visualize element vs visualize math | ICONOGRAPHY | MATH_PROPERTIES |
| 3 | Artifact in world vs GEK-T in world | MATERIAL_CULTURE | TRANSFORMATION |
| 4 | Material culture ritual vs STEM history | RITUAL_PRACTICE | STEM_HISTORY |
| 5 | Decomposition vs Invention | SEMIOTICS | INVENTION_CAUSATION |
| 6 | Art activity vs Decomposition analysis | ART_ACTIVITY | ENGINEERING_ACTIVITY |
| 7 | Symbolic rendering vs Design challenge | SYMBOLIC_RENDERING | DESIGN_CHALLENGE |
| 8 | Wrap-up / nutshell | SEL_SYNTHESIS | FUNCTION_SYNTHESIS |

---

## PLATE STRUCTURE

Each slot contains **plates** - paired content units for Day A and Day B:

```yaml
plate:
  plate_id: string           # P01, P02, etc.
  plate_type: string         # MYTHIC_ORIGIN, INVENTION_MECHANISM, etc.
  lens: string               # "A" (metaphor) or "B" (function) — DO NOT confuse with GEA (atomic)
  title: string              # Display title
  caption_student: string    # Student-facing caption (max 140 chars)
  teacher_bullets: []        # Teacher guidance points (max 8)

  tags:
    domain: string           # GEpHR, GEK, etc. (from SSOT-009)
    carriers: []             # CARR__[artifact_type]
    inventions: []           # INV__[invention_name]

  image_requirement:
    role: string             # CONTEXT_VISUAL, MECHANISM_VISUAL, etc.
    preferred_types: []      # illustration, artifact_photo, diagram
    source_priority: []      # museum_catalog, reconstruction, ai_generated
    ai_allowed: boolean
    must_include: []         # Required visual elements
    must_not_include: []     # Forbidden visual elements
```

---

## CIV PACKS & GLOBAL SCALING

This registry defines the **Shape Biography** schema. Individual biographies should live in civilization packs:
- `civ_pack/mesopotamia/...` (example)
- `civ_pack/egypt/...`
- `civ_pack/china/...`

**Required fields for global scale:** `civ_id`, `period_id`, `site_id`.

---

## ELEMENT REGISTRY

### 1. CIRCLE / SPHERE

```yaml
shape_bio_id: SB_MESO_CIRCLE_V1
ge_id: GE_A_CIRCLE
element_name: Circle
category: 2D-curved

core_property:
  name: Equidistance
  definition: All points equal distance from center
  proof_method: Measure multiple radii, confirm identical length

scientific_effects:
  - Infinite rotational symmetry
  - Even force distribution
  - Angular momentum conservation
  - Uniform pressure in vessels

deity_pairing:
  primary: Shamash
  domain: Sun, Justice, Truth
  symbol: Sun Disk with rays

mesopotamian_evidence:
  artifacts:
    - name: Potter's wheel
      period: Uruk (~3500 BCE)
      location: Uruk
      museum: British Museum, Louvre

    - name: Wheeled carts/chariots
      period: Early Dynastic (~2600 BCE)
      location: Ur (Royal Tombs)
      museum: British Museum (Standard of Ur)

    - name: Cylinder seals
      period: All periods
      location: Various
      museum: Multiple

    - name: Tablet of Shamash
      period: Neo-Babylonian
      location: Sippar
      museum: British Museum (BM 91000)

inventions:
  - INV__POTTER_WHEEL
  - INV__WHEEL_AND_AXLE
  - INV__CYLINDER_SEAL
  - INV__CIRCULAR_WELL

carriers:
  - CARR__SUN_DISK
  - CARR__WHEEL
  - CARR__AXLE
  - CARR__SEAL

tagging:
  gea: gea.circle
  gem: gem.rosette, gem.wheel_axle
  gek: gek.symmetry.radial
  geu: geu.solar_disk
  geok_t: geok-t.rotation
  deity: deity.meso.shamash
  elem: elem.circle
```

---

### 2. 8-POINTED STAR

```yaml
shape_bio_id: SB_MESO_STAR8_V1
ge_id: GE_A_STAR8
element_name: 8-Pointed Star
category: 2D-angular

core_property:
  name: Radial symmetry (8-fold)
  definition: 8 equal angles (45°) from center
  proof_method: Measure angles between rays, confirm 45° each

scientific_effects:
  - Balanced directional coverage
  - Consistent angular marking
  - Resonance patterns
  - Visual periodicity

deity_pairing:
  primary: Ishtar/Inanna
  domain: Love, War, Venus
  symbol: 8-pointed star (Venus marker)

mesopotamian_evidence:
  artifacts:
    - name: Ishtar Gate
      period: Neo-Babylonian (~575 BCE)
      location: Babylon
      museum: Pergamon Museum, Berlin

    - name: Star symbols on seals
      period: All periods
      location: Various
      museum: Multiple

    - name: Kudurru boundary stones
      period: Kassite/Neo-Babylonian
      location: Various
      museum: British Museum, Louvre

inventions:
  - INV__COMPASS_ROSE
  - INV__ASTRONOMICAL_OBSERVATION
  - INV__DIRECTIONAL_MARKER

carriers:
  - CARR__ISHTAR_STAR
  - CARR__VENUS_SYMBOL
  - CARR__GATE_DECORATION

tagging:
  gea: gea.star8
  gem: gem.star_polygon, gem.rosette_n
  gek: gek.symmetry.radial
  geu: geu.star8
  geok_t: geok-t.rotation, geok-t.projection
  deity: deity.meso.ishtar
  elem: elem.star8
```

---

### 3. CRESCENT / ARC

```yaml
shape_bio_id: SB_MESO_CRESCENT_V1
ge_id: GE_A_ARC
element_name: Crescent / Arc
category: 2D-curved

core_property:
  name: Continuous directional change
  definition: Segment of circle; constant curvature between two points
  proof_method: Identify center, measure radii to arc points

scientific_effects:
  - Phase modeling
  - Angular measurement (chord, arc, sagitta)
  - Periodic timekeeping
  - Celestial path tracking

deity_pairing:
  primary: Sin/Nanna
  domain: Moon, Time, Calendars
  symbol: Crescent moon (horizontal, boat-like)

mesopotamian_evidence:
  artifacts:
    - name: Lunar calendars (MUL.APIN)
      period: Old Babylonian onward
      location: Various
      museum: British Museum

    - name: Ur-Nammu stele
      period: Ur III (~2100 BCE)
      location: Ur
      museum: Penn Museum

    - name: Crescent standards
      period: All periods
      location: Various
      museum: Multiple

inventions:
  - INV__LUNAR_CALENDAR
  - INV__ECLIPSE_PREDICTION
  - INV__GNOMON_SHADOW_CLOCK

carriers:
  - CARR__CRESCENT_MOON
  - CARR__LUNAR_BOAT
  - CARR__STANDARD_TOP

tagging:
  gea: gea.arc
  gem: gem.arch
  gek: gek.angle.sum.triangle
  geu: geu.solar_disk (related)
  geok_t: geok-t.rotation
  deity: deity.meso.nanna
  elem: elem.arc
```

---

### 4. TRIANGLE

```yaml
shape_bio_id: SB_MESO_TRIANGLE_V1
ge_id: GE_A_TRIANGLE
element_name: Triangle
category: 2D-angular

core_property:
  name: Structural rigidity
  definition: Three sides create fixed angles; cannot deform without breaking
  proof_method: Build triangle from sticks, attempt to shift—cannot

scientific_effects:
  - Inherent rigidity
  - 180° angle sum
  - Pythagorean relationships
  - Triangulation for measurement

deity_pairing:
  primary: Enlil
  domain: Air, Authority, Divine Triad
  symbol: Divine triad (Enlil/Anu/Ea)

mesopotamian_evidence:
  artifacts:
    - name: Ziggurat steps
      period: All periods (~2100 BCE onward)
      location: Ur, Babylon, Borsippa
      museum: In situ, British Museum

    - name: Plimpton 322 tablet
      period: Old Babylonian (~1800 BCE)
      location: Larsa area
      museum: Columbia University

    - name: Surveying records
      period: Ur III onward
      location: Various
      museum: Multiple

inventions:
  - INV__ZIGGURAT_CONSTRUCTION
  - INV__SURVEYING_TRIANGULATION
  - INV__PYTHAGOREAN_CALCULATION

carriers:
  - CARR__ZIGGURAT_PROFILE
  - CARR__RAMP
  - CARR__TERRACE

tagging:
  gea: gea.triangle
  gem: gem.truss
  gek: gek.angle.sum.triangle, gek.stability.triangulation
  geu: (none specific)
  geok_t: geok-t.scaling
  deity: deity.meso.enlil
  elem: elem.triangle
```

---

### 5. SQUARE / RECTANGLE

```yaml
shape_bio_id: SB_MESO_SQUARE_V1
ge_id: GE_A_SQUARE
element_name: Square / Rectangle
category: 2D-angular

core_property:
  name: Right-angle regularity
  definition: Four sides with 90° corners; opposite sides parallel and equal
  proof_method: Measure angles (90°), measure opposite sides (equal)

scientific_effects:
  - Consistent area calculation
  - Orthogonal axis system
  - Efficient tiling/packing
  - Proportional design

deity_pairing:
  primary: Nabu
  domain: Writing, Wisdom, Scribes
  symbol: Writing tablet, stylus

mesopotamian_evidence:
  artifacts:
    - name: Cuneiform tablets
      period: All periods (~3200 BCE onward)
      location: Various
      museum: Multiple (tens of thousands)

    - name: Standardized bricks
      period: All periods
      location: Various
      museum: In situ, British Museum

    - name: City grid plans
      period: Various
      location: Babylon, Ur, Uruk
      museum: Archaeological records

inventions:
  - INV__CUNEIFORM_TABLET
  - INV__STANDARDIZED_BRICK
  - INV__CITY_GRID_PLANNING

carriers:
  - CARR__TABLET
  - CARR__BRICK
  - CARR__FIELD_PLOT

tagging:
  gea: gea.square
  gem: gem.grid
  gek: gek.area.rectangle
  geu: (none specific)
  geok_t: geok-t.tessellation
  deity: deity.meso.nabu
  elem: elem.square
```

---

### 6. SPIRAL

```yaml
shape_bio_id: SB_MESO_SPIRAL_V1
ge_id: GE_A_SPIRAL
element_name: Spiral
category: 2D-curved

core_property:
  name: Progressive expansion
  definition: Curve that winds outward from center at increasing distance
  proof_method: Measure distance from center at regular angle intervals

scientific_effects:
  - Constant tangent angle
  - Efficient flow distribution
  - Natural scaling patterns
  - Compact path coverage

deity_pairing:
  primary: Tiamat
  domain: Primordial chaos, Salt water
  symbol: Coiling serpent/dragon

mesopotamian_evidence:
  artifacts:
    - name: Spiral pottery motifs
      period: Ubaid (~5000 BCE) onward
      location: Various
      museum: Multiple

    - name: Coiled baskets
      period: All periods
      location: Various
      museum: Archaeological evidence

    - name: Spiral jewelry
      period: Royal Tombs (~2600 BCE)
      location: Ur
      museum: British Museum, Penn Museum

inventions:
  - INV__COILED_CONSTRUCTION
  - INV__SPIRAL_CHANNEL

carriers:
  - CARR__SERPENT_COIL
  - CARR__BASKET
  - CARR__JEWELRY

tagging:
  gea: gea.spiral
  gem: gem.helix
  gek: (none specific)
  geu: geu.spiral
  geok_t: geok-t.spiraling
  deity: deity.meso.tiamat
  elem: elem.spiral
```

---

### 7. HEXAGON

```yaml
shape_bio_id: SB_MESO_HEXAGON_V1
ge_id: GE_A_HEXAGON
element_name: Hexagon
category: 2D-angular

core_property:
  name: Optimal packing
  definition: 6 equal sides, 120° angles; tessellates with no gaps
  proof_method: Tile hexagons, observe complete coverage

scientific_effects:
  - Maximum area per perimeter in tiling
  - Load distribution to 6 neighbors
  - Minimum material for maximum space
  - Crystalline growth patterns

deity_pairing:
  primary: Nisaba
  domain: Grain, Writing, Surveying
  symbol: Grain stalk, hexagonal efficiency

mesopotamian_evidence:
  artifacts:
    - name: Grain storage calculations
      period: Ur III onward
      location: Various
      museum: Multiple

    - name: Field surveying tablets
      period: All periods
      location: Various
      museum: Multiple

inventions:
  - INV__EFFICIENT_STORAGE
  - INV__FIELD_SURVEYING

carriers:
  - CARR__GRAIN_MOTIF
  - CARR__HONEYCOMB_PATTERN

tagging:
  gea: gea.hexagon
  gem: gem.tessellation
  gek: gek.efficiency.packing
  geu: (none specific)
  geok_t: geok-t.tessellation
  deity: deity.meso.nisaba
  elem: elem.hexagon
```

---

### 8. PYRAMID / ZIGGURAT

```yaml
shape_bio_id: SB_MESO_PYRAMID_V1
ge_id: GE_A_PYRAMID
element_name: Pyramid / Ziggurat
category: 3D

core_property:
  name: Convergent stability
  definition: Polygonal base with triangular faces meeting at apex
  proof_method: Identify base shape, count triangular faces, locate apex

scientific_effects:
  - Wide base stability
  - Stepped energy dissipation
  - Drainage control
  - Accessible height

deity_pairing:
  primary: Marduk
  domain: Creation, Babylon, Sovereignty
  symbol: Ziggurat temple

mesopotamian_evidence:
  artifacts:
    - name: Great Ziggurat of Ur
      period: Ur III (~2100 BCE)
      location: Ur
      museum: In situ (partially reconstructed)

    - name: Etemenanki
      period: Neo-Babylonian
      location: Babylon
      museum: Archaeological remains

    - name: Ziggurat of Aqar Quf
      period: Kassite
      location: Near Baghdad
      museum: In situ

inventions:
  - INV__ZIGGURAT_TEMPLE
  - INV__STEPPED_DRAINAGE
  - INV__AGRICULTURAL_TERRACE

carriers:
  - CARR__ZIGGURAT
  - CARR__STEPPED_PLATFORM
  - CARR__TEMPLE_TOWER

tagging:
  gea: gea.pyramid
  gem: gem.truss
  gek: gek.stability.triangulation
  geu: (none specific)
  geok_t: geok-t.scaling
  deity: deity.meso.marduk
  elem: elem.pyramid
```

---

## RWI INTEGRATION

Each Shape Biography connects to the RWI (Research-Writing-Image) system:

### Research Layer
```yaml
research:
  primary_sources:
    - museum_catalogs: [British Museum, Louvre, Penn, Met, Yale]
    - archaeological_reports: []
    - cuneiform_translations: []

  secondary_sources:
    - academic_papers: []
    - textbooks: []

  evidence_requirements:
    - artifact_citation: required
    - period_verification: required
    - location_confirmation: required
```

### Writing Layer
```yaml
writing:
  student_caption:
    max_chars: 140
    tone: wonder, discovery
    avoid: technical jargon, math in Day A

  teacher_bullets:
    max_count: 8
    format: actionable guidance

  LO_template:
    day_a: "[Element] originates as [deity]'s [attribute] because [story] solved [problem]"
    day_b: "[Finding] confirms [property] because [rule] defines it"
```

### Image Layer
```yaml
image:
  acquisition_modes:
    MUSEUM_SEARCH: artifacts, historical objects
    STORYBOARD: myth scenes, deity depictions (AI or artist)
    DIAGRAM: math concepts, transformations (generated to spec)
    OVERLAY: element analysis on artifacts
    PROCESS: activity steps, materials

  source_priority:
    1: museum_catalog
    2: reconstruction
    3: ai_generated

  requirements_per_slot:
    slot_1: 2 plates (mythic + mechanism visuals)
    slot_2: 2 plates (iconography + math diagrams)
    # ... etc
```

---

## GRAPH NODE INTEGRATION

Each Shape Biography maps to the lesson graph structure:

```yaml
graph_node:
  node_type: SHAPE_BIOGRAPHY
  node_id: SB_[CIVILIZATION]_[ELEMENT]_V[version]

  connections:
    upstream:
      - CIVILIZATION_NODE
      - PERIOD_NODE

    downstream:
      - LESSON_WEEK_NODE
      - SECTION_NODE (A1-A7, B1-B8)

    lateral:
      - OTHER_SHAPE_BIO (related elements)
      - DEITY_NODE
      - ARTIFACT_NODE

  routing:
    week_assignment: [1-8]
    grade_band: [3-5, 6-8]
    day_a_sections: [A1, A2, A3, A4a-f, A5, A6, A7]
    day_b_sections: [B1, B2, B3, B4, B5, B6, B7, B8]
```

---

## PILOT CURRICULUM SEQUENCE

For the Mesopotamia Pilot (Grades 3-5, 48 lessons):

| Week | Element | Deity | Shape Bio ID |
|------|---------|-------|--------------|
| 1 | Circle | Shamash | SB_MESO_CIRCLE_V1 |
| 2 | 8-pointed Star | Ishtar | SB_MESO_STAR8_V1 |
| 3 | Triangle | Enlil | SB_MESO_TRIANGLE_V1 |
| 4 | Square | Nabu | SB_MESO_SQUARE_V1 |
| 5 | Spiral | Tiamat | SB_MESO_SPIRAL_V1 |
| 6 | Arc | Anu | SB_MESO_CRESCENT_V1 |
| 7 | Hexagon | Nisaba | SB_MESO_HEXAGON_V1 |
| 8 | Pyramid | Marduk | SB_MESO_PYRAMID_V1 |

**Note:** Week 2 has a known contradiction:
- HANDOFF_MASTER says: Week 2 = Sin/Nanna + Crescent
- SSOT-004 says: Week 2 = Ishtar + 8-Star

**Resolution:** Follow SSOT-004 sequence for now. Sin/Nanna + Crescent can be Week 6 (Arc).

---

## EXPORT DEFAULTS

```yaml
export:
  presentation:
    slide_one_image_rule: true
    caption_max_chars: 140
    teacher_bullets_max: 8

  html_lesson:
    section_template: SSOT-002
    tagging: SSOT-003

  json_manifest:
    include_tags: true
    include_image_requirements: true
```

---

## GOVERNANCE

```yaml
governance:
  frozen: false
  created_at: 2026-01-22
  author: system

  validation_rules:
    - Each element must have deity_pairing
    - Each element must have ≥2 artifact citations
    - Each element must have ≥1 invention
    - All tags must match SSOT-003 registry

  update_protocol:
    - Changes require SSOT version increment
    - Contradictions logged in SEMANTIC_MANIFEST
```

---

## VERSION HISTORY

| Date | Change | Author |
|------|--------|--------|
| 2026-01-22 | Created from SHAPE BIOGRAPHY.md + user JSON schema | System |

---

**END SSOT-016**