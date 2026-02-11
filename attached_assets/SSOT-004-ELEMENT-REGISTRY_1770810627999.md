# SSOT-004: ELEMENT REGISTRY
version: 5.0.0
generated_at: 2026-02-02


## Overview

Master list of all geometric elements used in curriculum.
Each element has: core property, metaphor potential, function potential, deity pairings by civilization.

---

## ELEMENT SCHEMA

```yaml
element:
  id: string           # elem.circle, elem.star8, etc.
  name: string         # Display name
  category: string     # 2D-curved, 2D-angular, 3D, composite
  
  core_property:       # THE defining geometric truth
    name: string
    definition: string
    proof_method: string
    
  metaphor_potential:  # What meanings it CAN carry
    - meaning: string
      why: string      # Why this shape suggests this meaning
      
  function_potential:  # What operations it CAN enable
    - function: string
      why: string      # Why this property enables this function
      
  deity_pairings:      # Which deities pair with this element
    mesopotamia: string
    egypt: string
    greece: string
    # etc.
    
  grade_levels: [3,4,5,6,7,8]  # When introduced/revisited
  
  related_elements: [] # Other elements often combined with this one
```

---

## 2D CURVED ELEMENTS

### CIRCLE

| Field | Value |
|-------|-------|
| **ID** | `elem.circle` |
| **Name** | Circle |
| **Category** | 2D-curved |
| **Grade Levels** | 3, 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Equidistance |
| Definition | All points equal distance from center |
| Proof Method | Measure multiple radii, confirm identical length |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Justice/fairness | Equal distance = equal treatment |
| Eternity/cycles | No beginning or end |
| Wholeness/unity | Unbroken, complete |
| Divine perfection | No imperfection, no corners |
| Protection | Boundary that encloses equally |

**Function Potential:**
| Function | Why |
|----------|-----|
| Rotation | Equidistance maintains constant axle contact |
| Rolling | Every point touches ground at same distance |
| Containment | Maximum area for perimeter |
| Measurement | Pi ratio enables calculations |
| Timekeeping | Uniform rotation = uniform time division |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Shamash | Sun disk, justice |
| Egypt | Ra/Aten | Sun disk, cosmic order |
| Greece | Helios/Apollo | Sun, perfection |
| Rome | Sol Invictus | Unconquered sun |
| Hindu | Sudarshana Chakra | Vishnu's disk weapon |

**Related Elements:** Sphere, spiral, wheel, mandala

---

### SPIRAL

| Field | Value |
|-------|-------|
| **ID** | `elem.spiral` |
| **Name** | Spiral |
| **Category** | 2D-curved |
| **Grade Levels** | 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Progressive expansion |
| Definition | Curve that winds outward from center at increasing distance |
| Proof Method | Measure distance from center at regular angle intervals, confirm growth |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Growth/evolution | Outward movement suggests development |
| Time/cycles | Returns but at new level |
| Journey/descent | Path that goes deeper or higher |
| Life force | Found in living things (shells, plants) |
| Cosmic motion | Galaxies, whirlpools |

**Function Potential:**
| Function | Why |
|----------|-----|
| Compact storage | Long length in small space |
| Force concentration | Tightening increases pressure |
| Efficient drainage | Natural water flow |
| Spring mechanics | Stores/releases energy |
| Growth patterns | Fibonacci efficiency |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Tiamat | Primordial chaos waters |
| Egypt | Wadjet | Cobra coil, protection |
| Greece | Hecate | Labyrinth, mystery |
| Celtic | Brigid | Growth, creativity |
| Hindu | Kundalini | Serpent energy |

**Related Elements:** Circle, volute, scroll, labyrinth

---

### ARC/CURVE

| Field | Value |
|-------|-------|
| **ID** | `elem.arc` |
| **Name** | Arc/Curve |
| **Category** | 2D-curved |
| **Grade Levels** | 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Continuous directional change |
| Definition | Segment of circle; constant curvature between two points |
| Proof Method | Identify center, measure radii to arc points, confirm equal |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Heaven/sky | Dome of heavens |
| Protection/shelter | Covers without crushing |
| Transition | Path between states |
| Blessing | Raised hands form arc |
| Connection | Bridge spans gap |

**Function Potential:**
| Function | Why |
|----------|-----|
| Load distribution | Transfers weight to sides |
| Spanning | Covers distance without center support |
| Structural strength | Compression path |
| Acoustic focus | Reflects sound to point |
| Aesthetic flow | Eye follows curve |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Anu | Sky vault |
| Egypt | Nut | Sky goddess body arched over earth |
| Greece | Iris | Rainbow arc messenger |
| Rome | Janus | Arched doorways |
| Hindu | Indra | Rainbow bow |

**Related Elements:** Circle, dome, vault, bridge, rainbow

---

## 2D ANGULAR ELEMENTS

### TRIANGLE

| Field | Value |
|-------|-------|
| **ID** | `elem.triangle` |
| **Name** | Triangle |
| **Category** | 2D-angular |
| **Grade Levels** | 3, 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Structural rigidity |
| Definition | Three sides create fixed angles; cannot deform without breaking |
| Proof Method | Build triangle from sticks, attempt to shift—cannot |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Stability | Cannot be pushed out of shape |
| Trinity/triads | Three parts unified |
| Hierarchy | Point at top, base at bottom |
| Direction | Points toward something |
| Balance | Three-point stance |

