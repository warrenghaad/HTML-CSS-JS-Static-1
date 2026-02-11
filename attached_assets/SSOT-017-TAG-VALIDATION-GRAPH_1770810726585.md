# SSOT-017: TAG VALIDATION GRAPH
version: 5.0.0
generated_at: 2026-02-02

# SSOT-017: TAG VALIDATION GRAPH

## Overview

This document defines a **graph-based tagging validation system** that serves as a backup to verify all Shape Biography content has proper tags. The system uses graph nodes to:

1. Track every taggable entity in the Shape Biography
2. Validate tag completeness and correctness
3. Detect tag updates and propagate changes
4. Provide audit trails for tag modifications

---

## GRAPH NODE TYPES FOR TAGGING

### Node Hierarchy

```
TAG_NAMESPACE (root)
  └── TAG_CATEGORY
        └── TAG_VALUE
              └── TAG_INSTANCE (link to content)
```

### Node Definitions

```yaml
nodes:
  TAG_NAMESPACE:
    description: Top-level tag family (gea, gem, gek, geu, geok-t, deity, elem, etc.)
    fields:
      - id: string          # ns_gea, ns_gem, etc.
      - name: string        # "GEA - Atomic Elements"
      - prefix: string      # "gea."
      - source_ssot: string # "SSOT-003"
      - validation_rules: [] # Rules for this namespace

  TAG_CATEGORY:
    description: Sub-category within namespace
    fields:
      - id: string          # cat_gea_2d_curved
      - name: string        # "2D Curved Elements"
      - namespace_id: string
      - required_fields: [] # What must be present

  TAG_VALUE:
    description: Specific tag value
    fields:
      - id: string          # tag_gea_circle
      - tag_string: string  # "gea.circle"
      - display_name: string # "Circle"
      - category_id: string
      - synonyms: []        # Alternative forms
      - deprecated: boolean
      - replaced_by: string # If deprecated

  TAG_INSTANCE:
    description: Application of tag to content
    fields:
      - id: string          # inst_SB_CIRCLE_gea_circle
      - tag_id: string      # tag_gea_circle
      - target_type: string # "shape_bio", "artifact", "invention", etc.
      - target_id: string   # SB_MESO_CIRCLE_V1
      - confidence: number  # 0-1 (for auto-tags)
      - source: string      # "manual", "auto", "imported"
      - validated: boolean
      - validated_by: string
      - validated_at: timestamp
```

---

## EDGE TYPES FOR TAG RELATIONSHIPS

```yaml
edges:
  # Structural
  CONTAINS:
    from: TAG_NAMESPACE
    to: TAG_CATEGORY

  HAS_VALUE:
    from: TAG_CATEGORY
    to: TAG_VALUE

  TAGGED_WITH:
    from: CONTENT_NODE (any)
    to: TAG_VALUE
    data:
      - instance_id: string
      - confidence: number
      - source: string

  # Relationships
  RELATED_TO:
    from: TAG_VALUE
    to: TAG_VALUE
    data:
      - relationship_type: string # "synonym", "broader", "narrower", "related"

  REPLACES:
    from: TAG_VALUE
    to: TAG_VALUE
    description: For deprecated tags

  REQUIRES:
    from: TAG_VALUE
    to: TAG_VALUE
    description: If tag A is present, tag B must also be present

  CONFLICTS_WITH:
    from: TAG_VALUE
    to: TAG_VALUE
    description: Tags that cannot coexist
```

---

## SHAPE BIOGRAPHY TAGGABLE ENTITIES

Every Shape Biography contains these taggable items:

### 1. Element Level Tags (Required)

| Entity | Required Tags | Validation Rule |
|--------|--------------|-----------------|
| Element itself | `gea.*`, `elem.*` | Must have exactly 1 GEA tag |
| Core property | `gek.*` | Must link to mathematical concept |
| Scientific effects | `gek.*` | At least 1 per effect |

### 2. Deity Pairing Tags (Required)

| Entity | Required Tags | Validation Rule |
|--------|--------------|-----------------|
| Primary deity | `deity.meso.*` | Exactly 1 primary |
| Domain | `focus.*` | At least 1 domain tag |
| Symbol | `gem.*` or `gea.*` | Symbol must be geometric |

