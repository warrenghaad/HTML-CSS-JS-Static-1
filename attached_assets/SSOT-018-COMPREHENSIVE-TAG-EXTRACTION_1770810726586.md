# SSOT-018: COMPREHENSIVE TAG EXTRACTION
version: 5.0.0
generated_at: 2026-02-02

# SSOT-018: COMPREHENSIVE TAG EXTRACTION

## Purpose

This document extracts and catalogs **EVERY taggable entity** from the Shape Biography and related curriculum materials. It serves as the complete reference for what must be tagged in the graph node system.

---

## TAG NAMESPACE HIERARCHY

```
CANON_TAG_ROOT
├── GE (Geometric Elements)
│   ├── GEA (Atomic)
│   ├── GEM (Molecular)
│   ├── GEK (Conceptual/Mathematical)
│   ├── GEU (Ubiquitous/Cross-cultural)
│   └── GEOK-T (Transformations)
│
├── HIST (Historical)
│   ├── CIV (Civilizations)
│   ├── PERIOD (Time Periods)
│   ├── RULER (Kings/Rulers)
│   ├── DYNASTY (Dynasties)
│   └── EVENT (Historical Events)
│
├── GEO (Geographic)
│   ├── CITY (Cities/Sites)
│   ├── REGION (Regions)
│   ├── RIVER (Rivers)
│   └── TEMPLE (Temple Complexes)
│
├── ART (Artifacts)
│   ├── TYPE (Artifact Types)
│   ├── MATERIAL (Materials)
│   ├── TECHNIQUE (Production Techniques)
│   └── MUSEUM (Museum Collections)
│
├── INV (Inventions)
│   ├── MECH (Mechanical)
│   ├── ARCH (Architectural)
│   ├── ADMIN (Administrative)
│   └── ASTRO (Astronomical)
│
├── DEITY (Divine Figures)
│   ├── MESO (Mesopotamian)


> **MULTI-CIV NOTE:** Deity tags are scoped by civilization: `deity.<civ>.<name>`. Mesopotamia is only one civ pack example.
│   ├── EGYPT (Egyptian)
│   └── GREECE (Greek)
│
├── SCI (Scientific Concepts)
│   ├── PHYS (Physics)
│   ├── MATH (Mathematics)
│   ├── ASTRO (Astronomy)
│   └── ENG (Engineering)
│
├── IMG (Image System)
│   ├── TYPE (Image Types)
│   ├── ROLE (Image Roles)
│   ├── SRC (Sources)
│   └── STATUS (Production Status)
│
└── CURR (Curriculum)
    ├── SSOT (Section Codes)
    ├── GRADE (Grade Levels)
    ├── WEEK (Week Numbers)
    └── DAY (Day A/B)
```

---

## COMPLETE EXTRACTION FROM SHAPE BIOGRAPHY

### 1. GEOMETRIC ELEMENTS (GE)

#### GEA - Atomic Elements
```yaml
gea_atomic:
  2d_curved:
    - tag: gea.circle
      mentioned_in: "Circle / Sphere section"
      description: "Constant radius from center"

    - tag: gea.arc
      mentioned_in: "Crescent / Arcs section"
      description: "Segment of circle, constant curvature"

    - tag: gea.spiral
      mentioned_in: "Spirals section"
      description: "Curve winding outward from center"

    - tag: gea.ellipse
      mentioned_in: "Ellipses section"
      description: "Constant sum of distances to foci"

  2d_angular:
    - tag: gea.triangle
      mentioned_in: "Triangle section"
      description: "Three-sided polygon, inherently rigid"

    - tag: gea.square
      mentioned_in: "Rectangle / Square section"
      description: "Four equal sides, 90° corners"

    - tag: gea.rectangle
      mentioned_in: "Rectangle / Square section"
      description: "Four right angles, parallel sides"

    - tag: gea.hexagon
      mentioned_in: "Tessellations section"
      description: "Six equal sides, 120° angles"

    - tag: gea.star8
      mentioned_in: "Radial Stars section"
      description: "8-pointed star, 45° angles"

    - tag: gea.chevron
      mentioned_in: "Waves / Chevrons section"
      description: "V-shaped pattern"

  3d:
    - tag: gea.sphere
      mentioned_in: "Circle / Sphere section"
      description: "3D extension of circle"

    - tag: gea.pyramid
      mentioned_in: "Stepped Pyramids / Ziggurats section"
      description: "Polygonal base, triangular faces"

    - tag: gea.cylinder
      mentioned_in: "Circle / Sphere section"
      description: "Circle extruded along axis"
```

#### GEM - Molecular Composites
```yaml
gem_molecular:
  - tag: gem.rosette
    components: [circle, radial_lines]
    mentioned_in: "Radial Stars section"

  - tag: gem.wheel_axle
    components: [circle, cylinder]
    mentioned_in: "Circle / Sphere section - Wheel and axle"

  - tag: gem.grid
    components: [lines, right_angles]
    mentioned_in: "Grids section"

  - tag: gem.tessellation
    components: [multiple_polygons]
    mentioned_in: "Tessellations section"

  - tag: gem.ziggurat
    components: [rectangles, triangular_profile]
    mentioned_in: "Stepped Pyramids / Ziggurats section"

  - tag: gem.arch
    components: [arc, keystone]
    mentioned_in: "Crescent / Arcs section"

  - tag: gem.truss
    components: [triangles]
    mentioned_in: "Triangle section"

  - tag: gem.helix
    components: [circle, spiral, 3d_path]
    mentioned_in: "Spirals section"

  - tag: gem.meander
    components: [lines, right_angles, repeating]
    mentioned_in: "Waves / Chevrons section"

  - tag: gem.balance_scale
    components: [line, bilateral_symmetry]
    mentioned_in: "Bilateral / D4 Symmetry section"

  - tag: gem.lamassu
    components: [rectangle, curve, composite_3d]
    mentioned_in: "Composite / 3D Composite Forms section"
```

