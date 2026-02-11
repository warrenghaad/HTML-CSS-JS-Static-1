# SSOT-009: GE ONTOLOGY + ELEMENT TAXONOMY (Collision-safe)
version: 5.0.0
generated_at: 2026-02-02

## Reserved acronyms (DO NOT REPURPOSE)
- **GEA** = *Geometric Atomic Elements* (your reserved meaning)
- **GEK** = reserved (do not redefine to GEF or anything else)

## Day routing names (avoid collisions)
Use:
- `day.A` + `lens.aesthetic`
- `day.B` + `lens.formal`

## Atomic vs Molecular prefixes (your requested fix)
- Atomic geometric element IDs: `A.GE.<id>`
- Molecular geometric element IDs: `M.GE.<id>`
- If you want “Day A” encoded: use tags `day.A` + `lens.aesthetic` (do not overload GEA)

---

## GE Ontology (source)
# SSOT-009: GEOMETRIC ELEMENT ONTOLOGY

## Purpose

This document defines the complete namespace taxonomy for geometric elements. These namespaces are **REQUIRED** for the curriculum's mycelial research design engine, which graphs geometric complexity across time to find correlations between human developmental phases and civilization efficiency.

---

## ⚠️ CRITICAL: ALL NAMESPACES MUST BE PRESERVED

| Namespace | Full Name | Purpose | Status |
|-----------|-----------|---------|--------|
| **GEA** | Geometric Elements Atomic | Basic primitives | ✅ REQUIRED |
| **GEM** | Geometric Elements Molecular | Composite forms | ✅ REQUIRED |
| **GEK** | Geometric Elements Konceptual | Mathematical/scientific concepts | ✅ REQUIRED |
| **GEU** | Geometric Elements Ubiquitous | Cross-cultural motifs | ✅ REQUIRED |
| **GEOK-T** | Geometric Elements Transformations | Movement-based, science-generating | ✅ REQUIRED |

---

---

## ANTI-COLLISION NOTE: “GEA” IS ATOMIC, NOT “ART”

- **GEA = Geometric Elements Atomic** (primitives).
- Day lenses must not reuse “GEA/GEF” acronyms. Use `day.A/day.B` + `mode.metaphor/mode.function`.

**Accepted aliases for readability:**
- `A.GE.*` → normalize to `gea.*`
- `M.GE.*` → normalize to `gem.*`

## PART 1: GEA — ATOMIC PRIMITIVES

Fundamental geometric forms that cannot be decomposed further.

### 1.1 By Dimension

| Dimension | Elements | Examples |
|-----------|----------|----------|
| **0D** | Point | dot, mark, center |
| **1D** | Line, Ray, Segment | edge, axis, boundary |
| **2D Curved** | Circle, Arc, Spiral, Ellipse | ring, crescent, volute |
| **2D Angular** | Triangle, Square, Rectangle, Polygon, Star | wedge, tablet, octagram |
| **3D** | Sphere, Cylinder, Cone, Pyramid, Prism, Cube | bead, column, ziggurat |

### 1.2 GEA Registry

| GEA Tag | Element | Core Property | Proof Method |
|---------|---------|---------------|--------------|
| `gea.point` | Point | Position only, no dimension | Mark location |
| `gea.line` | Line | Infinite length, no width | Extend in both directions |
| `gea.circle` | Circle | Equidistance from center | Compass construction |
| `gea.arc` | Arc | Continuous curvature | Portion of circle |
| `gea.spiral` | Spiral | Progressive expansion | Trace from center |
| `gea.triangle` | Triangle | 180° angle sum, rigidity | Angle measurement |
| `gea.square` | Square | 4 right angles, equal sides | Grid construction |
| `gea.hexagon` | Hexagon | 120° angles, optimal packing | Tessellation proof |
| `gea.star8` | 8-pointed Star | Radial symmetry order-8 | Count vertices |
| `gea.pyramid` | Pyramid | Convergent stability | Force diagram |

---

## PART 2: GEM — MOLECULAR COMPOSITES

Compound forms created by combining atomic elements.

### 2.1 GEM Registry

