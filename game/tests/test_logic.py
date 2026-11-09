# -*- coding: utf-8 -*-
"""Testes automatizados das regras independentes do Pygame."""
import ast
import os
import tempfile
import unittest
import unicodedata
import re
from pathlib import Path

from eco_nave.progress import Progress
from eco_nave.progress_store import ProgressStore
from eco_nave.ranking import RankingStore, RankEntry
from eco_nave.achievements import TITLE_MILESTONES

ROOT = Path(__file__).resolve().parents[1]


class ProgressTests(unittest.TestCase):
    def test_level_formula_and_existing_score_combo(self):
        p = Progress()
        self.assertEqual(p.register_hit().points, 100)
        self.assertEqual(p.register_hit().points, 100)
        self.assertEqual(p.register_hit().points, 100)
        self.assertEqual(p.register_hit().points, 100)
        self.assertEqual(p.register_hit().points, 200)
        self.assertEqual(p.level, 2)
        self.assertEqual(p.combo, 2)

    def test_title_milestones_are_emitted_at_expected_levels(self):
        p = Progress()
        emitted = []
        for _ in range(100):
            result = p.register_hit()
            if result.title_unlocked:
                emitted.append((p.level, result.title_unlocked["title"]))
        expected = [(level, data["title"]) for level, data in sorted(TITLE_MILESTONES.items())]
        self.assertEqual(emitted, expected)

    def test_miss_and_extra_life_rules_are_preserved(self):
        p = Progress()
        for _ in range(10):
            p.register_hit()
        self.assertEqual(p.lives, 4)
        p.register_miss()
        self.assertEqual(p.lives, 3)
        self.assertEqual(p.streak, 0)
        self.assertEqual(p.wrong, 1)


class PersistenceTests(unittest.TestCase):
    def test_progress_store_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "eco_progress.json")
            store = ProgressStore(path)
            self.assertTrue(store.discover("livro_antigo"))
            self.assertFalse(store.discover("livro_antigo"))
            self.assertTrue(store.unlock_achievement(3))
            store.register_workshop_completion()
            reopened = ProgressStore(path)
            self.assertIn("livro_antigo", reopened.discovered_ids)
            self.assertIn(3, reopened.achievement_levels)
            self.assertEqual(reopened.workshop_completions, 1)

    def test_corrupt_progress_file_does_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "eco_progress.json")
            Path(path).write_text("{bad json", encoding="utf-8")
            store = ProgressStore(path)
            self.assertEqual(store.discovered_ids, set())
            self.assertEqual(store.achievement_levels, set())

    def test_old_ranking_format_is_read_and_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ranking.txt")
            Path(path).write_text("Ana\t1250\t4\t01/01/2025\nBeto\t900\t3\t02/01/2025\n", encoding="utf-8")
            ranking = RankingStore(path)
            self.assertEqual([x.name for x in ranking.entries], ["Ana", "Beto"])
            entry = RankEntry.create("Caio", 1500, 5)
            self.assertTrue(ranking.add(entry))
            reopened = RankingStore(path)
            self.assertEqual(reopened.entries[0].name, "Caio")
            self.assertEqual(len(reopened.entries), 3)


class CatalogAndAssetTests(unittest.TestCase):
    def test_all_traditional_items_have_unique_stable_ids(self):
        ids = []
        names = []
        for path in (ROOT / "eco_nave" / "items").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for decorator in node.decorator_list:
                        if (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name)
                                and decorator.func.id == "item" and len(decorator.args) >= 2):
                            name = ast.literal_eval(decorator.args[1])
                            ident = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
                            ident = re.sub(r"[^a-z0-9]+", "_", ident).strip("_")
                            ids.append(ident)
                            names.append(name)
        self.assertEqual(len(names), 56)
        self.assertEqual(len(ids), len(set(ids)))
        for expected in ("Revista", "Livro antigo", "Borra de café", "Fralda descartável"):
            self.assertIn(expected, names)

    def test_audio_assets_exist_and_ogg_signature_is_valid(self):
        ogg = ROOT / "assets" / "audio" / "eco_nave_theme.ogg"
        wav = ROOT / "assets" / "audio" / "eco_nave_theme.wav"
        self.assertTrue(ogg.is_file() and ogg.stat().st_size > 10000)
        self.assertEqual(ogg.read_bytes()[:4], b"OggS")
        self.assertTrue(wav.is_file() and wav.stat().st_size > 100000)

    def test_workshop_catalog_contains_eight_devices_and_eight_components(self):
        tree = ast.parse((ROOT / "eco_nave" / "workshop_catalog.py").read_text(encoding="utf-8"))
        equipment = next(node for node in tree.body if isinstance(node, ast.Assign)
                         and any(isinstance(t, ast.Name) and t.id == "EQUIPMENT_CATALOG" for t in node.targets))
        components = next(node for node in tree.body if isinstance(node, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == "COMPONENTS" for t in node.targets))
        self.assertEqual(len(equipment.value.elts), 8)
        self.assertEqual(len(components.value.elts), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
