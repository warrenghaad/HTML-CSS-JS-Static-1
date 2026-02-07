import os
import json
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__, static_folder='.', static_url_path='')

DATABASE_URL = os.environ.get('DATABASE_URL')

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
