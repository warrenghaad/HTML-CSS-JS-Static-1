# SSOT-CONSTITUTION (Read First)
version: 5.0.0
generated_at: 2026-02-02

## Canon rule
If a tool output conflicts with this constitution, the tool output is invalid.

## Safety priority order
1) Protect data (no-delete, no-overwrite, canon read-only)
2) Preserve unknowns (novelty intake)
3) Patch-only changes with receipts
4) Human promotion into canon

---

## Original constitution (preserved)
D                                                                                                                                                                                                                                                           # SSOT CONSTITUTION & USER INTERFACE GUIDE
## Canon for Global K–12 (16+ civilizations) Curriculum System
## Date: January 7, 2026

---

## WHAT THIS DOCUMENT IS

This is the **CONSTITUTION** for the entire Civilization Pack (Mesopotamia) within the Global Curriculum System. Think of it as:

- **The rulebook** that governs all curriculum creation
- **The reference manual** for understanding how SSOTs work
- **The update guide** for making changes correctly
- **The interface documentation** for working with the system

**If you're confused about terminology, structure, or how to update something → START HERE.**

---

---

## 🔒 DECONTAMINATION & SAFETY FIRST (CANON IMMUTABILITY)

**This canon must be treated as read-only.** All automation must write only to STAGING and produce patchsets/reports.

**Three environments:**
1. **CANON (read-only)** — SSOTs, constitutions, registries
2. **STAGING (write)** — generated drafts, tags, patchsets, audit reports
3. **PRODUCTION (deploy)** — built HTML dashboard / app outputs

**Contamination signal:** unexpected scope shrink (e.g., “304 circle files”), missing civilizations/periods, or tag collapse.
When detected: stop writing, quarantine outputs, and generate a report.

## TABLE OF CONTENTS

