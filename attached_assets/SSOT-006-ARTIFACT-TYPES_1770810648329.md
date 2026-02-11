# SSOT-006: ARTIFACT TYPES
version: 5.0.0
generated_at: 2026-02-02


## Overview

Classification system for material culture objects used in curriculum.
Primary use: A4 sub-section selection (which categories of objects carry the element).
Each type has: definition, semiotic function, example objects, typical museum sources.

---

## ARTIFACT TYPE SCHEMA

```yaml
artifact_type:
  id: string           # art.sacred, art.ritual, etc.
  name: string         # Display name
  section_code: string # A4a, A4b, etc.
  
  definition: string   # What objects belong here
  semiotic_function: string  # How element functions as sign
  
  typical_objects: []  # Examples
  museum_sources: []   # Where to find these
  
  context_questions:   # Questions students should ask
    - question: string
    
  NOT_this_type: []    # Common misclassifications
```

---

## ARTIFACT TYPES

### SACRED/CEREMONIAL OBJECTS (A4a)

| Field | Value |
|-------|-------|
| **ID** | `art.sacred` |
| **Name** | Sacred/Ceremonial Objects |
| **Section Code** | A4a |

**Definition:**
Objects created specifically for religious/divine purposes. Used in worship, offerings, or representing deities. NOT everyday items that happen to be in temples.

**Semiotic Function:**
Element signals **divine significance** — marks object as belonging to or representing the deity's domain.

**Typical Objects:**
| Object Type | Example | Element Use |
|-------------|---------|-------------|
| Cult statues | Statue of deity | Element on deity's attribute |
| Votive offerings | Dedicatory plaques | Element marks sacred dedication |
| Divine symbols | Sun disk, star rosette | Element IS the symbol |
| Sacred vessels | Libation cups | Element marks divine recipient |
| Amulets/talismans | Protective charms | Element invokes divine protection |
| Altars | Offering tables | Element marks sacred space |

**Museum Sources:**
- British Museum (Mesopotamian galleries)
- Louvre (Ancient Near East)
- Metropolitan Museum of Art (Ancient Near East)
- Penn Museum
- Yale Babylonian Collection

**Context Questions:**
- Who was this object made for? (deity)
- What ritual would use this object?
- How does the element mark it as sacred?
- Why would putting this element here invoke the deity?

**NOT This Type:**
- Administrative seals (→ official)
- Temple inventory records (→ official)
- Jewelry worn by priests (→ personal)
- Temple architectural elements (→ architectural)

---

### RITUAL CONTEXT (A4b)

| Field | Value |
|-------|-------|
| **ID** | `art.ritual` |
| **Name** | Ritual Context |
| **Section Code** | A4b |

**Definition:**
Objects used IN ceremonies, festivals, or religious practices. Focus on the ACTION/EVENT, not the object alone. May include spaces, processions, performances.

**Semiotic Function:**
Element signals **ceremonial significance** — marks moment, action, or space as ritually important.

**Typical Objects/Contexts:**
| Context Type | Example | Element Use |
|--------------|---------|-------------|
| Processional items | Standards, banners | Element leads/marks procession |
| Festival gear | Ceremonial clothing, masks | Element identifies participant role |
| Ritual instruments | Music instruments, censers | Element on tools of worship |
| Sacred spaces | Shrines, holy of holies | Element marks boundary/threshold |
| Burial goods | Grave offerings | Element ensures divine reception |
| Sacrifice implements | Ritual blades, basins | Element marks sacred purpose |

**Museum Sources:**
- Archaeological site documentation
- British Museum (ritual objects)
- University museums with excavation collections
- Published excavation reports

**Context Questions:**
- What ceremony used this object?
- Who participated in the ritual?
- When/where did this ritual happen?
- How does the element change the action's meaning?

**NOT This Type:**
- Static cult images (→ sacred)
- Temple building plans (→ architectural)
- Records OF rituals (→ official)

---

### OFFICIAL/ADMINISTRATIVE OBJECTS (A4c)

| Field | Value |
|-------|-------|
| **ID** | `art.official` |
| **Name** | Official/Administrative Objects |
| **Section Code** | A4c |

**Definition:**
Objects used for governance, record-keeping, commerce, law, or state functions. Element signals authenticity, authority, or official status.