#### GEK - Conceptual/Mathematical
```yaml
gek_conceptual:
  symmetry:
    - tag: gek.symmetry.radial
      mentioned_in: "Circle, Radial Stars sections"
      description: "Rotational symmetry around center"

    - tag: gek.symmetry.bilateral
      mentioned_in: "Bilateral / D4 Symmetry section"
      description: "Mirror symmetry across line"

    - tag: gek.symmetry.d4
      mentioned_in: "Bilateral / D4 Symmetry section"
      description: "Square symmetry, 4 rotations + 4 reflections"

    - tag: gek.symmetry.translational
      mentioned_in: "Tessellations section"
      description: "Repeating pattern symmetry"

    - tag: gek.symmetry.wallpaper
      mentioned_in: "Symmetry Groups section"
      description: "17 plane symmetry groups"

  angles:
    - tag: gek.angle.right
      mentioned_in: "Rectangle / Square section"
      description: "90° angle"

    - tag: gek.angle.45
      mentioned_in: "Radial Stars section"
      description: "45° angle (360° ÷ 8)"

    - tag: gek.angle.30
      mentioned_in: "Radial Stars section"
      description: "30° angle (360° ÷ 12)"

    - tag: gek.angle.120
      mentioned_in: "Tessellations section"
      description: "120° angle (hexagon internal)"

    - tag: gek.angle.sum.180
      mentioned_in: "Triangle section"
      description: "Triangle angle sum = 180°"

    - tag: gek.angle.sum.360
      mentioned_in: "Circle section"
      description: "Full rotation = 360°"

  measurement:
    - tag: gek.measurement.radius
      mentioned_in: "Circle section"
      description: "Distance from center to edge"

    - tag: gek.measurement.diameter
      mentioned_in: "Circle section"
      description: "Distance across through center"

    - tag: gek.measurement.circumference
      mentioned_in: "Circle section"
      description: "Distance around circle"

    - tag: gek.measurement.chord
      mentioned_in: "Crescent / Arcs section"
      description: "Line segment between two arc points"

    - tag: gek.measurement.sagitta
      mentioned_in: "Crescent / Arcs section"
      description: "Height of arc above chord"

    - tag: gek.measurement.area
      mentioned_in: "Rectangle, Integration sections"
      description: "2D space measurement"

    - tag: gek.measurement.volume
      mentioned_in: "Integration section"
      description: "3D space measurement"

  ratios:
    - tag: gek.ratio.pi
      mentioned_in: "Circle section"
      description: "π = C/d ≈ 3.14159..."

    - tag: gek.ratio.golden
      mentioned_in: "Rectangle / Square section"
      description: "φ ≈ 1.618..."

    - tag: gek.ratio.pythagorean
      mentioned_in: "Triangle section"
      description: "a² + b² = c²"

  properties:
    - tag: gek.property.equidistance
      mentioned_in: "Circle section"
      description: "All points equal distance from center"

    - tag: gek.property.rigidity
      mentioned_in: "Triangle section"
      description: "Cannot deform without breaking"

    - tag: gek.property.optimal_packing
      mentioned_in: "Tessellations section"
      description: "Maximum area per perimeter"

    - tag: gek.property.connectivity
      mentioned_in: "Topology section"
      description: "Path existence between points"

    - tag: gek.property.genus
      mentioned_in: "Topology section"
      description: "Number of holes in shape"
```

#### GEOK-T - Transformations
```yaml
geok_t_transformations:
  - tag: geok-t.rotation
    mentioned_in: "Circle section - wheel rotation"
    science: ["angular_momentum", "torque", "centrifugal_force"]

  - tag: geok-t.translation
    mentioned_in: "Grids section"
    science: ["displacement", "linear_motion"]

  - tag: geok-t.reflection
    mentioned_in: "Bilateral Symmetry section"
    science: ["mirror_imaging", "bilateral_balance"]

  - tag: geok-t.scaling
    mentioned_in: "Triangle section - similar triangles"
    science: ["proportion", "similarity"]

  - tag: geok-t.tessellation
    mentioned_in: "Tessellations section"
    science: ["infinite_coverage", "packing_efficiency"]

  - tag: geok-t.spiraling
    mentioned_in: "Spirals section"
    science: ["springs", "screws", "DNA_helix"]

  - tag: geok-t.projection
    mentioned_in: "Right Triangle → Trigonometric section"
    science: ["shadows", "perspective", "mapping"]

  - tag: geok-t.accumulation
    mentioned_in: "Integration section"
    science: ["area_under_curve", "total_quantity"]

  - tag: geok-t.branching
    mentioned_in: "Fractals & Chaos section"
    science: ["self_similarity", "recursive_splitting"]
```

---

### 2. HISTORICAL PERIODS (HIST.PERIOD)

