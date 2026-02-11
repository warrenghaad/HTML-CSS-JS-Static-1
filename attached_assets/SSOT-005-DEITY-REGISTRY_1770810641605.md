# SSOT-005: DEITY REGISTRY
version: 5.0.0
generated_at: 2026-02-02


## Overview

Master list of deities used in curriculum.
Each deity has: civilization, domains, symbols, element pairings, key myths, artifacts.

---

## DEITY SCHEMA

```yaml
deity:
  id: string              # deity.meso.shamash
  name: string            # Display name
  alt_names: []           # Other names/spellings
  civilization: string    # mesopotamia, egypt, greece, etc.
  
  domains: []             # What they rule over
  symbols: []             # Visual identifiers
  element_pairing: string # Primary geometric element
  
  key_myths: []           # Stories used in curriculum
  key_artifacts: []       # Objects depicting this deity
  
  sel_themes: []          # Social-emotional connections
  invention_links: []     # STEM discoveries connected to deity
  
  iconography:            # How to recognize in art
    - feature: string
    - meaning: string
```

---

## MESOPOTAMIAN DEITIES

### SHAMASH

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.shamash` |
| **Name** | Shamash |
| **Alt Names** | Utu (Sumerian) |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Circle |

**Domains:**
- Sun
- Justice
- Truth
- Divination
- Law

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Sun disk with rays | Divine radiance, equal reach |
| Saw | Cutting through deception |
| Rod and ring | Measurement, authority |
| Rays emerging from shoulders | Dawn emergence |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Shamash gives laws to Hammurabi | Justice requires equal application | A1 |
| Shamash crosses the sky | Daily cycle, predictable path | A3 |
| Shamash sees all from above | Equal vision in all directions | A2 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Code of Hammurabi stele (top) | Louvre | A4a (sacred) |
| Tablet of Shamash (Sippar) | British Museum | A3 (iconography) |
| Cylinder seals with sun disk | Various | A4c (official) |
| Chariot wheel fragments | Various | A7/B1 (bridge) |

**SEL Themes:**
- Fairness in group work
- Consistent rules for everyone
- Seeing all perspectives equally

**Invention Links:**
- Wheel (rotation from equidistance)
- Sundial (tracking sun position)
- Standardized measurement

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Radial rays | Lines extending equally from disk or shoulders |
| Seated pose | Typically enthroned |
| Petitioners below | Smaller figures approaching |
| Mountain emergence | Rising between two peaks |

---

### ISHTAR/INANNA

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.ishtar` |
| **Name** | Ishtar |
| **Alt Names** | Inanna (Sumerian) |
| **Civilization** | Mesopotamia |
| **Element Pairing** | 8-pointed Star |

**Domains:**
- Love/sexuality
- War
- Venus (planet)
- Fertility
- Political power

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| 8-pointed star | Venus, divine radiance |
| Lion | War aspect, ferocity |
| Rosette | Fertility, beauty |
| Gate/door | Liminal power, transitions |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Descent to Underworld | Journey through 7 gates, transformation | A1 |
| Ishtar and Dumuzi | Love, loss, seasonal cycle | A2 |
| Ishtar's star guides travelers | Navigation, protection | B5/B6 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Ishtar Gate | Pergamon Museum | A7/B1 (bridge) |
| Queen of the Night relief | British Museum | A3 (iconography) |
| Star rosettes on glazed bricks | Various | A4e (architectural) |
| Lion of Babylon | Various | A4a (sacred) |

**SEL Themes:**
- Navigating strong emotions
- Finding guidance when lost
- Transformation through difficulty

**Invention Links:**
- Compass rose (8-point navigation)
- Astronomical observation (Venus tracking)
- Calendar systems (Venus cycle)

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| 8-pointed star | Usually above or near figure |
| Wings | Indicates divine status |
| Lions | Often flanking or beneath |
| Weapons | Mace, bow (war aspect) |
| Nude figure | Fertility aspect |

---

