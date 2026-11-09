# -*- coding: utf-8 -*-
"""Orientações para encontrar pontos oficiais de coleta no Brasil."""
import webbrowser
import pygame

from ..config import W
from ..text import TEXT
from ..ui import Ui
from .base import AttractState


SOURCES = [
    (pygame.K_1, "1", "SINIR · orientações oficiais", "Entenda a logística reversa e as etapas do sistema.",
     "https://sinir.gov.br/perfis/logistica-reversa/logistica-reversa/eletroeletronicos"),
    (pygame.K_2, "2", "GREEN ELETRON · localizador", "Pesquise pontos de entrega de eletroeletrônicos e pilhas/baterias.",
     "https://greeneletron.org.br/localizador"),
    (pygame.K_3, "3", "ABREE · pontos de recebimento", "Consulte pontos por CEP e confirme o produto aceito.",
     "https://abree.org.br/pontos-de-recebimento"),
]


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
        Ui.panel(surf, (92, 52, 1096, 690), border=(108, 204, 150), bw=3)
        TEXT.draw(surf, "DESCARTE NA VIDA REAL", 45, (142, 246, 178), (W // 2, 104), "center", bold=True,
                  outline=(12, 40, 28))
        TEXT.draw(surf, "Encontre pontos oficiais e confirme o que cada local recebe.", 20,
                  (215, 230, 242), (W // 2, 150), "center")
        instructions = [
            "Antes de levar um aparelho, consulte o localizador e verifique os produtos aceitos,",
            "horários, limites de quantidade e condições de entrega do ponto escolhido.",
            "Separe eletroeletrônicos dos resíduos comuns e apague seus dados pessoais.",
            "Não abra, perfure, dobre ou tente desmontar baterias. Não viole o equipamento.",
        ]
        for i, line in enumerate(instructions):
            TEXT.draw(surf, line, 18, (224, 234, 246), (W // 2, 204 + i * 30), "center")
        for i, (_key, number, title, desc, _url) in enumerate(SOURCES):
            y = 358 + i * 84
            Ui.panel(surf, (180, y, 920, 68), border=(66, 136, 102) if i == 1 else (70, 110, 154))
            TEXT.draw(surf, number, 25, (255, 226, 126), (214, y + 34), "center", bold=True)
            TEXT.draw(surf, title, 20, (255, 255, 255), (260, y + 17), "topleft", bold=True)
            TEXT.draw(surf, desc, 16, (190, 210, 232), (260, y + 44), "topleft")
        TEXT.draw(surf, "As condições podem variar por município e por operador. Sempre confirme antes de sair.",
                  17, (255, 198, 132), (W // 2, 632), "center", max_w=900)
        TEXT.draw(surf, "Pressione 1 / 2 / 3 para abrir os sites oficiais · ESC para voltar", 18,
                  (150, 245, 176), (W // 2, 680), "center", bold=True)