| GEM Tag | Composite | Atomic Components | Primary Function |
|---------|-----------|-------------------|------------------|
| `gem.rosette` | Rosette | circle + radial lines | Solar/divine symbols |
| `gem.meander` | Meander | line + right angles | Border patterns, flow |
| `gem.star_polygon` | Star Polygon | circle + triangles | Navigation, divinity |
| `gem.gear` | Gear | circle + triangles | Force transmission |
| `gem.wheel_axle` | Wheel + Axle | circle + square | Motion transfer |
| `gem.truss` | Truss | triangles + squares | Load distribution |
| `gem.helix` | Helix | circle + line (3D) | Lift, storage, DNA |
| `gem.tessellation` | Tessellation | multiple polygons | Infinite coverage |
| `gem.arch` | Arch | arcs + keystone | Load redirection |
| `gem.dome` | Dome | arcs + rotation | Enclosure, heaven |

### 2.2 Composition Notation

Format: `gem.[name](component1+component2, property=value)`

Examples:
- `gem.rosette(circle+line, petals=8)`
- `gem.star_polygon(circle+triangle, points=8)`
- `gem.tessellation(hexagon+triangle, type=semi-regular)`

---

## PART 3: GEK — KONCEPTUAL (Mathematical/Scientific)

Abstract mathematical and scientific concepts expressed through geometry.

### 3.1 Mathematical Concepts

| GEK Tag | Concept | Geometric Expression | Grade Level |
|---------|---------|---------------------|-------------|
| `gek.symmetry.bilateral` | Bilateral Symmetry | Reflection across axis | G3 |
| `gek.symmetry.radial` | Radial Symmetry | Rotation around center | G3-4 |
| `gek.symmetry.translational` | Translational Symmetry | Shift along vector | G4-5 |
| `gek.proportion.golden` | Golden Ratio | φ = 1.618... | G5 |
| `gek.proportion.pi` | Pi | π = 3.14159... | G4-5 |
| `gek.angle.right` | Right Angle | 90° | G3 |
| `gek.angle.sum.triangle` | Triangle Angle Sum | 180° | G4 |
| `gek.area.rectangle` | Area (rectangle) | l × w | G3-4 |
| `gek.volume.prism` | Volume (prism) | B × h | G5 |
| `gek.ratio` | Ratio | a : b | G4 |
| `gek.fraction` | Fraction | Part/Whole | G3-5 |

### 3.2 Scientific Concepts

| GEK Tag | Concept | Geometric Expression | Day B Section |
|---------|---------|---------------------|---------------|
| `gek.force.compression` | Compression | Inward arrows | B3, B4 |
| `gek.force.tension` | Tension | Outward arrows | B3, B4 |
| `gek.force.gravity` | Gravity | Downward vector | B3 |
| `gek.balance.static` | Static Balance | Equal forces | B4 |
| `gek.balance.dynamic` | Dynamic Balance | Rotation equilibrium | B4 |
| `gek.efficiency.packing` | Packing Efficiency | Space minimization | B3 |
| `gek.stability.triangulation` | Triangulation | Rigid structure | B3, B4 |

---

## PART 4: GEU — UBIQUITOUS (Cross-Cultural Motifs)

Geometric patterns that appear independently across 3+ civilizations.

### 4.1 Cross-Cultural Evidence Requirement

A motif qualifies as GEU if it:
1. Appears in **3+ distinct civilizations**
2. Emerged **independently** (no direct transmission)
3. Carries **similar meaning** across cultures

### 4.2 GEU Registry

| GEU Tag | Motif | Civilizations | Shared Meaning |
|---------|-------|---------------|----------------|
| `geu.solar_disk` | Solar Disk | Mesopotamia, Egypt, Greece, China, Mesoamerica, India | Divine light, justice |
| `geu.greek_meander` | Meander/Key | Greece, China, Mesoamerica | Eternal flow, path |
| `geu.celtic_knot` | Interlace | Celtic, Islamic, Viking, Chinese | Continuity, connection |
| `geu.lotus_rosette` | Lotus/Rosette | Egypt, India, Mesopotamia, China | Creation, purity |
| `geu.spiral` | Spiral | Celtic, Polynesian, Native American, Greek | Growth, journey |
| `geu.star8` | 8-pointed Star | Mesopotamia, Islamic, Christian, Buddhist | Divine radiance |
| `geu.swastika` | Hooked Cross | India, Greece, Native American, Buddhist | Solar motion, fortune |
| `geu.mandala` | Concentric Circles | India, Tibet, Navajo, Celtic | Cosmos, wholeness |
| `geu.tree_of_life` | Branching Tree | Mesopotamia, Norse, Kabbalah, Maya | Cosmic axis, life |
| `geu.labyrinth` | Unicursal Path | Crete, India, Scandinavia, Hopi | Journey, initiation |