### 3. Artifact Tags (Required per artifact)

| Entity | Required Tags | Validation Rule |
|--------|--------------|-----------------|
| Artifact name | `art.*` | Category tag required |
| Period | `civ.meso.*` | Sub-period recommended |
| Location | (custom) | City/site tag |
| Museum | `img.src.*` | If known |

### 4. Invention Tags (Required per invention)

| Entity | Required Tags | Validation Rule |
|--------|--------------|-----------------|
| Invention | `INV__*` | Canonical ID required |
| Carrier | `CARR__*` | Physical form tag |
| Transformation | `geok-t.*` | If applicable |

### 5. Image Requirement Tags (Per slot)

| Entity | Required Tags | Validation Rule |
|--------|--------------|-----------------|
| Image type | `img.type.*` | From SSOT-003 list |
| Image role | (custom) | CONTEXT_VISUAL, MECHANISM_VISUAL, etc. |
| Source priority | `img.src.*` | Ordered list |

---

## COMPLETE TAG REGISTRY FOR SHAPE BIOGRAPHY

### GEA Tags (Atomic Elements)

```yaml
gea_registry:
  - tag: gea.point
    display: Point
    dimension: 0D
    used_by: []

  - tag: gea.line
    display: Line
    dimension: 1D
    used_by: []

  - tag: gea.circle
    display: Circle
    dimension: 2D-curved
    used_by: [SB_MESO_CIRCLE_V1]

  - tag: gea.arc
    display: Arc
    dimension: 2D-curved
    used_by: [SB_MESO_CRESCENT_V1]

  - tag: gea.spiral
    display: Spiral
    dimension: 2D-curved
    used_by: [SB_MESO_SPIRAL_V1]

  - tag: gea.triangle
    display: Triangle
    dimension: 2D-angular
    used_by: [SB_MESO_TRIANGLE_V1]

  - tag: gea.square
    display: Square
    dimension: 2D-angular
    used_by: [SB_MESO_SQUARE_V1]

  - tag: gea.hexagon
    display: Hexagon
    dimension: 2D-angular
    used_by: [SB_MESO_HEXAGON_V1]

  - tag: gea.star8
    display: 8-Pointed Star
    dimension: 2D-angular
    used_by: [SB_MESO_STAR8_V1]

  - tag: gea.pyramid
    display: Pyramid
    dimension: 3D
    used_by: [SB_MESO_PYRAMID_V1]
```

### GEM Tags (Molecular Composites)

```yaml
gem_registry:
  - tag: gem.rosette
    display: Rosette
    components: [circle, radial_lines]
    used_by: [SB_MESO_CIRCLE_V1, SB_MESO_STAR8_V1]

  - tag: gem.wheel_axle
    display: Wheel + Axle
    components: [circle, square]
    used_by: [SB_MESO_CIRCLE_V1]

  - tag: gem.grid
    display: Grid/Lattice
    components: [lines, angles]
    used_by: [SB_MESO_SQUARE_V1]

  - tag: gem.star_polygon
    display: Star Polygon
    components: [circle, triangles]
    used_by: [SB_MESO_STAR8_V1]

  - tag: gem.truss
    display: Truss
    components: [triangles, squares]
    used_by: [SB_MESO_TRIANGLE_V1, SB_MESO_PYRAMID_V1]

  - tag: gem.tessellation
    display: Tessellation
    components: [multiple_polygons]
    used_by: [SB_MESO_HEXAGON_V1]

  - tag: gem.arch
    display: Arch
    components: [arcs, keystone]
    used_by: [SB_MESO_CRESCENT_V1]

  - tag: gem.helix
    display: Helix
    components: [circle, line_3d]
    used_by: [SB_MESO_SPIRAL_V1]
```

### GEK Tags (Conceptual/Mathematical)

