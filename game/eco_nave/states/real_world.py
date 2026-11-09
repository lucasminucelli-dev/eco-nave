# -*- coding: utf-8 -*-
"""Orientações para encontrar pontos oficiais de coleta de eletroeletrônicos no Brasil."""
import webbrowser

import pygame

from ..drawing import rr
from ..icons import draw_icon
from ..text import TEXT
from ..ui import Ui
from .base import AttractState

SOURCES = [
    (pygame.K_1, "1", "SINIR · logística reversa", "Entenda como funciona o sistema de eletroeletrônicos.",
     "https://sinir.gov.br/perfis/logistica-reversa/logistica-reversa/eletroeletronicos"),
    (pygame.K_2, "2", "GREEN ELETRON", "Procure pontos de entrega de eletroeletrônicos, pilhas e baterias.",
     "https://greeneletron.org.br"),
    (pygame.K_3, "3", "ABREE · pontos de recebimento", "Consulte pontos por CEP e confirme os produtos aceitos.",
     "https://abree.org.br/pontos-de-recebimento"),
]
CHECKLIST = (
    "Antes de ir, consulte o localizador e confirme os produtos aceitos, horários e limites de entrega.",
    "Separe eletroeletrônicos dos resíduos comuns e apague seus dados pessoais.",
    "Nunca abra, perfure, dobre ou tente desmontar baterias. Entregue o aparelho inteiro.",
)


class RealWorldState(AttractState):
    def handle_key(self, key):
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.game.set_state("menu")
            return
        for key_code, _number, _title, _description, url in SOURCES:
            if key == key_code:
                try:
                    webbrowser.open(url)
                except Exception:
                    pass
                self.game.snd.play("select")
                return

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (92, 40, 1096, 720), border=(108, 204, 150), bw=3)
        Ui.header(surf, "DESCARTE NA VIDA REAL", "Encontre pontos oficiais e confirme o que cada local recebe.",
                  (142, 246, 178), (12, 40, 28), y=84, size=40)
        TEXT.draw(surf, "ANTES DE LEVAR SEU APARELHO", 16, (130, 245, 160), (140, 178), "topleft", bold=True)
        Ui.bullets(surf, list(CHECKLIST), (140, 206, 1000, 150), (224, 234, 246), 19, 14, gap=10)
        TEXT.draw(surf, "SITES OFICIAIS (aperte o número para abrir no navegador)", 16, (130, 245, 160), (140, 384),
                  "topleft", bold=True)
        for i, (_key, number, title, desc, url) in enumerate(SOURCES):
            y = 414 + i * 86
            rr(surf, (12, 22, 40), (140, y, 1000, 74), 12, (70, 130, 170), 2)
            Ui.keycap(surf, 180, y + 37, number, 36)
            TEXT.draw(surf, title, 20, (255, 255, 255), (222, y + 24), "midleft", bold=True, max_w=700)
            TEXT.draw(surf, desc, 15, (190, 210, 232), (222, y + 50), "midleft", max_w=720)
            TEXT.draw(surf, url.replace("https://", ""), 12, (120, 160, 196), (1124, y + 50), "midright", max_w=330)
            draw_icon(surf, "pin", 1100, y + 24, 22, (130, 210, 110))
        Ui.fit_block(surf, "As regras podem variar por município e por operador. Sempre confirme antes de sair de casa.",
                     (140, 680, 1000, 28), (255, 198, 132), 16, 12, align="center")
        Ui.hint_bar(surf, [("1 2 3", "abrir site"), ("ESC", "voltar ao menu")], 730, 15)