1. [Core Principles](#core-principles)
2. [What is an SSOT?](#what-is-an-ssot)
3. [The SSOT Hierarchy](#the-ssot-hierarchy)
4. [How to Read SSOTs](#how-to-read-ssots)
5. [Critical Terminology](#critical-terminology)
6. [The Six Non-Negotiable Guardrails](#the-six-non-negotiable-guardrails)
7. [File Structure & Locations](#file-structure--locations)
8. [How to Update the System](#how-to-update-the-system)
9. [Working with the User Interface](#working-with-the-user-interface)
10. [Common Tasks & Where to Go](#common-tasks--where-to-go)

---

## CORE PRINCIPLES

### The Three Foundational Truths

1. **Metaphor Geometry Function: A Superimposed State where Metaphor and Function to co-exist**
   - Metaphor refers to symbolic thought processes that defines through association.  Metaphor enables understanding and problem solving.  
   - Function refers to individual geometric elements mathematical properties, scientific properties  
   - There is no causality necessary.  Geometry is subject agnostic.  
   - Metaphor is not exactly equivalent to, it does not merely "relate to" or "connects to". 
   - The SAME geometric property creates both meaning and capability
   - Example: Equal radius IS fairness (metaphor) AND IS fair distribution (function)

2. **Content Separate from Pedagogy**
   - WHAT we teach ≠ HOW we teach
   - Content = Geometric properties, artifacts, provable claims
   - Pedagogy = Methods, activities, engagement strategies

3. **Evidence Before Conclusions**
   - You cannot claim something without artifacts to prove it
   - Every statement must be backed by specific, citable content
   - Propositional logic: p → q iff w (Evidence → Claim only if Warrant exists)

---

## WHAT IS AN SSOT?

**SSOT = Single Source of Truth**

An SSOT is a document that defines ONE aspect of the curriculum system with complete authority. When there's a conflict or question, the SSOT is the final answer.

### Why SSOTs?

**The Problem:**
- Multiple documents saying different things
- Contradictions between files
- Unclear which version is correct
- Hours wasted finding "the right answer"

**The Solution:**
- ONE document per topic
- That document SUPERSEDES all others
- Clear hierarchy of which SSOT trumps which
- Always know where to look

### SSOT vs. Regular Document

| Regular Document | SSOT Document |
|------------------|---------------|
| Can be superseded | Cannot be superseded (except by higher SSOT) |
| May contradict others | Defines the truth |
| Reference material | Authoritative source |
| "One way to do it" | "THE way to do it" |

---

## THE SSOT HIERARCHY

### Level 1: MASTER SSOT (Supersedes Everything)

**Location:** `/Users/samimajeed/Documents/KEEP/SSOT_SYSTEM_V8/MASTER_SSOT_SUPERSEDES_ALL.md`

**What it defines:**
- The 16 section structure (Day A: A1-A8 | Day B: B1-B8)
- Week structure (Element + Deity + Metaphor + Function)
- Propositional logic framework
- Section-by-section rules

**When to use:** Defining section structure, section rules, week framework

---

### Level 2: Specialized SSOTs

#### **SSOT-002: Section Rules**
**Embedded in:** MASTER_SSOT_SUPERSEDES_ALL.md

**What it defines:**
- Requirements for each of 16 sections
- CAR templates per section
- Guardrails for each section
- What belongs in each section

---

#### **SSOT-004: Geometric Elements**
**Location:** Backend system (`ssot-ontologies.js`)

**What it defines:**
- 11 geometric elements (Circle, Triangle, Square, etc.)
- Core properties of each element
- Metaphor potential
- Function potential
- Grade-level appropriateness

---

#### **SSOT-005: Deities**
**Location:** Backend system (`ssot-ontologies.js`)

**What it defines:**
- 8 Mesopotamian deities
- Element pairings (Shamash ↔ Circle)
- Domains and symbols
- Key myths
- SEL themes

---

#### **SSOT-006: Artifact Types**
**Location:** Backend system (`ssot-ontologies.js`)

**What it defines:**
- 6 artifact categories (Sacred, Ritual, Official, Domestic, Architectural, Personal)
- Semiotic functions
- Typical objects per category
- Museum sources

---

### Level 3: Operational SSOTs

#### **Content Acquisition Restatement (CAR) SSOT**
**Location:** `/Users/samimajeed/Documents/Obsidian - Main Vault/PILOT - Mesapotamia Curriculum/system_pipeline/UI-SYS_FULL-V1/SSOTS and INTRUCTIONS/UI-SYS_MANIFESTS AND GUARDRAILS/CONTENT_ACQUISITION_RESTATEMENT_SSOT.md`

**What it defines:**
- What CARs are (replaces "Learning Objectives")
- The six non-negotiable requirements
- Propositional logic structure
- How to write CARs
- CAR format standards

**When to use:** Writing section conclusions, lesson plans, assessments

---

#### **Build Manifest SSOT**
**Location:** `/Users/samimajeed/Documents/Obsidian - Main Vault/PILOT - Mesapotamia Curriculum/system_pipeline/UI-SYS_FULL-V1/SSOTS and INTRUCTIONS/UI-SYS_MANIFESTS AND GUARDRAILS/build-manifest.md`

**What it defines:**
- How to create a curriculum manifest
- Step-by-step process
- Quality checks
- Artifact counting

---

### Level 4: Guardrail Documents

#### **Pedagogical vs. Content Guardrail**
**Location:** `UI-SYS_MANIFESTS AND GUARDRAILS/GUARDRAIL_PEDAGOGICAL_vs_CONTENT.md`

**What it defines:**
- How to separate HOW from WHAT
- Common violations
- Examples of correct separation

---

#### **Core Thesis: Metaphor = Function**
**Location:** `UI-SYS_MANIFESTS AND GUARDRAILS/CORE_THESIS_METAPHOR_EQUALS_FUNCTION.md`

**What it defines:**
- Why "IS" not "relates to"
- How to prove metaphor = function
- Bridge section requirements

---

## HOW TO READ SSOTs

### SSOT Document Structure

Most SSOTs follow this pattern:

```markdown
# TITLE
## Subtitle / Version Info

## ⚠️ NOTICE
(What this supersedes, what's critical)

## WHAT THIS IS
(Definition and purpose)

## THE RULES / REQUIREMENTS
(Non-negotiable specifications)

## EXAMPLES
(Correct and incorrect examples)

## FORMAT / TEMPLATE
(If applicable: exact formats to use)

## QUALITY CHECKS
(How to validate compliance)

## END OF SSOT
```

### How to Use an SSOT

1. **Read the ⚠️ NOTICE first**
   - Tells you what this supersedes
   - Alerts you to critical updates

2. **Read "WHAT THIS IS"**
   - Understand the purpose
   - Know when to use this SSOT

3. **Read "THE RULES"**
   - These are non-negotiable
   - Cannot be modified without system-wide update

4. **Study the EXAMPLES**
   - See correct application
   - Learn from violations

5. **Use the FORMAT**
   - Copy templates exactly
   - Adapt only where explicitly allowed

6. **Run QUALITY CHECKS**
   - Validate before finalizing
   - Ensure compliance

---

## CRITICAL TERMINOLOGY

### Terms You MUST Know

#### **CAR (Content Acquisition Restatement)**
**Replaces:** "Learning Objective" or "LO"

**Definition:** A declarative statement that restates what acquired content (artifacts, myths, observations) proves through propositional logic.

**NOT:** "Students will understand..."
**YES:** "Shamash's circular path proves fairness because constant radius creates equal treatment."

**Full documentation:** CONTENT_ACQUISITION_RESTATEMENT_SSOT.md

---

#### **Propositional Logic (p → q iff w)**
**What it means:**
```
p = Evidence (artifact, observation)
q = Claim (what we're stating)
w = Warrant (geometric property connecting p to q)
```

**Translation:** "Evidence demonstrates Claim if and only if Warrant exists."

**Example:**
- p: Shamash's circular path (from cylinder seal BM 89115)
- q: Represents fairness
- w: Circles maintain equal radius = equal treatment

---

#### **Metaphor = Function (NOT "relates to")**
**Wrong:** "Circles relate to fairness in meaning and structure."
**Right:** "Equal radius IS fairness—the SAME property creates both meaning and capability."

**The Thesis:** The metaphoric meaning and functional property are THE SAME THING, not two related things.

---

#### **Pedagogical vs. Content**
**Pedagogical:** HOW we teach (methods, activities, engagement)
**Content:** WHAT we teach (geometric properties, artifacts, conclusions)

**Must be separate:** Never mix "how" and "what" in the same field/statement.

---

#### **Artifact Description vs. Teaching Question**
**Artifact Description (Evidence):** MUST be declarative, identify features
- "Cylinder seal BM 89115: Shamash with seven radial beams, each 2.3cm from shoulders"

**Teaching Question (Pedagogy):** CAN be interrogative
- "Now that we see equal rays, why might that create fairness?"

**NEVER confuse these** - Evidence statements can't ask questions.

---

#### **The Six Non-Negotiables**
The six requirements every CAR MUST satisfy (see full section below).

---

## THE SIX NON-NEGOTIABLE GUARDRAILS

Every Content Acquisition Restatement (CAR) MUST pass all six:

### 1. Evidence Must Exist
❌ "Circles represent fairness"
✅ "Shamash's circular path [cylinder seal BM 89115] represents fairness"

**The test:** Can you point to the specific artifact?

---

### 2. Warrant Must Be Geometric
❌ "Shamash shows fairness because he is powerful"
✅ "Shamash shows fairness because circles maintain equal radius"

**The test:** Is the "because" clause a geometric property?

---

### 3. Logic Must Chain
❌ Section A3 CAR unrelated to Section A2
✅ Section A3 uses A2's conclusion + warrant as premise

**The test:** Does this section build on the previous one?

---

### 4. CARs Are Declarative, Not Activity Goals
❌ "Students will learn about circles"
✅ "Circles demonstrate fairness because equal radius creates equal treatment"

**The test:** Does it state what content proves, not what students do?

---

### 5. Artifacts Must Be Real and Cited
❌ "Ancient Mesopotamians used circles in rituals"
✅ "Cylinder seal BM 89115 shows Shamash with radial beams"

**The test:** Is there museum provenance and specific identification?

---

### 6. Artifact Descriptions IDENTIFY Features
❌ "Look at this seal. What do you notice?"
✅ "Seal shows seven radial beams, each 2.3cm from center, evenly spaced"

**The test:** Does the artifact caption state facts (not ask questions)?

---

## FILE STRUCTURE & LOCATIONS

### Where Everything Lives

```
/Users/samimajeed/Documents/Obsidian - Main Vault/PILOT - Mesapotamia Curriculum/
│
├── SSOT_CONSTITUTION.md  ← YOU ARE HERE
│
├── ARCHIVE/
│   └── MANIFEST GRADE 3.md  ← Gold standard example
│
├── .claude/
│   ├── MANIFEST_DIRECTIONS_DAY_A.md
│   └── MANIFEST_DIRECTIONS_DAY_B.md
│
├── system_pipeline/
│   └── UI-SYS_FULL-V1/
│       └── SSOTS and INTRUCTIONS/
│           └── UI-SYS_MANIFESTS AND GUARDRAILS/
│               ├── CONTENT_ACQUISITION_RESTATEMENT_SSOT.md  ← CAR rules
│               ├── CONTENT_ACQUISITION_RESTATEMENT_QUICK_REFERENCE.md
│               ├── build-manifest.md  ← How to build manifests
│               ├── CORE_THESIS_METAPHOR_EQUALS_FUNCTION.md
│               └── GUARDRAIL_PEDAGOGICAL_vs_CONTENT.md
│
└── /Users/samimajeed/Documents/KEEP/
    └── SSOT_SYSTEM_V8/
        └── MASTER_SSOT_SUPERSEDES_ALL.md  ← THE master SSOT
```

### Backend Files

```
/Users/samimajeed/mesopotamia-backend/
├── ssot-ontologies.js  ← Elements, Deities, Artifacts
├── server.js  ← API endpoints
├── supabase-schema.sql  ← Database structure
└── CONTENT_ACQUISITION_RESTATEMENTS_DIRECTIONS.md  ← CAR implementation guide
```

---

## HOW TO UPDATE THE SYSTEM

### When You Need to Change Something

#### **Step 1: Identify the SSOT**

Ask: "What am I changing?"

| What You're Changing | Which SSOT | Location |
|---------------------|-----------|----------|
| Section structure/rules | MASTER_SSOT | KEEP/SSOT_SYSTEM_V8/ |
| CAR format/requirements | CAR SSOT | UI-SYS_MANIFESTS AND GUARDRAILS/ |
| Element definitions | SSOT-004 | Backend/ssot-ontologies.js |
| Deity definitions | SSOT-005 | Backend/ssot-ontologies.js |
| Artifact categories | SSOT-006 | Backend/ssot-ontologies.js |
| Manifest process | build-manifest.md | UI-SYS_MANIFESTS AND GUARDRAILS/ |

---

#### **Step 2: Check SSOT Hierarchy**

**Can you make this change?**

✅ **YES if:**
- You're updating an example (doesn't change rules)
- You're clarifying language (doesn't change requirements)
- You're adding new elements/deities (following existing pattern)

❌ **NO (requires system-wide update) if:**
- Changing the six non-negotiables
- Modifying section structure (16 sections)
- Changing propositional logic framework
- Altering Metaphor = Function thesis

---

#### **Step 3: Make the Change**

1. **Update the SSOT document**
2. **Update the "Last Modified" date**
3. **Add a note to the ⚠️ NOTICE section if major change**
4. **Check for dependent SSOTs** that reference this one
5. **Update dependent SSOTs** to reflect change
6. **Update this Constitution** if it's a major change

---

#### **Step 4: Validate the Change**

Run through:
- [ ] Does this contradict any higher SSOT?
- [ ] Have I updated all dependent documents?
- [ ] Have I tested with an example?
- [ ] Does this maintain the three core principles?
- [ ] Does this preserve the six non-negotiables?

---

### Example: Adding a New Geometric Element

**Scenario:** You want to add "Rhombus" as a new element.

**Process:**

1. **Identify SSOT:** SSOT-004 (Geometric Elements) in `ssot-ontologies.js`

2. **Check hierarchy:** SSOT-004 is Level 2, can add elements if following pattern

3. **Make changes:**
   ```javascript
   // In ssot-ontologies.js
   'elem.rhombus': {
     id: 'elem.rhombus',
     name: 'Rhombus',
     core_property: 'Equal sides with variable angles',
     metaphor_potential: 'Flexibility within structure',
     function_potential: 'Tessellation and tiling',
     deity_pairing: ['deity.nabu'], // If appropriate
     grade_appropriate: [4, 5]
   }
   ```

4. **Update dependent docs:**
   - Update MASTER_SSOT element count (if it lists them)
   - Add to element sequence if needed
   - Create week structure if it gets one

5. **Validate:**
   - [ ] Follows same structure as other elements
   - [ ] Has core property defined
   - [ ] Has metaphor + function pairing
   - [ ] Deity pairing makes sense (or is left null)

---

## WORKING WITH THE USER INTERFACE

### The Curriculum Studio UI

The UI is built on these SSOTs. When you see something in the UI, it's enforcing an SSOT rule.

#### **UI Components → SSOT Mapping**

| UI Component | Enforces Which SSOT | What It Does |
|--------------|-------------------|--------------|
| **Section Editor** | MASTER_SSOT (002) | Enforces 16 sections, order, required fields |
| **CAR Input Field** | CAR SSOT | Validates propositional logic, checks evidence |
| **Artifact Selector** | SSOT-006 | Ensures artifact categories are correct |
| **A4 Subsection Builder** | SSOT-006 + A4 Guardrail | Validates 2+ subsections, different categories |
| **Element/Deity Pairing** | SSOT-004 + SSOT-005 | Only allows valid pairings |
| **Bridge Section Validator** | Metaphor = Function SSOT | Checks for "IS" language |

---

### Common UI Validation Messages

| Message | What It Means | Which SSOT | How to Fix |
|---------|--------------|-----------|------------|
| "CAR must cite evidence" | No artifact in statement | CAR SSOT (#1) | Add artifact reference |
| "Warrant must be geometric" | "Because" clause not geometric | CAR SSOT (#2) | Use geometric property |
| "Use 'IS' language in bridge" | Says "relates to" not "is" | Metaphor = Function | Change to "IS" |
| "A4 needs 2+ subsections" | Only 1 artifact category | SSOT-006 A4 Guardrail | Add different category |
| "Artifact description asks question" | Caption interrogative | CAR SSOT (#6) | Make declarative |
| "Section doesn't chain" | Doesn't use previous output | CAR SSOT (#3) | Use A2 conclusion in A3 |

---

### Where to Find Things in the UI

#### **Creating a Manifest:**
1. Select Grade (3, 4, or 5)
2. Select Week (I-VIII)
3. System auto-populates:
   - Element (from SSOT-004)
   - Deity (from SSOT-005, matched to element)
   - Week thesis template (from MASTER_SSOT)

#### **Writing a Section:**
1. Select Section Code (A1-A8, B1-B8)
2. System shows:
   - Section requirements (from MASTER_SSOT)
   - CAR template (from CAR SSOT)
   - Required artifacts (from SSOT-006)

3. You provide:
   - Content Acquisition Restatement (CAR)
   - Pedagogical Design (separate field)
   - Content Purpose (separate field)
   - Artifact IDs (validated against SSOT-006)

#### **Validating Your Work:**
- Green check = Passes all guardrails
- Yellow warning = Minor issue (can proceed)
- Red X = Violates SSOT (must fix)

Click the warning/error to see:
- Which SSOT is violated
- Which guardrail specifically
- How to fix it

---

## COMMON TASKS & WHERE TO GO

### "I need to write a CAR for Section A4"

**Go to:**
1. CAR SSOT (for format)
2. MASTER_SSOT Section A4 definition (for requirements)
3. SSOT-006 (for artifact types A4a-A4f)

**Steps:**
1. Read A4 requirements (2+ subsections, different categories)
2. Check CAR format (Evidence → Claim iff Warrant)
3. Cite specific artifacts (not plural "seals")
4. Ensure artifact descriptions identify features
5. Write CAR following propositional logic

---

### "I'm building a manifest for Grade 3 Week II"

**Go to:**
1. build-manifest.md (overall process)
2. ARCHIVE/MANIFEST GRADE 3.md (gold standard example)
3. MASTER_SSOT (section structure)

**Steps:**
1. Follow 7-step process in build-manifest.md
2. Use Grade 3 Week I as template
3. Validate against quality checklist
4. Count artifacts at end

---

### "I need to understand the Metaphor = Function thesis"

**Go to:**
1. CORE_THESIS_METAPHOR_EQUALS_FUNCTION.md
2. MASTER_SSOT (Bridge section B1)

**Key points:**
- Use "IS" not "relates to"
- Same property in both domains
- Bridge section must prove identity

---

### "I need to add a new artifact type"

**Go to:**
1. SSOT-006 (in backend ssot-ontologies.js)
2. Check if it fits existing 6 categories
3. If not, this is a MAJOR change → requires system update

**Process:**
- If it fits existing (e.g., new Sacred artifact) → just add to database
- If new category (e.g., "Agricultural") → update SSOT-006, MASTER_SSOT, all manifests

---

### "Something's broken/contradictory"

**Go to:**
1. This Constitution
2. Check SSOT hierarchy
3. Find which SSOT supersedes

**Process:**
1. Identify the contradiction
2. Find which SSOTs are involved
3. Higher SSOT wins (MASTER > Specialized > Operational)
4. Update lower SSOT to match
5. If both same level → check dates (newer wins, unless noted)

---

### "I want to change terminology"

**Example:** Like changing "Learning Objectives" to "Content Acquisition Restatements"

**Go to:**
1. Identify scope (how many docs affected?)
2. Update highest-level SSOT first (MASTER_SSOT)
3. Update specialized SSOTs
4. Update operational docs
5. Update UI
6. Update database field names
7. Update API endpoints
8. **Update this Constitution**

**This is a MAJOR change** - expect to touch 20+ files.

---

## QUICK REFERENCE CARDS

### The Three Core Principles

```
1. Metaphor IS Function (same property, both domains)
2. Content ≠ Pedagogy (separate what from how)
3. Evidence Before Conclusions (artifacts → claims)
```

### The Six Non-Negotiables

```
1. Evidence must exist (cite artifacts)
2. Warrant must be geometric (geometric property)
3. Logic must chain (section n+1 uses section n)
4. CARs are declarative (not "Students will...")
5. Artifacts real and cited (museum provenance)
6. Artifact descriptions identify (not ask questions)
```

### The Propositional Logic Formula

```
p → q iff w

p = Evidence
q = Claim
w = Warrant

"Evidence proves Claim if and only if Warrant exists"
```

### The SSOT Hierarchy

```
Level 1: MASTER_SSOT_SUPERSEDES_ALL.md
Level 2: SSOT-002, SSOT-004, SSOT-005, SSOT-006
Level 3: CAR SSOT, Build Manifest SSOT
Level 4: Guardrail documents
```

---

## WHEN IN DOUBT

### The Decision Tree

```
START: Do I need to change/create something?
│
├─ Is it changing structure/rules?
│  └─ YES → Check MASTER_SSOT first
│      └─ Violates SSOT? → DON'T DO IT
│      └─ Allowed? → Proceed, update dependents
│
├─ Is it a CAR/section conclusion?
│  └─ YES → Follow CAR SSOT six non-negotiables
│      └─ Passes all six? → Approved
│      └─ Fails any? → Fix until passes
│
├─ Is it artifact-related?
│  └─ YES → Check SSOT-006 categories
│      └─ Fits existing? → Add to database
│      └─ New category? → Major change, update system
│
└─ Is it contradictory to existing?
   └─ YES → Find SSOTs involved
       └─ Higher SSOT wins → Update lower
```

---

## FINAL WORD

**This system exists to prevent the problems we've experienced:**

- ❌ Hours searching for "the right version"
- ❌ Contradictions between documents
- ❌ Unclear which source is authoritative
- ❌ Wasted time on rework

**The SSOTs solve this by:**

- ✅ ONE source of truth per topic
- ✅ Clear hierarchy when conflicts arise
- ✅ Explicit supersession notices
- ✅ Validation at every step

**When you follow the SSOTs, you:**
- Know your work is correct
- Know it won't contradict later
- Know where to look when confused
- Save hours of debugging

**This Constitution helps you:**
- Understand what SSOTs are
- Know which one to use when
- Make changes correctly
- Keep the system consistent

---

## DOCUMENT HISTORY

| Date | Change | Reason |
|------|--------|--------|
| 2026-01-07 | Created SSOT Constitution | Centralize system understanding for UI work |
| 2026-01-07 | Added CAR terminology | Supersede "Learning Objectives" with "Content Acquisition Restatements" |

---

**Last Updated:** January 7, 2026
**Status:** Production Standard
**Supersedes:** All informal guides, README files, scattered instructions

---

**This is your map. Use it.**
