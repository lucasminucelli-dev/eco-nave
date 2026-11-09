# -*- coding: utf-8 -*-
"""Tela do ranking (top 10)."""
import math

import pygame

from ..config import W
from ..drawing import D
from ..text import TEXT
from ..ui import Ui
from ..utils import fmt, mix
from .base import AttractState


class RankingState(AttractState):
    def __init__(self, game):
        super().__init__(game)
        self.new_entry = None      # entrada recem-criada (destacada na tabela)
        self.note = ""             # aviso opcional abaixo da tabela

    def enter(self, new_entry=None, note="", **kwargs):
        self.new_entry = new_entry
        self.note = note

    def handle_key(self, key):
        game = self.game
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            game.start_game()
        elif key == pygame.K_ESCAPE:
            game.set_state("menu")

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        cx = W // 2
        TEXT.draw(surf, "RANKING", 64, (255, 226, 110), (cx, 62), "center", bold=True, outline=(40, 30, 10))
        pw = 800
        px = (W - pw) // 2
        Ui.panel(surf, (px, 112, pw, 462), border=(70, 110, 190))
        hy = 138
        head = (150, 172, 214)
        TEXT.draw(surf, "#", 15, head, (px + 30, hy), "midleft", bold=True)
        TEXT.draw(surf, "NOME", 15, head, (px + 80, hy), "midleft", bold=True)
        TEXT.draw(surf, "NÍVEL", 15, head, (px + 430, hy), "center", bold=True)
        TEXT.draw(surf, "DATA", 15, head, (px + 560, hy), "center", bold=True)
        TEXT.draw(surf, "PONTOS", 15, head, (px + pw - 30, hy), "midright", bold=True)
        entries = game.ranking.entries
        if not entries:
            TEXT.draw(surf, "Ainda não há pontuações. Seja o primeiro!", 24, (226, 234, 250), (cx, 340), "center")
        for i, e in enumerate(entries):
            y = 176 + i * 38
            mine = e is self.new_entry
            if mine:
                pulse = 0.5 + 0.5 * math.sin(game.t * 6)
                D.rect(surf, mix((30, 70, 60), (60, 140, 100), pulse), (px + 12, y - 17, pw - 24, 34), 0,
                       border_radius=8)
            elif i % 2 == 0:
                D.rect(surf, (18, 26, 54), (px + 12, y - 17, pw - 24, 34), 0, border_radius=8)
            if i < 3:
                rc = ((255, 214, 70), (208, 214, 226), (222, 150, 90))[i]
            else:
                rc = (200, 210, 235)
            tc = (255, 255, 255) if not mine else (170, 255, 190)
            TEXT.draw(surf, str(i + 1), 24, rc, (px + 30, y), "midleft", bold=True)
            TEXT.draw(surf, e.name, 24, tc, (px + 80, y), "midleft", bold=mine, max_w=300)
            TEXT.draw(surf, str(e.level), 22, (200, 210, 235), (px + 430, y), "center")
            TEXT.draw(surf, e.date, 18, (150, 165, 200), (px + 560, y), "center")
            TEXT.draw(surf, fmt(e.score), 26, tc, (px + pw - 30, y), "midright", bold=True)
        if self.note:
            TEXT.draw(surf, self.note, 22, (255, 200, 130), (cx, 604), "center", bold=True)
        elif self.new_entry is not None:
            TEXT.draw(surf, "Parabéns! Você entrou no ranking!", 22, (170, 255, 190), (cx, 604), "center",
                      bold=True)
        w1 = Ui.keylabel_width("ENTER") + 10 + TEXT.width("jogar de novo", 20)
        w2 = Ui.keylabel_width("ESC") + 10 + TEXT.width("menu", 20)
        x = (W - (w1 + 44 + w2)) // 2
        w = Ui.keylabel(surf, "ENTER", x, 656)
        r = TEXT.draw(surf, "jogar de novo", 20, (226, 234, 250), (x + w + 10, 656), "midleft")
        w = Ui.keylabel(surf, "ESC", r.right + 44, 656)
        TEXT.draw(surf, "menu", 20, (226, 234, 250), (r.right + 44 + w + 10, 656), "midleft")
