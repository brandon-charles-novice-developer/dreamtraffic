"""SQLite connection and query helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from dreamtraffic.config import DB_PATH

_connection: sqlite3.Connection | None = None


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Get or create a SQLite connection with row factory."""
    global _connection
    path = db_path or DB_PATH
    if _connection is None or db_path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        if db_path is None:
            _connection = conn
        return conn
    return _connection


def close_connection() -> None:
    """Close the global connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None


def execute(sql: str, params: tuple[Any, ...] = (), db_path: Path | None = None) -> sqlite3.Cursor:
    """Execute a SQL statement and return the cursor."""
    conn = get_connection(db_path)
    cursor = conn.execute(sql, params)
    conn.commit()
    return cursor


def fetch_one(sql: str, params: tuple[Any, ...] = (), db_path: Path | None = None) -> dict[str, Any] | None:
    """Fetch a single row as a dict."""
    conn = get_connection(db_path)
    row = conn.execute(sql, params).fetchone()
    if row is None:
        return None
    return dict(row)


def fetch_all(sql: str, params: tuple[Any, ...] = (), db_path: Path | None = None) -> list[dict[str, Any]]:
    """Fetch all rows as a list of dicts."""
    conn = get_connection(db_path)
    rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]
