# -*- coding: utf-8 -*-
"""Fim de jogo: mostra a pontuacao e pede o nome do jogador."""
import pygame

from ..config import H, NAME_MAX, RANKING_SIZE, W
from ..drawing import D
from ..events import TEXT_INPUT
from ..ranking import RankEntry
from ..items import ITEM_CATALOG
from ..text import TEXT
from ..ui import Ui
from ..utils import fmt
from .base import GameState


class NameEntryState(GameState):
    allow_mute = False         # aqui o jogador digita letras (inclusive o M)
    LOCK_TIME = 0.7            # ignora teclas logo depois do fim, para nao confirmar sem querer

    def __init__(self, game):
        super().__init__(game)
        self.name = ""
        self.lock = 0.0

    def enter(self, **kwargs):
        self.name = ""
        self.lock = self.LOCK_TIME
        self._text_input(True)

    def exit(self):
        self._text_input(False)

    @staticmethod
    def _text_input(on):
        try:
            if on:
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()
        except Exception:
            pass

    # ---- entrada
    def handle_event(self, ev):
        if TEXT_INPUT is not None and ev.type == TEXT_INPUT:
            if self.lock <= 0:
                for ch in ev.text:
                    if ch.isprintable() and len(self.name) < NAME_MAX:
                        self.name += ch
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.lock <= 0:
                self.confirm()

    def confirm(self):
        game = self.game
        progress = game.session.progress
        entry = RankEntry.create(self.name, progress.score, progress.level)
        if game.ranking.add(entry):
            game.set_state("ranking", new_entry=entry, note="")
        else:
            note = f"Sua pontuação ({fmt(progress.score)}) ficou fora do top {RANKING_SIZE}."
            game.set_state("ranking", new_entry=None, note=note)

    # ---- atualizacao e desenho
    def update(self, dt):
        super().update(dt)
        if self.lock > 0:
            self.lock -= dt
        self.game.session.update_effects(dt)

    def draw(self, surf):
        game = self.game
        progress = game.session.progress
        game.states["playing"].draw(surf)
        surf.blit(game.assets.dim, (0, 0))
        pw, ph = 820, 520
        px, py = (W - pw) // 2, (H - ph) // 2 - 8
        Ui.panel(surf, (px, py, pw, ph), alpha=252, border=(255, 130, 130), bw=3)
        cx = W // 2
        TEXT.draw(surf, "FIM DE JOGO", 54, (255, 120, 120), (cx, py + 42), "center", bold=True,
                  shadow=(0, 0, 0))
        TEXT.draw(surf, "SUA PONTUAÇÃO", 15, (150, 172, 214), (cx, py + 88), "center", bold=True)
        TEXT.draw(surf, fmt(progress.score), 54, (255, 255, 255), (cx, py + 124), "center", bold=True,
                  shadow=(0, 0, 0))
        stats = (f"Nível {progress.level}   ·   Acertos {progress.correct}   ·   Erros {progress.wrong}   ·   "
                 f"Precisão {progress.accuracy}%   ·   Melhor combo {progress.best_streak}")
        TEXT.draw(surf, stats, 17, (214, 224, 244), (cx, py + 172), "center", max_w=pw - 45)
        TEXT.draw(surf, "MAIOR TÍTULO: " + progress.highest_title, 20, (130, 245, 170),
                  (cx, py + 211), "center", bold=True, max_w=pw - 50)
        discovered = []
        for item_id in sorted(game.session.new_discoveries):
            idef = ITEM_CATALOG.by_id(item_id)
            if idef:
                discovered.append(idef.name)
        new_text = f"Novos objetos descobertos: {len(discovered)}"
        if discovered:
            new_text += " — " + ", ".join(discovered[:3])
            if len(discovered) > 3:
                new_text += ", ..."
        TEXT.draw(surf, new_text, 15, (190, 216, 238), (cx, py + 241), "center", max_w=pw - 60)
        TEXT.draw(surf, "Digite seu nome e pressione ENTER", 20, (255, 255, 255), (cx, py + 278), "center",
                  bold=True)
        box = pygame.Rect(0, 0, 440, 54)
        box.center = (cx, py + 324)
        D.rect(surf, (16, 22, 48), box, 0, border_radius=10)
        D.rect(surf, (110, 240, 150), box, 3, border_radius=10)
        caret = "|" if int(game.t * 2) % 2 == 0 else " "
        TEXT.draw(surf, self.name + caret, 32, (255, 255, 255), box.center, "center", bold=True, max_w=420)
        TEXT.draw(surf, f"{len(self.name)}/{NAME_MAX}", 13, (130, 145, 180),
                  (box.right - 8, box.bottom + 10), "midright")
        TEXT.draw(surf, "VOCÊ SABIA?", 14, (130, 245, 160), (cx, py + 407), "center", bold=True)
        for i, line in enumerate(TEXT.wrap(game.fact, 17, pw - 110)[:2]):
            TEXT.draw(surf, line, 17, (222, 230, 246), (cx, py + 433 + i * 22), "center")
