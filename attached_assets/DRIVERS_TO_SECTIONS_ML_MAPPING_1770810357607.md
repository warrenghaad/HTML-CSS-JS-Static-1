# MAGIC Drivers → Lesson Section Mapping

## Machine Learning Ontology for Global Cultural Motif Recognition

**Version:** 1.0 (February 2026)  
**Purpose:** Create systematic driver-to-content mapping enabling ML pattern recognition across all human civilizations (prehistory to present, global scope)

---

## Core Architecture

### The Challenge

Create a tagging ontology that allows machine learning systems to:

1. **Recognize driver patterns** in unmarked cultural artifacts
2. **Identify geometric motifs** even without explicit labeling
3. **Detect convergence moments** (discovery vs invention signatures)
4. **Compare across civilizations** finding universal vs culturally-specific patterns
5. **Predict missing connections** based on partial information
   **Mathematical Developments:** Number systems, calculations, proofs, and concepts
   6.- **Geometric & Artistic Achievements:** Visual arts, architecture, patterns, design principles
6. **Myths & Narratives:** Stories that shaped cultural understanding
7. **Inventions & Discoveries:** Technological and scientific breakthroughs
8. **Power Structures:** How societies organized themselves
9. **Famous Persons:** Key figures to study (with brief biographies)
10. **Standards Alignment:** Which grade levels work best with this content
11. **Hands-On Projects:** Exit ticket ideas for each era
12. **SEL Connections:** Social-emotional learning opportunities

### The Solution

Map each lesson section to **driver weight vectors** that ML can learn from, creating a self-improving classification system.

---

## Driver Weight Vector System

### Notation

Each content section gets a driver profile:

```
[M, A, G, I, C] where values = 0.0 to 1.0
```

**Example:**

```
"Shamash Circle Mythology" = [0.2, 0.7, 1.0, 0.9, 0.3]
```

Interpretation:

- M = 0.2 (low mathematical content, basic circle properties only)
- A = 0.7 (high aesthetic content, visual patterns discussed)
- G = 1.0 (geometric element is the subject)
- I = 0.9 (very high institutional/mythological content, Shamash as sun god)
- C = 0.3 (low power/control content, accessible knowledge)

---

## Day A / Day B Section Mapping

### Day A: GEpHR (Geometric Element as Metaphor)

**Primary drivers:** A + I (+ G always)  
**Typical weight profile:** [0.2-0.4, 0.7-0.9, 1.0, 0.7-0.9, 0.3-0.5]

**Content sections:**

#### Section 1: Mythological Context

**Driver weights:** [0.1, 0.6, 1.0, 0.9, 0.2]
**Tags:**

- `myth_primary`
- `deity_association`
- `symbolic_meaning`
- `cosmological_role`

**Example (Shamash/Circle):**
"Shamash was the sun god who traveled across the sky in a circular path each day, bringing justice and truth. His symbol was the sun disk - a perfect circle with rays."

**ML recognizable features:**

- Deity name mention → high I
- Astronomical description → moderate M
- Symbol description → high A + G
- Justice/truth language → high I (institutional values)
- Low power references → low C

---

#### Section 2: Cultural Aesthetic Patterns

**Driver weights:** [0.2, 0.9, 1.0, 0.5, 0.3]
**Tags:**

- `visual_pattern`
- `material_culture`
- `style_signature`
- `artifact_type`

**Example (Mesopotamian rosettes):**
"Mesopotamian artists loved creating rosette patterns - circles arranged in flower-like formations. These appeared on cylinder seals, palace walls, pottery, and jewelry. The repeating circular motifs felt 'right' to Mesopotamian eyes."

**ML recognizable features:**

- Pattern description → high A + G
- Multiple artifact types listed → high A (broad aesthetic application)
- "Felt right" language → moderate I (internalized aesthetics)
- Craftsmanship mentions → moderate M (technical skill)

---

#### Section 3: Symbolic/Ritual Use

**Driver weights:** [0.1, 0.5, 1.0, 0.9, 0.5]
**Tags:**

- `ritual_context`
- `ceremony_use`
- `belief_system`
- `sacred_geometry`

**Example (Temple placement):**
"Circles appeared in temple floor plans because they represented divine perfection. Priests would mark circular sacred spaces where only the initiated could enter during ceremonies honoring Shamash."

