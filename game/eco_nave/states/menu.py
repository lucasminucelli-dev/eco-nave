# -*- coding: utf-8 -*-
"""Tela inicial."""
import math

import pygame

from ..config import W
from ..text import TEXT
from ..ui import Ui
from ..utils import mix
from .base import AttractState


class MenuState(AttractState):
    def enter(self, **kwargs):
        self.game.ship.beam_t = 0.0

    def handle_key(self, key):
        game = self.game
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            game.start_game()
        elif key == pygame.K_r:
            game.set_state("ranking", new_entry=None, note="")
        elif key == pygame.K_o:
            game.set_state("workshop")
        elif key == pygame.K_c:
            game.set_state("codex")
        elif key == pygame.K_g:
            game.set_state("real_world")
        elif key == pygame.K_ESCAPE:
            game.running = False

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        ship = game.ship
        ship.draw(surf, game.assets, game.t, 66 + math.sin(ship.bob * 2.4) * 4, with_beam=False)
        # titulo
        TEXT.draw(surf, "ECO NAVE", 108, (112, 244, 158), (W // 2, 178), "center", bold=True, outline=(8, 40, 30))
        TEXT.draw(surf, "Desafio do Descarte Consciente", 32, (226, 236, 255), (W // 2, 252), "center",
                  bold=True, shadow=(0, 0, 0))
        # como jogar
        Ui.panel(surf, (230, 290, 820, 128), border=(70, 110, 190))
        Ui.keycap(surf, 300, 328, "left")
        Ui.keycap(surf, 342, 328, "right")
        TEXT.draw(surf, "mova o lixo para os lados", 20, (230, 236, 250), (368, 328), "midleft")
        Ui.keycap(surf, 690, 328, "down")
        TEXT.draw(surf, "acelera a queda", 20, (230, 236, 250), (716, 328), "midleft")
        TEXT.draw(surf, "Leve cada resíduo até a lixeira da cor certa. Errou 3 vezes? Fim de jogo!", 19,
                  (200, 214, 240), (W // 2, 366), "center")
        TEXT.draw(surf, "Lixo eletrônico não é lixo comum: pilhas, baterias e lâmpadas vão para pontos de coleta!",
                  19, (130, 245, 160), (W // 2, 396), "center", bold=True, max_w=780)
        # chamada
        pulse = 0.5 + 0.5 * math.sin(game.t * 4)
        col = mix((255, 255, 255), (255, 232, 110), pulse)
        TEXT.draw(surf, "Pressione ENTER para jogar", 34, col, (W // 2, 456), "center", bold=True,
                  shadow=(0, 0, 0))
        # Modos adicionais da versão 2.0.
        cards = [
            ("O", "OFICINA CIRCULAR", "Avalie e reaproveite", (46, 140, 116)),
            ("C", "ENCICLOPÉDIA", "Descubra os materiais", (54, 112, 174)),
            ("R", "RANKING", "Top 10 jogadores", (138, 104, 184)),
            ("G", "DESCARTE REAL", "Pontos de coleta", (82, 152, 104)),
        ]
        card_w, card_h, gap = 230, 68, 14
        total_w = len(cards) * card_w + (len(cards) - 1) * gap
        start_x = (W - total_w) // 2
        for i, (key, title, subtitle, color) in enumerate(cards):
            x = start_x + i * (card_w + gap)
            Ui.panel(surf, (x, 522, card_w, card_h), border=color, bw=2)
            Ui.keycap(surf, x + 15, 542, key)
            TEXT.draw(surf, title, 17, (245, 250, 255), (x + 62, 540), "topleft", bold=True)
            TEXT.draw(surf, subtitle, 14, (184, 204, 224), (x + 62, 563), "topleft")

        status = "mudo" if game.audio.muted else "ativo"
        controls = (f"M: áudio {status}   ·   [ ] música {int(game.audio.music_volume * 100)}%   ·   "
                    f"- / + efeitos {int(game.audio.fx_volume * 100)}%   ·   F11 tela cheia   ·   ESC sair")
        TEXT.draw(surf, controls, 15, (190, 204, 226), (W // 2, 610), "center", max_w=1120)
        TEXT.draw(surf, "ENTER jogar  |  O oficina  |  C enciclopédia  |  R ranking  |  G descarte real", 16,
                  (130, 245, 160), (W // 2, 646), "center", bold=True)
        game.session.bins.draw(surf, game.assets, game.t, None)
