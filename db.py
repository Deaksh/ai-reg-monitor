import sqlite3
from pathlib import Path
from datetime import datetime
import json

DB_PATH = Path("compliance.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Regulation versions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS regulation_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article TEXT,
        content TEXT,
        fetched_at TEXT
    )
    """)

    # Detected changes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS detected_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article TEXT,
        chunk_id TEXT,
        change_type TEXT,
        summary TEXT,
        confidence REAL,
        before TEXT,
        after TEXT,
        created_at TEXT
    )
    """)

    # Impact assessments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS impact_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        change_id INTEGER,
        applies BOOLEAN,
        risk_level TEXT,
        recommended_action TEXT,
        reasoning TEXT,
        confidence REAL,
        created_at TEXT
    )
    """)

    # Alerts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        change_id INTEGER,
        severity TEXT,
        message TEXT,
        created_at TEXT,
        acknowledged BOOLEAN DEFAULT 0
    )
    """)

    # Audit log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        payload TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_audit(event_type: str, payload: dict):
    conn = get_conn()
    conn.execute(
        "INSERT INTO audit_log VALUES (NULL, ?, ?, ?)",
        (event_type, json.dumps(payload), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