**Function Potential:**
| Function | Why |
|----------|-----|
| Structural support | Rigid under load |
| Measurement | Triangulation locates position |
| Force direction | Ramps, wedges |
| Sail shape | Catches wind efficiently |
| Roof pitch | Sheds water/snow |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Enlil/Anu/Ea | Divine triad |
| Egypt | Osiris/Isis/Horus | Family triad, pyramid |
| Greece | Zeus/Poseidon/Hades | Realm triad |
| Hindu | Brahma/Vishnu/Shiva | Trimurti |
| Christian | Trinity | Three-in-one |

**Related Elements:** Pyramid, truss, arrow, delta

---

### SQUARE/RECTANGLE

| Field | Value |
|-------|-------|
| **ID** | `elem.square` |
| **Name** | Square/Rectangle |
| **Category** | 2D-angular |
| **Grade Levels** | 3, 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Right-angle regularity |
| Definition | Four sides with 90° corners; opposite sides parallel and equal |
| Proof Method | Measure angles (90°), measure opposite sides (equal) |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Order/civilization | Human-made, not natural |
| Earth/material world | Four directions, four elements |
| Honesty | "Square deal," nothing hidden |
| Stability | Solid base |
| Boundaries | Property, territory |

**Function Potential:**
| Function | Why |
|----------|-----|
| Tessellation | Tiles without gaps |
| Construction | Stacks, aligns |
| Measurement | Standard units |
| Organization | Grid systems |
| Writing | Text blocks, tablets |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Nabu | Writing tablets, wisdom |
| Egypt | Geb | Earth god, land |
| Greece | Hestia | Hearth, home foundations |
| Rome | Terminus | Boundary stones |
| China | Earth element | Square earth under round heaven |

**Related Elements:** Cube, grid, frame, tablet

---

### 8-POINTED STAR

| Field | Value |
|-------|-------|
| **ID** | `elem.star8` |
| **Name** | 8-Pointed Star |
| **Category** | 2D-angular |
| **Grade Levels** | 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Radial symmetry (8-fold) |
| Definition | 8 equal angles (45°) from center; rotational symmetry at 45° intervals |
| Proof Method | Measure angles between rays, confirm 45° each (360° ÷ 8) |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Divine radiance | Light emanating in all directions |
| Protection | Coverage from all angles |
| Celestial bodies | Stars, Venus |
| Completion | All directions covered |
| Guidance | Points the way |

**Function Potential:**
| Function | Why |
|----------|-----|
| Directional orientation | 8 points = cardinal + intercardinal |
| Navigation | Compass divisions |
| Pattern creation | Rotational tiling |
| Time division | 8 watches, 8 festivals |
| Signal visibility | Recognizable from any angle |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Mesopotamia | Ishtar/Inanna | Venus star, love/war |
| Egypt | Seshat | Measurement, 7-pointed variant |
| Islam | Rub el Hizb | Quranic division marker |
| Buddhism | Dharma wheel | 8-fold path |
| Lakota | Morning Star | Venus, renewal |

**Related Elements:** Compass rose, octagon, rosette, mandala

---

### HEXAGON

| Field | Value |
|-------|-------|
| **ID** | `elem.hexagon` |
| **Name** | Hexagon |
| **Category** | 2D-angular |
| **Grade Levels** | 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Optimal packing |
| Definition | 6 equal sides, 120° angles; tessellates with no gaps |
| Proof Method | Tile hexagons, observe complete coverage; measure angles |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Natural wisdom | Bees "know" this shape |
| Efficiency | Maximum use of space |
| Community | Cells connect to neighbors |
| Harmony | Balanced, stable |
| Divine geometry | Perfect natural form |

**Function Potential:**
| Function | Why |
|----------|-----|
| Space efficiency | Most area per perimeter in tiling |
| Structural strength | Distributes load to 6 neighbors |
| Material efficiency | Minimum material for maximum space |
| Growth patterns | Crystalline structures |
| Mapping | Hex grids for games/strategy |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Egypt | Neith | Weaving, creation |
| Greece | Artemis | Bees sacred to her |
| Hindu | Anahata | Heart chakra symbol |
| Various | Bee goddesses | Honeycomb |

**Related Elements:** Honeycomb, snowflake, benzene ring, Star of David (hexagram)

---

### PENTAGON

| Field | Value |
|-------|-------|
| **ID** | `elem.pentagon` |
| **Name** | Pentagon |
| **Category** | 2D-angular |
| **Grade Levels** | 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Golden ratio relationship |
| Definition | 5 equal sides; diagonals create φ (phi) proportions |
| Proof Method | Measure diagonal ÷ side, find ≈ 1.618 |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Life/organic | 5-fold symmetry in living things (starfish, flowers) |
| Human form | 5 extremities |
| Health/protection | Pentagram associations |
| Mystery | Does not tessellate simply |
| Perfection | Golden ratio |