```yaml
periods:
  # Proto-historical
  - tag: period.ubaid
    dates: "~6500-4000 BCE"
    mentioned_in: "Spirals section - pottery motifs"

  - tag: period.uruk
    dates: "~4000-3100 BCE"
    mentioned_in: "Circle section - potter's wheel"

  - tag: period.jemdet_nasr
    dates: "~3100-2900 BCE"
    mentioned_in: "Writing development"

  # Early Dynastic
  - tag: period.early_dynastic
    dates: "~2900-2350 BCE"
    mentioned_in: "Radial Stars section - star symbols"

  - tag: period.early_dynastic_i
    dates: "~2900-2750 BCE"

  - tag: period.early_dynastic_ii
    dates: "~2750-2600 BCE"

  - tag: period.early_dynastic_iii
    dates: "~2600-2350 BCE"
    mentioned_in: "Circle section - Royal Tombs of Ur"

  # Akkadian
  - tag: period.akkadian
    dates: "~2350-2150 BCE"
    mentioned_in: "Administrative standardization"
    rulers: ["Sargon", "Naram-Sin"]

  # Ur III
  - tag: period.ur_iii
    dates: "~2112-2004 BCE"
    mentioned_in: "Triangle section - Ziggurat of Ur"
    rulers: ["Ur-Nammu", "Shulgi"]

  # Isin-Larsa / Old Babylonian
  - tag: period.isin_larsa
    dates: "~2004-1763 BCE"

  - tag: period.old_babylonian
    dates: "~1894-1595 BCE"
    mentioned_in: "Triangle section - Plimpton 322"
    rulers: ["Hammurabi"]

  # Kassite
  - tag: period.kassite
    dates: "~1595-1155 BCE"
    mentioned_in: "Radial Stars section - Kudurru stones"

  # Middle Assyrian / Middle Babylonian
  - tag: period.middle_assyrian
    dates: "~1392-1056 BCE"

  - tag: period.middle_babylonian
    dates: "~1155-1026 BCE"

  # Neo-Assyrian
  - tag: period.neo_assyrian
    dates: "~911-609 BCE"
    mentioned_in: "Composite Forms section - Lamassu"
    rulers: ["Sargon_II", "Sennacherib", "Ashurbanipal"]
    cities: ["Nineveh", "Khorsabad", "Nimrud"]

  # Neo-Babylonian
  - tag: period.neo_babylonian
    dates: "~626-539 BCE"
    mentioned_in: "Tessellations section - Ishtar Gate"
    rulers: ["Nebuchadnezzar_II", "Nabonidus"]
    cities: ["Babylon"]

  # Late Babylonian / Persian
  - tag: period.achaemenid
    dates: "~539-331 BCE"
    mentioned_in: "Astronomy texts"

  # Seleucid / Parthian
  - tag: period.seleucid
    dates: "~312-63 BCE"
    mentioned_in: "Crescent section - Eclipse prediction texts"
```

---

### 3. RULERS (HIST.RULER)

```yaml
rulers:
  # Sumerian
  - tag: ruler.gilgamesh
    period: early_dynastic
    city: Uruk
    mentioned_in: "Epic literature"

  - tag: ruler.ur_nammu
    period: ur_iii
    city: Ur
    dates: "~2112-2095 BCE"
    mentioned_in: "Triangle section - Ziggurat of Ur"
    achievements: ["Law code", "Ziggurat construction"]

  - tag: ruler.shulgi
    period: ur_iii
    city: Ur
    dates: "~2094-2047 BCE"
    achievements: ["Administrative reform", "Road building"]

  # Akkadian
  - tag: ruler.sargon_akkad
    period: akkadian
    city: Akkad
    dates: "~2334-2279 BCE"
    mentioned_in: "First empire"

  - tag: ruler.naram_sin
    period: akkadian
    city: Akkad
    dates: "~2254-2218 BCE"
    mentioned_in: "Victory stele"

  # Babylonian
  - tag: ruler.hammurabi
    period: old_babylonian
    city: Babylon
    dates: "~1792-1750 BCE"
    mentioned_in: "Law code"

  - tag: ruler.nebuchadnezzar_ii
    period: neo_babylonian
    city: Babylon
    dates: "~605-562 BCE"
    mentioned_in: "Tessellations section - Ishtar Gate"
    achievements: ["Ishtar Gate", "Hanging Gardens"]

  - tag: ruler.nabonidus
    period: neo_babylonian
    city: Babylon
    dates: "~556-539 BCE"
    mentioned_in: "Archaeological restorations"

  # Assyrian
  - tag: ruler.ashurnasirpal_ii
    period: neo_assyrian
    city: Nimrud
    dates: "~883-859 BCE"
    mentioned_in: "Palace reliefs"

  - tag: ruler.sargon_ii
    period: neo_assyrian
    city: Khorsabad
    dates: "~722-705 BCE"
    mentioned_in: "Composite Forms section - Lamassu"

  - tag: ruler.sennacherib
    period: neo_assyrian
    city: Nineveh
    dates: "~705-681 BCE"
    achievements: ["Palace without Rival"]

  - tag: ruler.ashurbanipal
    period: neo_assyrian
    city: Nineveh
    dates: "~668-627 BCE"
    achievements: ["Library of Ashurbanipal"]
```

---

### 4. CITIES & SITES (GEO.CITY)