### 4.3 Evolution Tracking: Motif → Monument → New Motif

| Phase | Description | Example |
|-------|-------------|---------|
| **Motif** | Simple symbol | Cave dots, painted spirals |
| **Monument** | Grand structure using motif | Pyramids, ziggurats, cathedrals |
| **New Motif** | Artistic evolution | Hieroglyphs, rose windows |
| **Next Monument** | New civilization's structure | Renaissance architecture |

---

## PART 5: GEOK-T — TRANSFORMATIONS

**CRITICAL FOR DAY B**: Movement-based operations that generate scientific principles.

### 5.1 Purpose

GEOK-T captures how geometric elements MOVE and what scientific principles emerge from that movement. This is essential for:
- **B3: Decomposition** — Breaking inventions into geometric + transformation components
- **B4: Mathematical Properties** — The science behind the movement
- **B5-B6: STEM activities** — Hands-on manipulation of transformations

### 5.2 GEOK-T Registry

| GEOK-T Tag | Transformation | GE Input | Science Generated |
|------------|----------------|----------|-------------------|
| `geok-t.rotation` | Rotation | Any | Centrifugal force, angular momentum, torque |
| `geok-t.translation` | Translation | Any | Velocity, linear momentum, displacement |
| `geok-t.reflection` | Reflection | Any | Symmetry, bilateral balance, mirror imaging |
| `geok-t.scaling` | Scaling | Any | Proportion, ratio, similarity |
| `geok-t.shearing` | Shearing | Polygon | Stress, deformation, parallelism |
| `geok-t.projection` | Projection | 3D → 2D | Perspective, mapping, shadows |
| `geok-t.revolution` | Revolution | 2D → 3D | Volume generation, lathe principle |
| `geok-t.tessellation` | Tessellation | Polygon | Infinite coverage, packing |
| `geok-t.folding` | Folding | Flat → 3D | Origami, packaging, metamaterials |
| `geok-t.spiraling` | Spiraling | Circle + translation | Screws, DNA, springs |

### 5.3 Transformation → Invention Mapping

| Invention | Primary GEOK-T | GEA/GEM Input | Science Principle |
|-----------|----------------|---------------|-------------------|
| Wheel | `geok-t.rotation` | `gea.circle` | Reduced friction, angular momentum |
| Potter's Wheel | `geok-t.rotation` + `geok-t.revolution` | `gea.circle` | Centrifugal shaping |
| Screw | `geok-t.spiraling` | `gem.helix` | Mechanical advantage, linear force |
| Lever | `geok-t.rotation` (pivot) | `gea.line` | Torque, mechanical advantage |
| Pulley | `geok-t.rotation` + `geok-t.translation` | `gea.circle` + `gea.line` | Force redirection |
| Arch | `geok-t.reflection` | `gea.arc` | Compression transfer |
| Gear Train | `geok-t.rotation` (multiple) | `gem.gear` | Ratio, speed/torque trade |
| Printing Press | `geok-t.rotation` + `geok-t.translation` | `gea.cylinder` | Replication, pressure |
| Astrolabe | `geok-t.rotation` + `geok-t.projection` | `gem.star_polygon` | Celestial mapping |

### 5.4 Day B Section Mapping

| Day B Section | GEOK-T Role |
|---------------|-------------|
| **B3: Decomposition** | Identify which transformations comprise the invention |
| **B4: Mathematical Properties** | Calculate the science generated by transformation |
| **B5: Problem-Solution** | Explain why this transformation solved the problem |
| **B6: Hands-On STEM** | Students physically perform the transformation |

---

## PART 6: DIMENSIONAL PROGRESSION FRAMEWORK

The research design engine tracks geometric complexity across human development:

### 6.1 Developmental Phases

| Phase | Dimension | Examples | Time Period |
|-------|-----------|----------|-------------|
| **1** | 0D-1D Insignia | Notches, tally marks, scratch lines | ~100,000 BCE |
| **2** | 2D Cave Art | Painted circles, spirals, handprints | ~40,000 BCE |
| **3** | 3D Mono/Megaliths | Standing stones, dolmens | ~10,000 BCE |
| **4** | Patterns/Tessellations | Pottery, weaving, basket patterns | ~6,000 BCE |
| **5** | Composite Structures | Ziggurats, pyramids, temples | ~3,000 BCE |
| **6** | Mechanical Compounds | Gears, screws, complex machines | ~500 BCE |

