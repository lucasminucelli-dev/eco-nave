# -*- coding: utf-8 -*-
"""Tela de pausa (desenhada por cima da partida congelada)."""
import pygame

from ..config import W
from ..text import TEXT
from ..ui import Ui
from .base import GameState


class PausedState(GameState):
    def handle_key(self, key):
        if key in (pygame.K_p, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.game.set_state("playing")
        elif key == pygame.K_ESCAPE:
            self.game.set_state("menu")

    def update(self, dt):
        """Tudo congelado durante a pausa (nem as estrelas se mexem)."""

    def draw(self, surf):
        game = self.game
        game.states["playing"].draw(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (W // 2 - 340, 190, 680, 330), alpha=252, border=(70, 110, 190))
        TEXT.draw(surf, "PAUSADO", 60, (255, 255, 255), (W // 2, 252), "center", bold=True, shadow=(0, 0, 0))
        Ui.hint_bar(surf, [("P", "continuar"), ("V", "áudio"), ("ESC", "menu")], 322, 17)
        TEXT.draw(surf, "VOCÊ SABIA?", 15, (130, 245, 160), (W // 2, 384), "center", bold=True)
        Ui.fit_block(surf, game.fact, (W // 2 - 300, 408, 600, 90), (222, 230, 246), 20, 14, align="center")