```yaml
gek_registry:
  # Symmetry
  - tag: gek.symmetry.radial
    display: Radial Symmetry
    used_by: [SB_MESO_CIRCLE_V1, SB_MESO_STAR8_V1]

  - tag: gek.symmetry.bilateral
    display: Bilateral Symmetry
    used_by: []

  # Angles
  - tag: gek.angle.right
    display: Right Angle (90°)
    used_by: [SB_MESO_SQUARE_V1]

  - tag: gek.angle.sum.triangle
    display: Triangle Angle Sum (180°)
    used_by: [SB_MESO_TRIANGLE_V1, SB_MESO_CRESCENT_V1]

  # Area/Volume
  - tag: gek.area.rectangle
    display: Area (rectangle)
    used_by: [SB_MESO_SQUARE_V1]

  # Properties
  - tag: gek.efficiency.packing
    display: Packing Efficiency
    used_by: [SB_MESO_HEXAGON_V1]

  - tag: gek.stability.triangulation
    display: Triangulation Stability
    used_by: [SB_MESO_TRIANGLE_V1, SB_MESO_PYRAMID_V1]

  # Forces
  - tag: gek.force.compression
    display: Compression
    used_by: [SB_MESO_PYRAMID_V1]
```

### GEU Tags (Ubiquitous/Cross-Cultural)

```yaml
geu_registry:
  - tag: geu.solar_disk
    display: Solar Disk
    civilizations: [mesopotamia, egypt, greece, china, mesoamerica, india]
    used_by: [SB_MESO_CIRCLE_V1]

  - tag: geu.star8
    display: 8-Pointed Star
    civilizations: [mesopotamia, islamic, christian, buddhist]
    used_by: [SB_MESO_STAR8_V1]

  - tag: geu.spiral
    display: Spiral
    civilizations: [celtic, polynesian, native_american, greek]
    used_by: [SB_MESO_SPIRAL_V1]
```

### GEOK-T Tags (Transformations)

```yaml
geok_t_registry:
  - tag: geok-t.rotation
    display: Rotation
    science: [centrifugal_force, angular_momentum, torque]
    used_by: [SB_MESO_CIRCLE_V1, SB_MESO_STAR8_V1, SB_MESO_CRESCENT_V1]

  - tag: geok-t.tessellation
    display: Tessellation
    science: [infinite_coverage, packing]
    used_by: [SB_MESO_SQUARE_V1, SB_MESO_HEXAGON_V1]

  - tag: geok-t.scaling
    display: Scaling
    science: [proportion, ratio, similarity]
    used_by: [SB_MESO_TRIANGLE_V1, SB_MESO_PYRAMID_V1]

  - tag: geok-t.spiraling
    display: Spiraling
    science: [screws, springs, DNA]
    used_by: [SB_MESO_SPIRAL_V1]

  - tag: geok-t.projection
    display: Projection
    science: [perspective, mapping, shadows]
    used_by: [SB_MESO_STAR8_V1]
```

### Deity Tags (Mesopotamia)

```yaml
deity_registry:
  - tag: deity.meso.shamash
    display: Shamash
    domain: [sun, justice, truth]
    element: gea.circle
    used_by: [SB_MESO_CIRCLE_V1]

  - tag: deity.meso.ishtar
    display: Ishtar/Inanna
    domain: [love, war, venus]
    element: gea.star8
    used_by: [SB_MESO_STAR8_V1]

  - tag: deity.meso.nanna
    display: Sin/Nanna
    domain: [moon, time, calendars]
    element: gea.arc
    used_by: [SB_MESO_CRESCENT_V1]

  - tag: deity.meso.enlil
    display: Enlil
    domain: [air, authority, divine_triad]
    element: gea.triangle
    used_by: [SB_MESO_TRIANGLE_V1]

  - tag: deity.meso.nabu
    display: Nabu
    domain: [writing, wisdom, scribes]
    element: gea.square
    used_by: [SB_MESO_SQUARE_V1]

  - tag: deity.meso.tiamat
    display: Tiamat
    domain: [chaos, salt_water, primordial]
    element: gea.spiral
    used_by: [SB_MESO_SPIRAL_V1]

  - tag: deity.meso.nisaba
    display: Nisaba
    domain: [grain, writing, surveying]
    element: gea.hexagon
    used_by: [SB_MESO_HEXAGON_V1]

  - tag: deity.meso.marduk
    display: Marduk
    domain: [creation, babylon, sovereignty]
    element: gea.pyramid
    used_by: [SB_MESO_PYRAMID_V1]
```

### Carrier Tags (Physical Forms)