### ENLIL

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.enlil` |
| **Name** | Enlil |
| **Alt Names** | Ellil |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Triangle |

**Domains:**
- Wind/air
- Storms
- Authority/kingship
- Destiny (tablets of)
- Earth/heaven separation

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Horned crown (7 horns) | Divine authority |
| Mountain | His dwelling at Nippur |
| Storm clouds | Power over elements |
| Tablets of Destiny | Control of fate |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Enlil separates heaven and earth | Creation of stable order | A1 |
| Enlil causes the flood | Power of natural forces | A2 |
| Enlil grants kingship | Authority derives from divine | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Ziggurat of Enlil at Nippur | Site/reconstructions | A4e (architectural) |
| Horned crown depictions | Various | A3 (iconography) |
| Royal inscriptions mentioning Enlil | Various | A4c (official) |

**SEL Themes:**
- Respecting authority
- Understanding consequences
- Stability through structure

**Invention Links:**
- Triangular structural supports
- Roof trusses
- Measuring angles for construction

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Horned crown | Multiple horn tiers |
| Seated on throne | Authority pose |
| Mountain base | Dwelling reference |
| Rarely shown directly | Often represented by symbols only |

---

### NABU

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.nabu` |
| **Name** | Nabu |
| **Alt Names** | Nebo |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Square/Rectangle |

**Domains:**
- Writing/scribes
- Wisdom
- Literacy
- Vegetation
- Prophecy

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Stylus | Writing tool |
| Clay tablet | Writing surface |
| Wedge mark | Cuneiform |
| Dragon-snake | Sacred animal |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Nabu records fates | Writing preserves truth | A1 |
| Nabu as Marduk's son | Knowledge serves power | A2 |
| Scribes as Nabu's servants | Profession as sacred duty | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Cuneiform tablets | British Museum, Yale | A4c (official), A7/B1 |
| Stylus examples | Various | A5a (technique) |
| E-zida temple remains | Site | A4e (architectural) |
| Nabu statues | Various | A3 (iconography) |

**SEL Themes:**
- Value of communication
- Recording and remembering
- Precision and care

**Invention Links:**
- Writing systems (cuneiform)
- Record-keeping
- Standardized measurements on tablets

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Stylus in hand | Held upright |
| Tablet in other hand | Rectangular |
| Scribal posture | Often standing or seated at work |
| Dragon-snake | At feet or nearby |

---

### TIAMAT

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.tiamat` |
| **Name** | Tiamat |
| **Alt Names** | — |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Spiral |

**Domains:**
- Primordial chaos
- Salt water/sea
- Creation (from her body)
- Dragons/monsters

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Serpent/dragon | Chaos, power |
| Waves | Primordial waters |
| Spiral | Churning chaos |
| Monsters | Her creations |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Tiamat vs. Marduk | Chaos overcome by order | A1 |
| World from Tiamat's body | Destruction yields creation | A2 |
| Tiamat's monster army | Creative potential in chaos | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Chaos monster depictions | Various | A3 (iconography) |
| Spiral decorations | Various | A4d (domestic) |
| Cylinder seals with combat myth | British Museum | A4a (sacred) |

**SEL Themes:**
- Managing overwhelming emotions
- Order from chaos
- Creative potential in difficulty

**Invention Links:**
- Spiral mechanisms (springs, scrolls)
- Water management (canals, drainage)
- Coiled rope storage

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Serpentine body | Long, coiling |
| Multiple heads (sometimes) | Dragon variants |
| Marduk combat scene | Usually being defeated |
| Water/waves | Background element |

---

### ANU

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.anu` |
| **Name** | Anu |
| **Alt Names** | An (Sumerian) |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Arc/Curve |

**Domains:**
- Sky/heavens
- Kingship of gods
- Cosmic order
- Stars

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Horned crown | Supreme divine authority |
| Sky vault/dome | Heavenly realm |
| Stars | His domain |
| Throne | Kingship |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Anu as father of gods | Origin of cosmic order | A1 |
| Anu's distant heaven | Sky as protective dome | A2 |
| Anu grants divine weapons | Authority transferred | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Arched doorways/gates | Various sites | A4e (architectural) |
| Sky band depictions | Various | A3 (iconography) |
| Star maps/planispheres | British Museum | A4c (official) |

**SEL Themes:**
- Looking at the big picture
- Protection from above
- Order in the universe

**Invention Links:**
- Arch construction
- Dome building
- Astronomical observation

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Rarely depicted directly | Usually symbolized |
| Sky band | Curved line with stars |
| Horned crown (highest tier) | Most horns = highest rank |
| Stars | Within curved band |

---

