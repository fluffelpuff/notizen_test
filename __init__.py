from .db import get_connection

INIT_SQL = """
CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT,
    text       TEXT,
    timestamp  TEXT,
    notice_id  TEXT
);

-- sinnvolle Indizes (optional, aber hilfreich fürs Suchen/Sortieren)
CREATE INDEX IF NOT EXISTS idx_notes_notice_id ON notes(notice_id);
CREATE INDEX IF NOT EXISTS idx_notes_timestamp ON notes(timestamp);
"""

conn = get_connection("app.db", init_sql=INIT_SQL)