**ML recognizable features:**

- Temple/sacred space mention → high I
- "Only initiated" → moderate C (restricted access)
- "Divine perfection" → high I (theological significance)
- Geometric planning → moderate M

---

#### Section 4: Cross-Cultural Comparison

**Driver weights:** [0.3, 0.8, 1.0, 0.7, 0.2]
**Tags:**

- `comparative_analysis`
- `cultural_variation`
- `universal_vs_specific`
- `multiple_civilizations`

**Example (Circle symbolism globally):**
"While Mesopotamians saw circles as Shamash's sun disk, Egyptians saw Ra's solar barque, Greeks saw perfect divine proportion, and Native Americans saw the sacred hoop representing life cycles. Same geometry, different meanings."

**ML recognizable features:**

- Multiple civilization names → `cross_cultural` tag
- "Same geometry, different meanings" → universal GEK vs specific GEpHR distinction
- Variety in I driver (different belief systems)
- Consistent G (circle) across all

---

### Day B: GEK (Geometric Element as Knowledge/Concept)

**Primary drivers:** M + C (+ G always)  
**Typical weight profile:** [0.7-0.9, 0.3-0.5, 1.0, 0.3-0.5, 0.5-0.8]

**Content sections:**

#### Section 1: Mathematical Properties

**Driver weights:** [0.9, 0.2, 1.0, 0.2, 0.1]
**Tags:**

- `geometric_definition`
- `mathematical_properties`
- `formal_proof`
- `quantitative_analysis`

**Example (Circle definition):**
"A circle is the set of all points equidistant from a center point. The distance from center to edge is the radius (r). The distance across the circle through the center is the diameter (d = 2r). The distance around the circle is the circumference (C = πd)."

**ML recognizable features:**

- Formal definitions → very high M
- Mathematical notation → very high M
- Equations present → very high M
- No cultural context → low I, low C
- Pure geometric description → high G

---

#### Section 2: Historical Discovery Timeline

**Driver weights:** [0.7, 0.3, 1.0, 0.4, 0.6]
**Tags:**

- `innovation_history`
- `discovery_moment`
- `timeline_marker`
- `knowledge_development`

**Example (Circle applications timeline):**
"3500 BCE: Potter's wheel invented (Mesopotamia) - first rotational symmetry application  
3000 BCE: Circle geometry in megalith placement (Britain)  
2600 BCE: Accurate π approximation 3.125 (Egypt)  
600 BCE: Proof that π is irrational (Greece)"

**ML recognizable features:**

- Date stamps → `temporal_anchor`
- Civilization location tags → geographic distribution
- "Invented" vs "discovered" → invention vs discovery distinction
- Technical achievement language → moderate C (who had knowledge)
- Multiple M advances shown → increasing mathematical sophistication

---

#### Section 3: Functional Applications

**Driver weights:** [0.8, 0.4, 1.0, 0.2, 0.7]
**Tags:**

- `practical_use`
- `mechanical_function`
- `engineering_application`
- `problem_solving`

