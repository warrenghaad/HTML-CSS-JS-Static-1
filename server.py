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

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