```yaml
cities:
  # Sumerian
  - tag: city.uruk
    region: southern_mesopotamia
    river: euphrates
    period: "~4000 BCE - 300 CE"
    mentioned_in: "Circle section - potter's wheel, cylinder seals"
    temples: ["Eanna", "Anu Ziggurat"]

  - tag: city.ur
    region: southern_mesopotamia
    river: euphrates
    period: "~3800 BCE - 500 BCE"
    mentioned_in: "Circle section - Royal Tombs, wheeled carts"
    temples: ["Ziggurat of Ur", "E-gish-shir-gal"]

  - tag: city.eridu
    region: southern_mesopotamia
    mentioned_in: "Oldest Sumerian city"

  - tag: city.nippur
    region: central_mesopotamia
    mentioned_in: "Religious center, Enlil worship"
    temples: ["Ekur"]

  - tag: city.lagash
    region: southern_mesopotamia
    mentioned_in: "Gudea statues"

  - tag: city.girsu
    region: southern_mesopotamia
    mentioned_in: "Administrative center"

  # Babylonian
  - tag: city.babylon
    region: central_mesopotamia
    river: euphrates
    period: "~2300 BCE - 300 CE"
    mentioned_in: "Tessellations - Ishtar Gate, Ziggurat section - Etemenanki"
    temples: ["Esagila", "Etemenanki"]
    gates: ["Ishtar Gate"]

  - tag: city.sippar
    region: central_mesopotamia
    mentioned_in: "Circle section - Shamash worship, Tablet of Shamash"
    temples: ["Ebabbar"]

  - tag: city.borsippa
    region: central_mesopotamia
    mentioned_in: "Ziggurat section"
    temples: ["Ezida", "Ziggurat of Borsippa"]

  - tag: city.larsa
    region: southern_mesopotamia
    mentioned_in: "Triangle section - Plimpton 322"

  # Assyrian
  - tag: city.assur
    region: northern_mesopotamia
    river: tigris
    mentioned_in: "Assyrian capital, religious center"

  - tag: city.nineveh
    region: northern_mesopotamia
    river: tigris
    period: "~6000 BCE - 612 BCE"
    mentioned_in: "Composite Forms section - Lamassu"
    palaces: ["Palace of Sennacherib", "North Palace"]

  - tag: city.nimrud
    region: northern_mesopotamia
    mentioned_in: "Neo-Assyrian capital"
    palaces: ["Northwest Palace"]

  - tag: city.khorsabad
    region: northern_mesopotamia
    mentioned_in: "Composite Forms section - Lamassu, Sargon II palace"
    palaces: ["Dur-Sharrukin"]

  # Other
  - tag: city.harran
    region: upper_mesopotamia
    mentioned_in: "Crescent section - Sin worship"
    temples: ["E-hul-hul"]

  - tag: city.mari
    region: middle_euphrates
    mentioned_in: "Palace archives"

  - tag: city.ebla
    region: syria
    mentioned_in: "Early archives"

  # Near Baghdad
  - tag: city.aqar_quf
    region: central_mesopotamia
    mentioned_in: "Ziggurat section - well-preserved ziggurat"
```

---

### 5. ARTIFACTS (ART)

#### Artifact Types
```yaml
artifact_types:
  # Writing
  - tag: art.type.tablet
    material: clay
    mentioned_in: "Rectangle section - cuneiform tablets"
    examples: ["Plimpton 322", "MUL.APIN", "Administrative tablets"]

  - tag: art.type.cylinder_seal
    material: stone
    mentioned_in: "Circle section - rolling motion creates pattern"

  - tag: art.type.stamp_seal
    material: stone

  - tag: art.type.kudurru
    material: stone
    mentioned_in: "Radial Stars section - boundary stones"

  # Containers
  - tag: art.type.pottery
    material: clay
    mentioned_in: "Circle section - potter's wheel"
    subtypes: ["bowl", "jar", "vessel"]

  - tag: art.type.basket
    material: reed
    mentioned_in: "Spirals section - coiled baskets"

  # Tools
  - tag: art.type.weight
    material: stone
    mentioned_in: "Bilateral Symmetry section - balance scales"

  - tag: art.type.plow
    material: wood_bronze

  - tag: art.type.axe
    material: bronze
    mentioned_in: "Composite Forms section"

  # Architectural elements
  - tag: art.type.brick
    material: mud_brick
    mentioned_in: "Rectangle section - standardized bricks"

  - tag: art.type.glazed_brick
    material: glazed_ceramic
    mentioned_in: "Tessellations section - Ishtar Gate"

  - tag: art.type.relief
    material: stone_alabaster
    mentioned_in: "Palace reliefs"

  # Sculpture
  - tag: art.type.lamassu
    material: stone
    mentioned_in: "Composite Forms section - gate guardians"

  - tag: art.type.statue
    material: stone_bronze

  - tag: art.type.stele
    material: stone
    mentioned_in: "Crescent section - Ur-Nammu stele"

  # Jewelry
  - tag: art.type.jewelry
    material: gold_silver
    mentioned_in: "Spirals section - spiral jewelry"
    subtypes: ["ring", "earring", "necklace", "bracelet"]

  # Transport
  - tag: art.type.wheel
    material: wood
    mentioned_in: "Circle section - wheeled carts"

  - tag: art.type.chariot
    material: wood_leather
    mentioned_in: "Circle section - Standard of Ur"

  - tag: art.type.boat
    material: reed_wood
    mentioned_in: "Composite Forms section"

  # Astronomical
  - tag: art.type.astrolabe
    mentioned_in: "Astronomy texts"

  - tag: art.type.gnomon
    material: stone_wood
    mentioned_in: "Crescent section - shadow clocks"

  # Mirrors
  - tag: art.type.mirror
    material: bronze
    mentioned_in: "Ellipses section - curved reflective surfaces"
```