**Example (Potter's wheel mechanics):**
"The potter's wheel uses rotational symmetry to create perfectly round vessels. As the wheel spins, the clay naturally forms a circle because every point on the rim travels the same distance from the center. This mechanical property made pottery faster and more uniform."

**ML recognizable features:**

- Mechanical description → high M
- "Made faster" → efficiency gain (invention marker)
- Practical benefits → moderate C (economic value)
- Physics/motion description → high M
- Functional outcome → application vs pure theory

---

#### Section 4: Control and Access

**Driver weights:** [0.5, 0.2, 1.0, 0.5, 0.9]
**Tags:**

- `knowledge_restriction`
- `power_structure`
- `access_control`
- `beneficiary_analysis`

**Example (Who knew circles):**
"In early Mesopotamia, advanced circular geometry was controlled by the scribal class - priests who studied mathematics in temple schools. Farmers used simple circles for well-digging, but complex calculations (finding π, calculating circumference) were restricted knowledge. This created power imbalance: those who could calculate had economic advantage in trade, architecture, and astronomy."

**ML recognizable features:**

- Class/hierarchy mentions → very high C
- "Restricted knowledge" → very high C
- "Power imbalance" → very high C
- Economic advantage language → high C
- "Temple schools" → moderate I (institutional control)
- Distinction between simple vs complex applications → M gradient showing access tiers

---

## Composite Tag System for ML Training

### Element Tags (Geometric)

```
circle, triangle, square, rectangle, pentagon, hexagon, octagon,
rhombus, trapezoid, star_8pt, star_5pt, spiral, ellipse, parabola,
cube, cylinder, sphere, pyramid, ziggurat, cone, helix
```

### Civilization Tags (Geographic/Cultural)

```
mesopotamia, egypt, greece, rome, china, india, maya, aztec, inca,
islamic_golden_age, medieval_europe, sub_saharan_africa, polynesia,
aboriginal_australia, japan, korea, persia, phoenicia, celtic,
viking, pre_columbian_north_america, etc.
```

### Time Period Tags

```
paleolithic, neolithic, bronze_age, iron_age, classical_antiquity,
medieval, renaissance, enlightenment, industrial, modern, contemporary
```

### Driver Composite Tags

**These describe convergence patterns:**

```
MA_aesthetic_mathematical     → High M + High A convergence
MI_institutional_rigorous    → High M + High I convergence
MC_power_calculation         → High M + High C convergence
AI_symbolic_belief          → High A + High I convergence
AC_aesthetic_control        → High A + High C convergence
IC_institutional_power      → High I + High C convergence

MAIC_full_convergence       → All four drivers high (discovery/invention moment)
M_dominant                  → Math-led development
A_dominant                  → Aesthetic-led development
I_dominant                  → Belief/institution-led development
C_dominant                  → Power-led development
```

### Discovery vs Invention Tags

```
discovery_theoretical        → New mathematical understanding
discovery_aesthetic         → New pattern/form recognition
discovery_symbolic          → New metaphorical connection
invention_tool             → Physical implementation (wheel, compass)
invention_technique        → New method/process
invention_system           → Large-scale application (architecture, calendar)
```

---

## Section-by-Section Driver Mapping Template

### Lesson Week Template: [Geometric Element] + [Deity/Theme]

#### **DAY A: GEpHR Stream**

**Section A1: Mythological Introduction**

- Driver Profile: `[M:0.1, A:0.6, G:1.0, I:0.9, C:0.2]`
- Primary Tags: `myth_primary`, `deity_association`, `{civilization}`
- Content Type: Narrative storytelling
- ML Training Feature: "Deity names + geometric symbols = high I + moderate A"

**Section A2: Material Culture Survey**

- Driver Profile: `[M:0.2, A:0.9, G:1.0, I:0.5, C:0.3]`
- Primary Tags: `artifact_analysis`, `visual_pattern`, `{material_type}`
- Content Type: Image-heavy artifact examination
- ML Training Feature: "Multiple artifact types + pattern descriptions = high A + G"

**Section A3: Symbolic Meaning**

- Driver Profile: `[M:0.1, A:0.5, G:1.0, I:0.9, C:0.5]`
- Primary Tags: `sacred_geometry`, `ritual_use`, `belief_system`
- Content Type: Theological/philosophical explanation
- ML Training Feature: "Sacred/ritual language + access restrictions = high I + moderate C"

**Section A4: Cross-Cultural Comparison**

- Driver Profile: `[M:0.3, A:0.8, G:1.0, I:0.7, C:0.2]`
- Primary Tags: `comparative_analysis`, `cultural_variation`, `universal_pattern`
- Content Type: Multi-civilization synthesis
- ML Training Feature: "Multiple civilization tags + 'same/different' language = pattern recognition training"

---

#### **DAY B: GEK Stream**

**Section B1: Geometric Definitions**

- Driver Profile: `[M:0.9, A:0.2, G:1.0, I:0.2, C:0.1]`
- Primary Tags: `formal_definition`, `mathematical_properties`, `equations`
- Content Type: Technical mathematical instruction
- ML Training Feature: "Equations + formal language = very high M"

**Section B2: Properties & Relationships**

- Driver Profile: `[M:0.8, A:0.3, G:1.0, I:0.2, C:0.2]`
- Primary Tags: `geometric_proof`, `property_analysis`, `theorem`
- Content Type: Logical reasoning and proof
- ML Training Feature: "If-then structures + logical operators = high M deductive reasoning"

**Section B3: Historical Applications**

- Driver Profile: `[M:0.7, A:0.4, G:1.0, I:0.4, C:0.6]`
- Primary Tags: `invention_timeline`, `practical_application`, `engineering`
- Content Type: Historical innovation case studies
- ML Training Feature: "Dates + locations + 'invented/discovered' = timeline + innovation tracking"

**Section B4: Discovery Timeline**

- Driver Profile: `[M:0.7, A:0.3, G:1.0, I:0.3, C:0.7]`
- Primary Tags: `innovation_sequence`, `efficiency_gain`, `knowledge_development`
- Content Type: Chronological progression of sophistication
- ML Training Feature: "Sequential improvements + efficiency language = invention stacking pattern"

**Section B5: Inventions Enabled**

- Driver Profile: `[M:0.8, A:0.4, G:1.0, I:0.2, C:0.8]`
- Primary Tags: `mechanical_application`, `tool_creation`, `functional_benefit`
- Content Type: Functional mechanism explanation
- ML Training Feature: "Tool names + mechanical descriptions = invention identification"

**Section B6: Power & Access**

- Driver Profile: `[M:0.5, A:0.2, G:1.0, I:0.5, C:0.9]`
- Primary Tags: `knowledge_control`, `access_restriction`, `beneficiary_analysis`
- Content Type: Critical social analysis
- ML Training Feature: "Class/hierarchy terms + 'restricted/controlled' = very high C"

---

## Feature Extraction for ML Pattern Recognition

### Text-Based Features

**High M Indicators:**

- Mathematical notation: π, φ, √, ², ³, Σ, ∫
- Equations and formulas
- Measurement units: cubits, degrees, radians
- Quantitative comparisons: "3x larger", "50% more efficient"
- Logical operators: "if...then", "therefore", "because"
- Technical geometry terms: radius, diameter, circumference, area, volume, angle

**High A Indicators:**

- Visual pattern descriptions: "repeating", "symmetrical", "decorative"
- Aesthetic judgment language: "beautiful", "harmonious", "pleasing"
- Color/texture descriptions
- Material mentions: clay, bronze, stone, gold
- Style identifiers: "ornate", "minimalist", "geometric"
- Artifact type names: seal, pottery, jewelry, architecture

**High I Indicators:**

- Deity/religious figure names
- Ritual/ceremony vocabulary: sacred, temple, priest, offering
- Belief system terms: cosmology, divine, spiritual, sacred
- Mythology narrative structures
- Philosophical/theological concepts
- Ethical/moral language: justice, truth, balance

**High C Indicators:**

- Power/hierarchy terms: king, priest class, elite, commoner
- Access language: restricted, exclusive, monopoly, controlled
- Economic terms: trade, wealth, resource, labor
- Institutional structures: school, guild, academy, court
- Benefit/advantage language: "only X could", "gave power to"
- Social stratification markers

---

### Visual/Artifact Features

**Image Analysis Tags:**

For each artifact image in the database:

```json
{
  "artifact_id": "SHA_001_sun_disk",
  "civilization": "mesopotamia",
  "time_period": "neo_assyrian",
  "date_range": "-900 to -600",
  "geometric_elements": ["circle", "ray", "star_8pt"],
  "material": "stone_relief",
  "context": "temple_wall",

  "driver_visual_features": {
    "M_features": {
      "symmetry_type": "radial",
      "symmetry_order": 8,
      "precision_level": 0.8,
      "geometric_construction_visible": true
    },
    "A_features": {
      "decoration_density": 0.9,
      "pattern_complexity": 0.7,
      "style_markers": ["rosette", "ray_pattern"],
      "cultural_signature_strength": 0.9
    },
    "I_features": {
      "deity_depicted": "shamash",
      "ritual_context_indicators": ["altar", "priest_figure"],
      "symbolic_elements": ["sun_disk", "divine_rays"]
    },
    "C_features": {
      "context_accessibility": "temple_restricted",
      "material_value": 0.6,
      "labor_investment": 0.8,
      "power_symbols_present": ["throne", "royal_inscription"]
    }
  },

  "computed_driver_weights": [0.6, 0.9, 1.0, 0.9, 0.7],
  "composite_tag": "MAIC_aesthetic_institutional_convergence",
  "discovery_invention_marker": "discovery_symbolic"
}
```

---

## Ontological Hierarchy Structure

### Level 1: Universal Categories

```
geometric_elements/
├── 0D: point, center, position
├── 1D: line, ray, path, curve
├── 2D: polygons, circles, irregular_2D
└── 3D: polyhedra, spheroids, irregular_3D
```

### Level 2: Cultural Instantiations

```
geometric_elements/2D/circle/
├── mesopotamian_circles/
│   ├── shamash_sun_disk
│   ├── ishtar_rosette
│   └── cylinder_seal_circles
├── egyptian_circles/
│   ├── ra_solar_disk
│   └── cartouche_ovals
├── greek_circles/
│   └── perfect_proportion
└── maya_circles/
    └── calendar_wheels
```

### Level 3: Driver Convergence Patterns

```
mesopotamian_circles/shamash_sun_disk/
├── mythological_layer/        [I:0.9, A:0.7]
├── aesthetic_layer/            [A:0.9, M:0.3]
├── mathematical_layer/         [M:0.8, G:1.0]
├── ritual_layer/               [I:0.9, C:0.6]
└── power_layer/                [C:0.8, I:0.6]
```

### Level 4: Temporal Evolution

```
mesopotamian_circles/timeline/
├── 3500_BCE: potter_wheel_invention      [M:0.8, A:0.6, C:0.7] → INVENTION
├── 3000_BCE: shamash_cult_establishment  [I:0.9, A:0.8, C:0.5] → DISCOVERY
├── 2500_BCE: cylinder_seal_standardization [M:0.7, A:0.8, C:0.8] → INVENTION
└── 2000_BCE: pi_approximation_3.125      [M:0.9, A:0.2, C:0.4] → DISCOVERY
```

---

## Machine Learning Training Strategy

### Phase 1: Supervised Learning (Hand-Tagged Corpus)

**Goal:** Train model on 1000+ explicitly tagged examples

**Training data structure:**

```json
{
  "content_id": "week01_dayA_section1_shamash_myth",
  "content_text": "[full text]",
  "content_images": ["SHA_001.jpg", "SHA_002.jpg"],
  "human_tagged_drivers": [0.2, 0.7, 1.0, 0.9, 0.3],
  "human_tagged_composite": ["AI_symbolic_belief", "aesthetic_institutional"],
  "civilization": "mesopotamia",
  "element": "circle",
  "time_period": "neo_assyrian"
}
```

**Model learns:**

- Text features → driver weights correlation
- Image features → driver weights correlation
- Civilization + element → expected driver profile
- Temporal patterns in driver convergence

---

### Phase 2: Semi-Supervised Expansion

**Goal:** Use trained model to tag unlabeled artifacts, human validates subset

**Process:**

1. Model predicts driver weights for new artifact
2. Model confidence score generated
3. Low confidence → human review required
4. High confidence → auto-tagged with periodic audit
5. Human corrections feed back into training

**Example workflow:**

```
New artifact uploaded → "Indus Valley seal with circular motif"
Model prediction: [M:0.6, A:0.8, G:1.0, I:0.7, C:0.5]
Confidence: 0.72 (medium)
→ Flagged for human review
Human adjusts: [M:0.5, A:0.9, G:1.0, I:0.8, C:0.4]
→ Correction updates model weights
```

---

### Phase 3: Unsupervised Clustering

**Goal:** Discover NEW patterns not explicitly tagged

**ML discovers:**

- Previously unrecognized convergence clusters
- Cross-civilization similarities not in curriculum
- Driver combinations that predict innovation moments
- Geometric elements that appear in multiple contexts

**Example discovery:**

```
Cluster identified: [M:0.4, A:0.9, G:1.0, I:0.3, C:0.2]
Appears in:
- Polynesian tapa cloth patterns
- Celtic knotwork
- West African adinkra symbols
- Pre-Columbian textile designs

Pattern recognized: "High aesthetic, low institutional/control"
→ Distributed folk art tradition vs centralized monumental art
New tag suggested: "vernacular_geometric_tradition"
```

---

## Cross-Validation & Quality Control

### Consistency Checks

**Driver weight constraints:**

- G (Geometry) should always be 0.8-1.0 in geometry curriculum content
- Sum of M+A+I+C should correlate with content depth (deeper analysis = higher total)
- Day A content should have A+I > M+C
- Day B content should have M+C > A+I

**Temporal consistency:**

- Earlier civilizations shouldn't show anachronistic sophistication
- Mathematical discoveries should show increasing M scores over time
- Institutional complexity (I) should track civilization development

**Geographic consistency:**

- Isolated civilizations shouldn't show suspiciously similar patterns unless convergent evolution
- Trade route connections should show pattern diffusion

---

### Anomaly Detection

**Flag for review if:**

- Driver weights dramatically differ from civilization baseline
- Geometric element appears in context with no precedent
- Temporal sequence seems reversed (complex before simple)
- Single artifact shows conflicting driver signals

**Example anomaly:**

```
Artifact: "Mississippian Woodhenge Circle"
Predicted: [M:0.2, A:0.4, G:1.0, I:0.6, C:0.3]
Expected (based on civilization): [M:0.6, A:0.7, G:1.0, I:0.8, C:0.5]

Anomaly reason: Archaeological evidence shows sophisticated astronomical alignment (high M)
not yet in training corpus → model underestimates M for this culture

Resolution: Human expert confirms, updates training data, model recalibrates
```

---

## Database Schema for ML System

### Core Tables

**artifacts**

```sql
CREATE TABLE artifacts (
  artifact_id VARCHAR PRIMARY KEY,
  civilization VARCHAR,
  time_period VARCHAR,
  date_range_start INT,
  date_range_end INT,
  geographic_origin VARCHAR,
  material VARCHAR,
  context VARCHAR,
  image_url VARCHAR,
  description TEXT,

  -- Driver weights (ML predicted + human validated)
  M_weight FLOAT,
  A_weight FLOAT,
  G_weight FLOAT,
  I_weight FLOAT,
  C_weight FLOAT,

  driver_confidence FLOAT,
  human_validated BOOLEAN,
  last_updated TIMESTAMP
);
```

**geometric_elements_instances**

```sql
CREATE TABLE geometric_elements_instances (
  instance_id VARCHAR PRIMARY KEY,
  artifact_id VARCHAR REFERENCES artifacts,
  element_type VARCHAR, -- circle, triangle, etc.

  -- Element-specific measurements
  symmetry_type VARCHAR,
  symmetry_order INT,
  construction_method VARCHAR,

  -- Relationship to other elements
  composite_of ARRAY,
  appears_with ARRAY,

  cultural_meaning TEXT,
  mathematical_properties JSONB
);
```

**driver_convergence_events**

```sql
CREATE TABLE driver_convergence_events (
  event_id VARCHAR PRIMARY KEY,
  civilization VARCHAR,
  date_range_start INT,
  date_range_end INT,

  -- What converged
  convergence_type VARCHAR, -- MA, MI, MAIC, etc.
  driver_weights FLOAT[],

  -- What resulted
  discovery_invention VARCHAR,
  outcome_description TEXT,

  -- Evidence
  artifact_ids ARRAY,
  textual_sources ARRAY,

  confidence_score FLOAT
);
```

**lesson_content**

```sql
CREATE TABLE lesson_content (
  content_id VARCHAR PRIMARY KEY,
  week_number INT,
  day VARCHAR, -- 'A' or 'B'
  section_number INT,

  element_focus VARCHAR,
  civilization_focus VARCHAR,

  content_text TEXT,
  content_images ARRAY,

  -- Driver tagging
  M_weight FLOAT,
  A_weight FLOAT,
  G_weight FLOAT,
  I_weight FLOAT,
  C_weight FLOAT,

  composite_tags ARRAY,

  -- Relationships
  related_artifacts ARRAY,
  prerequisite_concepts ARRAY,
  enables_concepts ARRAY
);
```

---

## API for ML Integration

### Endpoints

**POST /api/tag_artifact**
Submit new artifact for driver weight prediction

```json
{
  "artifact_id": "NEW_001",
  "image_url": "https://...",
  "description": "Circular bronze mirror from Shang Dynasty China",
  "civilization": "shang_china",
  "time_period": "bronze_age",
  "date_estimate": -1200
}

Response:
{
  "predicted_drivers": [0.6, 0.8, 1.0, 0.7, 0.6],
  "confidence": 0.81,
  "suggested_tags": ["bronze_work", "circular_mirror", "MI_institutional_rigorous"],
  "similar_artifacts": ["artifacts/SHA_045", "artifacts/EGY_102"],
  "requires_human_review": false
}
```

**GET /api/query_patterns**
Find artifacts matching driver convergence pattern

```json
{
  "driver_range": {
    "M": [0.7, 1.0],
    "A": [0.8, 1.0],
    "I": [0.0, 0.3],
    "C": [0.0, 0.3]
  },
  "civilization": "any",
  "element": "circle"
}

Response:
{
  "matches": [
    {
      "artifact_id": "GRE_089",
      "description": "Greek compass with mathematical inscriptions",
      "drivers": [0.9, 0.9, 1.0, 0.2, 0.2],
      "notes": "High MA convergence, low IC - mathematical aesthetic without institutional power"
    }
  ],
  "pattern_interpretation": "Technical innovation by individual mathematicians"
}
```

**POST /api/discover_clusters**
Run unsupervised clustering to find new patterns

```json
{
  "min_cluster_size": 10,
  "clustering_algorithm": "DBSCAN",
  "feature_space": ["driver_weights", "element_type", "time_period"]
}

Response:
{
  "clusters_found": 23,
  "novel_clusters": [
    {
      "cluster_id": "CLUST_007",
      "size": 47,
      "centroid_drivers": [0.3, 0.9, 1.0, 0.4, 0.2],
      "common_features": ["textile_pattern", "folk_tradition", "distributed_production"],
      "interpretation": "Vernacular geometric tradition cluster",
      "civilizations_represented": ["polynesia", "west_africa", "andean", "celtic"]
    }
  ]
}
```

---

## Progressive Training Curriculum

### Year 1: Foundation (1000 hand-tagged examples)

**Focus civilizations:** Mesopotamia, Egypt, Greece, Maya
**Elements:** Circle, triangle, square, 8-star
**Goal:** Establish baseline driver recognition

### Year 2: Expansion (5000 examples, 70% ML-tagged)

**Add civilizations:** China, India, Rome, Islamic Golden Age
**Add elements:** Pentagon, hexagon, rhombus, spiral
**Goal:** Cross-cultural pattern recognition

### Year 3: Global Coverage (20,000 examples, 90% ML-tagged)

**Add civilizations:** Sub-Saharan Africa, Polynesia, Pre-Columbian Americas, etc.
**Add elements:** Complex composites, 3D forms
**Goal:** Comprehensive global ontology

### Year 4+: Self-Improving System

**ML autonomously tags new uploads**
**Discovers novel patterns**
**Proposes new composite tags**
**Generates curriculum suggestions**

---

## Success Metrics

**Model Performance:**

- Driver weight prediction accuracy > 85%
- Civilization classification accuracy > 90%
- Element identification accuracy > 95%
- Discovery/invention distinction accuracy > 75%

**Human Validation:**

- <20% of predictions require human correction
- Expert agreement with ML tags > 80%
- False positive rate < 10%

**Coverage:**

- All major civilizations represented
- All fundamental geometric elements tagged
- Temporal span: 40,000 BCE to present
- Geographic: all inhabited continents

**Discovery Power:**

- ML identifies 5+ novel patterns per year not in curriculum
- Cross-civilization connections found: 20+ per year
- Predictive power: suggests missing artifacts that are later confirmed

---

## Documentation Status

**Current version:** 1.0 - Initial driver-to-section mapping with ML ontology structure

**Purpose:** Enable machine learning system to recognize M·A·I·C patterns in cultural artifacts globally, creating self-improving tagging ontology for Project Euclid curriculum expansion

**Next steps:**

1. Begin hand-tagging first 1000 artifacts with driver weights
2. Develop image analysis feature extraction algorithms
3. Build initial ML model on Mesopotamia pilot data
4. Validate predictions against expert knowledge
5. Iterate and expand

---

**END OF MAGIC DRIVERS → LESSON SECTION MAPPING DOCUMENT**