**Semiotic Function:**
Element signals **authority/authenticity** — marks object/document as legitimate, verified, state-sanctioned.

**Typical Objects:**
| Object Type | Example | Element Use |
|-------------|---------|-------------|
| Cylinder seals | Administrative seals | Element = owner/authority mark |
| Royal inscriptions | Steles, boundary stones | Element = divine sanction |
| Legal documents | Contracts, treaties | Element = witnessed/verified |
| Weights/measures | Standard weights | Element = official standard |
| Coinage/tokens | Trade markers | Element = value guarantee |
| Royal regalia | Crowns, scepters | Element = legitimate rule |

**Museum Sources:**
- British Museum (cuneiform collection)
- Yale Babylonian Collection (tablets)
- Louvre (steles, royal art)
- University collections (cylinder seals)

**Context Questions:**
- Who issued this object?
- What authority does the element represent?
- How did the element verify authenticity?
- What happens to documents without this element?

**NOT This Type:**
- Personal letters (→ domestic, unless official correspondence)
- Religious dedications by officials (→ sacred)
- Royal jewelry worn privately (→ personal)

---

### DOMESTIC/EVERYDAY OBJECTS (A4d)

| Field | Value |
|-------|-------|
| **ID** | `art.domestic` |
| **Name** | Domestic/Everyday Objects |
| **Section Code** | A4d |

**Definition:**
Objects used in daily life, home, work, or common activities. Element appears in vernacular contexts, suggesting widespread cultural meaning.

**Semiotic Function:**
Element signals **daily/cultural significance** — marks object as connected to cosmic/divine order even in ordinary use.

**Typical Objects:**
| Object Type | Example | Element Use |
|-------------|---------|-------------|
| Pottery/ceramics | Bowls, jars, vessels | Element decorates rim/body |
| Household tools | Spindle whorls, loom weights | Element on functional items |
| Furniture | Chair backs, boxes | Element decorates surfaces |
| Textiles | Woven patterns, borders | Element in design |
| Food prep | Grinding stones, ovens | Element on work surfaces |
| Children's items | Toys, cradles | Element provides protection |

**Museum Sources:**
- Archaeological site reports
- University museums (excavation collections)
- Regional/local history museums
- Published domestic archaeology studies

**Context Questions:**
- Who used this object every day?
- Why put a sacred symbol on a cooking pot?
- How did the element protect/bless daily life?
- What does widespread use tell us about the element's meaning?

**NOT This Type:**
- Luxury goods for elite (context-dependent)
- Temple inventory items (→ sacred/official)
- Trade goods with marks (→ official)

---

### ARCHITECTURAL ELEMENTS (A4e)

| Field | Value |
|-------|-------|
| **ID** | `art.architectural` |
| **Name** | Architectural Elements |
| **Section Code** | A4e |

**Definition:**
Building components: walls, gates, columns, floors, ceilings, foundations. Element appears on structures themselves.

**Semiotic Function:**
Element signals **spatial significance** — marks threshold, boundary, sacred space, protected zone, or structural feature.

**Typical Objects:**
| Object Type | Example | Element Use |
|-------------|---------|-------------|
| Gates/doorways | Ishtar Gate | Element marks transition |
| Wall decorations | Glazed brick reliefs | Element marks sacred boundary |
| Floor patterns | Mosaic, tile | Element defines space |
| Columns/pillars | Capital decorations | Element supports structure |
| Foundations | Foundation deposits | Element blesses/protects |
| Roof elements | Drain spouts, finials | Element crowns structure |

**Museum Sources:**
- Pergamon Museum (Ishtar Gate, Processional Way)
- British Museum (architectural fragments)
- Site photographs and reconstructions
- Published architectural studies

**Context Questions:**
- What kind of building has this element?
- What does entering through this element mean?
- How does the element mark inside vs. outside?
- Why protect this particular location?

**NOT This Type:**
- Portable shrines (→ sacred)
- Building dedication texts (→ official)
- Objects FOUND in buildings (categorize by object type)

---

### PERSONAL/WEARABLE (A4f)

| Field | Value |
|-------|-------|
| **ID** | `art.personal` |
| **Name** | Personal/Wearable |
| **Section Code** | A4f |

**Definition:**
Objects worn on the body or carried personally. Element marks individual's connection to divine, status, or protection.

