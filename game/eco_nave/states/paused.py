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
        Ui.panel(surf, (W // 2 - 340, 200, 680, 290), border=(70, 110, 190))
        TEXT.draw(surf, "PAUSADO", 64, (255, 255, 255), (W // 2, 262), "center", bold=True, shadow=(0, 0, 0))
        x = W // 2 - 250
        w = Ui.keylabel(surf, "P", x, 330)
        TEXT.draw(surf, "continuar", 20, (226, 234, 250), (x + w + 10, 330), "midleft")
        x2 = W // 2 + 30
        w = Ui.keylabel(surf, "ESC", x2, 330)
        TEXT.draw(surf, "voltar ao menu", 20, (226, 234, 250), (x2 + w + 10, 330), "midleft")
        TEXT.draw(surf, "VOCÊ SABIA?", 15, (130, 245, 160), (W // 2, 382), "center", bold=True)
        for i, line in enumerate(TEXT.wrap(game.fact, 20, 600)[:3]):
            TEXT.draw(surf, line, 20, (222, 230, 246), (W // 2, 414 + i * 26), "center")
