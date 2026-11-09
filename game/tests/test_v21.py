# -*- coding: utf-8 -*-
"""Testes das regras novas da versão 2.1 (sem janela)."""
import os
import random
import tempfile
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from eco_nave.effects import Effects  # noqa: E402
from eco_nave.items import ITEM_CATALOG  # noqa: E402
from eco_nave.progress import Progress  # noqa: E402
from eco_nave.progress_store import ProgressStore  # noqa: E402
from eco_nave.spawner import ItemSpawner  # noqa: E402
from eco_nave.ui import fit_block, measure_block  # noqa: E402
from eco_nave.workshop_catalog import (COMPONENTS, EQUIPMENT_CATALOG, SCENARIOS, ASSESSMENT_OPTIONS)  # noqa: E402
from eco_nave.workshop_run import WorkshopRun  # noqa: E402


class WorkshopRunTests(unittest.TestCase):
    def test_every_scenario_has_one_correct_option_and_feedback_for_the_others(self):
        keys = {o.key for o in ASSESSMENT_OPTIONS}
        for sc in SCENARIOS:
            self.assertIn(sc.answer, keys)
            self.assertEqual(set(sc.wrong), keys - {sc.answer}, sc.key)
        self.assertEqual({sc.answer for sc in SCENARIOS}, keys)       # a resposta certa varia

    def test_perfect_run_scores_and_accuracy(self):
        for sc in SCENARIOS:
            run = WorkshopRun(EQUIPMENT_CATALOG[0], scenario=sc)
            self.assertTrue(run.evaluate(sc.answer)[0])
            for c in COMPONENTS:
                self.assertTrue(run.classify(c, c.destination_key)[0])
            self.assertTrue(run.finished and run.perfect)
            self.assertEqual((run.score, run.accuracy), (150 + 100 * len(COMPONENTS), 100))

    def test_wrong_choices_explain_and_do_not_score(self):
        sc = SCENARIOS[0]
        run = WorkshopRun(EQUIPMENT_CATALOG[0], scenario=sc)
        ok, text = run.evaluate("recycle")
        self.assertFalse(ok)
        self.assertIn("Resposta adequada", text)
        ok, text = run.classify(COMPONENTS[-1], "reuse")          # bateria nunca é reutilização
        self.assertFalse(ok)
        self.assertIn("TRATAMENTO", text)
        self.assertEqual(run.score, 0)

    def test_scenario_choice_uses_private_rng_and_avoids_repeats(self):
        random.seed(5)
        before = random.getstate()
        seen = []
        last = None
        for _ in range(12):
            run = WorkshopRun(EQUIPMENT_CATALOG[0], rng=random.Random(), avoid_key=last)
            self.assertNotEqual(run.scenario.key, last)
            last = run.scenario.key
            seen.append(last)
        self.assertEqual(random.getstate(), before)                # sorteio global intacto
        self.assertGreater(len(set(seen)), 2)

    def test_safety_never_instructs_opening_batteries(self):
        for c in COMPONENTS:
            if c.item_id == "comp_bateria":
                self.assertEqual(c.destination_key, "special")
                self.assertIn("Não abra", c.fact)


class RulesPreservedTests(unittest.TestCase):
    def test_titles_once_per_game(self):
        p = Progress()
        titles = [r.title_unlocked["title"] for r in (p.register_hit() for _ in range(120)) if r.title_unlocked]
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(p.highest_title, "Guardião do Planeta")

    def test_spawner_never_returns_workshop_equipment_and_honours_weights(self):
        random.seed(1)
        sp = ItemSpawner(ITEM_CATALOG)
        counts = {}
        for _ in range(4000):
            it = sp.pick(640, 1)
            self.assertIsNotNone(it.bin_index)
            counts[it.name] = counts.get(it.name, 0) + 1
        heavy = [i for i in ITEM_CATALOG if i.spawn_weight > 1]
        self.assertTrue(heavy)                                      # lixo eletrônico/perigoso com destaque
        self.assertTrue(all(i.bin_index is not None for i in heavy))

    def test_effects_default_rng_is_global_random(self):
        random.seed(3)
        a = Effects()
        a.confetti(0, 0, (1, 2, 3), 5)
        pos_a = [(p.x, p.y) for p in a.particles]
        random.seed(3)
        b = Effects(random)
        b.confetti(0, 0, (1, 2, 3), 5)
        self.assertEqual(pos_a, [(p.x, p.y) for p in b.particles])


class ProgressStoreTests(unittest.TestCase):
    def test_corrupt_file_is_kept_as_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "p.json")
            with open(path, "w") as f:
                f.write("{quebrado")
            store = ProgressStore(path)
            self.assertTrue(store.load_error)
            self.assertTrue(os.path.exists(path + ".corrompido"))
            store.discover("x")
            self.assertIn("x", ProgressStore(path).discovered_ids)

    def test_workshop_stats_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "p.json")
            s = ProgressStore(path)
            s.register_workshop_completion(950, True)
            s.register_workshop_completion(400, False)
            r = ProgressStore(path)
            self.assertEqual((r.workshop_completions, r.workshop_best_score, r.workshop_perfect_runs), (2, 950, 1))


class TextFitTests(unittest.TestCase):
    def test_fit_block_stays_inside_rect(self):
        import pygame
        pygame.init()
        pygame.display.set_mode((400, 300))
        surf = pygame.Surface((400, 300))
        long = "Texto bem comprido para testar o ajuste automático de fonte. " * 10
        bottom, size = fit_block(surf, long, (10, 10, 300, 80), (255, 255, 255), 22, 11)
        self.assertLessEqual(bottom, 10 + 80 + 1)
        self.assertLessEqual(size, 22)
        self.assertGreater(measure_block(long, 300, 22), 80)


if __name__ == "__main__":
    unittest.main()