#### Materials
```yaml
materials:
  # Clay
  - tag: mat.clay
    mentioned_in: "Tablets, pottery, bricks"

  - tag: mat.mud_brick
    mentioned_in: "Rectangle section - construction"

  - tag: mat.fired_brick
    mentioned_in: "Tessellations section"

  - tag: mat.glazed_ceramic
    mentioned_in: "Ishtar Gate"

  # Stone
  - tag: mat.limestone
    mentioned_in: "Statues, reliefs"

  - tag: mat.alabaster
    mentioned_in: "Palace reliefs"

  - tag: mat.basalt
    mentioned_in: "Grinding stones"

  - tag: mat.diorite
    mentioned_in: "Statues (Gudea)"

  - tag: mat.lapis_lazuli
    mentioned_in: "Royal Tombs of Ur"

  - tag: mat.carnelian
    mentioned_in: "Seals, jewelry"

  # Metals
  - tag: mat.bronze
    mentioned_in: "Tools, weapons, mirrors"

  - tag: mat.copper
    mentioned_in: "Early metalwork"

  - tag: mat.gold
    mentioned_in: "Spirals section - jewelry"

  - tag: mat.silver
    mentioned_in: "Jewelry, currency"

  - tag: mat.iron
    mentioned_in: "Late period tools"

  # Organic
  - tag: mat.wood
    mentioned_in: "Wheels, tools"

  - tag: mat.reed
    mentioned_in: "Baskets, boats"

  - tag: mat.bitumen
    mentioned_in: "Waterproofing, mortar"

  - tag: mat.leather
    mentioned_in: "Scrolls, equipment"
```

#### Techniques
```yaml
techniques:
  # Pottery
  - tag: tech.wheel_throwing
    mentioned_in: "Circle section - potter's wheel"

  - tag: tech.coiling
    mentioned_in: "Spirals section - coiled construction"

  - tag: tech.firing
    mentioned_in: "Ceramic production"

  - tag: tech.glazing
    mentioned_in: "Tessellations section - Ishtar Gate"

  # Metalwork
  - tag: tech.casting
    mentioned_in: "Bronze tools"

  - tag: tech.hammering
    mentioned_in: "Gold jewelry"

  - tag: tech.lost_wax
    mentioned_in: "Sculpture"

  # Stonework
  - tag: tech.carving
    mentioned_in: "Reliefs, seals"

  - tag: tech.polishing
    mentioned_in: "Cylinder seals"

  - tag: tech.drilling
    mentioned_in: "Seal making"

  # Construction
  - tag: tech.brick_laying
    mentioned_in: "Rectangle section"

  - tag: tech.terracing
    mentioned_in: "Ziggurat section"

  - tag: tech.buttressing
    mentioned_in: "Wall construction"

  # Textile
  - tag: tech.weaving
    mentioned_in: "Tessellations section - textiles"

  - tag: tech.dyeing
    mentioned_in: "Textile production"

  # Writing
  - tag: tech.cuneiform
    mentioned_in: "Rectangle section - tablet production"

  - tag: tech.seal_rolling
    mentioned_in: "Circle section - cylinder seals"
```

---

### 6. INVENTIONS (INV)

```yaml
inventions:
  # Mechanical
  mechanical:
    - tag: inv.potter_wheel
      element: circle
      period: "~3500 BCE"
      location: Uruk
      mentioned_in: "Circle section"

    - tag: inv.wheel_axle
      element: circle
      period: "~3200 BCE"
      mentioned_in: "Circle section - transport"

    - tag: inv.plow
      element: triangle
      mentioned_in: "Agricultural technology"

    - tag: inv.shaduf
      element: lever
      mentioned_in: "Water lifting"

    - tag: inv.waterwheel
      element: circle
      mentioned_in: "Later irrigation"

  # Architectural
  architectural:
    - tag: inv.ziggurat
      element: pyramid
      period: "~2100 BCE"
      mentioned_in: "Ziggurat section"
      examples: ["Ur", "Babylon", "Borsippa"]

    - tag: inv.arch
      element: arc
      mentioned_in: "Crescent section - load distribution"

    - tag: inv.vault
      element: arc
      mentioned_in: "Ceiling construction"

    - tag: inv.dome
      element: sphere
      mentioned_in: "Ellipses section - acoustic focus"

    - tag: inv.terrace
      element: triangle
      mentioned_in: "Ziggurat section - stepped drainage"

    - tag: inv.canal
      element: rectangle
      mentioned_in: "Topology section - irrigation networks"

    - tag: inv.levee
      element: triangle
      mentioned_in: "Flood control"

  # Administrative
  administrative:
    - tag: inv.cuneiform
      element: square
      period: "~3200 BCE"
      mentioned_in: "Rectangle section - writing tablets"

    - tag: inv.cylinder_seal
      element: circle
      period: "~3500 BCE"
      mentioned_in: "Circle section - authentication"

    - tag: inv.calendar
      element: arc
      mentioned_in: "Crescent section - lunar calendar"

    - tag: inv.base60
      mentioned_in: "Trigonometry section - 360°"

    - tag: inv.standard_weights
      element: bilateral_symmetry
      mentioned_in: "Bilateral Symmetry section - balance scales"

    - tag: inv.standard_bricks
      element: square
      mentioned_in: "Rectangle section"

    - tag: inv.city_grid
      element: grid
      mentioned_in: "Grids section - urban planning"

  # Astronomical
  astronomical:
    - tag: inv.zodiac
      mentioned_in: "Circle section - celestial sphere"

    - tag: inv.eclipse_prediction
      element: arc
      mentioned_in: "Crescent section"

    - tag: inv.planetary_tables
      mentioned_in: "Astronomy"

    - tag: inv.gnomon_clock
      element: triangle
      mentioned_in: "Crescent section - shadow measurement"

    - tag: inv.astrolabe
      element: circle
      mentioned_in: "Star positions"

  # Mathematical
  mathematical:
    - tag: inv.pythagorean_triples
      element: triangle
      period: "~1800 BCE"
      artifact: "Plimpton 322"
      mentioned_in: "Triangle section"

    - tag: inv.area_calculation
      element: rectangle
      mentioned_in: "Integration section"

    - tag: inv.surveying
      element: triangle
      mentioned_in: "Triangle section - triangulation"
```

