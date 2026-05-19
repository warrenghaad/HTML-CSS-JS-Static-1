import os
import json
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI

app = Flask(__name__, static_folder='.', static_url_path='')

DATABASE_URL = os.environ.get('DATABASE_URL')
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))

ai_client = OpenAI(
    base_url=os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL'),
    api_key=os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY'),
)

ELEMENT_NOVELTY_STATUSES = ('existing', 'new', 'unknown')
ELEMENT_VALIDATION_STATUSES = ('valid', 'unknown', 'invalid')
ELEMENT_CONSOLIDATED_STATUSES = ('existing_valid', 'new_valid', 'unknown', 'invalid')
CATALOGABLE_EXTENSIONS = {
    '.html': 'html',
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.py': 'python',
}
STACK_LAYERS = ('backend', 'frontend', 'experimental', 'future-react')

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            doc_key VARCHAR(100) UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS document_versions (
            id SERIAL PRIMARY KEY,
            doc_key VARCHAR(100) NOT NULL,
            version_number INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            saved_at TIMESTAMP DEFAULT NOW(),
            save_note VARCHAR(500) DEFAULT ''
        )
    ''')
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_versions_doc_key 
        ON document_versions(doc_key, version_number DESC)
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS playground_drafts (
            id SERIAL PRIMARY KEY,
            draft_key VARCHAR(100) UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL DEFAULT 'Untitled Draft',
            html_content TEXT NOT NULL DEFAULT '',
            css_content TEXT NOT NULL DEFAULT '',
            status VARCHAR(20) NOT NULL DEFAULT 'draft',
            review_feedback TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS production_lessons (
            id SERIAL PRIMARY KEY,
            lesson_number INTEGER UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            unit VARCHAR(100) NOT NULL,
            god VARCHAR(100) DEFAULT '',
            artifact VARCHAR(255) DEFAULT '',
            math_concept VARCHAR(255) DEFAULT '',
            status VARCHAR(30) DEFAULT 'not_started',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    for col_def in [
        "activity TEXT DEFAULT ''",
        "location VARCHAR(255) DEFAULT ''",
        "geometric_theme VARCHAR(255) DEFAULT ''",
        "myth_theme VARCHAR(255) DEFAULT ''",
        "image_notes TEXT DEFAULT ''",
    ]:
        col_name = col_def.split()[0]
        cur.execute("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name='production_lessons' AND column_name=%s
        """, (col_name,))
        if not cur.fetchone():
            cur.execute(f"ALTER TABLE production_lessons ADD COLUMN {col_def}")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS production_teams (
            id SERIAL PRIMARY KEY,
            team_number INTEGER UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            description VARCHAR(500) DEFAULT '',
            color VARCHAR(20) DEFAULT '',
            category VARCHAR(50) DEFAULT '',
            tasks_total INTEGER DEFAULT 0,
            tasks_complete INTEGER DEFAULT 0
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS production_tasks (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES production_lessons(id),
            team_id INTEGER REFERENCES production_teams(id),
            task_type VARCHAR(100) NOT NULL,
            status VARCHAR(30) DEFAULT 'not_started',
            notes TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS production_assets (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES production_lessons(id),
            asset_type VARCHAR(30) NOT NULL,
            title VARCHAR(255) NOT NULL DEFAULT '',
            description TEXT DEFAULT '',
            source VARCHAR(255) DEFAULT '',
            source_url TEXT DEFAULT '',
            license VARCHAR(100) DEFAULT '',
            status VARCHAR(30) DEFAULT 'planned',
            filename VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_assets_lesson ON production_assets(lesson_id)
    ''')
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_assets_type ON production_assets(asset_type)
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS content_items (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES production_lessons(id),
            content_type VARCHAR(30) NOT NULL,
            title VARCHAR(255) NOT NULL DEFAULT '',
            body TEXT DEFAULT '',
            status VARCHAR(30) DEFAULT 'not_started',
            assigned_to VARCHAR(100) DEFAULT '',
            word_count INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_content_lesson ON content_items(lesson_id)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_content_type ON content_items(content_type)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS assembly_checklists (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES production_lessons(id),
            component VARCHAR(50) NOT NULL,
            status VARCHAR(30) DEFAULT 'pending',
            notes TEXT DEFAULT '',
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_assembly_lesson ON assembly_checklists(lesson_id)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS qa_reviews (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES production_lessons(id),
            category VARCHAR(50) NOT NULL,
            status VARCHAR(30) DEFAULT 'not_checked',
            reviewer_notes TEXT DEFAULT '',
            reviewed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_qa_lesson ON qa_reviews(lesson_id)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS day_b_elements (
            id SERIAL PRIMARY KEY,
            element_id VARCHAR(30) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(30) NOT NULL,
            deity_name VARCHAR(100) NOT NULL,
            deity_id VARCHAR(50) NOT NULL,
            core_property_name VARCHAR(100) NOT NULL,
            core_property_definition TEXT NOT NULL,
            core_property_proof TEXT NOT NULL,
            key_metaphor VARCHAR(100) NOT NULL,
            key_function VARCHAR(100) NOT NULL,
            week_number INTEGER UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS day_b_lessons (
            id SERIAL PRIMARY KEY,
            element_id INTEGER REFERENCES day_b_elements(id),
            grade INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            week_number INTEGER NOT NULL,
            status VARCHAR(30) DEFAULT 'not_started',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_dayb_lessons_grade ON day_b_lessons(grade)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_dayb_lessons_element ON day_b_lessons(element_id)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS element_reconciliations (
            id SERIAL PRIMARY KEY,
            canonical_element_id INTEGER REFERENCES day_b_elements(id),
            source_type VARCHAR(30) NOT NULL DEFAULT 'manual',
            source_key VARCHAR(255) UNIQUE NOT NULL,
            source_label VARCHAR(255) NOT NULL DEFAULT '',
            candidate_element_id VARCHAR(50) DEFAULT '',
            candidate_name VARCHAR(120) NOT NULL,
            candidate_category VARCHAR(60) DEFAULT '',
            candidate_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
            novelty_status VARCHAR(20) NOT NULL DEFAULT 'unknown',
            validation_status VARCHAR(20) NOT NULL DEFAULT 'unknown',
            consolidated_status VARCHAR(20) NOT NULL DEFAULT 'unknown',
            reason TEXT DEFAULT '',
            review_notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_element_recon_status ON element_reconciliations(consolidated_status)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_element_recon_source ON element_reconciliations(source_type)')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS day_b_sections (
            id SERIAL PRIMARY KEY,
            lesson_id INTEGER REFERENCES day_b_lessons(id),
            section_code VARCHAR(5) NOT NULL,
            section_name VARCHAR(100) NOT NULL,
            purpose TEXT NOT NULL DEFAULT '',
            duration VARCHAR(20) NOT NULL DEFAULT '',
            primary_drivers VARCHAR(50) NOT NULL DEFAULT '',
            lo_template TEXT NOT NULL DEFAULT '',
            lo_text TEXT DEFAULT '',
            content TEXT DEFAULT '',
            image_type VARCHAR(100) DEFAULT '',
            image_url TEXT DEFAULT '',
            carrier VARCHAR(255) DEFAULT '',
            ecd_claim TEXT DEFAULT '',
            ecd_evidence TEXT DEFAULT '',
            ecd_task TEXT DEFAULT '',
            b5_prior_refs JSONB DEFAULT '[]',
            status VARCHAR(30) DEFAULT 'not_started',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_dayb_sections_lesson ON day_b_sections(lesson_id)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_dayb_sections_code ON day_b_sections(section_code)')
    cur.close()
    conn.close()

def seed_lesson_variables(cur):
    cur.execute("SELECT id, title, god FROM production_lessons WHERE god IS NULL OR god = '' ORDER BY lesson_number")
    empty_lessons = cur.fetchall()
    if not empty_lessons:
        return

    var_lookup = {
        'The Fertile Crescent': ('Enki', 'Standard of Ur', 'Geometric shapes in maps', 'Map drawing, clay tablet', 'Southern Iraq', 'River curves & circles', 'Waters of creation', 'Satellite vs ancient maps'),
        'Sumerian Creation Myths': ('Nammu', 'Weld-Blundell Prism', 'Symmetry in creation', 'Creation story illustration', 'Eridu', 'Bilateral symmetry', 'Primordial ocean', 'Chaos-to-order visuals'),
        'The First Settlements': ('Enlil', 'Tell Brak Eye Idols', 'Area & perimeter of dwellings', 'Settlement layout design', 'Tell Brak', 'Rectangular grids', 'Taming the wild', 'Aerial settlement views'),
        'Birth of Agriculture': ('Ashnan', 'Seed Plow Model', 'Measurement & ratios', 'Planting grid activity', 'Girsu', 'Parallel lines, rows', 'Gift of grain', 'Farm tool close-ups'),
        'Early River Civilizations': ('Ea', 'Gudea Cylinders', 'Scale & proportion', 'River map overlay', 'Lagash', 'Meander curves', 'River journeys', 'Tigris/Euphrates imagery'),
        'Foundations of Society': ('Utu', 'Law Code Stele', 'Organizational charts', 'Society pyramid build', 'Nippur', 'Hierarchical triangles', 'Order from chaos', 'Social structure diagrams'),
        'The Sumerian Pantheon': ('An', 'Votive Statues', 'Angles of worship', 'Pantheon family tree', 'Uruk', 'Star polygons', 'Assembly of gods', 'Temple statue groupings'),
        'Enlil: Lord of the Wind': ('Enlil', 'Enlil Temple Model', 'Wind force vectors', 'Wind direction compass', 'Nippur', 'Directional arrows', 'Storm & calm', 'Wind pattern diagrams'),
        'Inanna: Queen of Heaven': ('Inanna', 'Inanna Vase', 'Rotational symmetry', 'Star of Inanna drawing', 'Uruk', 'Eight-pointed star', 'Descent & return', 'Venus star imagery'),
        'The Epic of Gilgamesh': ('Gilgamesh', 'Gilgamesh Tablet', 'Distance & journey math', 'Epic timeline map', 'Uruk', 'Spiral journey path', 'Quest for immortality', 'Hero journey scenes'),
        'Myths of the Underworld': ('Ereshkigal', 'Queen of Night Relief', 'Negative numbers & depth', 'Underworld layer diagram', 'Kur', 'Concentric circles down', 'Seven gates', 'Dark realm imagery'),
        'Rituals and Offerings': ('Ninhursag', 'Ram in Thicket', 'Fractions in offerings', 'Offering proportion chart', 'Ur', 'Division & fractions', 'Sacred giving', 'Ritual scene details'),
        'Rise of Ur and Uruk': ('Nanna', 'Royal Game of Ur', 'Grid coordinates', 'City plan grid overlay', 'Ur', 'Rectangular planning', 'City founding', 'Aerial city ruins'),
        'Ziggurats: Stairways to Heaven': ('Marduk', 'Ziggurat Model', 'Volume of stepped pyramids', '3D ziggurat construction', 'Babylon', 'Stacked rectangles', 'Climbing to heaven', 'Ziggurat cross-sections'),
        'City Walls and Gates': ('Adad', 'Ishtar Gate Tiles', 'Perimeter & fortification', 'Wall defense blueprint', 'Babylon', 'Rectangular perimeters', 'Protection & power', 'Ishtar Gate details'),
        'Palaces of Mesopotamia': ('Shamash', 'Balawat Gates', 'Floor plan geometry', 'Palace room layout', 'Nimrud', 'Complex floor plans', 'Royal grandeur', 'Palace relief carvings'),
        'Irrigation and Engineering': ('Enki', 'Canal Map Tablet', 'Water flow rates', 'Canal system design', 'Girsu', 'Channel networks', 'Taming the waters', 'Irrigation channel photos'),
        'Life in a City-State': ('Ningal', 'Marketplace Seal', 'Population statistics', 'Daily life diorama', 'Ur', 'Neighborhood grids', 'Community living', 'Market scene images'),
        'Cuneiform Writing System': ('Nabu', 'Cuneiform Tablet', 'Angles in wedge marks', 'Clay tablet pressing', 'Nippur', 'Wedge angles', 'Gift of writing', 'Cuneiform close-ups'),
        'Scribes and Schools': ('Nisaba', 'School Tablet', 'Counting systems base-60', 'Scribal practice exercise', 'Nippur', 'Ordered rows/columns', 'Knowledge keepers', 'School tablet replicas'),
        'Early Number Systems': ('Nabu', 'Counting Tokens', 'Base-60 number system', 'Number conversion activity', 'Susa', 'Positional notation', 'Counting the stars', 'Token & tablet photos'),
        'Babylonian Mathematics': ('Shamash', 'Plimpton 322', 'Pythagorean triples', 'Triangle construction', 'Larsa', 'Right triangles', 'Measuring the world', 'Plimpton 322 close-up'),
        'Astronomical Records': ('Sin', 'Venus Tablet', 'Circular measurement', 'Star chart plotting', 'Babylon', 'Circles & degrees', 'Reading the heavens', 'Star chart imagery'),
        'Libraries of Clay': ('Nabu', 'Library Catalog Tablet', 'Sorting & classification', 'Library catalog system', 'Nineveh', 'Organizational grids', 'Preserving knowledge', 'Ashurbanipal library'),
        'Cylinder Seals and Impressions': ('Ea', 'Cylinder Seal', 'Circumference & rotation', 'Seal rolling activity', 'Ur', 'Cylinders & circles', 'Identity marks', 'Seal impression details'),
        'Metalwork and Jewelry': ('Inanna', 'Gold Helmet of Meskalamdug', 'Weight & measurement', 'Jewelry design template', 'Ur', 'Circular forms', 'Adornment of gods', 'Royal jewelry photos'),
        'Pottery and Ceramics': ('Ninhursag', 'Ubaid Pottery', 'Volume of vessels', 'Pot shape design', 'Eridu', 'Cross-sections, curves', 'Shaping the earth', 'Painted pottery patterns'),
        'Textile Arts of Sumer': ('Uttu', 'Textile Fragment', 'Pattern tessellation', 'Weaving pattern grid', 'Ur', 'Repeating patterns', 'Weaving fate', 'Textile pattern close-ups'),
        'Musical Instruments': ('Inanna', 'Bull-Headed Lyre', 'Sound wave frequencies', 'String length experiment', 'Ur', 'Harmonic ratios', 'Music of the gods', 'Lyre reconstruction photos'),
        'Sculpture and Relief': ('Ningirsu', 'Stele of Vultures', 'Proportion in figures', 'Figure proportion grid', 'Girsu', 'Human proportions', 'Stories in stone', 'Relief carving details'),
        'Trade Routes of Mesopotamia': ('Shamash', 'Trade Record Tablet', 'Distance & rate problems', 'Trade route mapping', 'Dilmun', 'Network paths', 'Merchant journeys', 'Ancient route maps'),
        'Weights and Measures': ('Utu', 'Stone Weight Set', 'Unit conversion', 'Weight comparison lab', 'Ur', 'Balance & equality', 'Fair measure', 'Standard weight photos'),
        'Markets and Merchants': ('Shamash', 'Merchant Seal', 'Profit & loss calculation', 'Market price simulation', 'Sippar', 'Exchange ratios', 'Marketplace tales', 'Market scene seals'),
        'Resources and Raw Materials': ('Enki', 'Lapis Lazuli Artifacts', 'Supply & distribution', 'Resource allocation map', 'Badakhshan', 'Distribution networks', 'Gifts of the earth', 'Raw material samples'),
        'Maritime Trade': ('Enki', 'Model Boat', 'Speed & distance on water', 'Boat design challenge', 'Persian Gulf', 'Curved hull shapes', 'Sea voyages', 'Ancient boat models'),
        'Economic Tablets': ('Nabu', 'Drehem Tablet', 'Data tables & records', 'Spreadsheet recreation', 'Drehem', 'Data organization', 'Counting wealth', 'Economic tablet photos'),
        'The Code of Hammurabi': ('Shamash', 'Code of Hammurabi Stele', 'Logic & if-then statements', 'Law code writing activity', 'Babylon', 'Hierarchical structure', 'Divine justice', 'Hammurabi stele details'),
        'Kings and Dynasties': ('Enlil', 'Sumerian King List', 'Timeline & number lines', 'Dynasty timeline builder', 'Ur', 'Linear sequences', 'Rise & fall of kings', 'King list prism photos'),
        'Justice and Punishment': ('Utu', 'Court Record Tablet', 'Proportional reasoning', 'Justice scenario cards', 'Sippar', 'Balance & proportion', 'Scales of justice', 'Court scene imagery'),
        'Land Ownership': ('Enlil', 'Kudurru Boundary Stone', 'Area calculation', 'Land survey activity', 'Babylon', 'Boundary polygons', 'Marking the earth', 'Boundary stone symbols'),
        'Diplomacy and Treaties': ('Ea', 'Amarna Letters', 'Venn diagrams & sets', 'Treaty negotiation game', 'Amarna', 'Overlapping circles', 'Words of peace', 'Letter tablet photos'),
        'Military Organization': ('Nergal', 'Siege Scene Relief', 'Formation geometry', 'Battle formation design', 'Nineveh', 'Grid formations', 'Art of war', 'Battle relief details'),
        'Mesopotamia and Egypt': ('Shamash', 'Comparative Artifacts', 'Comparing geometric styles', 'Civilization comparison chart', 'Memphis', 'Contrasting shapes', 'Meeting of cultures', 'Side-by-side artifacts'),
        'Influence on Greek Thought': ('Nabu', 'Mathematical Tablet', 'Theorem comparison', 'Math history timeline', 'Athens', 'Proof structures', 'Seeds of philosophy', 'Greek/Babylonian math'),
        'Modern Archaeology': ('Nabu', 'Excavation Photo Set', 'Grid reference systems', 'Dig site grid activity', 'Nineveh', 'Coordinate grids', 'Uncovering the past', 'Excavation site photos'),
        'Preserving Ancient Sites': ('Ninhursag', 'Restoration Photos', 'Decay & rate of change', 'Preservation plan design', 'Babylon', 'Structural geometry', 'Saving heritage', 'Before/after restoration'),
        'Mathematics Through the Ages': ('Nabu', 'Math Evolution Chart', 'Number system evolution', 'Math timeline collage', 'Global', 'Evolving notation', 'Eternal numbers', 'Math system comparison'),
        'Mesopotamia in the Modern World': ('Enki', 'Modern Iraq Map', 'Statistical analysis', 'Legacy infographic design', 'Baghdad', 'Data visualization', 'Living legacy', 'Modern/ancient overlays'),
    }
    for lesson in empty_lessons:
        v = var_lookup.get(lesson['title'])
        if v:
            cur.execute('''
                UPDATE production_lessons SET god=%s, artifact=%s, math_concept=%s, activity=%s,
                location=%s, geometric_theme=%s, myth_theme=%s, image_notes=%s WHERE id=%s
            ''', (*v, lesson['id']))

def seed_production_data():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT COUNT(*) as cnt FROM production_teams')
    if cur.fetchone()['cnt'] > 0:
        seed_lesson_variables(cur)
        seed_assets(cur)
        seed_content_items(cur)
        seed_assembly_checklists(cur)
        seed_qa_reviews(cur)
        cur.close()
        conn.close()
        return

    teams = [
        (1, 'Sourcing', 'Find museum artifacts, 144+ items', '#FBC02D', 'sourcing'),
        (2, 'Download', 'Bulk download 2,400+ images', '#FBC02D', 'sourcing'),
        (3, 'Myth Writers', 'Write 144 text sections', '#FF9800', 'content'),
        (4, 'Overlay Designers', 'Create 400-600 SVG overlays', '#FF9800', 'content'),
        (5, 'Visual Storytelling', 'Create slide sequences & bridges', '#E91E63', 'visual'),
        (6, 'Math Writers', 'Write definitions, examples, 240+ problems', '#673AB7', 'math'),
        (7, 'Activity Designers', 'Design 96 activity sets', '#673AB7', 'math'),
        (8, 'Assembly', 'Combine into 48 complete lessons', '#009688', 'assembly'),
        (9, 'AI Image Gen', 'Generate 1,500+ images', '#FBC02D', 'sourcing'),
    ]
    for t in teams:
        cur.execute('''
            INSERT INTO production_teams (team_number, name, description, color, category)
            VALUES (%s, %s, %s, %s, %s)
        ''', t)

    lessons_by_unit = {
        'Origins & Creation': [
            'The Fertile Crescent',
            'Sumerian Creation Myths',
            'The First Settlements',
            'Birth of Agriculture',
            'Early River Civilizations',
            'Foundations of Society',
        ],
        'Gods & Mythology': [
            'The Sumerian Pantheon',
            'Enlil: Lord of the Wind',
            'Inanna: Queen of Heaven',
            'The Epic of Gilgamesh',
            'Myths of the Underworld',
            'Rituals and Offerings',
        ],
        'City-States & Architecture': [
            'Rise of Ur and Uruk',
            'Ziggurats: Stairways to Heaven',
            'City Walls and Gates',
            'Palaces of Mesopotamia',
            'Irrigation and Engineering',
            'Life in a City-State',
        ],
        'Writing & Mathematics': [
            'Cuneiform Writing System',
            'Scribes and Schools',
            'Early Number Systems',
            'Babylonian Mathematics',
            'Astronomical Records',
            'Libraries of Clay',
        ],
        'Art & Craftsmanship': [
            'Cylinder Seals and Impressions',
            'Metalwork and Jewelry',
            'Pottery and Ceramics',
            'Textile Arts of Sumer',
            'Musical Instruments',
            'Sculpture and Relief',
        ],
        'Trade & Economy': [
            'Trade Routes of Mesopotamia',
            'Weights and Measures',
            'Markets and Merchants',
            'Resources and Raw Materials',
            'Maritime Trade',
            'Economic Tablets',
        ],
        'Law & Governance': [
            'The Code of Hammurabi',
            'Kings and Dynasties',
            'Justice and Punishment',
            'Land Ownership',
            'Diplomacy and Treaties',
            'Military Organization',
        ],
        'Legacy & Connections': [
            'Mesopotamia and Egypt',
            'Influence on Greek Thought',
            'Modern Archaeology',
            'Preserving Ancient Sites',
            'Mathematics Through the Ages',
            'Mesopotamia in the Modern World',
        ],
    }

    unit_order = [
        'Origins & Creation',
        'Gods & Mythology',
        'City-States & Architecture',
        'Writing & Mathematics',
        'Art & Craftsmanship',
        'Trade & Economy',
        'Law & Governance',
        'Legacy & Connections',
    ]

    lesson_variables = {
        'The Fertile Crescent': ('Enki', 'Standard of Ur', 'Geometric shapes in maps', 'Map drawing, clay tablet', 'Southern Iraq', 'River curves & circles', 'Waters of creation', 'Satellite vs ancient maps'),
        'Sumerian Creation Myths': ('Nammu', 'Weld-Blundell Prism', 'Symmetry in creation', 'Creation story illustration', 'Eridu', 'Bilateral symmetry', 'Primordial ocean', 'Chaos-to-order visuals'),
        'The First Settlements': ('Enlil', 'Tell Brak Eye Idols', 'Area & perimeter of dwellings', 'Settlement layout design', 'Tell Brak', 'Rectangular grids', 'Taming the wild', 'Aerial settlement views'),
        'Birth of Agriculture': ('Ashnan', 'Seed Plow Model', 'Measurement & ratios', 'Planting grid activity', 'Girsu', 'Parallel lines, rows', 'Gift of grain', 'Farm tool close-ups'),
        'Early River Civilizations': ('Ea', 'Gudea Cylinders', 'Scale & proportion', 'River map overlay', 'Lagash', 'Meander curves', 'River journeys', 'Tigris/Euphrates imagery'),
        'Foundations of Society': ('Utu', 'Law Code Stele', 'Organizational charts', 'Society pyramid build', 'Nippur', 'Hierarchical triangles', 'Order from chaos', 'Social structure diagrams'),
        'The Sumerian Pantheon': ('An', 'Votive Statues', 'Angles of worship', 'Pantheon family tree', 'Uruk', 'Star polygons', 'Assembly of gods', 'Temple statue groupings'),
        'Enlil: Lord of the Wind': ('Enlil', 'Enlil Temple Model', 'Wind force vectors', 'Wind direction compass', 'Nippur', 'Directional arrows', 'Storm & calm', 'Wind pattern diagrams'),
        'Inanna: Queen of Heaven': ('Inanna', 'Inanna Vase', 'Rotational symmetry', 'Star of Inanna drawing', 'Uruk', 'Eight-pointed star', 'Descent & return', 'Venus star imagery'),
        'The Epic of Gilgamesh': ('Gilgamesh', 'Gilgamesh Tablet', 'Distance & journey math', 'Epic timeline map', 'Uruk', 'Spiral journey path', 'Quest for immortality', 'Hero journey scenes'),
        'Myths of the Underworld': ('Ereshkigal', 'Queen of Night Relief', 'Negative numbers & depth', 'Underworld layer diagram', 'Kur', 'Concentric circles down', 'Seven gates', 'Dark realm imagery'),
        'Rituals and Offerings': ('Ninhursag', 'Ram in Thicket', 'Fractions in offerings', 'Offering proportion chart', 'Ur', 'Division & fractions', 'Sacred giving', 'Ritual scene details'),
        'Rise of Ur and Uruk': ('Nanna', 'Royal Game of Ur', 'Grid coordinates', 'City plan grid overlay', 'Ur', 'Rectangular planning', 'City founding', 'Aerial city ruins'),
        'Ziggurats: Stairways to Heaven': ('Marduk', 'Ziggurat Model', 'Volume of stepped pyramids', '3D ziggurat construction', 'Babylon', 'Stacked rectangles', 'Climbing to heaven', 'Ziggurat cross-sections'),
        'City Walls and Gates': ('Adad', 'Ishtar Gate Tiles', 'Perimeter & fortification', 'Wall defense blueprint', 'Babylon', 'Rectangular perimeters', 'Protection & power', 'Ishtar Gate details'),
        'Palaces of Mesopotamia': ('Shamash', 'Balawat Gates', 'Floor plan geometry', 'Palace room layout', 'Nimrud', 'Complex floor plans', 'Royal grandeur', 'Palace relief carvings'),
        'Irrigation and Engineering': ('Enki', 'Canal Map Tablet', 'Water flow rates', 'Canal system design', 'Girsu', 'Channel networks', 'Taming the waters', 'Irrigation channel photos'),
        'Life in a City-State': ('Ningal', 'Marketplace Seal', 'Population statistics', 'Daily life diorama', 'Ur', 'Neighborhood grids', 'Community living', 'Market scene images'),
        'Cuneiform Writing System': ('Nabu', 'Cuneiform Tablet', 'Angles in wedge marks', 'Clay tablet pressing', 'Nippur', 'Wedge angles', 'Gift of writing', 'Cuneiform close-ups'),
        'Scribes and Schools': ('Nisaba', 'School Tablet', 'Counting systems base-60', 'Scribal practice exercise', 'Nippur', 'Ordered rows/columns', 'Knowledge keepers', 'School tablet replicas'),
        'Early Number Systems': ('Nabu', 'Counting Tokens', 'Base-60 number system', 'Number conversion activity', 'Susa', 'Positional notation', 'Counting the stars', 'Token & tablet photos'),
        'Babylonian Mathematics': ('Shamash', 'Plimpton 322', 'Pythagorean triples', 'Triangle construction', 'Larsa', 'Right triangles', 'Measuring the world', 'Plimpton 322 close-up'),
        'Astronomical Records': ('Sin', 'Venus Tablet', 'Circular measurement', 'Star chart plotting', 'Babylon', 'Circles & degrees', 'Reading the heavens', 'Star chart imagery'),
        'Libraries of Clay': ('Nabu', 'Library Catalog Tablet', 'Sorting & classification', 'Library catalog system', 'Nineveh', 'Organizational grids', 'Preserving knowledge', 'Ashurbanipal library'),
        'Cylinder Seals and Impressions': ('Ea', 'Cylinder Seal', 'Circumference & rotation', 'Seal rolling activity', 'Ur', 'Cylinders & circles', 'Identity marks', 'Seal impression details'),
        'Metalwork and Jewelry': ('Inanna', 'Gold Helmet of Meskalamdug', 'Weight & measurement', 'Jewelry design template', 'Ur', 'Circular forms', 'Adornment of gods', 'Royal jewelry photos'),
        'Pottery and Ceramics': ('Ninhursag', 'Ubaid Pottery', 'Volume of vessels', 'Pot shape design', 'Eridu', 'Cross-sections, curves', 'Shaping the earth', 'Painted pottery patterns'),
        'Textile Arts of Sumer': ('Uttu', 'Textile Fragment', 'Pattern tessellation', 'Weaving pattern grid', 'Ur', 'Repeating patterns', 'Weaving fate', 'Textile pattern close-ups'),
        'Musical Instruments': ('Inanna', 'Bull-Headed Lyre', 'Sound wave frequencies', 'String length experiment', 'Ur', 'Harmonic ratios', 'Music of the gods', 'Lyre reconstruction photos'),
        'Sculpture and Relief': ('Ningirsu', 'Stele of Vultures', 'Proportion in figures', 'Figure proportion grid', 'Girsu', 'Human proportions', 'Stories in stone', 'Relief carving details'),
        'Trade Routes of Mesopotamia': ('Shamash', 'Trade Record Tablet', 'Distance & rate problems', 'Trade route mapping', 'Dilmun', 'Network paths', 'Merchant journeys', 'Ancient route maps'),
        'Weights and Measures': ('Utu', 'Stone Weight Set', 'Unit conversion', 'Weight comparison lab', 'Ur', 'Balance & equality', 'Fair measure', 'Standard weight photos'),
        'Markets and Merchants': ('Shamash', 'Merchant Seal', 'Profit & loss calculation', 'Market price simulation', 'Sippar', 'Exchange ratios', 'Marketplace tales', 'Market scene seals'),
        'Resources and Raw Materials': ('Enki', 'Lapis Lazuli Artifacts', 'Supply & distribution', 'Resource allocation map', 'Badakhshan', 'Distribution networks', 'Gifts of the earth', 'Raw material samples'),
        'Maritime Trade': ('Enki', 'Model Boat', 'Speed & distance on water', 'Boat design challenge', 'Persian Gulf', 'Curved hull shapes', 'Sea voyages', 'Ancient boat models'),
        'Economic Tablets': ('Nabu', 'Drehem Tablet', 'Data tables & records', 'Spreadsheet recreation', 'Drehem', 'Data organization', 'Counting wealth', 'Economic tablet photos'),
        'The Code of Hammurabi': ('Shamash', 'Code of Hammurabi Stele', 'Logic & if-then statements', 'Law code writing activity', 'Babylon', 'Hierarchical structure', 'Divine justice', 'Hammurabi stele details'),
        'Kings and Dynasties': ('Enlil', 'Sumerian King List', 'Timeline & number lines', 'Dynasty timeline builder', 'Ur', 'Linear sequences', 'Rise & fall of kings', 'King list prism photos'),
        'Justice and Punishment': ('Utu', 'Court Record Tablet', 'Proportional reasoning', 'Justice scenario cards', 'Sippar', 'Balance & proportion', 'Scales of justice', 'Court scene imagery'),
        'Land Ownership': ('Enlil', 'Kudurru Boundary Stone', 'Area calculation', 'Land survey activity', 'Babylon', 'Boundary polygons', 'Marking the earth', 'Boundary stone symbols'),
        'Diplomacy and Treaties': ('Ea', 'Amarna Letters', 'Venn diagrams & sets', 'Treaty negotiation game', 'Amarna', 'Overlapping circles', 'Words of peace', 'Letter tablet photos'),
        'Military Organization': ('Nergal', 'Siege Scene Relief', 'Formation geometry', 'Battle formation design', 'Nineveh', 'Grid formations', 'Art of war', 'Battle relief details'),
        'Mesopotamia and Egypt': ('Shamash', 'Comparative Artifacts', 'Comparing geometric styles', 'Civilization comparison chart', 'Memphis', 'Contrasting shapes', 'Meeting of cultures', 'Side-by-side artifacts'),
        'Influence on Greek Thought': ('Nabu', 'Mathematical Tablet', 'Theorem comparison', 'Math history timeline', 'Athens', 'Proof structures', 'Seeds of philosophy', 'Greek/Babylonian math'),
        'Modern Archaeology': ('Nabu', 'Excavation Photo Set', 'Grid reference systems', 'Dig site grid activity', 'Nineveh', 'Coordinate grids', 'Uncovering the past', 'Excavation site photos'),
        'Preserving Ancient Sites': ('Ninhursag', 'Restoration Photos', 'Decay & rate of change', 'Preservation plan design', 'Babylon', 'Structural geometry', 'Saving heritage', 'Before/after restoration'),
        'Mathematics Through the Ages': ('Nabu', 'Math Evolution Chart', 'Number system evolution', 'Math timeline collage', 'Global', 'Evolving notation', 'Eternal numbers', 'Math system comparison'),
        'Mesopotamia in the Modern World': ('Enki', 'Modern Iraq Map', 'Statistical analysis', 'Legacy infographic design', 'Baghdad', 'Data visualization', 'Living legacy', 'Modern/ancient overlays'),
    }

    lesson_num = 1
    for unit_name in unit_order:
        for title in lessons_by_unit[unit_name]:
            vars_data = lesson_variables.get(title, ('', '', '', '', '', '', '', ''))
            cur.execute('''
                INSERT INTO production_lessons (lesson_number, title, unit, god, artifact, math_concept, activity, location, geometric_theme, myth_theme, image_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (lesson_num, title, unit_name, vars_data[0], vars_data[1], vars_data[2], vars_data[3], vars_data[4], vars_data[5], vars_data[6], vars_data[7]))
            lesson_num += 1

    cur.execute('SELECT id FROM production_lessons ORDER BY lesson_number')
    lesson_rows = cur.fetchall()
    cur.execute('SELECT id, team_number, name FROM production_teams ORDER BY team_number')
    team_rows = cur.fetchall()

    team_task_types = {
        1: 'sourcing',
        2: 'download',
        3: 'myth_writing',
        4: 'overlay',
        5: 'storytelling',
        6: 'math',
        7: 'activities',
        8: 'assembly',
        9: 'ai_images',
    }

    for lesson in lesson_rows:
        for team in team_rows:
            task_type = team_task_types[team['team_number']]
            cur.execute('''
                INSERT INTO production_tasks (lesson_id, team_id, task_type, status)
                VALUES (%s, %s, %s, 'not_started')
            ''', (lesson['id'], team['id'], task_type))

    seed_assets(cur)
    seed_content_items(cur)
    seed_assembly_checklists(cur)
    seed_qa_reviews(cur)

    cur.close()
    conn.close()

def seed_assets(cur):
    cur.execute('SELECT COUNT(*) as cnt FROM production_assets')
    if cur.fetchone()['cnt'] > 0:
        return
    cur.execute('SELECT id, lesson_number, title, artifact, god FROM production_lessons ORDER BY lesson_number')
    all_lessons = cur.fetchall()

    museums = ['Metropolitan Museum', 'British Museum', 'Louvre', 'Penn Museum', 'Oriental Institute']

    for i, lesson in enumerate(all_lessons):
        lid = lesson['id']
        artifact_name = lesson['artifact'] or f"Artifact {lesson['lesson_number']}"
        god_name = lesson['god'] or 'Unknown'
        museum = museums[i % len(museums)]

        cur.execute('''
            INSERT INTO production_assets (lesson_id, asset_type, title, description, source, license, status)
            VALUES (%s, 'artifact', %s, %s, %s, 'Public Domain', 'planned')
        ''', (lid, artifact_name, f'Primary artifact for lesson {lesson["lesson_number"]}', museum))
        cur.execute('''
            INSERT INTO production_assets (lesson_id, asset_type, title, description, source, license, status)
            VALUES (%s, 'artifact', %s, %s, %s, 'Public Domain', 'planned')
        ''', (lid, f'{artifact_name} - Detail View', f'Detail photograph of {artifact_name}', museum))
        cur.execute('''
            INSERT INTO production_assets (lesson_id, asset_type, title, description, source, license, status)
            VALUES (%s, 'artifact', %s, %s, %s, 'Public Domain', 'planned')
        ''', (lid, f'{artifact_name} - Context', f'Contextual view showing {artifact_name} in museum setting', museum))

        for j, img_type in enumerate(['Hero image', 'Artifact photo 1', 'Artifact photo 2', 'Background texture', 'Map/diagram']):
            cur.execute('''
                INSERT INTO production_assets (lesson_id, asset_type, title, description, source, status)
                VALUES (%s, 'download', %s, %s, %s, 'planned')
            ''', (lid, f'{img_type} - L{lesson["lesson_number"]}', f'{img_type} for {lesson["title"]}', f'{museum} Digital Archive'))

        gen_items = [
            (f'{god_name} character portrait', 'myth_character', 'Gemini API'),
            (f'{god_name} in scene', 'myth_character', 'Gemini API'),
            (f'Geometric concept diagram', 'concept_diagram', 'OpenAI API'),
            (f'Activity step illustration', 'activity_visual', 'OpenAI API'),
        ]
        for title_g, desc, src in gen_items:
            cur.execute('''
                INSERT INTO production_assets (lesson_id, asset_type, title, description, source, status)
                VALUES (%s, 'generated', %s, %s, %s, 'planned')
            ''', (lid, f'{title_g} - L{lesson["lesson_number"]}', desc, src))

        for ov_type in ['Primary geometric overlay', 'Measurement labels overlay']:
            cur.execute('''
                INSERT INTO production_assets (lesson_id, asset_type, title, description, status)
                VALUES (%s, 'overlay', %s, %s, 'planned')
            ''', (lid, f'{ov_type} - L{lesson["lesson_number"]}', f'SVG overlay for {lesson["title"]}'))

def seed_content_items(cur):
    cur.execute('SELECT COUNT(*) as cnt FROM content_items')
    if cur.fetchone()['cnt'] > 0:
        return
    cur.execute('SELECT id, lesson_number, title, god, myth_theme, math_concept, activity FROM production_lessons ORDER BY lesson_number')
    all_lessons = cur.fetchall()
    writers = ['Writer A', 'Writer B', 'Writer C', 'Writer D', 'Writer E']
    for i, lesson in enumerate(all_lessons):
        lid = lesson['id']
        lnum = lesson['lesson_number']
        god = lesson['god'] or 'Unknown'
        myth = lesson['myth_theme'] or 'Mythology'
        math = lesson['math_concept'] or 'Mathematics'
        act = lesson['activity'] or 'Activity'
        w = writers[i % len(writers)]
        items = [
            ('myth', f'{god}: {myth}', f'Mythological narrative for lesson {lnum} featuring {god}', w),
            ('math', f'Math: {math}', f'Mathematical content covering {math} for lesson {lnum}', w),
            ('visual_story', f'Visual Story: {lesson["title"]}', f'Visual storytelling script with image sequences for lesson {lnum}', w),
            ('activity', f'Activity: {act}', f'Student activity instructions for {act} in lesson {lnum}', w),
        ]
        for ctype, title, body_desc, assigned in items:
            cur.execute('''
                INSERT INTO content_items (lesson_id, content_type, title, body, status, assigned_to)
                VALUES (%s, %s, %s, %s, 'not_started', %s)
            ''', (lid, ctype, title, body_desc, assigned))

def seed_assembly_checklists(cur):
    cur.execute('SELECT COUNT(*) as cnt FROM assembly_checklists')
    if cur.fetchone()['cnt'] > 0:
        return
    cur.execute('SELECT id, lesson_number FROM production_lessons ORDER BY lesson_number')
    all_lessons = cur.fetchall()
    components = [
        ('artifacts_ready', 'All museum artifacts sourced and cataloged'),
        ('downloads_ready', 'All download images acquired'),
        ('content_written', 'Myth, math, and activity text finalized'),
        ('ai_images_generated', 'AI-generated images created and approved'),
        ('overlays_designed', 'Geometric overlays designed in SVG'),
        ('layout_assembled', 'Full lesson layout assembled and formatted'),
    ]
    for lesson in all_lessons:
        for comp, note in components:
            cur.execute('''
                INSERT INTO assembly_checklists (lesson_id, component, status, notes)
                VALUES (%s, %s, 'pending', %s)
            ''', (lesson['id'], comp, note))

def seed_qa_reviews(cur):
    cur.execute('SELECT COUNT(*) as cnt FROM qa_reviews')
    if cur.fetchone()['cnt'] > 0:
        return
    cur.execute('SELECT id, lesson_number FROM production_lessons ORDER BY lesson_number')
    all_lessons = cur.fetchall()
    categories = [
        ('content_accuracy', 'Historical and factual accuracy of all text'),
        ('visual_quality', 'Image resolution, composition, and relevance'),
        ('math_correctness', 'Mathematical examples, problems, and solutions verified'),
        ('accessibility', 'Alt text, readability, color contrast compliance'),
        ('standards_alignment', 'Alignment with curriculum standards and learning objectives'),
    ]
    for lesson in all_lessons:
        for cat, note in categories:
            cur.execute('''
                INSERT INTO qa_reviews (lesson_id, category, status, reviewer_notes)
                VALUES (%s, %s, 'not_checked', %s)
            ''', (lesson['id'], cat, note))

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def serve_favicon():
    return ('', 204)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/documents/<doc_key>', methods=['GET'])
def get_document(doc_key):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM documents WHERE doc_key = %s', (doc_key,))
    doc = cur.fetchone()
    if not doc:
        cur.close()
        conn.close()
        return jsonify({'doc_key': doc_key, 'title': '', 'content': '', 'exists': False})
    doc['updated_at'] = doc['updated_at'].isoformat() if doc['updated_at'] else None
    cur.close()
    conn.close()
    return jsonify({**dict(doc), 'exists': True})

@app.route('/api/documents/<doc_key>', methods=['PUT'])
def save_document(doc_key):
    data = request.get_json()
    title = data.get('title', 'Untitled')
    content = data.get('content', '')
    save_note = data.get('save_note', '')

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        'SELECT MAX(version_number) as max_ver FROM document_versions WHERE doc_key = %s',
        (doc_key,)
    )
    result = cur.fetchone()
    next_version = (result['max_ver'] or 0) + 1

    cur.execute('''
        INSERT INTO documents (doc_key, title, content, updated_at)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (doc_key) DO UPDATE SET
            title = EXCLUDED.title,
            content = EXCLUDED.content,
            updated_at = NOW()
    ''', (doc_key, title, content))

    cur.execute('''
        INSERT INTO document_versions (doc_key, version_number, title, content, saved_at, save_note)
        VALUES (%s, %s, %s, %s, NOW(), %s)
    ''', (doc_key, next_version, title, content, save_note))

    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'version': next_version,
        'saved_at': datetime.now().isoformat()
    })

@app.route('/api/documents/<doc_key>/versions', methods=['GET'])
def get_versions(doc_key):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT id, version_number, title, saved_at, save_note,
               LENGTH(content) as content_length
        FROM document_versions 
        WHERE doc_key = %s 
        ORDER BY version_number DESC
    ''', (doc_key,))
    versions = cur.fetchall()
    for v in versions:
        v['saved_at'] = v['saved_at'].isoformat() if v['saved_at'] else None
    cur.close()
    conn.close()
    return jsonify(versions)

@app.route('/api/documents/<doc_key>/versions/<int:version_number>', methods=['GET'])
def get_version(doc_key, version_number):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT * FROM document_versions 
        WHERE doc_key = %s AND version_number = %s
    ''', (doc_key, version_number))
    version = cur.fetchone()
    cur.close()
    conn.close()
    if not version:
        return jsonify({'error': 'Version not found'}), 404
    version['saved_at'] = version['saved_at'].isoformat() if version['saved_at'] else None
    return jsonify(dict(version))

@app.route('/api/documents/<doc_key>/versions/<int:version_number>/restore', methods=['POST'])
def restore_version(doc_key, version_number):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT * FROM document_versions 
        WHERE doc_key = %s AND version_number = %s
    ''', (doc_key, version_number))
    version = cur.fetchone()
    if not version:
        cur.close()
        conn.close()
        return jsonify({'error': 'Version not found'}), 404

    cur.execute(
        'SELECT MAX(version_number) as max_ver FROM document_versions WHERE doc_key = %s',
        (doc_key,)
    )
    result = cur.fetchone()
    next_version = (result['max_ver'] or 0) + 1

    cur.execute('''
        INSERT INTO documents (doc_key, title, content, updated_at)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (doc_key) DO UPDATE SET
            title = EXCLUDED.title,
            content = EXCLUDED.content,
            updated_at = NOW()
    ''', (doc_key, version['title'], version['content']))

    cur.execute('''
        INSERT INTO document_versions (doc_key, version_number, title, content, saved_at, save_note)
        VALUES (%s, %s, %s, %s, NOW(), %s)
    ''', (doc_key, next_version, version['title'], version['content'],
          f'Restored from version {version_number}'))

    cur.close()
    conn.close()

    return jsonify({
        'success': True,
        'version': next_version,
        'saved_at': datetime.now().isoformat()
    })

@app.route('/api/playground/drafts', methods=['GET'])
def list_drafts():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT id, draft_key, title, status, review_feedback,
               LENGTH(html_content) as html_length,
               created_at, updated_at
        FROM playground_drafts ORDER BY updated_at DESC
    ''')
    drafts = cur.fetchall()
    for d in drafts:
        d['created_at'] = d['created_at'].isoformat() if d['created_at'] else None
        d['updated_at'] = d['updated_at'].isoformat() if d['updated_at'] else None
    cur.close()
    conn.close()
    return jsonify(drafts)

@app.route('/api/playground/drafts/<draft_key>', methods=['GET'])
def get_draft(draft_key):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM playground_drafts WHERE draft_key = %s', (draft_key,))
    draft = cur.fetchone()
    cur.close()
    conn.close()
    if not draft:
        return jsonify({'exists': False, 'draft_key': draft_key})
    draft['created_at'] = draft['created_at'].isoformat() if draft['created_at'] else None
    draft['updated_at'] = draft['updated_at'].isoformat() if draft['updated_at'] else None
    return jsonify({**dict(draft), 'exists': True})

@app.route('/api/playground/drafts/<draft_key>', methods=['PUT'])
def save_draft(draft_key):
    data = request.get_json()
    title = data.get('title', 'Untitled Draft')
    html_content = data.get('html_content', '')
    css_content = data.get('css_content', '')

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO playground_drafts (draft_key, title, html_content, css_content, updated_at)
        VALUES (%s, %s, %s, %s, NOW())
        ON CONFLICT (draft_key) DO UPDATE SET
            title = EXCLUDED.title,
            html_content = EXCLUDED.html_content,
            css_content = EXCLUDED.css_content,
            updated_at = NOW()
    ''', (draft_key, title, html_content, css_content))
    cur.close()
    conn.close()
    return jsonify({'success': True, 'saved_at': datetime.now().isoformat()})

@app.route('/api/playground/drafts/<draft_key>', methods=['DELETE'])
def delete_draft(draft_key):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM playground_drafts WHERE draft_key = %s', (draft_key,))
    cur.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/playground/review', methods=['POST'])
def ai_review():
    data = request.get_json()
    html_content = data.get('html_content', '')
    css_content = data.get('css_content', '')
    title = data.get('title', 'Untitled')
    draft_key = data.get('draft_key', '')

    prompt = f"""You are reviewing a draft page for the Geo-Arts Curriculum System — a visual-first educational platform that processes content through 5 engines: Governance, Knowledge Graph, RWI System, Lesson Builder, and Teacher/Student Facing.

Review the following HTML/CSS draft and provide feedback on:
1. **Content Quality** — Is the content clear, educational, and well-organized?
2. **Visual Design** — Does the layout work well? Any improvements?
3. **Curriculum Alignment** — Does it fit the Geo-Arts visual-first philosophy (every content piece needs an image)?
4. **Technical Quality** — Is the HTML/CSS well-structured and accessible?
5. **Suggestions** — What specific improvements would make this better?

Give a rating: PASS (ready to use), NEEDS WORK (has issues), or REVISE (major changes needed).

Draft Title: {title}

HTML Content:
```html
{html_content[:8000]}
```

{f'CSS Content:' if css_content else ''}
{f'```css' if css_content else ''}
{css_content[:3000] if css_content else ''}
{f'```' if css_content else ''}

Provide your review in a clear, friendly format. Be specific with suggestions."""

    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        feedback = response.choices[0].message.content

        if draft_key:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                UPDATE playground_drafts 
                SET review_feedback = %s, status = 'reviewed', updated_at = NOW()
                WHERE draft_key = %s
            ''', (feedback, draft_key))
            cur.close()
            conn.close()

        return jsonify({'success': True, 'feedback': feedback})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/production/stats', methods=['GET'])
def production_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT COUNT(*) as total FROM production_lessons')
    total_lessons = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as cnt FROM production_lessons WHERE status = 'complete'")
    lessons_complete = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM production_lessons WHERE status = 'in_progress'")
    lessons_in_progress = cur.fetchone()['cnt']
    cur.execute('SELECT COUNT(*) as total FROM production_tasks')
    total_tasks = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as cnt FROM production_tasks WHERE status = 'complete'")
    tasks_complete = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM production_tasks WHERE status = 'in_progress'")
    tasks_in_progress = cur.fetchone()['cnt']
    cur.execute("""
        SELECT COUNT(DISTINCT t.id) as cnt FROM production_teams t
        JOIN production_tasks pt ON pt.team_id = t.id
        WHERE pt.status = 'in_progress'
    """)
    teams_active = cur.fetchone()['cnt']
    cur.close()
    conn.close()
    return jsonify({
        'total_lessons': total_lessons,
        'lessons_complete': lessons_complete,
        'lessons_in_progress': lessons_in_progress,
        'total_tasks': total_tasks,
        'tasks_complete': tasks_complete,
        'tasks_in_progress': tasks_in_progress,
        'teams_active': teams_active,
        'museum_artifacts': '144+',
        'downloaded_images': '2,400+',
        'ai_generated_images': '1,500+',
        'myth_sections': 144,
        'geometric_overlays': '400-600',
        'math_problems': '240+',
        'activity_sets': 96,
    })

@app.route('/api/production/teams', methods=['GET'])
def production_teams():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT t.*,
            COUNT(pt.id) as computed_tasks_total,
            COUNT(pt.id) FILTER (WHERE pt.status = 'complete') as computed_tasks_complete,
            COUNT(pt.id) FILTER (WHERE pt.status = 'in_progress') as computed_tasks_in_progress
        FROM production_teams t
        LEFT JOIN production_tasks pt ON pt.team_id = t.id
        GROUP BY t.id
        ORDER BY t.team_number
    ''')
    teams = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for t in teams:
        total = t['computed_tasks_total']
        complete = t['computed_tasks_complete']
        progress_pct = round((complete / total * 100) if total > 0 else 0, 1)
        result.append({
            'id': t['id'],
            'team_number': t['team_number'],
            'name': t['name'],
            'description': t['description'],
            'color': t['color'],
            'category': t['category'],
            'tasks_total': total,
            'tasks_complete': complete,
            'tasks_in_progress': t['computed_tasks_in_progress'],
            'progress_pct': progress_pct,
        })
    return jsonify(result)

@app.route('/api/production/lessons', methods=['GET'])
def production_lessons():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM production_lessons ORDER BY lesson_number')
    lessons = cur.fetchall()
    cur.execute('''
        SELECT pt.lesson_id, pt.task_type, pt.status
        FROM production_tasks pt
        ORDER BY pt.lesson_id
    ''')
    all_tasks = cur.fetchall()
    cur.close()
    conn.close()

    tasks_by_lesson = {}
    for task in all_tasks:
        lid = task['lesson_id']
        if lid not in tasks_by_lesson:
            tasks_by_lesson[lid] = {}
        tasks_by_lesson[lid][task['task_type']] = task['status']

    stage_keys = ['sourcing', 'download', 'myth_writing', 'overlay',
                  'storytelling', 'math', 'activities', 'ai_images', 'assembly']

    result = []
    for l in lessons:
        lesson_tasks = tasks_by_lesson.get(l['id'], {})
        stages = {}
        for key in stage_keys:
            stages[key] = lesson_tasks.get(key, 'not_started')
        entry = {
            'id': l['id'],
            'lesson_number': l['lesson_number'],
            'title': l['title'],
            'unit': l['unit'],
            'status': l['status'],
            'stages': stages,
        }
        if l.get('created_at'):
            entry['created_at'] = l['created_at'].isoformat()
        if l.get('updated_at'):
            entry['updated_at'] = l['updated_at'].isoformat()
        result.append(entry)
    return jsonify(result)

@app.route('/api/production/tasks/<int:task_id>', methods=['PUT'])
def update_production_task(task_id):
    data = request.get_json()
    new_status = data.get('status', 'not_started')
    if new_status not in ('not_started', 'in_progress', 'complete', 'blocked'):
        return jsonify({'error': 'Invalid status'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        UPDATE production_tasks SET status = %s, updated_at = NOW()
        WHERE id = %s RETURNING *
    ''', (new_status, task_id))
    task = cur.fetchone()
    if not task:
        cur.close()
        conn.close()
        return jsonify({'error': 'Task not found'}), 404

    lesson_id = task['lesson_id']
    cur.execute('SELECT status FROM production_tasks WHERE lesson_id = %s', (lesson_id,))
    task_statuses = [r['status'] for r in cur.fetchall()]

    if all(s == 'complete' for s in task_statuses):
        lesson_status = 'complete'
    elif any(s in ('in_progress', 'complete') for s in task_statuses):
        lesson_status = 'in_progress'
    else:
        lesson_status = 'not_started'

    cur.execute('''
        UPDATE production_lessons SET status = %s, updated_at = NOW()
        WHERE id = %s
    ''', (lesson_status, lesson_id))

    task['updated_at'] = task['updated_at'].isoformat() if task['updated_at'] else None
    cur.close()
    conn.close()
    return jsonify(dict(task))

@app.route('/api/production/tasks/by-lesson/<int:lesson_id>/<int:team_number>', methods=['GET'])
def get_task_by_lesson_team(lesson_id, team_number):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT pt.id as task_id, pt.status, pt.task_type
        FROM production_tasks pt
        JOIN production_teams tm ON pt.team_id = tm.id
        WHERE pt.lesson_id = %s AND tm.team_number = %s
    ''', (lesson_id, team_number))
    task = cur.fetchone()
    cur.close()
    conn.close()
    if not task:
        return jsonify({'task_id': None, 'error': 'Task not found'}), 404
    return jsonify(dict(task))

@app.route('/api/production/lessons/<int:lesson_id>', methods=['PUT'])
def update_production_lesson(lesson_id):
    data = request.get_json()
    new_status = data.get('status', 'not_started')
    if new_status not in ('not_started', 'in_progress', 'complete', 'blocked'):
        return jsonify({'error': 'Invalid status'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        UPDATE production_lessons SET status = %s, updated_at = NOW()
        WHERE id = %s RETURNING *
    ''', (new_status, lesson_id))
    lesson = cur.fetchone()
    cur.close()
    conn.close()
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    lesson['created_at'] = lesson['created_at'].isoformat() if lesson['created_at'] else None
    lesson['updated_at'] = lesson['updated_at'].isoformat() if lesson['updated_at'] else None
    return jsonify(dict(lesson))

VARIABLE_COLS = ['god', 'artifact', 'math_concept', 'activity', 'location', 'geometric_theme', 'myth_theme', 'image_notes']

@app.route('/api/production/variables', methods=['GET'])
def production_variables():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT id, lesson_number, title, unit, god, artifact, math_concept,
               activity, location, geometric_theme, myth_theme, image_notes
        FROM production_lessons ORDER BY lesson_number
    ''')
    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lessons)

@app.route('/api/production/variables/<int:lesson_id>', methods=['PUT'])
def update_lesson_variables(lesson_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    set_parts = []
    values = []
    for col in VARIABLE_COLS:
        if col in data:
            set_parts.append(f"{col} = %s")
            values.append(data[col])
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(lesson_id)
    cur.execute(f'''
        UPDATE production_lessons SET {', '.join(set_parts)}
        WHERE id = %s RETURNING id, lesson_number, title, unit, god, artifact,
        math_concept, activity, location, geometric_theme, myth_theme, image_notes
    ''', values)
    lesson = cur.fetchone()
    cur.close()
    conn.close()
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    return jsonify(dict(lesson))

ASSET_STATUSES = ('planned', 'sourced', 'downloaded', 'ready', 'rejected')

@app.route('/api/production/assets/stats', methods=['GET'])
def asset_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT asset_type,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'ready') as ready,
            COUNT(*) FILTER (WHERE status = 'sourced') as sourced,
            COUNT(*) FILTER (WHERE status = 'downloaded') as downloaded,
            COUNT(*) FILTER (WHERE status = 'planned') as planned,
            COUNT(*) FILTER (WHERE status = 'rejected') as rejected
        FROM production_assets
        GROUP BY asset_type
        ORDER BY asset_type
    ''')
    by_type = cur.fetchall()
    cur.execute('''
        SELECT COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'ready') as ready
        FROM production_assets
    ''')
    overall = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({'by_type': by_type, 'overall': dict(overall)})

@app.route('/api/production/assets', methods=['GET'])
def list_assets():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    asset_type = request.args.get('type', '')
    lesson_id = request.args.get('lesson_id', '')
    status = request.args.get('status', '')

    where_parts = []
    params = []
    if asset_type:
        where_parts.append("a.asset_type = %s")
        params.append(asset_type)
    if lesson_id:
        where_parts.append("a.lesson_id = %s")
        params.append(int(lesson_id))
    if status:
        where_parts.append("a.status = %s")
        params.append(status)

    where_clause = (' WHERE ' + ' AND '.join(where_parts)) if where_parts else ''

    cur.execute(f'''
        SELECT a.*, pl.lesson_number, pl.title as lesson_title, pl.unit
        FROM production_assets a
        JOIN production_lessons pl ON a.lesson_id = pl.id
        {where_clause}
        ORDER BY pl.lesson_number, a.asset_type, a.id
    ''', params)
    assets = cur.fetchall()
    cur.close()
    conn.close()
    for a in assets:
        a['created_at'] = a['created_at'].isoformat() if a.get('created_at') else None
        a['updated_at'] = a['updated_at'].isoformat() if a.get('updated_at') else None
    return jsonify(assets)

@app.route('/api/production/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    asset_type = data.get('asset_type', 'artifact')
    title = data.get('title', '')
    if not lesson_id or not title:
        return jsonify({'error': 'lesson_id and title required'}), 400
    if asset_type not in ('artifact', 'download', 'generated', 'overlay'):
        return jsonify({'error': 'Invalid asset_type'}), 400
    status = data.get('status', 'planned')
    if status not in ASSET_STATUSES:
        return jsonify({'error': f'Invalid status. Use: {ASSET_STATUSES}'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        INSERT INTO production_assets (lesson_id, asset_type, title, description, source, source_url, license, status, filename)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    ''', (lesson_id, asset_type, title,
          data.get('description', ''), data.get('source', ''),
          data.get('source_url', ''), data.get('license', ''),
          status, data.get('filename', '')))
    asset = cur.fetchone()
    cur.close()
    conn.close()
    asset['created_at'] = asset['created_at'].isoformat() if asset.get('created_at') else None
    asset['updated_at'] = asset['updated_at'].isoformat() if asset.get('updated_at') else None
    return jsonify(dict(asset)), 201

@app.route('/api/production/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    allowed = ['title', 'description', 'source', 'source_url', 'license', 'status', 'filename']
    set_parts = []
    values = []
    for col in allowed:
        if col in data:
            if col == 'status' and data[col] not in ASSET_STATUSES:
                cur.close()
                conn.close()
                return jsonify({'error': f'Invalid status. Use: {ASSET_STATUSES}'}), 400
            set_parts.append(f"{col} = %s")
            values.append(data[col])
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(asset_id)
    cur.execute(f'''
        UPDATE production_assets SET {', '.join(set_parts)}
        WHERE id = %s RETURNING *
    ''', values)
    asset = cur.fetchone()
    cur.close()
    conn.close()
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404
    asset['created_at'] = asset['created_at'].isoformat() if asset.get('created_at') else None
    asset['updated_at'] = asset['updated_at'].isoformat() if asset.get('updated_at') else None
    return jsonify(dict(asset))

@app.route('/api/production/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('DELETE FROM production_assets WHERE id = %s RETURNING id', (asset_id,))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({'error': 'Asset not found'}), 404
    return jsonify({'deleted': True, 'id': asset_id})

CONTENT_STATUSES = ('not_started', 'drafting', 'review', 'revision', 'approved')
CONTENT_TYPES = ('myth', 'math', 'visual_story', 'activity')

@app.route('/api/production/content/stats', methods=['GET'])
def content_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT content_type,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'approved') as approved,
            COUNT(*) FILTER (WHERE status = 'drafting') as drafting,
            COUNT(*) FILTER (WHERE status = 'review') as in_review,
            COUNT(*) FILTER (WHERE status = 'revision') as revision,
            COUNT(*) FILTER (WHERE status = 'not_started') as not_started
        FROM content_items
        GROUP BY content_type
        ORDER BY content_type
    ''')
    by_type = cur.fetchall()
    cur.execute('''
        SELECT COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'approved') as approved
        FROM content_items
    ''')
    overall = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({'by_type': by_type, 'overall': dict(overall)})

@app.route('/api/production/content', methods=['GET'])
def list_content():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    content_type = request.args.get('type', '')
    lesson_id = request.args.get('lesson_id', '')
    status = request.args.get('status', '')
    where_parts = []
    params = []
    if content_type:
        where_parts.append("c.content_type = %s")
        params.append(content_type)
    if lesson_id:
        where_parts.append("c.lesson_id = %s")
        params.append(int(lesson_id))
    if status:
        where_parts.append("c.status = %s")
        params.append(status)
    where_clause = (' WHERE ' + ' AND '.join(where_parts)) if where_parts else ''
    cur.execute(f'''
        SELECT c.*, pl.lesson_number, pl.title as lesson_title, pl.unit
        FROM content_items c
        JOIN production_lessons pl ON c.lesson_id = pl.id
        {where_clause}
        ORDER BY pl.lesson_number, c.content_type, c.id
    ''', params)
    items = cur.fetchall()
    cur.close()
    conn.close()
    for item in items:
        item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
        item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(items)

@app.route('/api/production/content', methods=['POST'])
def create_content():
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    content_type = data.get('content_type', 'myth')
    title = data.get('title', '')
    if not lesson_id or not title:
        return jsonify({'error': 'lesson_id and title required'}), 400
    if content_type not in CONTENT_TYPES:
        return jsonify({'error': f'Invalid content_type. Use: {CONTENT_TYPES}'}), 400
    status = data.get('status', 'not_started')
    if status not in CONTENT_STATUSES:
        return jsonify({'error': f'Invalid status. Use: {CONTENT_STATUSES}'}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        INSERT INTO content_items (lesson_id, content_type, title, body, status, assigned_to, word_count, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *
    ''', (lesson_id, content_type, title, data.get('body', ''), status,
          data.get('assigned_to', ''), data.get('word_count', 0), data.get('notes', '')))
    item = cur.fetchone()
    cur.close()
    conn.close()
    item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
    item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(dict(item)), 201

@app.route('/api/production/content/<int:item_id>', methods=['PUT'])
def update_content(item_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    allowed = ['title', 'body', 'status', 'assigned_to', 'word_count', 'notes']
    set_parts = []
    values = []
    for col in allowed:
        if col in data:
            if col == 'status' and data[col] not in CONTENT_STATUSES:
                cur.close()
                conn.close()
                return jsonify({'error': f'Invalid status. Use: {CONTENT_STATUSES}'}), 400
            set_parts.append(f"{col} = %s")
            values.append(data[col])
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(item_id)
    cur.execute(f'''
        UPDATE content_items SET {', '.join(set_parts)}
        WHERE id = %s RETURNING *
    ''', values)
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        return jsonify({'error': 'Content item not found'}), 404
    item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
    item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(dict(item))

@app.route('/api/production/content/<int:item_id>', methods=['DELETE'])
def delete_content(item_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('DELETE FROM content_items WHERE id = %s RETURNING id', (item_id,))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({'error': 'Content item not found'}), 404
    return jsonify({'deleted': True, 'id': item_id})

ASSEMBLY_STATUSES = ('pending', 'in_progress', 'complete', 'blocked')
ASSEMBLY_COMPONENTS = ('artifacts_ready', 'downloads_ready', 'content_written', 'ai_images_generated', 'overlays_designed', 'layout_assembled')

@app.route('/api/production/assembly/stats', methods=['GET'])
def assembly_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT component,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'complete') as complete,
            COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress,
            COUNT(*) FILTER (WHERE status = 'pending') as pending,
            COUNT(*) FILTER (WHERE status = 'blocked') as blocked
        FROM assembly_checklists
        GROUP BY component
        ORDER BY component
    ''')
    by_component = cur.fetchall()
    cur.execute('''
        SELECT COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'complete') as complete
        FROM assembly_checklists
    ''')
    overall = cur.fetchone()
    cur.execute('''
        SELECT pl.id as lesson_id, pl.lesson_number, pl.title, pl.unit,
            COUNT(ac.id) as total_components,
            COUNT(ac.id) FILTER (WHERE ac.status = 'complete') as complete_components
        FROM production_lessons pl
        LEFT JOIN assembly_checklists ac ON ac.lesson_id = pl.id
        GROUP BY pl.id, pl.lesson_number, pl.title, pl.unit
        ORDER BY pl.lesson_number
    ''')
    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'by_component': by_component, 'overall': dict(overall), 'lessons': lessons})

@app.route('/api/production/assembly', methods=['GET'])
def list_assembly():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    lesson_id = request.args.get('lesson_id', '')
    status = request.args.get('status', '')
    where_parts = []
    params = []
    if lesson_id:
        where_parts.append("ac.lesson_id = %s")
        params.append(int(lesson_id))
    if status:
        where_parts.append("ac.status = %s")
        params.append(status)
    where_clause = (' WHERE ' + ' AND '.join(where_parts)) if where_parts else ''
    cur.execute(f'''
        SELECT ac.*, pl.lesson_number, pl.title as lesson_title, pl.unit
        FROM assembly_checklists ac
        JOIN production_lessons pl ON ac.lesson_id = pl.id
        {where_clause}
        ORDER BY pl.lesson_number, ac.component
    ''', params)
    items = cur.fetchall()
    cur.close()
    conn.close()
    for item in items:
        item['completed_at'] = item['completed_at'].isoformat() if item.get('completed_at') else None
        item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
        item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(items)

@app.route('/api/production/assembly/<int:item_id>', methods=['PUT'])
def update_assembly(item_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    new_status = data.get('status')
    notes = data.get('notes')
    set_parts = []
    values = []
    if new_status:
        if new_status not in ASSEMBLY_STATUSES:
            cur.close()
            conn.close()
            return jsonify({'error': f'Invalid status. Use: {ASSEMBLY_STATUSES}'}), 400
        set_parts.append("status = %s")
        values.append(new_status)
        if new_status == 'complete':
            set_parts.append("completed_at = NOW()")
        else:
            set_parts.append("completed_at = NULL")
    if notes is not None:
        set_parts.append("notes = %s")
        values.append(notes)
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(item_id)
    cur.execute(f'''
        UPDATE assembly_checklists SET {', '.join(set_parts)}
        WHERE id = %s RETURNING *
    ''', values)
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        return jsonify({'error': 'Assembly item not found'}), 404
    item['completed_at'] = item['completed_at'].isoformat() if item.get('completed_at') else None
    item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
    item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(dict(item))

QA_STATUSES = ('not_checked', 'pass', 'fail', 'needs_revision')
QA_CATEGORIES = ('content_accuracy', 'visual_quality', 'math_correctness', 'accessibility', 'standards_alignment')

@app.route('/api/production/qa/stats', methods=['GET'])
def qa_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT category,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'pass') as passed,
            COUNT(*) FILTER (WHERE status = 'fail') as failed,
            COUNT(*) FILTER (WHERE status = 'needs_revision') as needs_revision,
            COUNT(*) FILTER (WHERE status = 'not_checked') as not_checked
        FROM qa_reviews
        GROUP BY category
        ORDER BY category
    ''')
    by_category = cur.fetchall()
    cur.execute('''
        SELECT COUNT(*) as total,
            COUNT(*) FILTER (WHERE status = 'pass') as passed,
            COUNT(*) FILTER (WHERE status = 'fail') as failed,
            COUNT(*) FILTER (WHERE status = 'needs_revision') as needs_revision,
            COUNT(*) FILTER (WHERE status = 'not_checked') as not_checked
        FROM qa_reviews
    ''')
    overall = cur.fetchone()
    cur.execute('''
        SELECT pl.id as lesson_id, pl.lesson_number, pl.title, pl.unit,
            COUNT(qr.id) as total_checks,
            COUNT(qr.id) FILTER (WHERE qr.status = 'pass') as passed_checks,
            COUNT(qr.id) FILTER (WHERE qr.status = 'fail') as failed_checks
        FROM production_lessons pl
        LEFT JOIN qa_reviews qr ON qr.lesson_id = pl.id
        GROUP BY pl.id, pl.lesson_number, pl.title, pl.unit
        ORDER BY pl.lesson_number
    ''')
    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'by_category': by_category, 'overall': dict(overall), 'lessons': lessons})

