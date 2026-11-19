import os
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest import mock

from repquest import db


class StarterDatabaseTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "nested" / "school.db"

    def tearDown(self):
        self._tmp.cleanup()

    def test_init_creates_a_new_file_with_schema_meta(self):
        self.assertFalse(self.path.exists())
        self.assertEqual(db.init_db(self.path), self.path)
        self.assertTrue(self.path.is_file())
        with closing(db.connect(self.path)) as conn:
            self.assertEqual(db.table_names(conn), ["schema_meta"])
            self.assertEqual(db.schema_version(conn), db.SCHEMA_VERSION)

    def test_init_is_idempotent(self):
        db.init_db(self.path)
        db.init_db(self.path)
        with closing(db.connect(self.path)) as conn:
            count = conn.execute("SELECT COUNT(*) FROM schema_meta").fetchone()[0]
        self.assertEqual(count, 1)

    def test_foreign_keys_are_on(self):
        with closing(db.connect(self.path)) as conn:
            self.assertEqual(conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)

    def test_env_override_selects_the_file(self):
        with mock.patch.dict(os.environ, {db.DB_PATH_ENV: str(self.path)}):
            self.assertEqual(db.db_path(), self.path)
            db.init_db()
        self.assertTrue(self.path.is_file())

    def test_default_path_is_inside_ignored_data_dir(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop(db.DB_PATH_ENV, None)
            self.assertEqual(db.db_path(), db.PROJECT_ROOT / "data" / "repquest_school.db")


if __name__ == "__main__":
    unittest.main()
