import sqlite3
from config import Config

def get_db():
    return sqlite3.connect(Config.DB_NAME)

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS api_keys 
    (
        id INTEGER PRIMARY KEY,
        name TEXT,
        key_string TEXT UNIQUE,
        created_at TEXT,
        limit_count INTEGER DEFAULT 100,
        used_count INTEGER DEFAULT 0
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS usage_logs 
    (
        id INTEGER PRIMARY KEY,
        key_string TEXT,
        timestamp TEXT,
        status TEXT
    )''')

    conn.commit()
    conn.close()