**Function Potential:**
| Function | Why |
|----------|-----|
| Aesthetic proportion | Phi ratio pleases eye |
| Security | Harder to breach (US Pentagon) |
| Biological growth | Flower patterns |
| Recognition | Distinctive, memorable |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Greece | Aphrodite | Apple star (5-pointed) |
| Babylon | Ishtar | 5-pointed Venus path |
| Pythagorean | Hygieia | Health symbol |
| Wicca | Goddess | Pentacle |

**Related Elements:** Pentagram, star, apple cross-section, starfish

---

## 3D ELEMENTS

### SPHERE

| Field | Value |
|-------|-------|
| **ID** | `elem.sphere` |
| **Name** | Sphere |
| **Category** | 3D |
| **Grade Levels** | 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | 3D equidistance |
| Definition | All surface points equal distance from center |
| Proof Method | Measure from center to multiple surface points |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Cosmos | Celestial sphere, planets |
| Perfection | No preferred direction |
| Totality | Contains all directions |
| Soul | Complete, contained |

**Function Potential:**
| Function | Why |
|----------|-----|
| Rolling (any direction) | Equidistance in 3D |
| Minimal surface | Least area for volume |
| Even pressure | Equal in all directions |
| Astronomical modeling | Celestial mechanics |

**Related Elements:** Circle, dome, ball, globe, bubble

---

### PYRAMID

| Field | Value |
|-------|-------|
| **ID** | `elem.pyramid` |
| **Name** | Pyramid |
| **Category** | 3D |
| **Grade Levels** | 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Convergent stability |
| Definition | Polygonal base with triangular faces meeting at apex |
| Proof Method | Identify base shape, count triangular faces, locate apex |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Ascension | Points upward to heaven |
| Hierarchy | Base supports apex |
| Eternity | Stable, enduring |
| Sun rays | Descending light |
| Power concentration | Many support one |

**Function Potential:**
| Function | Why |
|----------|-----|
| Structural stability | Wide base, low center of gravity |
| Weight distribution | Mass flows to base |
| Monumental presence | Visible from distance |
| Astronomical alignment | Precise orientation possible |

**Deity Pairings:**
| Civilization | Deity | Domain Connection |
|--------------|-------|-------------------|
| Egypt | Ra/Osiris | Sun rays, resurrection |
| Mesopotamia | Ziggurat temples | Mountain of the gods |
| Maya | Kukulcan | Temple pyramids |

**Related Elements:** Triangle, tetrahedron, ziggurat, obelisk

---

### CUBE

| Field | Value |
|-------|-------|
| **ID** | `elem.cube` |
| **Name** | Cube |
| **Category** | 3D |
| **Grade Levels** | 4, 5, 6, 7, 8 |

**Core Property:**
| Field | Value |
|-------|-------|
| Name | Uniform 3D regularity |
| Definition | 6 equal square faces, 12 equal edges, 8 vertices, all 90° |
| Proof Method | Measure all edges (equal), all angles (90°) |

**Metaphor Potential:**
| Meaning | Why |
|---------|-----|
| Earth/material | Solid, grounded |
| Stability | Sits flat on any face |
| Truth | "Squared," honest |
| Foundation | Building block |

**Function Potential:**
| Function | Why |
|----------|-----|
| Stacking | Flat faces align |
| Space filling | Tessellates in 3D |
| Standardization | Unit of measure |
| Dice/randomness | Equal probability faces |

**Related Elements:** Square, box, brick, die

---

## ELEMENT QUICK REFERENCE

| ID | Name | Core Property | Key Metaphor | Key Function |
|----|------|---------------|--------------|--------------|
| elem.circle | Circle | Equidistance | Justice | Rotation |
| elem.spiral | Spiral | Progressive expansion | Growth | Storage |
| elem.arc | Arc/Curve | Continuous curvature | Heaven | Load distribution |
| elem.triangle | Triangle | Structural rigidity | Stability | Support |
| elem.square | Square | Right-angle regularity | Order | Tessellation |
| elem.star8 | 8-pointed Star | Radial symmetry | Divine radiance | Navigation |
| elem.hexagon | Hexagon | Optimal packing | Natural wisdom | Efficiency |
| elem.pentagon | Pentagon | Golden ratio | Life/organic | Aesthetic proportion |
| elem.sphere | Sphere | 3D equidistance | Cosmos | Rolling |
| elem.pyramid | Pyramid | Convergent stability | Ascension | Weight distribution |
| elem.cube | Cube | Uniform regularity | Earth | Stacking |

---

## MESOPOTAMIA PILOT ELEMENT SEQUENCE

| Week | Element | Deity | Core Property |
|------|---------|-------|---------------|
| 1 | Circle | Shamash | Equidistance |
| 2 | 8-pointed Star | Ishtar | Radial symmetry |
| 3 | Triangle | Enlil | Structural rigidity |
| 4 | Square | Nabu | Right-angle regularity |
| 5 | Spiral | Tiamat | Progressive expansion |
| 6 | Arc | Anu | Continuous curvature |
| 7 | Hexagon | Nisaba | Optimal packing |
| 8 | Pyramid | Marduk | Convergent stability |