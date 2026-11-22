"""Repository rules: Android build settings and English-only project text."""

import configparser
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".venv", ".venv-build", ".buildozer", "bin", "dist", "data", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".ini", ".spec", ".cfg", ".toml"}
# People's names keep their correct spelling; every other text in the project is English.
NAMES = ("Mehmet Arif Yörük", "Arda Tözün", "Duru Göktaş")
TURKISH_LETTERS = re.compile("[\u00e7\u011f\u0131\u00f6\u015f\u00fc\u00c7\u011e\u0130\u00d6\u015e\u00dc]")


def project_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and not SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
            yield path


class BuildSettingsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = configparser.ConfigParser(interpolation=None)
        parser.read(ROOT / "buildozer.spec", encoding="utf-8")
        cls.app = parser["app"]

    def test_separate_app_identity(self):
        self.assertEqual(self.app["title"], "RepQuest School")
        self.assertEqual(f'{self.app["package.domain"]}.{self.app["package.name"]}', "com.repquest.school")

    def test_arm64_build(self):
        archs = [arch.strip() for arch in self.app["android.archs"].split(",")]
        self.assertIn("arm64-v8a", archs)

    def test_offline_app_requests_no_permissions(self):
        self.assertNotIn("android.permissions", self.app)

    def test_python_kivy_sqlite_requirements(self):
        requirements = [item.strip().split("==")[0] for item in self.app["requirements"].split(",")]
        for name in ("python3", "kivy", "sqlite3"):
            self.assertIn(name, requirements)

    def test_kivy_entry_point(self):
        self.assertTrue((ROOT / "main.py").is_file())
        self.assertIn("RepQuestSchoolApp().run()", (ROOT / "main.py").read_text(encoding="utf-8"))


class EnglishOnlyTest(unittest.TestCase):
    def test_no_turkish_text_outside_names(self):
        offenders = []
        for path in project_text_files():
            text = path.read_text(encoding="utf-8")
            for name in NAMES:
                text = text.replace(name, "")
            for number, line in enumerate(text.splitlines(), start=1):
                if TURKISH_LETTERS.search(line):
                    offenders.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