### NISABA

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.nisaba` |
| **Name** | Nisaba |
| **Alt Names** | Nidaba |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Hexagon |

**Domains:**
- Grain/harvest
- Writing (early)
- Surveying
- Accounting
- Wisdom

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Grain stalk | Harvest, abundance |
| Measuring rod | Surveying, boundaries |
| Stylus (early period) | Writing |
| Stars on head | Divine wisdom |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Nisaba measures the fields | Land division, fairness | A1 |
| Nisaba counts the grain | Abundance through order | A2 |
| Nisaba teaches scribes | Wisdom transmitted | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Grain storage vessels | Various | A4d (domestic) |
| Field survey tablets | Various | A4c (official) |
| Hexagonal patterns in temples | Various sites | A4e (architectural) |

**SEL Themes:**
- Fairness in sharing
- Planning and organization
- Patience yields abundance

**Invention Links:**
- Land surveying (hexagonal grids)
- Efficient storage
- Agricultural planning

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Grain in hand/crown | Stalks visible |
| Measuring tools | Rod, cord |
| Seated scribe pose | Writing tablets nearby |
| Stars | On headdress |

---

### MARDUK

| Field | Value |
|-------|-------|
| **ID** | `deity.meso.marduk` |
| **Name** | Marduk |
| **Alt Names** | Bel (Lord) |
| **Civilization** | Mesopotamia |
| **Element Pairing** | Pyramid/Ziggurat |

**Domains:**
- Chief deity (Babylon)
- Creation
- Justice
- Magic/wisdom
- Storm

**Symbols:**
| Symbol | Meaning |
|--------|---------|
| Mushussu dragon | Sacred animal |
| Spade/hoe | Creation of world |
| Bow | Storm weapon |
| Ziggurat | His temple Esagila |

**Key Myths:**
| Myth | Curriculum Use | Section |
|------|----------------|---------|
| Marduk defeats Tiamat | Order from chaos | A1 |
| Marduk creates humanity | Purpose through creation | A2 |
| Marduk raises Babylon | Monumental achievement | A3 |

**Key Artifacts:**
| Artifact | Museum | Use |
|----------|--------|-----|
| Mushussu dragon reliefs | Pergamon Museum | A3 (iconography) |
| Ziggurat of Babylon (Etemenanki) | Reconstructions | A4e, A7/B1 |
| Marduk statue descriptions | Texts | A4a (sacred) |
| Processional Way decorations | Pergamon Museum | A4e (architectural) |

**SEL Themes:**
- Rising to challenges
- Building something great
- Leadership through achievement

**Invention Links:**
- Monumental architecture
- Pyramid/ziggurat construction
- Urban planning

**Iconography Guide:**
| Feature | How to Identify |
|---------|-----------------|
| Mushussu dragon | Snake-dragon hybrid |
| Spade symbol | Triangular tool |
| Horned crown | High-ranking deity |
| Associated with Babylon | Processional context |

---

## DEITY QUICK REFERENCE (MESOPOTAMIA)

| ID | Name | Element | Primary Domain | Key Symbol |
|----|------|---------|----------------|------------|
| deity.meso.shamash | Shamash | Circle | Sun/Justice | Sun disk |
| deity.meso.ishtar | Ishtar | 8-Star | Love/War/Venus | 8-pointed star |
| deity.meso.enlil | Enlil | Triangle | Wind/Authority | Horned crown |
| deity.meso.nabu | Nabu | Square | Writing/Wisdom | Stylus & tablet |
| deity.meso.tiamat | Tiamat | Spiral | Chaos/Sea | Serpent |
| deity.meso.anu | Anu | Arc | Sky/Heaven | Sky vault |
| deity.meso.nisaba | Nisaba | Hexagon | Grain/Surveying | Grain stalk |
| deity.meso.marduk | Marduk | Pyramid | Chief deity | Mushussu dragon |

---

## DEITY-ELEMENT LOGIC

Each pairing follows this logic:
1. **Visual match** — Deity's symbol contains the element
2. **Domain match** — Deity's power relates to element's function
3. **Metaphor match** — Deity's meaning aligns with element's symbolism

| Deity | Element | Visual | Domain | Metaphor |
|-------|---------|--------|--------|----------|
| Shamash | Circle | Sun disk | Equal judgment | Fairness = equal distance |
| Ishtar | 8-Star | Star symbol | Venus/navigation | Guidance = directional rays |
| Enlil | Triangle | Mountain peak | Stability | Authority = structural support |
| Nabu | Square | Tablet shape | Writing | Order = gridded organization |
| Tiamat | Spiral | Coiling serpent | Chaos waters | Primordial = progressive expansion |
| Anu | Arc | Sky vault | Heavens | Protection = spanning coverage |
| Nisaba | Hexagon | Grain patterns | Agriculture | Efficiency = optimal packing |
| Marduk | Pyramid | Ziggurat | Supremacy | Ascension = convergent stability |