---

### 7. DEITIES (DEITY)

```yaml
deities:
  mesopotamian:
    # Major deities
    - tag: deity.meso.shamash
      alternate: ["Utu"]
      domain: ["sun", "justice", "truth", "divination"]
      element: circle
      symbol: "Sun disk with rays"
      cult_centers: ["Sippar", "Larsa"]
      mentioned_in: "Circle section - primary deity"

    - tag: deity.meso.ishtar
      alternate: ["Inanna"]
      domain: ["love", "war", "venus", "fertility"]
      element: star8
      symbol: "8-pointed star"
      cult_centers: ["Uruk", "Nineveh"]
      mentioned_in: "Radial Stars section"

    - tag: deity.meso.nanna
      alternate: ["Sin"]
      domain: ["moon", "time", "calendars", "wisdom"]
      element: arc
      symbol: "Crescent moon"
      cult_centers: ["Ur", "Harran"]
      mentioned_in: "Crescent section"

    - tag: deity.meso.enlil
      domain: ["air", "wind", "authority", "destiny"]
      element: triangle
      cult_centers: ["Nippur"]
      mentioned_in: "Triangle section"

    - tag: deity.meso.nabu
      domain: ["writing", "wisdom", "scribes", "literacy"]
      element: square
      symbol: "Writing stylus, tablet"
      cult_centers: ["Borsippa"]
      mentioned_in: "Rectangle section"

    - tag: deity.meso.marduk
      domain: ["creation", "babylon", "sovereignty", "magic"]
      element: pyramid
      symbol: "Mušḫuššu dragon, spade"
      cult_centers: ["Babylon"]
      mentioned_in: "Ziggurat section"

    - tag: deity.meso.tiamat
      domain: ["primordial_chaos", "salt_water", "dragons"]
      element: spiral
      mentioned_in: "Spirals section"

    - tag: deity.meso.enki
      alternate: ["Ea"]
      domain: ["fresh_water", "wisdom", "crafts", "magic"]
      element: spiral
      symbol: "Flowing water"
      cult_centers: ["Eridu"]
      mentioned_in: "Waves / Chevrons section"

    - tag: deity.meso.anu
      domain: ["sky", "heavens", "kingship"]
      element: arc
      cult_centers: ["Uruk"]
      mentioned_in: "Crescent section - sky vault"

    - tag: deity.meso.nisaba
      domain: ["grain", "writing", "surveying", "learning"]
      element: hexagon
      mentioned_in: "Tessellations section - efficient packing"

    - tag: deity.meso.ninurta
      domain: ["war", "agriculture", "hunting"]
      element: triangle
      mentioned_in: "Warrior deity"

    - tag: deity.meso.adad
      alternate: ["Ishkur"]
      domain: ["storm", "rain", "lightning"]
      mentioned_in: "Weather"

    - tag: deity.meso.nergal
      domain: ["underworld", "plague", "war"]
      cult_centers: ["Kutha"]

  egyptian:
    - tag: deity.egypt.ra
      alternate: ["Aten"]
      domain: ["sun", "creation", "kingship"]
      element: circle
      mentioned_in: "Circle section - deity pairings"

    - tag: deity.egypt.nut
      domain: ["sky", "heavens", "night"]
      element: arc
      mentioned_in: "Crescent section - body arched over earth"

    - tag: deity.egypt.geb
      domain: ["earth", "land"]
      element: square
      mentioned_in: "Rectangle section"

    - tag: deity.egypt.osiris
      domain: ["underworld", "resurrection", "agriculture"]
      element: triangle
      mentioned_in: "Triangle section - pyramids"

    - tag: deity.egypt.neith
      domain: ["weaving", "creation", "war"]
      element: hexagon
      mentioned_in: "Tessellations section"

    - tag: deity.egypt.wadjet
      domain: ["protection", "cobra"]
      element: spiral
      mentioned_in: "Spirals section"

    - tag: deity.egypt.seshat
      domain: ["measurement", "writing", "astronomy"]
      element: star7
      mentioned_in: "Radial Stars section"

  greek:
    - tag: deity.greece.helios
      alternate: ["Apollo"]
      domain: ["sun", "music", "prophecy"]
      element: circle
      mentioned_in: "Circle section - deity pairings"

    - tag: deity.greece.zeus
      domain: ["sky", "thunder", "kingship"]
      element: triangle
      mentioned_in: "Triangle section - divine triad"

    - tag: deity.greece.hestia
      domain: ["hearth", "home", "domestic"]
      element: square
      mentioned_in: "Rectangle section"

    - tag: deity.greece.artemis
      domain: ["hunting", "moon", "nature"]
      element: hexagon
      mentioned_in: "Tessellations section - bees sacred"

    - tag: deity.greece.hecate
      domain: ["magic", "crossroads", "underworld"]
      element: spiral
      mentioned_in: "Spirals section - labyrinth"

    - tag: deity.greece.iris
      domain: ["rainbow", "messenger"]
      element: arc
      mentioned_in: "Crescent section - rainbow arc"
```

