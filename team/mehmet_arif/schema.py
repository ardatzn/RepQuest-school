"""Product tables and relations. Owner: Mehmet Arif Yörük.

Expected behavior and the acceptance example: see README.md in this folder.

Rules from the shared contract (repquest/contracts.py):
- IDs are TEXT: ``user_id``, ``exercise_id``, ``template_id`` and ``workout_id``. A template such as ``workout_a`` is
  not a finished workout; finishing a workout creates a new ``workout_id``.
- XP awards are unique per ``workout_id`` and keep the date they were earned.
- The setup must work on an empty database and be safe to run again.

The shared connection and the ``schema_meta`` version table live in ``repquest/db.py``. When the product tables are
ready, call ``create_product_tables`` from ``repquest.db.init_db`` and raise ``SCHEMA_VERSION`` (coordinate that
shared change with the team).

The function below is a suggested starting point. You may change it in your pull request.
"""

from __future__ import annotations

import sqlite3


def create_product_tables(conn: sqlite3.Connection) -> None:
    """Create the product tables and their relations if they are missing."""
    raise NotImplementedError("Mehmet Arif Yörük: product tables not built yet")