```yaml
carrier_registry:
  # Circle carriers
  - tag: CARR__SUN_DISK
    element: gea.circle
    description: Solar disk symbol

  - tag: CARR__WHEEL
    element: gea.circle
    description: Wheel (transport)

  - tag: CARR__AXLE
    element: gea.circle
    description: Axle through wheel

  - tag: CARR__SEAL
    element: gea.circle
    description: Cylinder seal

  # Star carriers
  - tag: CARR__ISHTAR_STAR
    element: gea.star8
    description: 8-pointed Ishtar symbol

  - tag: CARR__VENUS_SYMBOL
    element: gea.star8
    description: Venus marker

  - tag: CARR__GATE_DECORATION
    element: gea.star8
    description: Ishtar Gate stars

  # Crescent carriers
  - tag: CARR__CRESCENT_MOON
    element: gea.arc
    description: Lunar crescent

  - tag: CARR__LUNAR_BOAT
    element: gea.arc
    description: Moon as boat

  # Triangle carriers
  - tag: CARR__ZIGGURAT_PROFILE
    element: gea.triangle
    description: Stepped pyramid profile

  - tag: CARR__RAMP
    element: gea.triangle
    description: Construction ramp

  # Square carriers
  - tag: CARR__TABLET
    element: gea.square
    description: Cuneiform tablet

  - tag: CARR__BRICK
    element: gea.square
    description: Standardized brick

  # Spiral carriers
  - tag: CARR__SERPENT_COIL
    element: gea.spiral
    description: Coiling serpent

  # Pyramid carriers
  - tag: CARR__ZIGGURAT
    element: gea.pyramid
    description: Temple tower
```

### Invention Tags

```yaml
invention_registry:
  # Circle inventions
  - tag: INV__POTTER_WHEEL
    element: gea.circle
    period: ~3500 BCE
    location: Uruk

  - tag: INV__WHEEL_AND_AXLE
    element: gea.circle
    period: ~3200 BCE
    location: Mesopotamia

  - tag: INV__CYLINDER_SEAL
    element: gea.circle
    period: ~3500 BCE
    location: Uruk

  # Star inventions
  - tag: INV__COMPASS_ROSE
    element: gea.star8
    description: Directional marker

  - tag: INV__ASTRONOMICAL_OBSERVATION
    element: gea.star8
    description: Star tracking

  # Crescent inventions
  - tag: INV__LUNAR_CALENDAR
    element: gea.arc
    description: Moon-based calendar

  - tag: INV__ECLIPSE_PREDICTION
    element: gea.arc
    description: Eclipse forecasting

  # Triangle inventions
  - tag: INV__ZIGGURAT_CONSTRUCTION
    element: gea.triangle
    description: Stepped temple building

  - tag: INV__SURVEYING_TRIANGULATION
    element: gea.triangle
    description: Land measurement

  # Square inventions
  - tag: INV__CUNEIFORM_TABLET
    element: gea.square
    description: Writing system

  - tag: INV__STANDARDIZED_BRICK
    element: gea.square
    description: Uniform building material

  - tag: INV__CITY_GRID_PLANNING
    element: gea.square
    description: Urban layout
```

---

## VALIDATION RULES

### Rule 1: Required Tags per Shape Biography

```yaml
validation_rule_01:
  name: shape_bio_required_tags
  description: Every Shape Biography must have these tags
  required:
    - exactly_one: gea.*
    - exactly_one: deity.meso.*
    - at_least_one: gek.*
    - at_least_one: geok-t.*
    - at_least_one: CARR__*
    - at_least_one: INV__*
```

### Rule 2: Deity-Element Consistency

```yaml
validation_rule_02:
  name: deity_element_match
  description: Deity tag must match element tag
  rules:
    - if: deity.meso.shamash
      then_must_have: gea.circle
    - if: deity.meso.ishtar
      then_must_have: gea.star8
    - if: deity.meso.nanna
      then_must_have: gea.arc
    - if: deity.meso.enlil
      then_must_have: gea.triangle
    - if: deity.meso.nabu
      then_must_have: gea.square
    - if: deity.meso.tiamat
      then_must_have: gea.spiral
    - if: deity.meso.nisaba
      then_must_have: gea.hexagon
    - if: deity.meso.marduk
      then_must_have: gea.pyramid
```

### Rule 3: Carrier-Element Consistency

