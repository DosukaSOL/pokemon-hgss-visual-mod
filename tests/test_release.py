#!/usr/bin/env python3
"""Lightweight release checks (no ROMs required).

Verifies that every release patch listed in release/release_manifest.json
exists, matches its recorded SHA-256, and follows the naming convention.
Run with:  python -m unittest discover tests
Full validation (requires local ROMs):  python scripts/validate.py
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "release" / "release_manifest.json"
NAME_RE = re.compile(
    r"^(heartgold|soulsilver)-english-visual-plus-"
    r"(visual-only|safe|full|conservative-camera)-\d+\.\d+\.\d+\.xdelta$")


class TestReleaseManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MANIFEST.exists():
            raise unittest.SkipTest("release manifest not built yet")
        cls.manifest = json.loads(MANIFEST.read_text())

    def test_eight_builds(self):
        self.assertEqual(len(self.manifest["builds"]), 8)
        combos = {(b["game"], b["variant"]) for b in self.manifest["builds"]}
        self.assertEqual(len(combos), 8)

    def test_patches_exist_and_match_hashes(self):
        for b in self.manifest["builds"]:
            patch = REPO_ROOT / b["patch"]
            self.assertTrue(patch.exists(), patch)
            digest = hashlib.sha256(patch.read_bytes()).hexdigest()
            self.assertEqual(digest, b["patch_sha256"], patch.name)

    def test_naming_convention(self):
        for b in self.manifest["builds"]:
            self.assertRegex(Path(b["patch"]).name, NAME_RE)

    def test_no_roms_in_release(self):
        leaked = list((REPO_ROOT / "release").rglob("*.nds"))
        self.assertEqual(leaked, [], "ROMs must never be in release/")


class TestRomManifest(unittest.TestCase):
    def test_manifest_wellformed(self):
        data = json.loads((REPO_ROOT / "tests" / "rom_manifest.json").read_text())
        for rom in data["roms"]:
            self.assertRegex(rom["sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(rom["game_code"], r"^[A-Z]{4}$")


if __name__ == "__main__":
    unittest.main()