---

### 8. SCIENTIFIC CONCEPTS (SCI)

```yaml
scientific_concepts:
  physics:
    - tag: sci.phys.angular_momentum
      mentioned_in: "Circle section - rotation"

    - tag: sci.phys.centrifugal_force
      mentioned_in: "Circle section - spinning"

    - tag: sci.phys.torque
      mentioned_in: "Circle section - rotation"

    - tag: sci.phys.compression
      mentioned_in: "Triangle section - load distribution"

    - tag: sci.phys.tension
      mentioned_in: "Structural forces"

    - tag: sci.phys.pressure
      mentioned_in: "Circle section - vessels"

    - tag: sci.phys.friction
      mentioned_in: "Wheel mechanics"

    - tag: sci.phys.gravity
      mentioned_in: "Pyramid section - stability"

    - tag: sci.phys.buoyancy
      mentioned_in: "Boat design"

    - tag: sci.phys.acoustics
      mentioned_in: "Ellipses section - focal behavior"

    - tag: sci.phys.optics
      mentioned_in: "Ellipses section - reflectors"

  mathematics:
    - tag: sci.math.pi
      mentioned_in: "Circle section"

    - tag: sci.math.pythagorean_theorem
      mentioned_in: "Triangle section"

    - tag: sci.math.trigonometry
      mentioned_in: "Trigonometric Thinking section"

    - tag: sci.math.area_calculation
      mentioned_in: "Rectangle, Integration sections"

    - tag: sci.math.volume_calculation
      mentioned_in: "Integration section"

    - tag: sci.math.base60
      mentioned_in: "Mesopotamian number system"

    - tag: sci.math.fractions
      mentioned_in: "Reciprocal tables"

    - tag: sci.math.algebra
      mentioned_in: "Babylonian mathematics"

  astronomy:
    - tag: sci.astro.lunar_phases
      mentioned_in: "Crescent section"

    - tag: sci.astro.eclipse
      mentioned_in: "Crescent section - prediction"

    - tag: sci.astro.heliacal_rising
      mentioned_in: "Radial Stars section"

    - tag: sci.astro.zodiac
      mentioned_in: "Circle section - celestial sphere"

    - tag: sci.astro.planetary_motion
      mentioned_in: "Ellipses section"

    - tag: sci.astro.calendar
      mentioned_in: "Crescent section - lunar calendar"

  engineering:
    - tag: sci.eng.load_distribution
      mentioned_in: "Triangle, Arc sections"

    - tag: sci.eng.drainage
      mentioned_in: "Ziggurat section"

    - tag: sci.eng.irrigation
      mentioned_in: "Canal systems"

    - tag: sci.eng.surveying
      mentioned_in: "Triangle section"

    - tag: sci.eng.construction
      mentioned_in: "Various sections"
```

---

### 9. MUSEUMS (ART.MUSEUM)

```yaml
museums:
  - tag: museum.british_museum
    location: London
    holdings: ["Ishtar Gate lions", "Lamassu", "Tablets", "Cylinder seals", "Tablet of Shamash"]
    mentioned_in: "Multiple sections"

  - tag: museum.louvre
    location: Paris
    holdings: ["Code of Hammurabi", "Lamassu", "Cylinder seals"]
    mentioned_in: "Multiple sections"

  - tag: museum.pergamon
    location: Berlin
    holdings: ["Ishtar Gate", "Processional Way"]
    mentioned_in: "Tessellations section"

  - tag: museum.penn_museum
    location: Philadelphia
    holdings: ["Royal Tombs of Ur", "Ur-Nammu stele"]
    mentioned_in: "Circle section"

  - tag: museum.met
    location: New York
    holdings: ["Cylinder seals", "Reliefs"]

  - tag: museum.yale_babylonian
    location: New Haven
    holdings: ["Mathematical tablets", "YBC tablets"]

  - tag: museum.columbia_rare_books
    location: New York
    holdings: ["Plimpton 322"]
    mentioned_in: "Triangle section"

  - tag: museum.oriental_institute
    location: Chicago
    holdings: ["Khorsabad materials", "Tablets"]

  - tag: museum.iraq_museum
    location: Baghdad
    holdings: ["In situ finds", "Tablets"]

  - tag: museum.vorderasiatisches
    location: Berlin
    holdings: ["Tablets", "Seals"]
```

---

### 10. IMAGE SYSTEM TAGS (IMG)