```yaml
validation_rule_03:
  name: carrier_element_match
  description: Carrier tag must match its element
  rules:
    - CARR__SUN_DISK requires gea.circle
    - CARR__WHEEL requires gea.circle
    - CARR__ISHTAR_STAR requires gea.star8
    - CARR__CRESCENT_MOON requires gea.arc
    # ... etc
```

### Rule 4: Artifact Tag Completeness

```yaml
validation_rule_04:
  name: artifact_completeness
  description: Every artifact must have minimum tags
  required_per_artifact:
    - art.* (category)
    - civ.meso.* or civ.mesopotamia
    - period or date
    - location (recommended)
    - museum (if known)
```

### Rule 5: Image Requirement Tags

```yaml
validation_rule_05:
  name: image_requirement_tags
  description: Every image requirement must have type
  required:
    - img.type.*
    - role specification
```

---

## TAG AUDIT QUERIES

### Query 1: Find Untagged Content

```cypher
// Pseudo-Cypher for graph query
MATCH (sb:ShapeBio)
WHERE NOT (sb)-[:TAGGED_WITH]->(:TAG_VALUE {namespace: 'gea'})
RETURN sb.id AS missing_gea_tag
```

### Query 2: Find Invalid Tag Combinations

```cypher
MATCH (sb:ShapeBio)-[:TAGGED_WITH]->(deity:TAG_VALUE {namespace: 'deity'})
MATCH (sb)-[:TAGGED_WITH]->(elem:TAG_VALUE {namespace: 'gea'})
WHERE NOT deity.expected_element = elem.tag_string
RETURN sb.id, deity.tag_string, elem.tag_string AS mismatch
```

### Query 3: Find Deprecated Tags Still In Use

```cypher
MATCH (content)-[:TAGGED_WITH]->(tag:TAG_VALUE {deprecated: true})
RETURN content.id, tag.tag_string, tag.replaced_by
```

### Query 4: Tag Coverage Report

```cypher
MATCH (sb:ShapeBio)
OPTIONAL MATCH (sb)-[:TAGGED_WITH]->(gea:TAG_VALUE {namespace: 'gea'})
OPTIONAL MATCH (sb)-[:TAGGED_WITH]->(deity:TAG_VALUE {namespace: 'deity'})
OPTIONAL MATCH (sb)-[:TAGGED_WITH]->(gek:TAG_VALUE {namespace: 'gek'})
OPTIONAL MATCH (sb)-[:TAGGED_WITH]->(geok:TAG_VALUE {namespace: 'geok-t'})
RETURN sb.id,
       CASE WHEN gea IS NOT NULL THEN '✓' ELSE '✗' END AS has_gea,
       CASE WHEN deity IS NOT NULL THEN '✓' ELSE '✗' END AS has_deity,
       CASE WHEN gek IS NOT NULL THEN '✓' ELSE '✗' END AS has_gek,
       CASE WHEN geok IS NOT NULL THEN '✓' ELSE '✗' END AS has_geok
```

---

## TAG UPDATE PROPAGATION

When a tag is updated or deprecated:

```yaml
update_protocol:
  1_mark_deprecated:
    - Set tag.deprecated = true
    - Set tag.replaced_by = new_tag_id
    - Set tag.deprecated_at = timestamp

  2_find_affected:
    - Query all TAG_INSTANCE with this tag
    - Generate report of affected content

  3_notify:
    - Log to tag_changes.log
    - Add to validation queue

  4_migrate (optional):
    - If auto_migrate = true
    - Create new TAG_INSTANCE with replacement tag
    - Mark old instance as migrated

  5_validate:
    - Run validation rules on affected content
    - Report any new violations
```

---

## SHAPE BIOGRAPHY TAG CHECKLIST

For each element in the Shape Biography, verify:

### Circle (SB_MESO_CIRCLE_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.circle | ☐ | ☐ |
| GEM | gem.rosette, gem.wheel_axle | ☐ | ☐ |
| GEK | gek.symmetry.radial | ☐ | ☐ |
| GEU | geu.solar_disk | ☐ | ☐ |
| GEOK-T | geok-t.rotation | ☐ | ☐ |
| Deity | deity.meso.shamash | ☐ | ☐ |
| Carriers | CARR__SUN_DISK, CARR__WHEEL, CARR__AXLE, CARR__SEAL | ☐ | ☐ |
| Inventions | INV__POTTER_WHEEL, INV__WHEEL_AND_AXLE, INV__CYLINDER_SEAL | ☐ | ☐ |
| Artifacts | British Museum, Louvre, Penn | ☐ | ☐ |

