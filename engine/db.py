import sqlite3
import json
import uuid
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'claritygrc.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id TEXT PRIMARY KEY,
            system_name TEXT,
            system_type TEXT,
            created_at TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            eu_classification TEXT,
            data_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_assessment(system_name, system_type, risk_score, risk_level, eu_classification, full_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    assessment_id = str(uuid.uuid4())[:8]
    created_at = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO assessments (id, system_name, system_type, created_at, risk_score, risk_level, eu_classification, data_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (assessment_id, system_name, system_type, created_at, risk_score, risk_level, eu_classification, json.dumps(full_data)))
    conn.commit()
    conn.close()
    return assessment_id

def get_assessment(assessment_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT data_json FROM assessments WHERE id = ?', (assessment_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def get_history(system_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, created_at, risk_score, risk_level, eu_classification
        FROM assessments WHERE system_name = ?
        ORDER BY created_at DESC
    ''', (system_name,))
    rows = c.fetchall()
    conn.close()
    return [
        {'id': r[0], 'created_at': r[1], 'risk_score': r[2], 'risk_level': r[3], 'eu_classification': r[4]}
        for r in rows
    ]