```yaml
image_tags:
  types:
    - tag: img.type.deity_image
      description: "Portrait of divine figure"
      mentioned_in: "Day A Image Prompt Schema"

    - tag: img.type.artifact_photo
      description: "Museum artifact photograph"

    - tag: img.type.reconstruction
      description: "Archaeological reconstruction"

    - tag: img.type.diagram
      description: "Mathematical/scientific diagram"

    - tag: img.type.illustration
      description: "Educational illustration"

    - tag: img.type.myth_scene
      description: "Mythological narrative scene"

    - tag: img.type.ritual_scene
      description: "Ceremonial practice"

    - tag: img.type.process_image
      description: "Technique/process demonstration"

    - tag: img.type.comparison
      description: "Side-by-side comparison"

    - tag: img.type.overlay
      description: "SVG annotation overlay"

  roles:
    - tag: img.role.primary_analysis
      description: "Main image for geometric analysis"

    - tag: img.role.supporting_example
      description: "Additional evidence"

    - tag: img.role.context_visual
      description: "Cultural/historical context"

    - tag: img.role.mechanism_visual
      description: "How it works"

    - tag: img.role.step_diagram
      description: "Sequential construction"

  sources:
    - tag: img.src.museum_catalog
      description: "Official museum image"
      priority: 1

    - tag: img.src.academic_publication
      description: "Journal/book image"
      priority: 2

    - tag: img.src.reconstruction
      description: "Archaeological reconstruction"
      priority: 3

    - tag: img.src.ai_generated
      description: "AI-generated image"
      priority: 4

    - tag: img.src.textbook_diagram
      description: "Educational resource"
      priority: 5

  status:
    - tag: img.status.required
    - tag: img.status.approved
    - tag: img.status.pending_review
    - tag: img.status.needs_replacement
    - tag: img.status.ai_allowed
    - tag: img.status.ai_not_allowed
```

---

### 11. CURRICULUM TAGS (CURR)

```yaml
curriculum_tags:
  ssot_sections:
    day_a:
      - tag: curr.ssot.a1
        name: "Myth Retelling"
        focus: "Origin story, deity introduction"

      - tag: curr.ssot.a2
        name: "SEL + Metaphor"
        focus: "Personal connection"

      - tag: curr.ssot.a3
        name: "Iconographic & Mythic Art"
        focus: "Visual features of deity"

      - tag: curr.ssot.a4
        name: "Semiotics on Objects & in Ritual"
        focus: "Material culture"

      - tag: curr.ssot.a5
        name: "Technique OR Design"  # Note: Contradiction exists
        focus: "How element was made"

      - tag: curr.ssot.a6
        name: "Activity"
        focus: "Student creates"

      - tag: curr.ssot.a7
        name: "Bridge (Exit)"
        focus: "Cliffhanger question"

    day_b:
      - tag: curr.ssot.b1
        name: "Bridge Review"
        focus: "Answer A7"

      - tag: curr.ssot.b2
        name: "Math Proof"
        focus: "Verify property"

      - tag: curr.ssot.b3
        name: "Transformation"
        focus: "Property in operation"

      - tag: curr.ssot.b4
        name: "Mechanics"
        focus: "Physical result"

      - tag: curr.ssot.b5
        name: "STEM History"
        focus: "Timeline contribution"

      - tag: curr.ssot.b6
        name: "The Moment"
        focus: "Specific invention"

      - tag: curr.ssot.b7
        name: "Activity"
        focus: "Student builds"

      - tag: curr.ssot.b8
        name: "Exit Ticket"
        focus: "Synthesize"

  grades:
    - tag: curr.grade.g3
    - tag: curr.grade.g4
    - tag: curr.grade.g5
    - tag: curr.grade.g6
    - tag: curr.grade.g7
    - tag: curr.grade.g8

  weeks:
    - tag: curr.week.w1
      element: circle
      deity: shamash

    - tag: curr.week.w2
      element: star8
      deity: ishtar

    - tag: curr.week.w3
      element: triangle
      deity: enlil

    - tag: curr.week.w4
      element: square
      deity: nabu

    - tag: curr.week.w5
      element: spiral
      deity: tiamat

    - tag: curr.week.w6
      element: arc
      deity: anu

    - tag: curr.week.w7
      element: hexagon
      deity: nisaba

    - tag: curr.week.w8
      element: pyramid
      deity: marduk

  days:
    - tag: curr.day.a
      focus: "Metaphor"

    - tag: curr.day.b
      focus: "Function"

    - tag: curr.day.bridge
      focus: "Transition"
```

---

## TAG COUNT SUMMARY

| Namespace | Count | Description |
|-----------|-------|-------------|
| GEA | 15 | Atomic geometric elements |
| GEM | 12 | Molecular composites |
| GEK | 35 | Conceptual/mathematical properties |
| GEOK-T | 9 | Transformations |
| PERIOD | 20 | Historical periods |
| RULER | 15 | Kings and rulers |
| CITY | 25 | Cities and sites |
| ART.TYPE | 25 | Artifact types |
| MAT | 20 | Materials |
| TECH | 20 | Techniques |
| INV | 30 | Inventions |
| DEITY | 35 | Divine figures |
| SCI | 30 | Scientific concepts |
| MUSEUM | 10 | Museum collections |
| IMG | 20 | Image system |
| CURR | 25 | Curriculum |
| **TOTAL** | **~350** | Unique tags |

---

## VALIDATION REQUIREMENTS

Every Shape Biography section must have:

1. **Minimum 1 GEA tag** (primary element)
2. **Minimum 1 DEITY tag** (paired deity)
3. **Minimum 1 PERIOD tag** for each mentioned artifact
4. **Minimum 1 CITY tag** for each mentioned location
5. **All mentioned artifacts tagged** with ART.TYPE + MAT
6. **All mentioned inventions tagged** with INV
7. **All mentioned scientific concepts tagged** with SCI

---

**END SSOT-018**


---

## MAGIC DRIVERS (CONNECTIVE TISSUE)

Drivers are not geometric elements; they are routing/interpretive labels:
- `driver.M` (Math/Formal)
- `driver.A` (Aesthetics/Art)
- `driver.G` (Geometry element focus)
- `driver.I` (Ideology/Meaning)
- `driver.C` (Czar/Power/Institution)