### 8-Pointed Star (SB_MESO_STAR8_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.star8 | ☐ | ☐ |
| GEM | gem.star_polygon, gem.rosette_n | ☐ | ☐ |
| GEK | gek.symmetry.radial | ☐ | ☐ |
| GEU | geu.star8 | ☐ | ☐ |
| GEOK-T | geok-t.rotation, geok-t.projection | ☐ | ☐ |
| Deity | deity.meso.ishtar | ☐ | ☐ |
| Carriers | CARR__ISHTAR_STAR, CARR__VENUS_SYMBOL, CARR__GATE_DECORATION | ☐ | ☐ |
| Inventions | INV__COMPASS_ROSE, INV__ASTRONOMICAL_OBSERVATION | ☐ | ☐ |

### Crescent/Arc (SB_MESO_CRESCENT_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.arc | ☐ | ☐ |
| GEM | gem.arch | ☐ | ☐ |
| GEK | gek.angle.sum.triangle | ☐ | ☐ |
| GEU | — | ☐ | ☐ |
| GEOK-T | geok-t.rotation | ☐ | ☐ |
| Deity | deity.meso.nanna | ☐ | ☐ |
| Carriers | CARR__CRESCENT_MOON, CARR__LUNAR_BOAT | ☐ | ☐ |
| Inventions | INV__LUNAR_CALENDAR, INV__ECLIPSE_PREDICTION | ☐ | ☐ |

### Triangle (SB_MESO_TRIANGLE_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.triangle | ☐ | ☐ |
| GEM | gem.truss | ☐ | ☐ |
| GEK | gek.angle.sum.triangle, gek.stability.triangulation | ☐ | ☐ |
| GEU | — | ☐ | ☐ |
| GEOK-T | geok-t.scaling | ☐ | ☐ |
| Deity | deity.meso.enlil | ☐ | ☐ |
| Carriers | CARR__ZIGGURAT_PROFILE, CARR__RAMP | ☐ | ☐ |
| Inventions | INV__ZIGGURAT_CONSTRUCTION, INV__SURVEYING_TRIANGULATION | ☐ | ☐ |

### Square (SB_MESO_SQUARE_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.square | ☐ | ☐ |
| GEM | gem.grid | ☐ | ☐ |
| GEK | gek.area.rectangle | ☐ | ☐ |
| GEU | — | ☐ | ☐ |
| GEOK-T | geok-t.tessellation | ☐ | ☐ |
| Deity | deity.meso.nabu | ☐ | ☐ |
| Carriers | CARR__TABLET, CARR__BRICK | ☐ | ☐ |
| Inventions | INV__CUNEIFORM_TABLET, INV__STANDARDIZED_BRICK, INV__CITY_GRID_PLANNING | ☐ | ☐ |

### Spiral (SB_MESO_SPIRAL_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.spiral | ☐ | ☐ |
| GEM | gem.helix | ☐ | ☐ |
| GEK | — | ☐ | ☐ |
| GEU | geu.spiral | ☐ | ☐ |
| GEOK-T | geok-t.spiraling | ☐ | ☐ |
| Deity | deity.meso.tiamat | ☐ | ☐ |
| Carriers | CARR__SERPENT_COIL | ☐ | ☐ |
| Inventions | INV__COILED_CONSTRUCTION | ☐ | ☐ |

### Hexagon (SB_MESO_HEXAGON_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.hexagon | ☐ | ☐ |
| GEM | gem.tessellation | ☐ | ☐ |
| GEK | gek.efficiency.packing | ☐ | ☐ |
| GEU | — | ☐ | ☐ |
| GEOK-T | geok-t.tessellation | ☐ | ☐ |
| Deity | deity.meso.nisaba | ☐ | ☐ |
| Carriers | CARR__GRAIN_MOTIF | ☐ | ☐ |
| Inventions | INV__EFFICIENT_STORAGE, INV__FIELD_SURVEYING | ☐ | ☐ |