@app.route('/api/production/qa', methods=['GET'])
def list_qa():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    lesson_id = request.args.get('lesson_id', '')
    status = request.args.get('status', '')
    category = request.args.get('category', '')
    where_parts = []
    params = []
    if lesson_id:
        where_parts.append("qr.lesson_id = %s")
        params.append(int(lesson_id))
    if status:
        where_parts.append("qr.status = %s")
        params.append(status)
    if category:
        where_parts.append("qr.category = %s")
        params.append(category)
    where_clause = (' WHERE ' + ' AND '.join(where_parts)) if where_parts else ''
    cur.execute(f'''
        SELECT qr.*, pl.lesson_number, pl.title as lesson_title, pl.unit
        FROM qa_reviews qr
        JOIN production_lessons pl ON qr.lesson_id = pl.id
        {where_clause}
        ORDER BY pl.lesson_number, qr.category
    ''', params)
    items = cur.fetchall()
    cur.close()
    conn.close()
    for item in items:
        item['reviewed_at'] = item['reviewed_at'].isoformat() if item.get('reviewed_at') else None
        item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
        item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(items)

@app.route('/api/production/qa/<int:item_id>', methods=['PUT'])
def update_qa(item_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    new_status = data.get('status')
    notes = data.get('reviewer_notes')
    set_parts = []
    values = []
    if new_status:
        if new_status not in QA_STATUSES:
            cur.close()
            conn.close()
            return jsonify({'error': f'Invalid status. Use: {QA_STATUSES}'}), 400
        set_parts.append("status = %s")
        values.append(new_status)
        set_parts.append("reviewed_at = NOW()")
    if notes is not None:
        set_parts.append("reviewer_notes = %s")
        values.append(notes)
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(item_id)
    cur.execute(f'''
        UPDATE qa_reviews SET {', '.join(set_parts)}
        WHERE id = %s RETURNING *
    ''', values)
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        return jsonify({'error': 'QA review not found'}), 404
    item['reviewed_at'] = item['reviewed_at'].isoformat() if item.get('reviewed_at') else None
    item['created_at'] = item['created_at'].isoformat() if item.get('created_at') else None
    item['updated_at'] = item['updated_at'].isoformat() if item.get('updated_at') else None
    return jsonify(dict(item))

DAYB_SECTION_DEFS = [
    ('B1', 'Bridge Review', 'Answer A7 question - reveal function', '5-7 min', 'drv.G',
     '[Civic object] uses [element] for [function] - now you see why it is there.',
     'Same artifact as A7, now with function labeled/arrows'),
    ('B2', 'Math Proof', 'Verify property through measurement/demonstration', '7-10 min', 'drv.M',
     '[Finding] confirms [property] because [rule] defines it.',
     'Measurement/verification diagram'),
    ('B3', 'Transformation', 'Element in operation - what the math property enables', '7-10 min', 'drv.M',
     '[Element] can [operation verb] because [B2 principle] enables it.',
     'Transformation/vector diagram, motion illustration'),
    ('B4', 'Mechanics', 'What the transformation produces - mechanical result', '5-7 min', 'drv.M',
     '[Operation] produces [result] because [property in motion].',
     'Force/motion diagram, mechanical illustration'),
    ('B5', 'STEM History (Cumulative)', 'Cumulative B2+B3+B4 convergence - where elements sit in STEM timeline', '5-7 min', 'drv.C,drv.I',
     '[Element] contributed to [field] because [property] enabled [advancement].',
     'Historical artifact, timeline diagram, scientific instrument'),
    ('B6', 'The Moment (Invention)', 'Specific discovery/innovation/invention for this lesson', '7-10 min', 'drv.M,drv.C',
     '[Civilization] [discovered/invented] [thing] because [element property] solved [specific problem].',
     'Invention artifact, reconstruction, historical illustration'),
    ('B7', 'Activity', 'Student builds/tests using engineering method', '15-20 min', 'drv.M,drv.C',
     '[Element] can be [built/tested] as [model] because [construction method] applies [principle].',
     'Build instructions, materials list, test setup'),
    ('B8', 'Exit Ticket', 'Synthesize metaphor + function - same property enables both', '5-7 min', 'drv.G',
     '[Element] unites [metaphor meaning] and [function] because [same property] enables both.',
     'Comparison visual, split image (metaphor artifact and function artifact)'),
]

DAYB_LO_TEXTS = {
    'elem.circle': {
        'B1': 'Chariot wheel uses circle for rotation - now you see why the symbol is there',
        'B2': 'Identical radius measurements confirm circularity because equidistance defines circles',
        'B3': 'Circle can rotate uniformly because equidistance maintains constant axle contact',
        'B4': 'Uniform rotation produces smooth motion because constant contact eliminates wobble',
        'B5': 'Circles contributed to astronomy because equidistance enabled celestial tracking',
        'B6': 'Mesopotamians invented the wheel (~3500 BCE) because circular rotation solved transport friction',
        'B7': 'Circle can be tested as wheel model because axle-hole alignment applies equidistance',
        'B8': 'Circle unites Shamash\'s justice and wheel rotation because equidistant radii enable both',
    },
    'elem.star8': {
        'B1': 'Ishtar Gate uses 8-pointed stars for directional orientation - now you see why they mark the entrance',
        'B2': 'Equal 45-degree angles confirm radial symmetry because 360 divided by 8 equals 45 defines the division',
        'B3': '8-pointed star can project directional vectors because equal angles create uniform coverage',
        'B4': 'Directional projection produces orientation reference because known angles create predictable positions',
        'B5': '8-pointed geometry contributed to navigation because radial division enabled star-based wayfinding. Prior: Circle\'s equidistance enabled celestial tracking (B2-B4).',
        'B6': 'Mesopotamians developed the compass rose because 8-point division solved directional disorientation',
        'B7': '8-pointed star can be tested as compass tool because aligned angles indicate cardinal directions',
        'B8': '8-pointed star unites Ishtar\'s protection and compass navigation because equal radial angles enable both',
    },
    'elem.triangle': {
        'B1': 'Ziggurat steps use triangles for structural support - now you see why temples stand tall',
        'B2': 'Fixed angles confirm rigidity because three sides with locked vertices cannot deform',
        'B3': 'Triangle can resist lateral force because structural rigidity prevents deformation under load',
        'B4': 'Resistance to deformation produces stable structures because locked angles distribute force to foundation',
        'B5': 'Triangles contributed to architecture and engineering because rigidity enabled load-bearing structures. Prior: Circle enabled rotation, Star enabled navigation (B2-B4).',
        'B6': 'Mesopotamians engineered the truss (~3000 BCE) because triangular rigidity solved roof-span collapse',
        'B7': 'Triangle can be tested as bridge truss because three-sided frame applies structural rigidity',
        'B8': 'Triangle unites Enlil\'s authority (stable, immovable) and structural engineering because rigidity enables both',
    },
    'elem.square': {
        'B1': 'Clay tablets use rectangles for organized writing - now you see why scribes chose this shape',
        'B2': 'Right-angle measurements confirm regularity because four 90-degree corners with parallel sides define squares',
        'B3': 'Square can tessellate without gaps because right angles and equal sides enable perfect tiling',
        'B4': 'Tessellation produces complete coverage because aligned edges leave no wasted space',
        'B5': 'Squares contributed to urban planning and writing because regularity enabled grid systems and standardized records. Prior: Circle enabled rotation, Star enabled navigation, Triangle enabled structures (B2-B4).',
        'B6': 'Mesopotamians invented the standardized brick (~4000 BCE) because rectangular regularity solved construction alignment',
        'B7': 'Square can be tested as city grid model because right-angle layout applies regularity and tessellation',
        'B8': 'Square unites Nabu\'s wisdom (ordered knowledge) and city planning because right-angle regularity enables both',
    },
    'elem.spiral': {
        'B1': 'Scroll cylinder uses spiral for compact information storage - now you see why scribes used this form',
        'B2': 'Increasing radius measurements confirm spiral because progressive expansion defines the outward curve',
        'B3': 'Spiral can compress long lengths into small space because progressive expansion enables compact winding',
        'B4': 'Compact winding produces efficient storage because coiling maximizes length in minimal area',
        'B5': 'Spirals contributed to mechanics and hydraulics because progressive expansion enabled springs and water flow. Prior: Circle enabled rotation, Star enabled navigation, Triangle enabled structures, Square enabled planning (B2-B4).',
        'B6': 'Mesopotamians developed irrigation channels (~5000 BCE) because spiral water flow solved efficient drainage',
        'B7': 'Spiral can be tested as spring model because coiled wire applies progressive expansion under tension',
        'B8': 'Spiral unites Tiamat\'s primordial chaos (swirling waters) and spring mechanics because progressive expansion enables both',
    },
    'elem.arc': {
        'B1': 'City gate archway uses arc for spanning openings - now you see why gates have curved tops',
        'B2': 'Equal radii to arc points confirm curvature because constant radius from center defines the arc segment',
        'B3': 'Arc can distribute weight to both sides because continuous curvature redirects downward force laterally',
        'B4': 'Lateral force distribution produces stable spans because compression along the curve eliminates central support need',
        'B5': 'Arcs contributed to civil engineering because load distribution enabled monumental gateways and bridges. Prior: Circle, Star, Triangle, Square, Spiral properties enabled rotation, navigation, structures, planning, and mechanics (B2-B4).',
        'B6': 'Mesopotamians engineered the true arch (~2000 BCE) because curved load distribution solved wide-span entry construction',
        'B7': 'Arc can be tested as bridge model because curved block alignment applies load distribution',
        'B8': 'Arc unites Anu\'s sky vault (heavens arching overhead) and architectural spanning because continuous curvature enables both',
    },
    'elem.hexagon': {
        'B1': 'Grain storage vessels use hexagonal packing for efficiency - now you see why nature chose this shape',
        'B2': 'Six equal 120-degree angles confirm hexagonal regularity because equal sides tessellating with no gaps define hexagons',
        'B3': 'Hexagon can tile surfaces completely because optimal angles create seamless coverage with zero waste',
        'B4': 'Complete tiling produces maximum storage efficiency because each cell shares walls with six neighbors',
        'B5': 'Hexagons contributed to materials science and resource management because optimal packing enabled efficient storage and distribution. Prior: Circle, Star, Triangle, Square, Spiral, Arc properties enabled rotation, navigation, structures, planning, mechanics, and spanning (B2-B4).',
        'B6': 'Mesopotamians optimized grain storage (~4500 BCE) because hexagonal vessel arrangement solved warehouse space limitations',
        'B7': 'Hexagon can be tested as storage optimization model because honeycomb tiling applies optimal packing',
        'B8': 'Hexagon unites Nisaba\'s wisdom (efficient record-keeping) and storage engineering because optimal packing enables both',
    },
    'elem.pyramid': {
        'B1': 'Ziggurats use pyramid form for monumental stability - now you see why temples reach toward heaven',
        'B2': 'Wide base and converging faces confirm stability because mass distributed below center of gravity resists toppling',
        'B3': 'Pyramid can channel weight downward because convergent faces direct all force toward the broad base',
        'B4': 'Downward force channeling produces permanent monuments because gravitational alignment prevents structural failure',
        'B5': 'Pyramids contributed to monumental architecture and astronomy because convergent stability enabled tall aligned structures. CUMULATIVE SYNTHESIS: All 8 elements\' B2-B4 chains - Circle\'s rotation, Star\'s navigation, Triangle\'s rigidity, Square\'s tessellation, Spiral\'s compression, Arc\'s spanning, Hexagon\'s packing - converge to show how geometry enabled civilization.',
        'B6': 'Mesopotamians built the Great Ziggurat of Ur (~2100 BCE) because pyramidal convergent stability solved multi-story temple construction',
        'B7': 'Pyramid can be tested as ziggurat model because stacked layers apply convergent stability and weight distribution',
        'B8': 'Pyramid unites Marduk\'s cosmic authority (hierarchy of heavens) and monumental engineering because convergent stability enables both',
    },
}

DAYB_CONTENT_TEMPLATES = {
    'B1': 'Students revisit the artifact from Day A\'s exit ticket. The teacher reveals the functional purpose of the {element_name} in the {carrier} - connecting the symbolic meaning explored on Day A to the real-world engineering function that the geometric property enables.',
    'B2': 'Students conduct hands-on measurement to verify the core property of {element_name}: {core_property}. Through direct observation and measurement, students confirm that {core_definition} - building mathematical proof through empirical evidence.',
    'B3': 'Students explore how the verified property of {element_name} enables transformation. Because {core_property} has been proven, students can now see how {element_name} performs its key operation, connecting static property to dynamic behavior.',
    'B4': 'Students examine the mechanical result produced by {element_name}\'s transformation. The chain from proof (B2) through transformation (B3) to mechanism (B4) shows how geometric properties produce real-world engineering outcomes.',
    'B5': 'Students place {element_name} in the STEM timeline, examining how {core_property} contributed to historical advancement. This cumulative section connects current element knowledge to all previously studied elements, building a coherent picture of how geometry enabled civilization.',
    'B6': 'Students learn about a specific moment of invention where {element_name}\'s property of {core_property} solved a real engineering problem. This grounds abstract geometric knowledge in concrete historical achievement by {deity_name}\'s civilization.',
    'B7': 'Students engage in hands-on engineering activity, building and testing a model that applies {element_name}\'s property of {core_property}. Through construction and experimentation, students experience how geometric principles translate into functional designs.',
    'B8': 'Students synthesize the entire Day B arc by connecting {deity_name}\'s metaphorical meaning to {element_name}\'s functional application. The exit ticket reveals that the same geometric property enables both the cultural symbol and the engineering function.',
}

DAYB_CARRIERS = {
    'elem.circle': {'B1': 'Chariot wheel', 'B2': 'Compass and string', 'B3': 'Rotating disk', 'B4': 'Wheel and axle model', 'B5': 'Astronomical instruments', 'B6': 'Mesopotamian wheel artifact', 'B7': 'Wheel construction kit', 'B8': 'Shamash sun disk / wheel'},
    'elem.star8': {'B1': 'Ishtar Gate', 'B2': 'Protractor and compass', 'B3': 'Directional star model', 'B4': 'Compass rose', 'B5': 'Navigation instruments', 'B6': 'Ancient compass rose', 'B7': 'Star compass tool', 'B8': 'Ishtar star / compass'},
    'elem.triangle': {'B1': 'Ziggurat', 'B2': 'Stick triangle model', 'B3': 'Truss frame', 'B4': 'Load-bearing structure', 'B5': 'Architectural timeline', 'B6': 'Mesopotamian truss', 'B7': 'Bridge truss kit', 'B8': 'Enlil / structural truss'},
    'elem.square': {'B1': 'Clay tablet', 'B2': 'Right-angle measuring tools', 'B3': 'Tiling grid', 'B4': 'Brick wall model', 'B5': 'Urban planning maps', 'B6': 'Standardized brick', 'B7': 'City grid model', 'B8': 'Nabu tablet / city grid'},
    'elem.spiral': {'B1': 'Scroll cylinder', 'B2': 'Spiral measuring tools', 'B3': 'Coiled rope model', 'B4': 'Spring mechanism', 'B5': 'Hydraulic timeline', 'B6': 'Irrigation channel model', 'B7': 'Spring construction kit', 'B8': 'Tiamat waters / spring'},
    'elem.arc': {'B1': 'City gate archway', 'B2': 'Arc measuring tools', 'B3': 'Arch load model', 'B4': 'Bridge span model', 'B5': 'Engineering timeline', 'B6': 'True arch model', 'B7': 'Arch bridge kit', 'B8': 'Anu sky vault / arch'},
    'elem.hexagon': {'B1': 'Grain storage vessel', 'B2': 'Hexagon measuring tools', 'B3': 'Honeycomb tiling model', 'B4': 'Storage efficiency model', 'B5': 'Materials science timeline', 'B6': 'Grain storage arrangement', 'B7': 'Honeycomb construction kit', 'B8': 'Nisaba grain / honeycomb'},
    'elem.pyramid': {'B1': 'Ziggurat of Ur', 'B2': 'Pyramid measuring tools', 'B3': 'Weight channel model', 'B4': 'Monument stability model', 'B5': 'Architecture timeline', 'B6': 'Great Ziggurat of Ur', 'B7': 'Ziggurat construction kit', 'B8': 'Marduk / ziggurat'},
}

DAYB_ECD = {
    'elem.circle': {
        'B1': {
            3: ('Student knows that wheels use circles to roll smoothly', 'Student can point to the circle shape in a wheel', 'Identify the circle in a chariot wheel picture'),
            4: ('Student understands that circular shape enables wheel rotation', 'Student can explain why a wheel needs to be round', 'Compare round vs square wheel and explain difference'),
            5: ('Student can reason that equidistance is the property enabling smooth rotation', 'Student can analyze how changing radius affects wheel function', 'Design an experiment testing wheel smoothness with different shapes'),
        },
        'B2': {
            3: ('Student knows that all radii of a circle are the same length', 'Student can measure radii and confirm they match', 'Measure 4 radii of a drawn circle with a ruler'),
            4: ('Student understands that equal radii define what makes a shape a circle', 'Student can demonstrate equidistance using string and pin', 'Use string-pivot method to draw circle and verify radii'),
            5: ('Student can reason that equidistance is the defining property separating circles from other curves', 'Student can evaluate whether irregular shapes meet circle criteria', 'Test 3 shapes and prove which are true circles using measurement'),
        },
        'B3': {
            3: ('Student knows that circles can spin around their center', 'Student can rotate a circular object on a pencil', 'Spin a cardboard circle on a pencil point'),
            4: ('Student understands that equidistance allows uniform rotation', 'Student can demonstrate and explain smooth vs bumpy rotation', 'Compare spinning a circle vs oval on an axle'),
            5: ('Student can reason that constant radius ensures consistent contact during rotation', 'Student can predict rotation behavior from radius measurements', 'Calculate contact points during one full rotation'),
        },
        'B4': {
            3: ('Student knows that smooth spinning makes things move without bumps', 'Student can observe smooth motion in a wheel demo', 'Roll circular vs non-circular objects and describe motion'),
            4: ('Student understands that constant contact produces smooth mechanical motion', 'Student can connect radius consistency to motion quality', 'Build simple wheel and test load-carrying smoothness'),
            5: ('Student can reason that eliminating wobble requires geometric perfection of equidistance', 'Student can evaluate wheel designs for mechanical efficiency', 'Design optimal wheel and justify dimensions mathematically'),
        },
        'B5': {
            3: ('Student knows that ancient people used circles to watch the sky', 'Student can identify circular tools used in astronomy', 'Match circular instruments to their sky-watching purpose'),
            4: ('Student understands that circular measurement enabled tracking celestial objects', 'Student can explain how circle properties help track stars', 'Plot star positions on a circular chart'),
            5: ('Student can reason that equidistance enabled precise angular measurement for astronomy', 'Student can analyze how circular instruments improved celestial prediction', 'Design a simple astrolabe and explain geometric principles'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians made the first wheels', 'Student can describe what the first wheel looked like', 'Draw and label a Mesopotamian wheel'),
            4: ('Student understands that circular rotation solved the problem of moving heavy loads', 'Student can explain why the wheel was revolutionary', 'Compare dragging vs rolling and measure force difference'),
            5: ('Student can reason that the wheel invention required understanding equidistance to function', 'Student can evaluate the engineering challenges of early wheel design', 'Design a wheel-and-axle system and explain geometric requirements'),
        },
        'B7': {
            3: ('Student knows that a wheel needs a hole in the center for an axle', 'Student can build a simple wheel from cardboard', 'Build a wheel from a cardboard circle and test rolling'),
            4: ('Student understands that axle placement must be at the center for smooth rotation', 'Student can test different axle positions and compare results', 'Build wheels with center vs off-center axles and compare'),
            5: ('Student can reason that axle-hole alignment demonstrates equidistance in engineering', 'Student can optimize wheel design through iterative testing', 'Design, build, and test a wheel system measuring smoothness quantitatively'),
        },
        'B8': {
            3: ('Student knows that circles mean fairness (Shamash) and also make wheels turn', 'Student can name both meanings of circles', 'Draw two pictures: circle as fairness and circle as wheel'),
            4: ('Student understands that the same property (equidistance) enables both justice symbolism and wheel function', 'Student can explain the connection between fairness and rotation', 'Write a paragraph connecting Shamash justice to wheel mechanics'),
            5: ('Student can reason that equidistance simultaneously enables metaphorical and functional applications', 'Student can synthesize cultural and engineering perspectives on circles', 'Create a presentation uniting Shamash symbolism with wheel engineering'),
        },
    },
    'elem.star8': {
        'B1': {
            3: ('Student knows that the Ishtar Gate has star patterns', 'Student can find 8-pointed stars on the gate', 'Circle all 8-pointed stars in an Ishtar Gate image'),
            4: ('Student understands that 8-pointed stars mark directions on the gate', 'Student can explain why stars help with orientation', 'Label compass directions on an 8-pointed star'),
            5: ('Student can reason that radial symmetry provides directional information', 'Student can analyze how star placement creates navigational cues', 'Map the directional logic of stars on the Ishtar Gate'),
        },
        'B2': {
            3: ('Student knows that an 8-pointed star has 8 equal spaces between points', 'Student can count the points and spaces', 'Count points and measure spaces between them'),
            4: ('Student understands that 45-degree angles create 8-fold symmetry', 'Student can measure angles between star points', 'Use a protractor to verify 45-degree angles'),
            5: ('Student can reason that 360/8=45 defines the mathematical basis for 8-fold symmetry', 'Student can prove symmetry through angular measurement', 'Construct an 8-pointed star using only compass and straightedge'),
        },
        'B3': {
            3: ('Student knows that star points can show directions', 'Student can match star points to directions', 'Point to N, S, E, W on an 8-pointed star'),
            4: ('Student understands that equal angles create uniform directional coverage', 'Student can demonstrate how star points map to compass directions', 'Align an 8-pointed star with a compass and verify directions'),
            5: ('Student can reason that uniform angular distribution enables comprehensive directional projection', 'Student can calculate intercardinal positions from angular division', 'Derive all 8 compass directions from angular division of 360'),
        },
        'B4': {
            3: ('Student knows that knowing directions helps people find their way', 'Student can use star points to identify directions', 'Navigate a simple maze using 8-point directions'),
            4: ('Student understands that predictable angles create reliable orientation systems', 'Student can explain why consistent angles matter for navigation', 'Create a direction-finding tool from an 8-pointed star'),
            5: ('Student can reason that fixed angular references produce reliable navigation systems', 'Student can evaluate the precision of star-based orientation', 'Calculate bearing errors from imprecise angular division'),
        },
        'B5': {
            3: ('Student knows that ancient people used stars to find their way', 'Student can describe how stars helped travelers', 'Draw a picture of a traveler using stars for directions'),
            4: ('Student understands that 8-point geometry enabled systematic navigation', 'Student can connect star geometry to navigation history', 'Create a timeline of navigation tools using star geometry'),
            5: ('Student can reason that radial division was foundational to navigation science', 'Student can analyze the cumulative role of circle and star geometry in navigation', 'Write an analysis connecting equidistance and radial symmetry in navigation history'),
        },
        'B6': {
            3: ('Student knows that the compass rose shows 8 directions', 'Student can identify parts of a compass rose', 'Label all 8 points on a compass rose'),
            4: ('Student understands that 8-point division solved the problem of getting lost', 'Student can explain why 8 directions are better than 4', 'Compare 4-point vs 8-point compass and list advantages'),
            5: ('Student can reason that systematic angular division was a breakthrough in spatial reasoning', 'Student can evaluate the mathematical elegance of the compass rose', 'Design an improved compass rose and justify the geometry'),
        },
        'B7': {
            3: ('Student knows that you can make a compass from a star shape', 'Student can build a simple star compass', 'Cut out an 8-pointed star and use it to find directions'),
            4: ('Student understands that aligned angles indicate real directions', 'Student can calibrate a star compass to true north', 'Build and calibrate an 8-pointed star compass'),
            5: ('Student can reason that angular precision determines navigational accuracy', 'Student can test compass accuracy through multiple trials', 'Build, calibrate, and test a star compass measuring angular error'),
        },
        'B8': {
            3: ('Student knows that the star means protection (Ishtar) and also helps navigation', 'Student can name both meanings of the 8-pointed star', 'Draw the star as protection symbol and as compass'),
            4: ('Student understands that radial symmetry enables both divine symbolism and practical navigation', 'Student can explain the dual purpose of star geometry', 'Write comparing Ishtar protection to compass navigation'),
            5: ('Student can reason that equal angular division simultaneously enables symbolic and functional applications', 'Student can synthesize mythological and scientific perspectives', 'Create a presentation uniting Ishtar symbolism with navigation science'),
        },
    },
    'elem.triangle': {
        'B1': {
            3: ('Student knows that ziggurats use triangle shapes to stay strong', 'Student can find triangles in ziggurat pictures', 'Circle all triangle shapes in a ziggurat image'),
            4: ('Student understands that triangles provide structural support in buildings', 'Student can explain why triangles make buildings stronger', 'Compare triangle vs rectangle strength in a structure model'),
            5: ('Student can reason that structural rigidity from fixed angles enables monumental architecture', 'Student can analyze how triangular elements distribute force', 'Diagram force distribution through triangular supports in a ziggurat'),
        },
        'B2': {
            3: ('Student knows that triangles cannot be pushed out of shape', 'Student can push on a triangle and see it stays rigid', 'Build a triangle from sticks and try to change its shape'),
            4: ('Student understands that three fixed sides create locked angles', 'Student can demonstrate rigidity vs flexibility in shapes', 'Compare triangle vs square stick models under pressure'),
            5: ('Student can reason that three sides uniquely constrain all angles, creating inherent rigidity', 'Student can prove that triangles are the only rigid polygon', 'Test rigidity of 3, 4, 5, 6-sided shapes and explain results mathematically'),
        },
        'B3': {
            3: ('Student knows that triangles can hold up heavy things', 'Student can place weight on a triangle structure', 'Stack books on triangle vs rectangle frames'),
            4: ('Student understands that rigidity prevents collapse under lateral force', 'Student can demonstrate force resistance in triangular frames', 'Apply sideways force to triangle and rectangle frames, measure deflection'),
            5: ('Student can reason that geometric rigidity translates directly to structural load resistance', 'Student can predict failure points in non-triangulated structures', 'Design a structure and predict where it needs triangulation'),
        },
        'B4': {
            3: ('Student knows that strong triangles help build tall buildings', 'Student can explain why triangle shapes are in bridges', 'Build tallest possible tower using triangle supports'),
            4: ('Student understands that locked angles distribute force to foundations', 'Student can trace force paths through triangular structures', 'Draw force arrows through a truss showing load distribution'),
            5: ('Student can reason that force distribution through rigid angles enables load-bearing architecture', 'Student can evaluate structural designs for force distribution efficiency', 'Calculate load distribution in a simple truss system'),
        },
        'B5': {
            3: ('Student knows that ancient builders used triangles in their buildings', 'Student can identify triangles in ancient structures', 'Find triangles in pictures of ancient buildings'),
            4: ('Student understands that triangular rigidity advanced architecture and engineering', 'Student can connect triangle properties to engineering history', 'Create a timeline of triangle use in architecture'),
            5: ('Student can reason that rigidity was foundational to architectural engineering across civilizations', 'Student can analyze cumulative geometric contributions to engineering', 'Write analysis connecting circle, star, and triangle contributions to civilization'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians used triangles in roof supports', 'Student can describe what a truss looks like', 'Draw a simple roof truss with triangles'),
            4: ('Student understands that triangular trusses solved the problem of spanning wide spaces', 'Student can explain why triangles work better than beams for roofs', 'Build a truss model and test its span capability'),
            5: ('Student can reason that triangular rigidity was the key insight enabling truss engineering', 'Student can evaluate different truss designs for efficiency', 'Design and compare multiple truss configurations mathematically'),
        },
        'B7': {
            3: ('Student knows that you can build a strong bridge with triangles', 'Student can build a triangle bridge from craft sticks', 'Build a bridge using triangle shapes and test with weight'),
            4: ('Student understands that three-sided frames create structural rigidity', 'Student can optimize a bridge design using triangulation', 'Build two bridges (with/without triangles) and compare strength'),
            5: ('Student can reason that systematic triangulation maximizes structural integrity', 'Student can iterate bridge designs based on load testing data', 'Design, build, test, and improve a truss bridge measuring load capacity'),
        },
        'B8': {
            3: ('Student knows that triangles mean strength (Enlil) and also hold up buildings', 'Student can name both meanings of triangles', 'Draw triangles as Enlil power and as building support'),
            4: ('Student understands that rigidity enables both divine authority symbolism and structural engineering', 'Student can explain the connection between stability and authority', 'Write comparing Enlil authority to structural engineering'),
            5: ('Student can reason that structural rigidity simultaneously enables metaphorical and functional applications', 'Student can synthesize mythological and engineering perspectives', 'Create a presentation uniting Enlil authority with structural engineering'),
        },
    },
    'elem.square': {
        'B1': {
            3: ('Student knows that clay tablets are rectangle-shaped for writing', 'Student can identify the rectangular shape of tablets', 'Find rectangles in clay tablet images'),
            4: ('Student understands that rectangular shape organizes written information', 'Student can explain why scribes chose rectangular tablets', 'Compare writing on round vs rectangular surfaces'),
            5: ('Student can reason that right-angle regularity enables systematic information organization', 'Student can analyze how shape influences writing systems', 'Design an optimal writing surface shape and justify geometrically'),
        },
        'B2': {
            3: ('Student knows that squares have corners that are all the same', 'Student can check corners with a square corner tool', 'Test corners of shapes with a right-angle checker'),
            4: ('Student understands that four 90-degree angles with parallel sides define squares', 'Student can measure and verify right angles', 'Measure all angles and sides of a square with tools'),
            5: ('Student can reason that right-angle regularity uniquely enables tessellation and grid systems', 'Student can prove square properties through measurement', 'Prove that a quadrilateral is a square using angle and side measurements'),
        },
        'B3': {
            3: ('Student knows that squares fit together without gaps', 'Student can tile squares on a surface', 'Cover a surface completely with square tiles'),
            4: ('Student understands that right angles enable gap-free tessellation', 'Student can demonstrate why squares tessellate but other shapes may not', 'Compare tessellation of squares, triangles, and pentagons'),
            5: ('Student can reason that 90-degree angles summing to 360 at vertices enables perfect tessellation', 'Student can prove tessellation mathematically', 'Calculate angle sums at tessellation vertices for different shapes'),
        },
        'B4': {
            3: ('Student knows that fitting shapes together covers a whole area', 'Student can show complete coverage with square tiles', 'Fill a frame completely with square blocks'),
            4: ('Student understands that aligned edges create efficient space coverage', 'Student can calculate area coverage using tessellation', 'Calculate how many tiles needed to cover a given area'),
            5: ('Student can reason that tessellation produces mathematically complete coverage with zero waste', 'Student can evaluate different tessellation patterns for efficiency', 'Compare space efficiency of square vs hexagonal tessellation'),
        },
        'B5': {
            3: ('Student knows that ancient cities were built using grid patterns', 'Student can identify grids in city maps', 'Find grid patterns in ancient city plan images'),
            4: ('Student understands that rectangular regularity enabled urban planning and record-keeping', 'Student can connect square properties to urban development', 'Create a timeline of grid-based inventions'),
            5: ('Student can reason that right-angle regularity was foundational to multiple civilizational advances', 'Student can analyze cumulative geometric contributions', 'Write analysis of how circle, star, triangle, and square advanced civilization'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians made bricks all the same size', 'Student can describe why same-size bricks are useful', 'Stack uniform vs random-sized blocks and compare results'),
            4: ('Student understands that standardized bricks solved construction alignment problems', 'Student can explain why standardization was revolutionary', 'Build a wall with uniform vs varied bricks and compare stability'),
            5: ('Student can reason that rectangular regularity enabled construction standardization', 'Student can evaluate the engineering impact of the standardized brick', 'Design a standardized building component and justify dimensions'),
        },
        'B7': {
            3: ('Student knows that you can plan a city using a grid', 'Student can lay out a simple grid', 'Design a small city using a grid of squares'),
            4: ('Student understands that right-angle layouts create organized spaces', 'Student can design and justify a city grid layout', 'Design a city grid with zones and explain layout choices'),
            5: ('Student can reason that grid systems optimize spatial organization through regularity', 'Student can optimize a city design based on geometric principles', 'Design, test, and optimize a city grid measuring efficiency metrics'),
        },
        'B8': {
            3: ('Student knows that squares mean order (Nabu) and also organize cities', 'Student can name both meanings of squares', 'Draw squares as Nabu wisdom and as city grid'),
            4: ('Student understands that regularity enables both ordered knowledge and urban planning', 'Student can explain the connection between writing order and city order', 'Write comparing Nabu writing system to city grid planning'),
            5: ('Student can reason that right-angle regularity simultaneously enables symbolic and functional organization', 'Student can synthesize cultural and engineering perspectives', 'Create a presentation uniting Nabu wisdom with urban engineering'),
        },
    },
    'elem.spiral': {
        'B1': {
            3: ('Student knows that scroll shapes help store long things in small spaces', 'Student can roll paper into a spiral shape', 'Roll a long strip of paper into a spiral'),
            4: ('Student understands that spiral form enables compact storage', 'Student can explain why scrolls use spiral winding', 'Compare flat vs rolled storage of a long message'),
            5: ('Student can reason that progressive expansion enables efficient space utilization', 'Student can analyze how spiral geometry optimizes storage density', 'Calculate storage density of spiral vs flat arrangement'),
        },
        'B2': {
            3: ('Student knows that spirals get bigger as they go outward', 'Student can trace a spiral and see it growing', 'Trace a spiral and measure width at different points'),
            4: ('Student understands that increasing radius defines spiral expansion', 'Student can measure progressive expansion in a spiral', 'Measure distances from center at regular intervals in a spiral'),
            5: ('Student can reason that progressive expansion is the defining mathematical property of spirals', 'Student can verify expansion rates through measurement', 'Graph radius vs angle measurements to prove progressive expansion'),
        },
        'B3': {
            3: ('Student knows that spirals can hold long things in a small space', 'Student can coil rope into a small pile', 'Coil a long rope and measure how small it gets'),
            4: ('Student understands that progressive winding compresses length into compact area', 'Student can demonstrate compact winding with different materials', 'Compare coiled vs uncoiled length-to-area ratios'),
            5: ('Student can reason that progressive expansion enables maximum length storage in minimum area', 'Student can calculate compression ratios of spiral winding', 'Derive the relationship between coil tightness and storage efficiency'),
        },
        'B4': {
            3: ('Student knows that coiling things saves space', 'Student can compare coiled vs uncoiled objects', 'Compare space used by coiled vs straight rope'),
            4: ('Student understands that coiling maximizes storage by using area efficiently', 'Student can measure space saved by coiling', 'Calculate space savings from coiling a measured length'),
            5: ('Student can reason that spiral mechanics produce optimal storage through geometric efficiency', 'Student can evaluate different coiling strategies', 'Design and compare multiple storage strategies measuring efficiency'),
        },
        'B5': {
            3: ('Student knows that springs and water channels use spiral shapes', 'Student can identify spirals in machines', 'Find spiral shapes in pictures of machines and water systems'),
            4: ('Student understands that progressive expansion enabled mechanical and hydraulic inventions', 'Student can connect spiral properties to mechanical history', 'Create a timeline of spiral-based inventions'),
            5: ('Student can reason that progressive expansion was foundational to mechanics and hydraulics', 'Student can analyze cumulative geometric contributions', 'Write analysis connecting all five elements contributions to civilization'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians used spiral channels for water', 'Student can describe how water flows in a spiral', 'Draw a spiral water channel'),
            4: ('Student understands that spiral flow solved drainage and irrigation problems', 'Student can explain why spirals work for water management', 'Build a spiral channel model and test water flow'),
            5: ('Student can reason that progressive expansion enabled efficient water distribution', 'Student can evaluate spiral vs straight channel efficiency', 'Design an irrigation system comparing spiral and straight channels'),
        },
        'B7': {
            3: ('Student knows that you can make a spring by coiling wire', 'Student can coil wire into a spring shape', 'Coil wire around a pencil to make a spring'),
            4: ('Student understands that coiled wire applies progressive expansion under tension', 'Student can test spring behavior with different coil tightness', 'Build springs with different coil spacing and compare bounce'),
            5: ('Student can reason that spring mechanics depend on progressive expansion geometry', 'Student can optimize spring design through testing', 'Design, build, and test springs measuring force vs compression'),
        },
        'B8': {
            3: ('Student knows that spirals mean powerful water (Tiamat) and also make springs work', 'Student can name both meanings of spirals', 'Draw spiral as Tiamat chaos and as spring'),
            4: ('Student understands that progressive expansion enables both chaos symbolism and spring mechanics', 'Student can explain the connection between water chaos and spring energy', 'Write comparing Tiamat chaos waters to spring mechanics'),
            5: ('Student can reason that progressive expansion simultaneously enables metaphorical and functional applications', 'Student can synthesize mythological and engineering perspectives', 'Create a presentation uniting Tiamat symbolism with spiral mechanics'),
        },
    },
    'elem.arc': {
        'B1': {
            3: ('Student knows that arched doorways are curved on top', 'Student can find arches in building pictures', 'Circle all arches in city gate images'),
            4: ('Student understands that arcs enable wide openings without center support', 'Student can explain why arches curve upward', 'Compare arched vs flat-topped doorways for strength'),
            5: ('Student can reason that continuous curvature enables load distribution across spans', 'Student can analyze how arch shape affects load bearing', 'Diagram force paths through an arch structure'),
        },
        'B2': {
            3: ('Student knows that arcs are parts of circles', 'Student can find the center of an arc', 'Draw an arc and mark its center point'),
            4: ('Student understands that constant radius from center defines arc curvature', 'Student can measure radii to verify arc properties', 'Measure multiple radii from center to arc points'),
            5: ('Student can reason that constant curvature is the defining property of true arcs', 'Student can distinguish true arcs from irregular curves', 'Test curves and prove which are true arcs using radius measurement'),
        },
        'B3': {
            3: ('Student knows that arches spread weight to both sides', 'Student can see how weight goes sideways in an arch', 'Place weight on arch model and observe side support'),
            4: ('Student understands that curvature redirects downward force laterally', 'Student can demonstrate force redirection in arch models', 'Build arch from blocks and test weight distribution'),
            5: ('Student can reason that continuous curvature systematically redirects force through compression', 'Student can predict force paths through arch geometry', 'Calculate force components in an arch under load'),
        },
        'B4': {
            3: ('Student knows that arches can hold up heavy walls above openings', 'Student can describe why arches are strong', 'Build an arch from blocks and test how much weight it holds'),
            4: ('Student understands that compression along the curve eliminates need for center support', 'Student can explain why arches span wider than beams', 'Compare maximum span of arch vs beam using same materials'),
            5: ('Student can reason that lateral force distribution produces stable spans through geometric compression', 'Student can evaluate arch designs for span efficiency', 'Design arches with different curves and compare load capacity'),
        },
        'B5': {
            3: ('Student knows that ancient people built arches for gates and bridges', 'Student can identify arches in ancient buildings', 'Find arches in pictures of ancient structures'),
            4: ('Student understands that load distribution enabled monumental gateway construction', 'Student can connect arc properties to engineering history', 'Create a timeline of arch-based engineering achievements'),
            5: ('Student can reason that arch geometry was foundational to civil engineering advancement', 'Student can analyze cumulative geometric contributions', 'Write analysis of six elements contributions to engineering'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians built real arches from bricks', 'Student can describe what a true arch looks like', 'Draw an arch showing how bricks are arranged'),
            4: ('Student understands that curved load distribution solved wide-span construction', 'Student can explain the engineering breakthrough of the true arch', 'Build a model arch from shaped blocks'),
            5: ('Student can reason that the true arch was a geometric engineering breakthrough', 'Student can evaluate arch construction techniques', 'Design an arch bridge specifying block angles mathematically'),
        },
        'B7': {
            3: ('Student knows that you can build a bridge with an arch shape', 'Student can build a simple arch from blocks', 'Build an arch bridge from cardboard pieces'),
            4: ('Student understands that curved block alignment distributes load', 'Student can test arch bridge strength', 'Build arch bridge and test maximum load before failure'),
            5: ('Student can reason that geometric precision in block angles determines arch strength', 'Student can optimize arch design through testing', 'Design, build, and test arch bridges measuring load capacity vs curve angle'),
        },
        'B8': {
            3: ('Student knows that arcs mean the sky (Anu) and also hold up buildings', 'Student can name both meanings of arcs', 'Draw arc as sky vault and as bridge arch'),
            4: ('Student understands that continuous curvature enables both sky symbolism and architectural spanning', 'Student can explain the connection between sky dome and arch construction', 'Write comparing Anu sky vault to arch engineering'),
            5: ('Student can reason that continuous curvature simultaneously enables metaphorical and functional applications', 'Student can synthesize mythological and engineering perspectives', 'Create a presentation uniting Anu sky vault with arch engineering'),
        },
    },
    'elem.hexagon': {
        'B1': {
            3: ('Student knows that hexagon shapes pack together tightly', 'Student can fit hexagon tiles together', 'Fit hexagon tiles together with no gaps'),
            4: ('Student understands that hexagonal packing maximizes storage efficiency', 'Student can explain why hexagons pack better than squares', 'Compare hexagonal vs square packing for storage'),
            5: ('Student can reason that optimal packing geometry enables maximum efficiency', 'Student can analyze why hexagons appear in nature', 'Calculate area efficiency of hexagonal vs square packing'),
        },
        'B2': {
            3: ('Student knows that hexagons have 6 equal sides and angles', 'Student can count sides and measure angles', 'Count sides and check angles of hexagon shapes'),
            4: ('Student understands that 120-degree angles enable gap-free tessellation', 'Student can measure hexagon angles and verify regularity', 'Measure all angles of a hexagon with protractor'),
            5: ('Student can reason that 120-degree angles summing to 360 at vertices enable perfect tessellation', 'Student can prove hexagonal tessellation mathematically', 'Prove hexagonal tessellation using angle calculations'),
        },
        'B3': {
            3: ('Student knows that hexagons cover surfaces with no gaps', 'Student can tile a surface with hexagons', 'Cover a surface completely with hexagon tiles'),
            4: ('Student understands that optimal angles create seamless coverage', 'Student can demonstrate zero-waste hexagonal tiling', 'Tile a surface and calculate coverage percentage'),
            5: ('Student can reason that hexagonal tessellation produces mathematically optimal coverage', 'Student can compare hexagonal to other tessellation efficiencies', 'Calculate and compare coverage ratios of hexagonal vs other tessellations'),
        },
        'B4': {
            3: ('Student knows that honeycomb cells save space by sharing walls', 'Student can describe why honeycomb is efficient', 'Count shared walls in a honeycomb pattern'),
            4: ('Student understands that shared walls maximize storage with minimal material', 'Student can calculate material savings from wall sharing', 'Compare material used in hexagonal vs square storage grids'),
            5: ('Student can reason that wall sharing produces maximum storage efficiency per unit of material', 'Student can evaluate storage designs for material efficiency', 'Design and compare storage systems measuring material-to-volume ratios'),
        },
        'B5': {
            3: ('Student knows that nature uses hexagons in honeycombs and crystals', 'Student can find hexagons in nature pictures', 'Find hexagon shapes in nature photographs'),
            4: ('Student understands that optimal packing enabled efficient resource management', 'Student can connect hexagonal geometry to materials science', 'Create a timeline of hexagonal discoveries in nature and technology'),
            5: ('Student can reason that optimal packing principles connect mathematics to materials science', 'Student can analyze cumulative geometric contributions across all elements', 'Write comprehensive analysis of seven elements contributions to civilization'),
        },
        'B6': {
            3: ('Student knows that Mesopotamians arranged storage jars efficiently', 'Student can describe how hexagonal packing saves space', 'Arrange circular jars in hexagonal pattern'),
            4: ('Student understands that hexagonal arrangement solved storage space limitations', 'Student can demonstrate space savings from hexagonal packing', 'Compare hexagonal vs grid arrangement for circular objects'),
            5: ('Student can reason that applying optimal packing geometry solved resource management challenges', 'Student can evaluate historical storage solutions', 'Design an optimal warehouse layout using hexagonal principles'),
        },
        'B7': {
            3: ('Student knows that you can make a honeycomb pattern', 'Student can build a honeycomb from paper', 'Build a honeycomb structure from paper strips'),
            4: ('Student understands that honeycomb tiling demonstrates optimal packing', 'Student can test honeycomb strength and efficiency', 'Build honeycomb and square grid structures, compare strength'),
            5: ('Student can reason that honeycomb geometry optimizes both strength and space', 'Student can optimize storage design through testing', 'Design, build, and test storage structures measuring efficiency'),
        },
        'B8': {
            3: ('Student knows that hexagons mean wisdom (Nisaba) and also save space in storage', 'Student can name both meanings of hexagons', 'Draw hexagon as Nisaba wisdom and as honeycomb storage'),
            4: ('Student understands that optimal packing enables both efficient record-keeping and storage engineering', 'Student can explain the connection between wisdom and efficiency', 'Write comparing Nisaba record-keeping to storage engineering'),
            5: ('Student can reason that optimal packing simultaneously enables metaphorical and functional applications', 'Student can synthesize cultural and engineering perspectives', 'Create a presentation uniting Nisaba wisdom with storage engineering'),
        },
    },
    'elem.pyramid': {
        'B1': {
            3: ('Student knows that ziggurats are wide at the bottom and narrow at the top', 'Student can describe the shape of a ziggurat', 'Draw a ziggurat showing wide base and narrow top'),
            4: ('Student understands that pyramidal form creates monumental stability', 'Student can explain why ziggurats are shaped like pyramids', 'Compare stability of pyramid vs box shapes'),
            5: ('Student can reason that convergent geometry produces maximum structural stability', 'Student can analyze how pyramid proportions affect stability', 'Calculate center of gravity for different pyramid proportions'),
        },
        'B2': {
            3: ('Student knows that pyramids are strong because they are wide at the bottom', 'Student can show that wide-based shapes are hard to push over', 'Push on pyramid vs tall rectangle and compare stability'),
            4: ('Student understands that mass below center of gravity creates stability', 'Student can demonstrate how base width affects topple resistance', 'Build pyramids with different base widths and test stability'),
            5: ('Student can reason that mass distribution below center of gravity is the defining stability principle', 'Student can calculate center of gravity for pyramid shapes', 'Prove stability through center of gravity calculations'),
        },
        'B3': {
            3: ('Student knows that pyramid shapes push weight down to the ground', 'Student can describe how weight goes downward in a pyramid', 'Stack blocks in pyramid shape and describe weight flow'),
            4: ('Student understands that convergent faces direct force toward the base', 'Student can demonstrate downward force channeling', 'Build a pyramid and trace weight paths from top to base'),
            5: ('Student can reason that geometric convergence systematically channels force to the foundation', 'Student can predict force distribution in pyramidal structures', 'Calculate force vectors through convergent faces'),
        },
        'B4': {
            3: ('Student knows that pyramids last a very long time because they are so stable', 'Student can explain why pyramids do not fall over', 'Compare how long different block arrangements stay standing'),
            4: ('Student understands that gravitational alignment prevents structural failure', 'Student can connect stability to monument permanence', 'Test different monument shapes for long-term stability'),
            5: ('Student can reason that convergent stability and gravitational alignment produce structural permanence', 'Student can evaluate monument designs for longevity', 'Design a monument optimizing stability and calculate failure conditions'),
        },
        'B5': {
            3: ('Student knows that many ancient cultures built pyramids and ziggurats', 'Student can name places with pyramids', 'Match pyramid/ziggurat images to their civilizations'),
            4: ('Student understands that convergent stability enabled monumental architecture worldwide', 'Student can connect pyramid geometry to architectural history', 'Create a comprehensive timeline of all 8 geometric contributions'),
            5: ('Student can reason that all 8 geometric properties cumulatively enabled civilization', 'Student can synthesize all elements contributions into a coherent narrative', 'Write cumulative synthesis essay connecting all 8 elements to civilization'),
        },
        'B6': {
            3: ('Student knows that the Ziggurat of Ur is a very old pyramid building', 'Student can describe the Ziggurat of Ur', 'Draw and label the Ziggurat of Ur'),
            4: ('Student understands that pyramidal stability solved multi-story construction challenges', 'Student can explain the engineering of the ziggurat', 'Build a multi-story ziggurat model and test stability'),
            5: ('Student can reason that convergent stability was the key engineering principle enabling tall structures', 'Student can evaluate ziggurat design decisions', 'Analyze the Ziggurat of Ur dimensions and calculate stability factors'),
        },
        'B7': {
            3: ('Student knows that you can build a ziggurat from stacked layers', 'Student can build a simple ziggurat model', 'Build a ziggurat from cardboard layers'),
            4: ('Student understands that stacked layers apply convergent stability', 'Student can optimize a ziggurat design for height', 'Build ziggurats with different proportions and test maximum height'),
            5: ('Student can reason that layer proportions determine structural performance', 'Student can iterate ziggurat designs based on performance data', 'Design, build, and test ziggurat models optimizing height-to-stability ratio'),
        },
        'B8': {
            3: ('Student knows that pyramids mean power (Marduk) and also make tall buildings stable', 'Student can name both meanings of pyramids', 'Draw pyramid as Marduk power and as stable building'),
            4: ('Student understands that convergent stability enables both divine authority symbolism and monumental engineering', 'Student can explain the connection between hierarchy and stability', 'Write comparing Marduk cosmic authority to ziggurat engineering'),
            5: ('Student can reason that convergent stability simultaneously enables metaphorical and functional applications', 'Student can synthesize all cultural and engineering perspectives across the curriculum', 'Create a final presentation synthesizing all 8 elements mythology and engineering'),
        },
    },
}

DAYB_ELEMENT_ORDER = ['elem.circle', 'elem.star8', 'elem.triangle', 'elem.square', 'elem.spiral', 'elem.arc', 'elem.hexagon', 'elem.pyramid']

def seed_day_b_data():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT COUNT(*) as cnt FROM day_b_elements')
    if cur.fetchone()['cnt'] > 0:
        cur.close()
        conn.close()
        return

    elements = [
        ('elem.circle', 'Circle', '2D-curved', 'Shamash', 'deity.meso.shamash', 'Equidistance', 'All points equal distance from center', 'Measure multiple radii, confirm identical length', 'Justice/fairness', 'Rotation', 1),
        ('elem.star8', '8-Pointed Star', '2D-angular', 'Ishtar', 'deity.meso.ishtar', 'Radial symmetry (8-fold)', '8 equal angles (45 degrees) from center; rotational symmetry at 45-degree intervals', 'Measure angles between rays, confirm 45 degrees each', 'Divine radiance', 'Navigation', 2),
        ('elem.triangle', 'Triangle', '2D-angular', 'Enlil', 'deity.meso.enlil', 'Structural rigidity', 'Three sides create fixed angles; cannot deform without breaking', 'Build triangle from sticks, attempt to shift - cannot', 'Stability', 'Structural support', 3),
        ('elem.square', 'Square/Rectangle', '2D-angular', 'Nabu', 'deity.meso.nabu', 'Right-angle regularity', 'Four sides with 90-degree corners; opposite sides parallel and equal', 'Measure angles (90 degrees), measure opposite sides (equal)', 'Order/civilization', 'Tessellation', 4),
        ('elem.spiral', 'Spiral', '2D-curved', 'Tiamat', 'deity.meso.tiamat', 'Progressive expansion', 'Curve that winds outward from center at increasing distance', 'Measure distance from center at regular angle intervals, confirm growth', 'Growth/evolution', 'Compact storage', 5),
        ('elem.arc', 'Arc/Curve', '2D-curved', 'Anu', 'deity.meso.anu', 'Continuous directional change', 'Segment of circle; constant curvature between two points', 'Identify center, measure radii to arc points, confirm equal', 'Heaven/sky', 'Load distribution', 6),
        ('elem.hexagon', 'Hexagon', '2D-angular', 'Nisaba', 'deity.meso.nisaba', 'Optimal packing', '6 equal sides, 120-degree angles; tessellates with no gaps', 'Tile hexagons, observe complete coverage; measure angles', 'Natural wisdom', 'Space efficiency', 7),
        ('elem.pyramid', 'Pyramid', '3D', 'Marduk', 'deity.meso.marduk', 'Convergent stability', 'Polygonal base with triangular faces meeting at apex', 'Identify base shape, count triangular faces, locate apex', 'Ascension', 'Weight distribution', 8),
    ]

    elem_db_ids = {}
    for e in elements:
        cur.execute('''
            INSERT INTO day_b_elements (element_id, name, category, deity_name, deity_id,
                core_property_name, core_property_definition, core_property_proof,
                key_metaphor, key_function, week_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        ''', e)
        elem_db_ids[e[0]] = cur.fetchone()['id']

    for elem_data in elements:
        eid = elem_data[0]
        ename = elem_data[1]
        deity = elem_data[3]
        week = elem_data[10]
        core_prop = elem_data[5]
        core_def = elem_data[6]
        db_eid = elem_db_ids[eid]

        for grade in [3, 4, 5]:
            title = f"Week {week}: {ename} / {deity} - Grade {grade} Day B"
            cur.execute('''
                INSERT INTO day_b_lessons (element_id, grade, title, week_number)
                VALUES (%s, %s, %s, %s) RETURNING id
            ''', (db_eid, grade, title, week))
            lesson_id = cur.fetchone()['id']

            prior_elems = DAYB_ELEMENT_ORDER[:DAYB_ELEMENT_ORDER.index(eid)]

            for sdef in DAYB_SECTION_DEFS:
                scode, sname, spurpose, sdur, sdrivers, slo_tmpl, simg_type = sdef
                lo_text = DAYB_LO_TEXTS.get(eid, {}).get(scode, '')
                carrier = DAYB_CARRIERS.get(eid, {}).get(scode, deity)

                content = DAYB_CONTENT_TEMPLATES.get(scode, '').format(
                    element_name=ename, deity_name=deity, carrier=carrier,
                    core_property=core_prop, core_definition=core_def
                )

                ecd = DAYB_ECD.get(eid, {}).get(scode, {}).get(grade, ('', '', ''))
                ecd_claim, ecd_evidence, ecd_task = ecd

                b5_refs = []
                if scode == 'B5':
                    for pe in prior_elems:
                        pe_idx = DAYB_ELEMENT_ORDER.index(pe)
                        pe_data = elements[pe_idx]
                        b5_refs.append({
                            'element_id': pe,
                            'element_name': pe_data[1],
                            'week': pe_data[10],
                            'sections': ['B2', 'B3', 'B4'],
                            'core_property': pe_data[5],
                        })

                cur.execute('''
                    INSERT INTO day_b_sections (lesson_id, section_code, section_name, purpose,
                        duration, primary_drivers, lo_template, lo_text, content, image_type,
                        carrier, ecd_claim, ecd_evidence, ecd_task, b5_prior_refs)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (lesson_id, scode, sname, spurpose, sdur, sdrivers, slo_tmpl,
                      lo_text, content, simg_type, carrier, ecd_claim, ecd_evidence,
                      ecd_task, json.dumps(b5_refs)))

    cur.close()
    conn.close()


def _element_consolidated_status(novelty_status, validation_status):
    if validation_status == 'invalid':
        return 'invalid'
    if novelty_status == 'existing' and validation_status == 'valid':
        return 'existing_valid'
    if novelty_status == 'new' and validation_status == 'valid':
        return 'new_valid'
    return 'unknown'


def _validate_element_statuses(novelty_status, validation_status):
    if novelty_status not in ELEMENT_NOVELTY_STATUSES:
        raise ValueError(f'Invalid novelty_status. Use: {ELEMENT_NOVELTY_STATUSES}')
    if validation_status not in ELEMENT_VALIDATION_STATUSES:
        raise ValueError(f'Invalid validation_status. Use: {ELEMENT_VALIDATION_STATUSES}')


def _slugify(value):
    text = ''.join(ch.lower() if ch.isalnum() else '-' for ch in (value or '').strip())
    while '--' in text:
        text = text.replace('--', '-')
    return text.strip('-') or 'item'


def _canonical_element_payload(row):
    return {
        'element_id': row['element_id'],
        'name': row['name'],
        'category': row['category'],
        'deity_name': row['deity_name'],
        'deity_id': row['deity_id'],
        'core_property_name': row['core_property_name'],
        'core_property_definition': row['core_property_definition'],
        'core_property_proof': row['core_property_proof'],
        'key_metaphor': row['key_metaphor'],
        'key_function': row['key_function'],
        'week_number': row['week_number'],
    }


def sync_element_reconciliations():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM day_b_elements ORDER BY week_number')
    rows = cur.fetchall()
    for row in rows:
        cur.execute('''
            INSERT INTO element_reconciliations (
                canonical_element_id, source_type, source_key, source_label,
                candidate_element_id, candidate_name, candidate_category, candidate_payload,
                novelty_status, validation_status, consolidated_status, reason, updated_at
            )
            VALUES (%s, 'day_b_element', %s, %s, %s, %s, %s, %s, 'existing', 'valid', 'existing_valid', %s, NOW())
            ON CONFLICT (source_key) DO UPDATE SET
                canonical_element_id = EXCLUDED.canonical_element_id,
                source_label = EXCLUDED.source_label,
                candidate_element_id = EXCLUDED.candidate_element_id,
                candidate_name = EXCLUDED.candidate_name,
                candidate_category = EXCLUDED.candidate_category,
                candidate_payload = EXCLUDED.candidate_payload,
                novelty_status = EXCLUDED.novelty_status,
                validation_status = EXCLUDED.validation_status,
                consolidated_status = EXCLUDED.consolidated_status,
                updated_at = NOW()
        ''', (
            row['id'],
            f"day_b:{row['element_id']}",
            f"Canonical Day B element · Week {row['week_number']}",
            row['element_id'],
            row['name'],
            row['category'],
            json.dumps(_canonical_element_payload(row)),
            'Seeded from canonical day_b_elements baseline.',
        ))
    cur.close()
    conn.close()


def _dayb_dt(row, *fields):
    for f in fields:
        if f in row and row[f] is not None:
            row[f] = row[f].isoformat()
        elif f in row:
            row[f] = None


def _element_recon_select(cur, where_clause='', params=None):
    cur.execute(f'''
        SELECT er.*,
               e.element_id AS canonical_element_code,
               e.name AS canonical_element_name,
               e.week_number AS canonical_week_number
        FROM element_reconciliations er
        LEFT JOIN day_b_elements e ON er.canonical_element_id = e.id
        {where_clause}
        ORDER BY
            CASE er.consolidated_status
                WHEN 'existing_valid' THEN 1
                WHEN 'new_valid' THEN 2
                WHEN 'unknown' THEN 3
                WHEN 'invalid' THEN 4
                ELSE 5
            END,
            COALESCE(e.week_number, 9999),
            er.candidate_name
    ''', params or [])
    rows = cur.fetchall()
    for row in rows:
        _dayb_dt(row, 'created_at', 'updated_at')
    return rows


def _catalog_title(rel_path):
    stem = os.path.splitext(os.path.basename(rel_path))[0]
    return stem.replace('-', ' ').replace('_', ' ').strip().title() or os.path.basename(rel_path)


def _catalog_layer(rel_path, ext):
    if rel_path.startswith('attached_assets/'):
        return 'experimental'
    if ext == '.py':
        return 'backend'
    if ext in ('.jsx', '.tsx', '.ts'):
        return 'future-react'
    return 'frontend'


def _build_repo_catalog():
    rows = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for name in files:
            if name.startswith('.'):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in CATALOGABLE_EXTENSIONS:
                continue
            abs_path = os.path.join(root, name)
            rel_path = os.path.relpath(abs_path, REPO_ROOT).replace(os.sep, '/')
            layer = _catalog_layer(rel_path, ext)
            rows.append({
                'name': name,
                'title': _catalog_title(rel_path),
                'relative_path': rel_path,
                'href': '/' + rel_path,
                'extension': ext.lstrip('.'),
                'file_type': CATALOGABLE_EXTENSIONS[ext],
                'layer': layer,
                'size_bytes': os.path.getsize(abs_path),
                'python_group': (
                    'active_backend'
                    if ext == '.py' and not rel_path.startswith('attached_assets/')
                    else 'attached_asset'
                    if ext == '.py'
                    else ''
                ),
            })
    rows.sort(key=lambda row: (row['layer'], row['extension'], row['relative_path']))
    return rows


@app.route('/api/dayb/elements', methods=['GET'])
def dayb_elements():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM day_b_elements ORDER BY week_number')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for r in rows:
        _dayb_dt(r, 'created_at')
    return jsonify(rows)


@app.route('/api/dayb/element-reconciliations/summary', methods=['GET'])
def dayb_element_reconciliations_summary():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT consolidated_status, COUNT(*) AS n
        FROM element_reconciliations
        GROUP BY consolidated_status
    ''')
    by_status = {row['consolidated_status']: row['n'] for row in cur.fetchall()}
    cur.execute('''
        SELECT novelty_status, validation_status, COUNT(*) AS n
        FROM element_reconciliations
        GROUP BY novelty_status, validation_status
    ''')
    matrix = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        'counts': {status: by_status.get(status, 0) for status in ELEMENT_CONSOLIDATED_STATUSES},
        'matrix': matrix,
    })


@app.route('/api/dayb/element-reconciliations', methods=['GET', 'POST'])
def dayb_element_reconciliations():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        candidate_name = (data.get('candidate_name') or '').strip()
        if not candidate_name:
            return jsonify({'error': 'candidate_name is required'}), 400
        novelty_status = (data.get('novelty_status') or 'unknown').strip()
        validation_status = (data.get('validation_status') or 'unknown').strip()
        try:
            _validate_element_statuses(novelty_status, validation_status)
        except ValueError:
            return jsonify({
                'error': 'Invalid novelty_status or validation_status',
                'allowed_novelty_statuses': ELEMENT_NOVELTY_STATUSES,
                'allowed_validation_statuses': ELEMENT_VALIDATION_STATUSES,
            }), 400
        canonical_element_id = data.get('canonical_element_id')
        source_type = (data.get('source_type') or 'manual').strip() or 'manual'
        source_key = (data.get('source_key') or '').strip() or f'{source_type}:{_slugify(candidate_name)}:{int(datetime.utcnow().timestamp())}'
        source_label = (data.get('source_label') or candidate_name).strip()
        candidate_payload = data.get('candidate_payload') if isinstance(data.get('candidate_payload'), dict) else {}
        consolidated_status = _element_consolidated_status(novelty_status, validation_status)
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if canonical_element_id:
            cur.execute('SELECT id FROM day_b_elements WHERE id = %s', (canonical_element_id,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({'error': 'canonical_element_id not found'}), 404
        try:
            cur.execute('''
                INSERT INTO element_reconciliations (
                    canonical_element_id, source_type, source_key, source_label,
                    candidate_element_id, candidate_name, candidate_category, candidate_payload,
                    novelty_status, validation_status, consolidated_status, reason, review_notes, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
            ''', (
                canonical_element_id,
                source_type,
                source_key,
                source_label,
                (data.get('candidate_element_id') or '').strip(),
                candidate_name,
                (data.get('candidate_category') or '').strip(),
                json.dumps(candidate_payload),
                novelty_status,
                validation_status,
                consolidated_status,
                (data.get('reason') or '').strip(),
                (data.get('review_notes') or '').strip(),
            ))
            rec_id = cur.fetchone()['id']
        except psycopg2.Error:
            cur.close()
            conn.close()
            return jsonify({'error': 'source_key must be unique'}), 409
        cur.close()
        conn.close()
        return dayb_element_reconciliation_detail(rec_id)

    q = request.args.get('q', '').strip().lower()
    source = request.args.get('source', '').strip().lower()
    consolidated_status = request.args.get('status', '').strip().lower()
    novelty = request.args.get('novelty', '').strip().lower()
    validation = request.args.get('validation', '').strip().lower()
    wants_new = request.args.get('new', '').strip().lower()
    wants_valid = request.args.get('valid', '').strip().lower()
    wants_unknown = request.args.get('unknown', '').strip().lower()

    where_parts = []
    params = []
    if source:
        where_parts.append('LOWER(er.source_type) = %s')
        params.append(source)
    if consolidated_status:
        where_parts.append('er.consolidated_status = %s')
        params.append(consolidated_status)
    if novelty:
        where_parts.append('er.novelty_status = %s')
        params.append(novelty)
    if validation:
        where_parts.append('er.validation_status = %s')
        params.append(validation)
    if wants_new in ('1', 'true', 'yes'):
        where_parts.append("er.novelty_status = 'new'")
    if wants_valid in ('1', 'true', 'yes'):
        where_parts.append("er.validation_status = 'valid'")
    if wants_unknown in ('1', 'true', 'yes'):
        where_parts.append("er.consolidated_status = 'unknown'")
    if q:
        where_parts.append('''(
            LOWER(er.candidate_name) LIKE %s OR
            LOWER(er.candidate_element_id) LIKE %s OR
            LOWER(er.source_label) LIKE %s OR
            LOWER(COALESCE(e.element_id, '')) LIKE %s OR
            LOWER(COALESCE(e.name, '')) LIKE %s
        )''')
        like = f'%{q}%'
        params.extend([like, like, like, like, like])

    where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ''
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    rows = _element_recon_select(cur, where_clause, params)
    cur.close()
    conn.close()
    return jsonify({
        'items': rows,
        'count': len(rows),
        'filters': {
            'q': q,
            'source': source,
            'status': consolidated_status,
            'novelty': novelty,
            'validation': validation,
            'new': wants_new,
            'valid': wants_valid,
            'unknown': wants_unknown,
        },
    })


@app.route('/api/dayb/element-reconciliations/<int:rec_id>', methods=['GET', 'PUT'])
def dayb_element_reconciliation_detail(rec_id):
    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM element_reconciliations WHERE id = %s', (rec_id,))
        current = cur.fetchone()
        if not current:
            cur.close()
            conn.close()
            return jsonify({'error': 'Element reconciliation not found'}), 404

        updates = []
        values = []
        if 'canonical_element_id' in data:
            canonical_element_id = data.get('canonical_element_id')
            if canonical_element_id:
                cur.execute('SELECT id FROM day_b_elements WHERE id = %s', (canonical_element_id,))
                if not cur.fetchone():
                    cur.close()
                    conn.close()
                    return jsonify({'error': 'canonical_element_id not found'}), 404
            updates.append('canonical_element_id = %s')
            values.append(canonical_element_id)
        for field in ('source_type', 'source_key', 'source_label', 'candidate_element_id', 'candidate_name', 'candidate_category', 'reason', 'review_notes'):
            if field in data:
                updates.append(f'{field} = %s')
                values.append((data.get(field) or '').strip() if isinstance(data.get(field), str) or data.get(field) is None else data.get(field))
        if 'candidate_payload' in data:
            if not isinstance(data.get('candidate_payload'), dict):
                cur.close()
                conn.close()
                return jsonify({'error': 'candidate_payload must be an object'}), 400
            updates.append('candidate_payload = %s')
            values.append(json.dumps(data.get('candidate_payload') or {}))

        novelty_status = (data.get('novelty_status') or current['novelty_status']).strip()
        validation_status = (data.get('validation_status') or current['validation_status']).strip()
        try:
            _validate_element_statuses(novelty_status, validation_status)
        except ValueError:
            cur.close()
            conn.close()
            return jsonify({
                'error': 'Invalid novelty_status or validation_status',
                'allowed_novelty_statuses': ELEMENT_NOVELTY_STATUSES,
                'allowed_validation_statuses': ELEMENT_VALIDATION_STATUSES,
            }), 400
        if 'novelty_status' in data:
            updates.append('novelty_status = %s')
            values.append(novelty_status)
        if 'validation_status' in data:
            updates.append('validation_status = %s')
            values.append(validation_status)
        consolidated_status = _element_consolidated_status(novelty_status, validation_status)
        updates.append('consolidated_status = %s')
        values.append(consolidated_status)
        updates.append('updated_at = NOW()')
        values.append(rec_id)
        try:
            cur.execute(f'''
                UPDATE element_reconciliations
                SET {', '.join(updates)}
                WHERE id = %s
            ''', values)
        except psycopg2.Error:
            cur.close()
            conn.close()
            return jsonify({'error': 'source_key must be unique'}), 409
        cur.close()
        conn.close()

    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    rows = _element_recon_select(cur, 'WHERE er.id = %s', [rec_id])
    cur.close()
    conn.close()
    if not rows:
        return jsonify({'error': 'Element reconciliation not found'}), 404
    return jsonify(rows[0])


@app.route('/api/dayb/lessons', methods=['GET'])
def dayb_lessons():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    where_parts = []
    params = []
    grade = request.args.get('grade', '')
    element_id = request.args.get('element_id', '')
    status = request.args.get('status', '')
    if grade:
        where_parts.append('l.grade = %s')
        params.append(int(grade))
    if element_id:
        where_parts.append('l.element_id = %s')
        params.append(int(element_id))
    if status:
        where_parts.append('l.status = %s')
        params.append(status)
    where_clause = (' WHERE ' + ' AND '.join(where_parts)) if where_parts else ''
    cur.execute(f'''
        SELECT l.*, e.element_id as element_code, e.name as element_name,
               e.deity_name, e.deity_id, e.core_property_name, e.key_metaphor, e.key_function
        FROM day_b_lessons l
        JOIN day_b_elements e ON l.element_id = e.id
        {where_clause}
        ORDER BY l.week_number, l.grade
    ''', params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for r in rows:
        _dayb_dt(r, 'created_at', 'updated_at')
    return jsonify(rows)


@app.route('/api/dayb/lessons/<int:lesson_id>', methods=['GET'])
def dayb_lesson_detail(lesson_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT l.*, e.element_id as element_code, e.name as element_name,
               e.deity_name, e.deity_id, e.core_property_name, e.core_property_definition,
               e.core_property_proof, e.key_metaphor, e.key_function, e.category
        FROM day_b_lessons l
        JOIN day_b_elements e ON l.element_id = e.id
        WHERE l.id = %s
    ''', (lesson_id,))
    lesson = cur.fetchone()
    if not lesson:
        cur.close()
        conn.close()
        return jsonify({'error': 'Lesson not found'}), 404
    _dayb_dt(lesson, 'created_at', 'updated_at')
    cur.execute('''
        SELECT * FROM day_b_sections WHERE lesson_id = %s ORDER BY section_code
    ''', (lesson_id,))
    sections = cur.fetchall()
    cur.close()
    conn.close()
    for s in sections:
        _dayb_dt(s, 'created_at', 'updated_at')
    lesson['sections'] = sections
    return jsonify(lesson)


@app.route('/api/dayb/lessons/<int:lesson_id>', methods=['PUT'])
def dayb_lesson_update(lesson_id):
    data = request.get_json()
    new_status = data.get('status', 'not_started')
    if new_status not in ('not_started', 'in_progress', 'review', 'complete'):
        return jsonify({'error': 'Invalid status'}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        UPDATE day_b_lessons SET status = %s, updated_at = NOW()
        WHERE id = %s RETURNING *
    ''', (new_status, lesson_id))
    lesson = cur.fetchone()
    cur.close()
    conn.close()
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    _dayb_dt(lesson, 'created_at', 'updated_at')
    return jsonify(lesson)


@app.route('/api/dayb/sections/<int:section_id>', methods=['GET'])
def dayb_section_detail(section_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT s.*, l.grade, l.title as lesson_title, l.week_number,
               e.element_id as element_code, e.name as element_name,
               e.deity_name, e.deity_id, e.core_property_name
        FROM day_b_sections s
        JOIN day_b_lessons l ON s.lesson_id = l.id
        JOIN day_b_elements e ON l.element_id = e.id
        WHERE s.id = %s
    ''', (section_id,))
    section = cur.fetchone()
    cur.close()
    conn.close()
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    _dayb_dt(section, 'created_at', 'updated_at')
    return jsonify(section)


@app.route('/api/dayb/sections/<int:section_id>', methods=['PUT'])
def dayb_section_update(section_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    allowed = ['lo_text', 'content', 'image_url', 'carrier', 'ecd_claim', 'ecd_evidence', 'ecd_task', 'status', 'b5_prior_refs']
    set_parts = []
    values = []
    for col in allowed:
        if col in data:
            if col == 'status' and data[col] not in ('not_started', 'drafting', 'review', 'complete'):
                cur.close()
                conn.close()
                return jsonify({'error': 'Invalid status'}), 400
            if col == 'b5_prior_refs':
                set_parts.append(f"{col} = %s")
                values.append(json.dumps(data[col]))
            else:
                set_parts.append(f"{col} = %s")
                values.append(data[col])
    if not set_parts:
        cur.close()
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    set_parts.append("updated_at = NOW()")
    values.append(section_id)
    cur.execute(f'''
        UPDATE day_b_sections SET {', '.join(set_parts)}
        WHERE id = %s RETURNING *
    ''', values)
    section = cur.fetchone()
    cur.close()
    conn.close()
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    _dayb_dt(section, 'created_at', 'updated_at')
    return jsonify(section)


@app.route('/api/dayb/stats', methods=['GET'])
def dayb_stats():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT COUNT(*) as total_lessons,
            COUNT(*) FILTER (WHERE status = 'complete') as completed_lessons,
            COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress_lessons,
            COUNT(*) FILTER (WHERE status = 'review') as review_lessons,
            COUNT(*) FILTER (WHERE status = 'not_started') as not_started_lessons
        FROM day_b_lessons
    ''')
    lesson_stats = cur.fetchone()
    cur.execute('''
        SELECT COUNT(*) as total_sections,
            COUNT(*) FILTER (WHERE status = 'complete') as completed_sections,
            COUNT(*) FILTER (WHERE status = 'drafting') as drafting_sections,
            COUNT(*) FILTER (WHERE status = 'review') as review_sections,
            COUNT(*) FILTER (WHERE status = 'not_started') as not_started_sections
        FROM day_b_sections
    ''')
    section_stats = cur.fetchone()
    cur.execute('''
        SELECT l.grade,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE l.status = 'complete') as completed
        FROM day_b_lessons l
        GROUP BY l.grade ORDER BY l.grade
    ''')
    by_grade = cur.fetchall()
    cur.execute('''
        SELECT e.name as element_name, e.week_number,
            COUNT(l.id) as total_lessons,
            COUNT(l.id) FILTER (WHERE l.status = 'complete') as completed_lessons
        FROM day_b_elements e
        LEFT JOIN day_b_lessons l ON l.element_id = e.id
        GROUP BY e.id, e.name, e.week_number
        ORDER BY e.week_number
    ''')
    by_element = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        'lessons': dict(lesson_stats),
        'sections': dict(section_stats),
        'by_grade': by_grade,
        'by_element': by_element,
    })


@app.route('/api/dayb/b5-chain/<int:lesson_id>', methods=['GET'])
def dayb_b5_chain(lesson_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT l.grade, l.week_number, e.id as elem_db_id, e.element_id as element_code,
               e.name as element_name, e.week_number as elem_week
        FROM day_b_lessons l
        JOIN day_b_elements e ON l.element_id = e.id
        WHERE l.id = %s
    ''', (lesson_id,))
    lesson = cur.fetchone()
    if not lesson:
        cur.close()
        conn.close()
        return jsonify({'error': 'Lesson not found'}), 404

    grade = lesson['grade']
    elem_week = lesson['elem_week']

    cur.execute('''
        SELECT s.*, l.week_number, e.element_id as element_code, e.name as element_name,
               e.deity_name, e.core_property_name
        FROM day_b_sections s
        JOIN day_b_lessons l ON s.lesson_id = l.id
        JOIN day_b_elements e ON l.element_id = e.id
        WHERE l.grade = %s
          AND e.week_number < %s
          AND s.section_code IN ('B2', 'B3', 'B4')
        ORDER BY e.week_number, s.section_code
    ''', (grade, elem_week))
    chain = cur.fetchall()
    cur.close()
    conn.close()
    for s in chain:
        _dayb_dt(s, 'created_at', 'updated_at')
    return jsonify({
        'lesson_id': lesson_id,
        'grade': grade,
        'current_element': lesson['element_name'],
        'current_week': elem_week,
        'chain': chain,
    })


# =====================================================================
# Drive Ingester + Reconciliation
# =====================================================================
import gdrive_helper

INGESTABLE_FIELDS = ['section_name', 'purpose', 'content']
import re as _re
SECTION_CODE_RE = _re.compile(r'^[AB][1-8]$')

def init_ingester_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ingest_candidates (
            id SERIAL PRIMARY KEY,
            source VARCHAR(20) NOT NULL DEFAULT 'gdrive',
            source_file_id VARCHAR(120) NOT NULL,
            source_file_name VARCHAR(255) NOT NULL,
            source_path TEXT DEFAULT '',
            lesson_key VARCHAR(40) NOT NULL,
            grade INTEGER NOT NULL,
            week INTEGER NOT NULL,
            day VARCHAR(2) NOT NULL,
            payload JSONB NOT NULL,
            modified_time VARCHAR(40) DEFAULT '',
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            decision_notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE (source, source_file_id)
        )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_ingest_status ON ingest_candidates(status)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_ingest_lesson_key ON ingest_candidates(lesson_key)')
    cur.close()
    conn.close()


def _safe_drive_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs), None
    except Exception as e:
        return None, str(e)


@app.route('/api/ingest/drive/list', methods=['GET'])
def ingest_drive_list():
    folder_id = request.args.get('folder_id', '').strip()
    if not folder_id:
        return jsonify({'error': 'folder_id required'}), 400
    files, err = _safe_drive_call(gdrive_helper.list_folder, folder_id)
    if err:
        return jsonify({'error': err}), 502
    return jsonify({'folder_id': folder_id, 'files': files})


@app.route('/api/ingest/scan', methods=['POST'])
def ingest_scan():
    data = request.get_json(silent=True) or {}
    folder_id = (data.get('folder_id') or '').strip()
    max_depth = int(data.get('max_depth') or 3)
    if not folder_id:
        return jsonify({'error': 'folder_id required'}), 400
    candidates, err = _safe_drive_call(gdrive_helper.scan_for_sections, folder_id, max_depth)
    if err:
        return jsonify({'error': err}), 502

    conn = get_db()
    cur = conn.cursor()
    inserted, updated, failed = 0, 0, []
    for c in candidates:
        try:
            payload = gdrive_helper.get_file_json(c['sections_file_id'])
        except Exception as e:
            failed.append({'lesson_key': c['lesson_key'], 'error': str(e)})
            continue
        cur.execute('''
            INSERT INTO ingest_candidates
                (source, source_file_id, source_file_name, source_path, lesson_key,
                 grade, week, day, payload, modified_time, status, updated_at)
            VALUES ('gdrive', %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
            ON CONFLICT (source, source_file_id) DO UPDATE SET
                payload = EXCLUDED.payload,
                modified_time = EXCLUDED.modified_time,
                source_path = EXCLUDED.source_path,
                updated_at = NOW(),
                status = CASE WHEN ingest_candidates.status IN ('accepted','rejected')
                              THEN ingest_candidates.status ELSE 'pending' END
            RETURNING (xmax = 0) AS inserted
        ''', (c['sections_file_id'], c['sections_file_name'], c['folder_path'],
              c['lesson_key'], c['grade'], c['week'], c['day'],
              json.dumps(payload), c.get('modified_time') or ''))
        was_inserted = cur.fetchone()[0]
        if was_inserted:
            inserted += 1
        else:
            updated += 1
    cur.close()
    conn.close()
    return jsonify({
        'scanned': len(candidates),
        'inserted': inserted,
        'updated': updated,
        'failed': failed,
    })


@app.route('/api/ingest/candidates', methods=['GET'])
def ingest_candidates_list():
    status = request.args.get('status', '').strip()
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if status:
        cur.execute('''SELECT id, source_file_name, source_path, lesson_key, grade, week, day,
                              status, modified_time, updated_at
                       FROM ingest_candidates WHERE status = %s
                       ORDER BY grade, week, day, lesson_key''', (status,))
    else:
        cur.execute('''SELECT id, source_file_name, source_path, lesson_key, grade, week, day,
                              status, modified_time, updated_at
                       FROM ingest_candidates
                       ORDER BY status, grade, week, day, lesson_key''')
    rows = cur.fetchall()
    cur.execute('''SELECT status, COUNT(*) AS n FROM ingest_candidates GROUP BY status''')
    counts = {r['status']: r['n'] for r in cur.fetchall()}
    cur.close()
    conn.close()
    return jsonify({'candidates': rows, 'counts': counts})


def _lookup_db_lesson(cur, grade, week, day):
    # The DB only models Day B lessons today; Day A content has no DB analog.
    if (day or '').upper() != 'B':
        return None
    cur.execute('''
        SELECT l.id, l.title, l.grade, l.week_number, e.name AS element_name
        FROM day_b_lessons l
        JOIN day_b_elements e ON l.element_id = e.id
        WHERE l.grade = %s AND e.week_number = %s
        LIMIT 1
    ''', (grade, week))
    return cur.fetchone()


@app.route('/api/ingest/candidates/<int:cid>/diff', methods=['GET'])
def ingest_candidate_diff(cid):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM ingest_candidates WHERE id = %s', (cid,))
    cand = cur.fetchone()
    if not cand:
        cur.close(); conn.close()
        return jsonify({'error': 'not found'}), 404

    drive_payload = cand['payload'] or {}
    db_lesson = _lookup_db_lesson(cur, cand['grade'], cand['week'], cand['day'])
    db_sections = []
    if db_lesson:
        cur.execute('SELECT * FROM day_b_sections WHERE lesson_id = %s ORDER BY section_code', (db_lesson['id'],))
        db_sections = cur.fetchall()
    db_by_code = {s['section_code']: s for s in db_sections}

    diff = []
    drive_codes = [k for k in drive_payload.keys() if not k.startswith('_')]
    all_codes = sorted(set(drive_codes + list(db_by_code.keys())))
    for code in all_codes:
        drive_sec = drive_payload.get(code) or {}
        db_sec = db_by_code.get(code) or {}
        fields = {}
        for fld, drive_key in [
            ('section_name', 'name'),
            ('purpose', 'purpose'),
            ('content', 'content'),
        ]:
            drive_val = drive_sec.get(drive_key, '') if isinstance(drive_sec, dict) else ''
            db_val = (db_sec.get(fld) if isinstance(db_sec, dict) else '') or ''
            fields[fld] = {
                'drive': drive_val,
                'db': db_val,
                'changed': (drive_val or '') != (db_val or ''),
                'db_empty': not (db_val or '').strip(),
            }
        artifacts = drive_sec.get('artifacts') if isinstance(drive_sec, dict) else None
        diff.append({
            'section_code': code,
            'in_drive': bool(drive_sec),
            'in_db': bool(db_sec),
            'fields': fields,
            'artifacts': artifacts or [],
        })

    cur.close()
    conn.close()
    return jsonify({
        'candidate': {
            'id': cand['id'],
            'lesson_key': cand['lesson_key'],
            'grade': cand['grade'], 'week': cand['week'], 'day': cand['day'],
            'source_file_name': cand['source_file_name'],
            'source_path': cand['source_path'],
            'status': cand['status'],
            'modified_time': cand['modified_time'],
        },
        'db_lesson': db_lesson,
        'sections': diff,
        'ingestable_fields': INGESTABLE_FIELDS,
    })


@app.route('/api/ingest/candidates/<int:cid>/apply', methods=['POST'])
def ingest_candidate_apply(cid):
    data = request.get_json(silent=True) or {}
    selections = data.get('selections') or []
    allow_clear = bool(data.get('allow_clear'))  # opt-in to overwrite DB with blank Drive value
    if not selections:
        return jsonify({'error': 'selections required: [{section_code, fields:[...]}]'}), 400

    # Use a single transaction for the whole apply operation.
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM ingest_candidates WHERE id = %s FOR UPDATE', (cid,))
        cand = cur.fetchone()
        if not cand:
            return jsonify({'error': 'not found'}), 404

        db_lesson = _lookup_db_lesson(cur, cand['grade'], cand['week'], cand['day'])
        if not db_lesson:
            return jsonify({'error': f'No matching lesson in DB for grade={cand["grade"]} week={cand["week"]} day={cand["day"]}'}), 409

        payload = cand['payload'] or {}
        cur.execute('SELECT id, section_code FROM day_b_sections WHERE lesson_id = %s', (db_lesson['id'],))
        db_codes = {row['section_code']: row['id'] for row in cur.fetchall()}

        applied, skipped = [], []
        for sel in selections:
            code = (sel.get('section_code') or '').strip().upper()
            fields = [f for f in (sel.get('fields') or []) if f in INGESTABLE_FIELDS]
            if not SECTION_CODE_RE.match(code):
                skipped.append({'section_code': code, 'reason': 'invalid_section_code'})
                continue
            if not fields:
                skipped.append({'section_code': code, 'reason': 'no_valid_fields'})
                continue
            drive_sec = payload.get(code)
            if not isinstance(drive_sec, dict):
                skipped.append({'section_code': code, 'reason': 'not_in_drive'})
                continue
            sec_id = db_codes.get(code)

            field_to_drive_key = {'section_name': 'name', 'purpose': 'purpose', 'content': 'content'}
            values = {}
            for fld in fields:
                v = drive_sec.get(field_to_drive_key[fld], '')
                if v is None:
                    v = ''
                if not isinstance(v, str):
                    v = json.dumps(v)
                if not v.strip() and not allow_clear:
                    # protect against accidental wipes
                    continue
                values[fld] = v

            if not values:
                skipped.append({'section_code': code, 'reason': 'all_drive_values_blank_no_clear_opt'})
                continue

            if sec_id:
                set_parts = [f"{k} = %s" for k in values.keys()]
                params = list(values.values()) + [sec_id]
                cur.execute(
                    f"UPDATE day_b_sections SET {', '.join(set_parts)}, updated_at = NOW() WHERE id = %s",
                    params)
            else:
                cur.execute('''INSERT INTO day_b_sections
                               (lesson_id, section_code, section_name, purpose, content)
                               VALUES (%s, %s, %s, %s, %s)''',
                            (db_lesson['id'], code,
                             values.get('section_name', ''),
                             values.get('purpose', ''),
                             values.get('content', '')))
            applied.append({'section_code': code, 'fields': list(values.keys())})

        new_status = 'accepted' if applied else cand['status']
        cur.execute("UPDATE ingest_candidates SET status=%s, updated_at=NOW() WHERE id=%s",
                    (new_status, cid))
        conn.commit()
        return jsonify({'ok': True, 'applied': applied, 'skipped': skipped,
                        'lesson_id': db_lesson['id']})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'apply failed: {e}'}), 500
    finally:
        conn.close()


@app.route('/api/ingest/candidates/<int:cid>/reject', methods=['POST'])
def ingest_candidate_reject(cid):
    notes = ((request.get_json(silent=True) or {}).get('notes') or '').strip()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE ingest_candidates SET status='rejected', decision_notes=%s, updated_at=NOW() WHERE id=%s",
                (notes, cid))
    found = cur.rowcount
    cur.close(); conn.close()
    if not found:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'ok': True})


@app.route('/api/ingest/candidates/<int:cid>/reset', methods=['POST'])
def ingest_candidate_reset(cid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE ingest_candidates SET status='pending', decision_notes='', updated_at=NOW() WHERE id=%s",
                (cid,))
    found = cur.rowcount
    cur.close(); conn.close()
    if not found:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'ok': True})


@app.route('/api/catalog/files/summary', methods=['GET'])
def catalog_files_summary():
    rows = _build_repo_catalog()
    by_extension = {}
    by_type = {}
    by_layer = {layer: 0 for layer in STACK_LAYERS}
    python_links = []
    for row in rows:
        by_extension[row['extension']] = by_extension.get(row['extension'], 0) + 1
        by_type[row['file_type']] = by_type.get(row['file_type'], 0) + 1
        by_layer[row['layer']] = by_layer.get(row['layer'], 0) + 1
        if row['extension'] == 'py':
            python_links.append({
                'name': row['name'],
                'relative_path': row['relative_path'],
                'href': row['href'],
                'python_group': row['python_group'],
            })
    return jsonify({
        'total_files': len(rows),
        'by_extension': by_extension,
        'by_type': by_type,
        'by_layer': by_layer,
        'python_links': python_links,
    })


@app.route('/api/catalog/files', methods=['GET'])
def catalog_files():
    rows = _build_repo_catalog()
    extension = request.args.get('extension', '').strip().lower().lstrip('.')
    file_type = request.args.get('type', '').strip().lower()
    layer = request.args.get('layer', '').strip().lower()
    q = request.args.get('q', '').strip().lower()
    python_only = request.args.get('python_only', '').strip().lower()
    if extension:
        rows = [row for row in rows if row['extension'] == extension]
    if file_type:
        rows = [row for row in rows if row['file_type'] == file_type]
    if layer:
        rows = [row for row in rows if row['layer'] == layer]
    if python_only in ('1', 'true', 'yes'):
        rows = [row for row in rows if row['extension'] == 'py']
    if q:
        rows = [
            row for row in rows
            if q in row['name'].lower()
            or q in row['title'].lower()
            or q in row['relative_path'].lower()
            or q in row['layer'].lower()
            or q in row['file_type'].lower()
        ]
    return jsonify({
        'files': rows,
        'count': len(rows),
        'filters': {
            'extension': extension,
            'type': file_type,
            'layer': layer,
            'q': q,
            'python_only': python_only,
        },
    })


@app.route('/api/catalog/stack', methods=['GET'])
def catalog_stack():
    rows = _build_repo_catalog()
    layers = {layer: [] for layer in STACK_LAYERS}
    for row in rows:
        layers.setdefault(row['layer'], []).append(row)
    return jsonify({
        'layers': layers,
        'development_plan': [
            'Use backend scripts and APIs as the canonical integration layer.',
            'Use frontend HTML and shared scripts for current multi-page tooling.',
            'Treat attached_assets as experimental/imported references until promoted.',
            'Reserve JSX/TS/TSX slots for a future React workspace once a runtime/build path is added.',
        ],
    })


with app.app_context():
    init_db()
    seed_production_data()
    seed_day_b_data()
    sync_element_reconciliations()
    init_ingester_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
