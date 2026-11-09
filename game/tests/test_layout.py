# -*- coding: utf-8 -*-
"""Detector de sobreposição: registra o retângulo de todo texto desenhado em cada tela e
falha se dois textos se cruzam ou se algum sai da janela (o defeito 'palavra em cima de palavra')."""
import os
import tempfile
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

import eco_nave  # noqa: E402
from eco_nave.config import H, W  # noqa: E402
from eco_nave.progress_store import ProgressStore  # noqa: E402
from eco_nave.ranking import RankEntry, RankingStore  # noqa: E402
from eco_nave.states.playing import PlayingState  # noqa: E402
from eco_nave.text import TextRenderer  # noqa: E402
from eco_nave.workshop_catalog import COMPONENTS, DESTINATIONS  # noqa: E402

TOL = 3          # px de tolerância (antialiasing e sombras)


class Recorder:
    def __init__(self):
        self.items = []
        self.on = True
        self._orig = TextRenderer.draw

    def start(self):
        rec = self

        def draw(self_, surf, text, size, color, pos, anchor="center", **kw):
            r = rec._orig(self_, surf, text, size, color, pos, anchor, **kw)
            if rec.on and tuple(surf.get_size()) == (W, H):
                rec.items.append((text, (r.x, r.y, r.w, r.h)))
            return r
        TextRenderer.draw = draw

    def stop(self):
        TextRenderer.draw = self._orig

    def clear(self):
        self.items = []


def _silenced(orig_draw, rec):
    """Versão de 'draw' que não registra textos (para o que fica por baixo de um modal)."""
    def wrapper(self_, surf):
        prev = rec.on
        rec.on = False
        try:
            return orig_draw(self_, surf)
        finally:
            rec.on = prev
    return wrapper


def _overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (min(ax + aw, bx + bw) - max(ax, bx) > TOL) and (min(ay + ah, by + bh) - max(ay, by) > TOL)


class LayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((W, H))
        cls.tmp = tempfile.mkdtemp()
        cls._orig_path = ProgressStore.default_path
        ProgressStore.default_path = classmethod(lambda c: os.path.join(cls.tmp, "progress.json"))
        cls._orig_save = RankingStore.save
        RankingStore.save = lambda self: True
        cls.rec = Recorder()
        cls.rec.start()
        cls.game = eco_nave.Game(cls.screen, ranking_path=os.path.join(cls.tmp, "ranking.txt"))
        for i in list(eco_nave.items.ITEM_CATALOG.ids())[:20]:
            cls.game.progress_store.discover(i)
        names = ["Ana", "Beto", "Caio Eduardo", "Dani", "Eva", "Fábio", "Gabi", "Hugo", "Ivo", "Júlia"]
        cls.game.ranking.entries = [RankEntry(n, 9000 - i * 700, 9 - i // 2, "21/09/2026") for i, n in enumerate(names)]

    @classmethod
    def tearDownClass(cls):
        cls.rec.stop()
        ProgressStore.default_path = cls._orig_default if hasattr(cls, "_orig_default") else cls._orig_path
        RankingStore.save = cls._orig_save

    def tearDown(self):
        self.game.audio_panel.close()

    # ---------------------------------------------------------------- utilidades
    def key(self, k):
        self.game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=k))

    def run_frames(self, n):
        for _ in range(n):
            self.game.update(1 / 60)

    def check(self, label, skip_world=False):
        """Desenha a tela atual e confere sobreposição e limites."""
        rec = self.rec
        rec.clear()
        patched = []
        if skip_world:       # texto por baixo de um modal (painel opaco por cima) não conta
            targets = {PlayingState}
            targets.add(type(self.game.state))
            for cls in targets:
                orig = cls.draw
                patched.append((cls, orig))
                cls.draw = _silenced(orig, rec)
            if self.game.audio_panel.visible:
                pass
        try:
            self.game.draw()
        finally:
            for cls, orig in patched:
                cls.draw = orig
        items = rec.items
        problems = []
        for text, (x, y, w, h) in items:
            if x < -TOL or y < -TOL or x + w > W + TOL or y + h > H + TOL:
                problems.append(f"fora da janela: {text!r} {(x, y, w, h)}")
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][0].strip() and items[j][0].strip() and _overlap(items[i][1], items[j][1]):
                    problems.append(f"sobrepostos: {items[i][0][:40]!r} x {items[j][0][:40]!r}")
        self.assertFalse(problems, label + ":\n  " + "\n  ".join(problems[:8]))
        self.assertGreater(len(items), 2, label + ": nenhum texto desenhado")

    def go(self, name, **kw):
        self.game.set_state(name, **kw)
        self.run_frames(3)

    # -------------------------------------------------------------------- telas
    def test_hub_and_help(self):
        self.go("menu")
        self.check("menu")
        for k in (pygame.K_DOWN, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT):
            self.key(k)
            self.check("menu selecao " + str(k))
        self.go("menu")
        self.rec.clear()
        self.game.draw()
        from eco_nave.config import BIN_BODY_TOP
        low = [(t, r) for t, r in self.rec.items if r[1] + r[3] > BIN_BODY_TOP - 8]
        self.assertFalse(low, "texto do menu invadindo as lixeiras: %r" % low[:3])
        self.go("help")
        self.check("ajuda")

    def test_workshop_every_stage(self):
        self.go("workshop")
        w = self.game.state
        self.run_frames(40)
        self.check("oficina avaliacao")
        for i, opt_key in enumerate(("reuse", "repair", "recycle")):
            w.opt_sel = i
            w.mode = "select"
            w.run.eval_choice = None
            w.key = None
            w.run.evaluate(opt_key)
            w.feedback = ("Texto de teste. " * 12, i % 2 == 0)
            w.mode = "feedback"
            self.check("oficina avaliacao feedback " + opt_key)
        self.key(pygame.K_RETURN)
        self.run_frames(120)
        self.check("oficina triagem")
        self.key(pygame.K_RETURN)
        self.check("oficina triagem escolhendo destino")
        self.key(pygame.K_RETURN)
        self.run_frames(5)
        self.check("oficina triagem feedback")
        w._finish_flight()
        for comp in COMPONENTS[1:]:
            w.mode, w.part_sel = "select", COMPONENTS.index(comp)
            w.tray_sel = [d[0] for d in DESTINATIONS].index(comp.destination_key)
            w._confirm_part()
            w._finish_flight()
        self.assertTrue(w.run.finished)
        w._to_summary()
        self.run_frames(30)
        self.check("oficina resultado")

    def test_codex_every_group(self):
        self.go("codex")
        for _ in range(12):
            for _step in range(3):
                self.check("enciclopedia grupo " + str(self.game.state.group_index))
                self.key(pygame.K_RIGHT)
            self.key(pygame.K_e)

    def test_real_world_ranking_pause_name_audio(self):
        self.go("real_world")
        self.check("descarte real")
        self.go("ranking", new_entry=self.game.ranking.entries[2], note="")
        self.check("ranking")
        self.go("playing", new_game=True)
        self.run_frames(90)
        self.check("partida")
        self.key(pygame.K_p)
        self.run_frames(2)
        rec = self.rec
        orig_draw = PlayingState.draw
        PlayingState.draw = _silenced(orig_draw, rec)
        try:
            self.check("pausa")
        finally:
            PlayingState.draw = orig_draw
        self.game.audio_panel.open()
        self.check("audio", skip_world=True)
        self.game.audio_panel.close()
        self.game.session.progress.score = 5000
        self.go("name")
        orig_draw = PlayingState.draw
        PlayingState.draw = _silenced(orig_draw, rec)
        try:
            self.check("fim de jogo")
        finally:
            PlayingState.draw = orig_draw


if __name__ == "__main__":
    unittest.main()
