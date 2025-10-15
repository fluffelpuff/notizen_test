from .db import transaction
from .format import format_ts
from datetime import datetime, timezone
import secrets

def add_notice_to_db_and_get_id(title:str, text:str) -> object:
    hex_id = secrets.token_hex(12)
    ts = datetime.now(timezone.utc).isoformat()

    with transaction() as conn:
        conn.execute("INSERT INTO notes (title, text, timestamp, notice_id) VALUES (?, ?, ?, ?)", (title, text, ts, hex_id))

    return {"id":hex_id, "timestamp":format_ts(ts)}

def delete_notice_by_id(notice_id: str) -> bool:
    notice_id = (notice_id or "").strip()
    if not notice_id:
        return False
    with transaction() as conn:
        conn.execute("DELETE FROM notes WHERE notice_id = ?", (notice_id,))

def update_notice_by_id(notice_id: str, title: str | None = None, text: str | None = None, timestamp: str | None = None) -> bool:
    nid = (notice_id or "").strip()
    if not nid:
        return False

    sets, params = [], []
    if title is not None:
        sets.append("title = ?"); params.append(title)
    if text is not None:
        sets.append("text = ?"); params.append(text)
    if timestamp is not None:
        sets.append("timestamp = ?"); params.append(timestamp)
    if not sets:
        return False 

    sql = f"UPDATE notes SET {', '.join(sets)} WHERE notice_id = ?"
    params.append(nid)

    with transaction() as conn:
        cur = conn.execute(sql, tuple(params))
        return cur.rowcount > 0

def get_all_notice_from_db() -> list:
    with transaction() as conn:
        rows = conn.execute(
            "SELECT title, text, timestamp, notice_id FROM notes ORDER BY id DESC"
        ).fetchall()

    return [
        {
            "id": notice_id,
            "title": title or "",
            "text": text or "",
            "timestamp": format_ts(ts),
        }
        for (title, text, ts, notice_id) in rows
    ]