### 6.2 Correlation Hypothesis

The curriculum's research design engine explores:
- How geometric complexity tracks civilization efficiency
- Whether pattern recognition (GEU emergence) predicts innovation
- How transformation mastery (GEOK-T) enables technological leaps

---

## PART 7: TAG SYNTAX

### 7.1 Namespace Prefixes

| Prefix | Namespace | Example |
|--------|-----------|---------|
| `gea.` | Atomic | `gea.circle`, `gea.triangle` |
| `gem.` | Molecular | `gem.rosette`, `gem.truss` |
| `gek.` | Konceptual | `gek.symmetry.radial`, `gek.force.tension` |
| `geu.` | Ubiquitous | `geu.solar_disk`, `geu.celtic_knot` |
| `geok-t.` | Transformation | `geok-t.rotation`, `geok-t.spiraling` |

### 7.2 Combined Tags

An artifact may carry multiple GE tags:

```yaml
tags:
  GEA: [circle, line]
  GEM: [rosette(petals=8)]
  GEK: [symmetry.radial(order=8), proportion.pi]
  GEU: [solar_disk]
  GEOK-T: [rotation]
```

---

## PART 8: INTEGRATION WITH OTHER SSOTs

| SSOT | Integration Point |
|------|-------------------|
| SSOT-002 (Section Rules) | Day B sections B3, B4 require GEOK-T |
| SSOT-003 (Tagging) | GE namespaces registered in `elem.*` hierarchy |
| SSOT-004 (Element Registry) | GEA elements listed with properties |
| SSOT-005 (Deity Registry) | Deity ↔ GE pairings |
| TPL-002 (Artifact Template) | GE fields in YAML |

---

## VERSION HISTORY

| Date | Change | Reason |
|------|--------|--------|
| 2024-12-29 | Created | Preserve all GE namespaces; correct prior DISCARD error |
| 2024-12-29 | Added GEOK-T | User directive: transformations generate Day B science |

---

## Element Taxonomy (source)
# SSOT-009: GEOMETRIC ELEMENT TAXONOMY (GEA/GEM/GEK/GEU)

## ⚠️ EVOLVING TAXONOMY — Research Design Engine

**GE = visual with GEOMETRIC components** (not all visual, only geometric)

**Approach:** Inductive. Catalog civilizations → patterns emerge → terms created. Maximum visibility. No premature optimization.

---

## TAXONOMY

| Code | Scope |
|------|-------|
| **GEA** | Atomic forms (~32 insignia) - inherently cross-cultural |
| **GEM** | Composed patterns (grids, friezes, symmetries) |
| **GEK** | Dimensional operations + math/science concepts |
| **GEU** | Cross-cultural marker for GEM |

---

## GEK: DIMENSIONAL OPERATIONS

From JSON ontology combinatorics:

| Code | Operation | Example |
|------|-----------|---------|
| GEK-1Don2D | 1D on 2D surface | Line drawing on tablet |
| GEK-1Don3D | 1D on 3D surface | Wire wrapped on vessel |
| GEK-2Don2D | 2D on 2D surface | Painted pattern on wall |
| GEK-2Don3D | 2D on 3D surface | Pattern on pottery |
| GEK-2Dto3D | 2D extruded to 3D | Column from circle |
| GEK-3Don2D | 3D projected to 2D | **Painting**, relief, cylinder seal impression |
| GEK-3Dof2D | 3D version of 2D | Dome from circle |

---

## PRESERVED FOR DATA COLLECTION

- All GEA tags kept (research visibility)
- All civilization prefixes kept (pattern discovery)
- Full prefix chains until patterns emerge

---

## VERSION

| Date | Change |
|------|--------|
| 2024-12-29 | GE = geometric visual only. GEK = dimensional ops. Research engine approach. |

---

## GEA: THE 32 ATOMIC INSIGNIA

All civilizations developed these independently:

