# db.py
from __future__ import annotations
import sqlite3
from pathlib import Path
import threading
import atexit

_CONNECTION: sqlite3.Connection | None = None
_EXEC_LOCK = threading.Lock()
_LOCK = threading.Lock()

def get_connection(db_path: str | Path = "app.db", init_sql: str | None = None) -> sqlite3.Connection:
    global _CONNECTION
    if _CONNECTION is not None:
        return _CONNECTION

    with _LOCK:
        if _CONNECTION is not None:
            return _CONNECTION

        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        is_new = not db_path.exists()

        uri = f"file:{db_path.as_posix()}?cache=shared"
        conn = sqlite3.connect(
            uri,
            uri=True,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
            isolation_level=None,
        )

        if is_new and init_sql:
            with conn:
                conn.executescript(init_sql)

        _CONNECTION = conn
        atexit.register(_safe_close)
        return _CONNECTION

def transaction():
    """Kontextmanager für atomare Transaktionen über die eine Connection."""
    conn = get_connection()
    class _Tx:
        def __enter__(self):
            _EXEC_LOCK.acquire()
            conn.execute("BEGIN")
            return conn
        def __exit__(self, exc_type, exc, tb):
            try:
                if exc_type is None:
                    conn.execute("COMMIT")
                else:
                    conn.execute("ROLLBACK")
            finally:
                _EXEC_LOCK.release()
    return _Tx()

def _safe_close() -> None:
    global _CONNECTION
    try:
        if _CONNECTION is not None:
            _CONNECTION.close()
    finally:
        _CONNECTION = None