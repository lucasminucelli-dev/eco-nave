# -*- coding: utf-8 -*-
"""Tela 'Como jogar': controles, regras e a legenda das 10 lixeiras."""
import pygame

from ..bins import BINS
from ..config import W
from ..drawing import rr
from ..text import TEXT
from ..ui import Ui
from .base import AttractState

RULES = (
    "Leve cada resíduo até a lixeira da cor certa antes que ele chegue ao chão.",
    "Cada acerto dá pontos; sequências de acertos aumentam o combo (até x5).",
    "Você começa com 3 vidas. A cada 5 acertos o nível sobe e a nave acelera.",
    "Nos níveis 3, 5, 10, 15 e 20 você conquista títulos especiais.",
)


class HelpState(AttractState):
    def handle_key(self, key):
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_h):
            self.game.set_state("menu")
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.game.start_game()

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (70, 36, 1140, 728), border=(236, 200, 110), bw=3)
        Ui.header(surf, "COMO JOGAR", None, (255, 226, 126), (50, 36, 10), y=84)

        # --- controles (coluna esquerda)
        lx, top = 120, 150
        TEXT.draw(surf, "CONTROLES", 17, (130, 245, 160), (lx, top), "topleft", bold=True)
        rows = [(("left", "right"), "mover o lixo para os lados  (ou A / D)"), (("down",), "acelerar a queda  (ou S)"),
                (("P",), "pausar a partida  (ou ESC)"), (("M",), "ligar ou desligar o áudio"),
                (("V",), "ajustar volume da música e dos efeitos"), (("F11",), "tela cheia")]
        y = top + 42
        for keys, text in rows:
            x = lx + 18
            for k in keys:
                if k in ("left", "right", "down"):
                    Ui.keycap(surf, x + 17, y, k, 32)
                    x += 38
                else:
                    x += Ui.keylabel(surf, k, x, y, 15) + 6
            TEXT.draw(surf, text, 17, (226, 234, 250), (lx + 100, y), "midleft", max_w=410)
            y += 46

        # --- regras (coluna direita)
        rx, rw = 690, 470
        TEXT.draw(surf, "REGRAS", 17, (130, 245, 160), (rx, top), "topleft", bold=True)
        y = top + 36
        for rule in RULES:
            bottom, _size = Ui.fit_block(surf, rule, (rx + 22, y, rw - 22, 58), (226, 234, 250), 17, 14)
            pygame.draw.circle(surf, (130, 245, 160), (rx + 6, y + 10), 4)
            y = bottom + 16

        # --- legenda das lixeiras (cor + nome + material: nunca depende só da cor)
        ly = 468
        TEXT.draw(surf, "AS 10 LIXEIRAS DA COLETA SELETIVA", 17, (130, 245, 160), (W // 2, ly), "center", bold=True)
        cw, chh, gap = 200, 40, 12
        x0 = (W - (5 * cw + 4 * gap)) // 2
        for i, b in enumerate(BINS):
            x = x0 + (i % 5) * (cw + gap)
            yy = ly + 24 + (i // 5) * (chh + 10)
            rr(surf, (12, 18, 38), (x, yy, cw, chh), 9, (70, 96, 140), 1)
            rr(surf, b.color, (x + 6, yy + 6, 16, chh - 12), 5, (230, 236, 248), 1)
            TEXT.draw(surf, b.name.title(), 14, (255, 255, 255), (x + 30, yy + 12), "midleft", bold=True, max_w=cw - 38)
            TEXT.draw(surf, b.material, 12, (186, 206, 228), (x + 30, yy + 28), "midleft", max_w=cw - 38)

        Ui.fit_block(surf, "Lixo eletrônico não é lixo comum: pilhas, baterias e lâmpadas vão para pontos de coleta, "
                           "e aparelhos inteiros seguem para a logística reversa.",
                     (150, 610, W - 300, 44), (130, 245, 160), 17, 13, bold=True, align="center")
        Ui.hint_bar(surf, [("ENTER", "jogar"), ("ESC", "voltar ao menu")], 716, 16)
