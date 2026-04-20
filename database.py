import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("orca.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        input TEXT,
        result TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_analysis(user, input_data, result):
    conn = sqlite3.connect("orca.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO analyses (user, input, result, timestamp)
    VALUES (?, ?, ?, ?)
    """, (user, input_data, result, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_history(user):
    conn = sqlite3.connect("orca.db")
    c = conn.cursor()

    c.execute("""
    SELECT input, result, timestamp FROM analyses
    WHERE user=?
    ORDER BY id DESC
    """, (user,))

    data = c.fetchall()
    conn.close()
    return data