### Pyramid (SB_MESO_PYRAMID_V1)

| Tag Category | Required | Present | Valid |
|--------------|----------|---------|-------|
| GEA | gea.pyramid | ☐ | ☐ |
| GEM | gem.truss | ☐ | ☐ |
| GEK | gek.stability.triangulation, gek.force.compression | ☐ | ☐ |
| GEU | — | ☐ | ☐ |
| GEOK-T | geok-t.scaling | ☐ | ☐ |
| Deity | deity.meso.marduk | ☐ | ☐ |
| Carriers | CARR__ZIGGURAT | ☐ | ☐ |
| Inventions | INV__ZIGGURAT_TEMPLE, INV__STEPPED_DRAINAGE, INV__AGRICULTURAL_TERRACE | ☐ | ☐ |

---

## IMPLEMENTATION: GRAPH NODE SCRIPT

```javascript
// tag-validation-graph.js
// Creates graph nodes for tag validation system

const TAG_NAMESPACES = [
  { id: 'ns_gea', name: 'GEA - Atomic Elements', prefix: 'gea.' },
  { id: 'ns_gem', name: 'GEM - Molecular Composites', prefix: 'gem.' },
  { id: 'ns_gek', name: 'GEK - Conceptual', prefix: 'gek.' },
  { id: 'ns_geu', name: 'GEU - Ubiquitous', prefix: 'geu.' },
  { id: 'ns_geok_t', name: 'GEOK-T - Transformations', prefix: 'geok-t.' },
  { id: 'ns_deity', name: 'Deity', prefix: 'deity.' },
  { id: 'ns_carrier', name: 'Carrier', prefix: 'CARR__' },
  { id: 'ns_invention', name: 'Invention', prefix: 'INV__' },
];

function validateShapeBio(shapeBioId, tags) {
  const errors = [];
  const warnings = [];

  // Rule 1: Required namespaces
  const requiredNamespaces = ['gea', 'deity', 'geok-t'];
  for (const ns of requiredNamespaces) {
    const hasTag = tags.some(t => t.startsWith(ns + '.') || t.startsWith(ns.toUpperCase() + '__'));
    if (!hasTag) {
      errors.push(`Missing required tag namespace: ${ns}`);
    }
  }

  // Rule 2: Deity-Element consistency
  const deityTag = tags.find(t => t.startsWith('deity.meso.'));
  const geaTag = tags.find(t => t.startsWith('gea.'));
  if (deityTag && geaTag) {
    const expectedElement = DEITY_ELEMENT_MAP[deityTag];
    if (expectedElement && expectedElement !== geaTag) {
      errors.push(`Deity ${deityTag} expects element ${expectedElement}, but found ${geaTag}`);
    }
  }

  // Rule 3: At least one carrier
  const hasCarrier = tags.some(t => t.startsWith('CARR__'));
  if (!hasCarrier) {
    warnings.push('No carrier tag found');
  }

  // Rule 4: At least one invention
  const hasInvention = tags.some(t => t.startsWith('INV__'));
  if (!hasInvention) {
    warnings.push('No invention tag found');
  }

  return { shapeBioId, valid: errors.length === 0, errors, warnings };
}

const DEITY_ELEMENT_MAP = {
  'deity.meso.shamash': 'gea.circle',
  'deity.meso.ishtar': 'gea.star8',
  'deity.meso.nanna': 'gea.arc',
  'deity.meso.enlil': 'gea.triangle',
  'deity.meso.nabu': 'gea.square',
  'deity.meso.tiamat': 'gea.spiral',
  'deity.meso.nisaba': 'gea.hexagon',
  'deity.meso.marduk': 'gea.pyramid',
};

module.exports = { validateShapeBio, TAG_NAMESPACES, DEITY_ELEMENT_MAP };
```

---

## VERSION HISTORY

| Date | Change | Author |
|------|--------|--------|
| 2026-01-22 | Created tag validation graph system | System |

---

**END SSOT-017**

---

## UNKNOWN TAG HANDLING (NOVELTY INTAKE)

When a tag is unrecognized:
- Preserve it as-is in content
- Create/attach a `TAG_VALUE` node with `deprecated: false` and `status: unknown`
- Attach `flag.tag_unknown` and route to Novelty Intake for later taxonomy expansion