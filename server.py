import os
import json
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI

app = Flask(__name__, static_folder='.', static_url_path='')

DATABASE_URL = os.environ.get('DATABASE_URL')

ai_client = OpenAI(
    base_url=os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL'),
    api_key=os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY'),
)

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

    cur.close()
    conn.close()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

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

with app.app_context():
    init_db()
    seed_production_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