| # | Element | Dimension | Notes |
|---|---------|-----------|-------|
| 1 | Point | 0D | |
| 2 | Line | 1D | |
| 3 | Angle | 1D | Acute, Right, Obtuse |
| 4 | Circle | 2D | |
| 5 | Arc | 1D | |
| 6 | Spiral | 1D→2D | Archimedean, Logarithmic |
| 7 | Triangle | 2D | Equilateral, Isoceles, Scalene |
| 8 | Square | 2D | |
| 9 | Rectangle | 2D | |
| 10 | Diamond/Rhombus | 2D | |
| 11 | Pentagon | 2D | |
| 12 | Hexagon | 2D | |
| 13 | Octagon | 2D | |
| 14 | Star (generic) | 2D | n-pointed |
| 15 | Cross | 2D | |
| 16 | Crescent | 2D | |
| 17 | Wave/Sine | 1D | |
| 18 | Zigzag | 1D | |
| 19 | Chevron | 2D | |
| 20 | Sphere | 3D | |
| 21 | Cylinder | 3D | |
| 22 | Cone | 3D | |
| 23 | Pyramid | 3D | |
| 24 | Cube | 3D | |
| ... | [to be completed] | | |

**Tag format:** `#GE/A/[element]` or `#GEA.[element]`

---

## GEM: MOLECULAR COMPOSITIONS

Patterns built from GEA. May or may not be cross-cultural.

| Element | Composed Of | Cross-Cultural? |
|---------|-------------|-----------------|
| Grid | Line + Angle | Yes (GEU) |
| Radial_Symmetry | Circle + Division | Yes (GEU) |
| Bilateral_Symmetry | Line + Reflection | Yes (GEU) |
| Frieze | Line + Repeat | Yes (GEU) |
| Meander | Line + Angle + Path | Yes (GEU) |
| Guilloche | Arc + Interlace | Yes (GEU) |
| Tessellation | Polygon + Repeat | Yes (GEU) |
| Rosette_n | Circle + n-division | Yes (GEU) |
| Star_8 | Triangle + Rotation | Yes (GEU) |
| Interlace | Curve + Over-Under | Yes (GEU) |

**Tag format:** `#GE/M/[element]` or `#GEM.[element]`

---

## GEK & GEU: CONTEXT MODIFIERS

**GEK** = Math/science context. Add when discussing principle, not just form.
**GEU** = Cross-cultural marker. Add to GEM when documenting 3+ civ appearance.

```
#GE/M/radial_symmetry          (just the form)
#GE/M/radial_symmetry #GEK     (discussing load distribution math)
#GE/M/radial_symmetry #GEU     (documenting cross-cultural instances)
```

---

## DEITY ↔ SYMBOL RELATIONSHIPS

**Deities are NOT GE's.** But they USE GE's as symbols.

| Deity | Symbol (GE) | Relationship |
|-------|-------------|--------------|
| Shamash | `#GE/M/star_8` + `#GE/A/circle` | uses_symbol |
| Ishtar | `#GE/M/star_8` | uses_symbol |
| Ningishzida | `#GE/A/spiral` + `#GE/M/interlace` | uses_symbol |
| Marduk | `#GE/M/rosette_n` | uses_symbol |
| Sin | `#GE/A/crescent` | uses_symbol |

**In graph terms:**
```
(:Deity {id:"shamash"})-[:USES_SYMBOL]->(:GEM {id:"star_8"})
(:GEM {id:"star_8"})-[:COMPOSED_OF]->(:GEA {id:"triangle"})
```

**In Obsidian:** Use `[[links]]` or YAML `symbol_ge:` property, not merged tags.

---

## TAGGING OPTIONS (For Discussion)

**Option A: Nested tags**
```
#GEA_circle
#GEM Patterns
#GEM-K_radial Symmetry
#GEAK  
#GE/U  (modifier)
```

**Option B: Dot notation**
```
#GEA.circle
#GEM.radial
```

**Option C: YAML properties (Dataview)**
```yaml
ge_type: atomic
ge_element: circle
ge_context: [conceptual]
```

**Recommendation:** Option A or C. Option C most flexible for queries.

---

## OPEN QUESTIONS

1. Complete the 32 GEA list - what's missing?
2. Which GEMs are NOT cross-cultural? (culture-specific compositions)
3. Graph database choice for web app? (Neo4j, Dgraph, or simpler?)

---

## VERSION

| Date | Change |
|------|--------|
| 2024-12-29 | Created. Corrected: GE=visual only, deities separate, GEA inherently ubiquitous |
