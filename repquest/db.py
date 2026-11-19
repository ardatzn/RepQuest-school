"""Shared SQLite connection and starter setup, used by every team feature.

What exists now: a connection helper and an idempotent setup that works on an empty file. It creates only the
``schema_meta`` table, which records the schema version. The app calls ``init_db`` on start with a file in the app's
private data folder, so it works offline on the phone.

The product tables and their relations are Mehmet Arif Yörük's assignment (``team/mehmet_arif/schema.py``). Changes to
this shared file are coordinated through the team.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "repquest_school.db"
DB_PATH_ENV = "REPQUEST_DB_PATH"

# Starter schema has no product tables yet. Raise this when product tables are added.
SCHEMA_VERSION = 0


def db_path() -> Path:
    """The database file: ``$REPQUEST_DB_PATH`` when set, otherwise ``data/repquest_school.db``."""
    override = os.environ.get(DB_PATH_ENV)
    return Path(override) if override else DEFAULT_DB_PATH


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    """Open a connection with foreign keys on and rows readable by column name."""
    target = Path(path) if path is not None else db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: Path | str | None = None) -> Path:
    """Create the starter schema if it is missing. Safe to run on every app start; returns the database path."""
    target = Path(path) if path is not None else db_path()
    with connect(target) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        conn.execute(
            "INSERT OR IGNORE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )
    conn.close()
    return target


def schema_version(conn: sqlite3.Connection) -> int:
    """The schema version stored in ``schema_meta``."""
    row = conn.execute("SELECT value FROM schema_meta WHERE key = 'schema_version'").fetchone()
    if row is None:
        raise RuntimeError("schema_meta has no schema_version; run init_db() first")
    return int(row["value"])


def table_names(conn: sqlite3.Connection) -> list[str]:
    """User tables in the database, sorted by name."""
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [row["name"] for row in rows]