**Semiotic Function:**
Element signals **individual significance** — marks wearer's identity, protection, status, or devotion.

**Typical Objects:**
| Object Type | Example | Element Use |
|-------------|---------|-------------|
| Jewelry | Necklaces, earrings, rings | Element as pendant/decoration |
| Amulets | Protective pendants | Element invokes deity |
| Seals (personal) | Individual cylinder seals | Element identifies owner |
| Clothing fasteners | Pins, fibulae | Element decorates functional item |
| Hair ornaments | Combs, pins | Element adorns person |
| Cosmetic items | Mirror backs, applicators | Element beautifies ritual |

**Museum Sources:**
- Metropolitan Museum of Art (jewelry collections)
- British Museum (jewelry, seals)
- University museums
- Published burial/grave good studies

**Context Questions:**
- Who wore this object?
- What protection or status did the element give?
- How does wearing the element connect person to deity?
- Was this everyday wear or special occasion?

**NOT This Type:**
- Royal regalia (→ official, unless worn informally)
- Priestly vestments (→ ritual/sacred)
- Grave goods (→ ritual, unless specifically personal items)

---

## TYPE SELECTION LOGIC FOR A4

### Guardrails (from SSOT-002)
- Must select ≥2 types per lesson
- Each type must have DIFFERENT artifact
- Each artifact must be NAMED specifically
- Each must have DIFFERENT semiotic function

### Selection Questions

1. **What categories of objects carry this element in this civilization?**
   - List all attested categories from archaeological record

2. **Which categories show DIFFERENT meanings?**
   - Select types where element signals different things
   - Example: Circle on seal (authority) vs. circle on bowl (cosmic order)

3. **Which categories have accessible artifacts?**
   - Prioritize categories with museum images available
   - Check Creative Commons / Open Access status

4. **Which categories maximize cultural spread?**
   - Select types that show element across society
   - Elite + common, sacred + secular when possible

### Example Selection (Circle/Shamash)

| Type | Artifact | Semiotic Function | Different? |
|------|----------|-------------------|------------|
| A4a (sacred) | Code of Hammurabi stele | Divine authority over law | ✓ |
| A4c (official) | Cylinder seal of official X | Authentication/verification | ✓ Different from A4a |
| A4d (domestic) | Ceramic bowl with rim band | Cosmic order in daily life | ✓ Different from above |
| A4e (architectural) | Temple doorway with disk | Sacred threshold | ✓ Different from above |

**Valid:** 4 types, 4 different named artifacts, 4 different functions

### Invalid Selection Example

| Type | Artifact | Issue |
|------|----------|-------|
| A4a | "Sacred objects" | ❌ Plural, not specific |
| A4c | "Official seals" | ❌ Plural, not specific |
| A4a | Another sacred object | ❌ Repeat category |

---

## ARTIFACT RECORD TEMPLATE

When documenting an artifact for curriculum use:

```yaml
artifact:
  name: "Code of Hammurabi Stele"
  id: art.meso.hammurabi_stele
  
  type: sacred          # A4 category
  type_code: A4a
  
  element: circle
  element_location: "Header relief, sun disk behind Shamash"
  
  semiotic_function: "Signals divine sanction of laws"
  
  civilization: mesopotamia
  period: "Old Babylonian (c. 1792-1750 BCE)"
  
  current_location:
    museum: Louvre
    accession: Sb 8
    gallery: "Ancient Near East, Ground Floor"
  
  image:
    source: "Wikimedia Commons"
    license: "Public Domain"
    url: "[URL]"
  
  curriculum_use:
    lesson: MESO-W1
    section: A4a
    lo_text: "Circle signals divine judgment on the Code of Hammurabi stele because header placement marks Shamash's authority over laws"
```

---

## TYPE QUICK REFERENCE

| Code | Type | Semiotic Function | Key Question |
|------|------|-------------------|--------------|
| A4a | Sacred/Ceremonial | Divine significance | Made for deity? |
| A4b | Ritual Context | Ceremonial significance | Used in ceremony? |
| A4c | Official/Administrative | Authority/authenticity | State-sanctioned? |
| A4d | Domestic/Everyday | Daily/cultural significance | Used at home? |
| A4e | Architectural | Spatial significance | Part of building? |
| A4f | Personal/Wearable | Individual significance | Worn on body? |