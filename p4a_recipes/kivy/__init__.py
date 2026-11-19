"""Kivy recipe for the RepQuest School APK: the upstream python-for-android recipe without network-only packages.

The upstream recipe also installs requests, certifi, chardet, idna and urllib3. With python-for-android 2026.05.09,
installing requests fails because pip rejects the Android wheel of its dependency charset-normalizer. RepQuest School
works offline and never imports Kivy's network modules, so this recipe keeps only filetype, which kivy.core.image needs.
Everything else, including the upstream patches, comes from the original recipe.
"""

from os.path import dirname

import pythonforandroid.recipes.kivy as upstream


class OfflineKivyRecipe(upstream.KivyRecipe):
    python_depends = ["filetype"]

    def get_recipe_dir(self):
        # Use the upstream folder so the upstream patch files are found.
        return dirname(upstream.__file__)


recipe = OfflineKivyRecipe()
