# -*- coding: utf-8 -*-
"""Enciclopédia persistente de resíduos, eletroeletrônicos e componentes."""
import pygame

from ..bins import BINS
from ..config import W
from ..drawing import D, rr
from ..items import ITEM_CATALOG
from ..text import TEXT
from ..ui import Ui
from ..workshop_catalog import COMPONENTS, EQUIPMENT_CATALOG, render_component, render_equipment
from .base import AttractState


GROUPS = [
    ("azul", "PAPEL E PAPELÃO"),
    ("vermelho", "PLÁSTICOS"),
    ("verde", "VIDROS"),
    ("amarelo", "METAIS"),
    ("preto", "MADEIRA"),
    ("marrom", "ORGÂNICOS"),
    ("cinza", "NÃO RECICLÁVEIS"),
    ("laranja", "PERIGOSOS"),
    ("branco", "RESÍDUOS DE SAÚDE"),
    ("roxo", "RADIOATIVOS"),
    ("equipment", "ELETROELETRÔNICOS"),
    ("components", "COMPONENTES"),
]


class CodexState(AttractState):
    def __init__(self, game):
        super().__init__(game)
        self.group_index = 0
        self.selected = 0
        self.records = {}
        self._build_records()

    def _build_records(self):
        grouped = {key: [] for key, _label in GROUPS}
        for idef in ITEM_CATALOG:
            grouped.setdefault(idef.category, []).append({"kind": "item", "data": idef, "id": idef.item_id})
        for equipment in EQUIPMENT_CATALOG:
            grouped["equipment"].append({"kind": "equipment", "data": equipment, "id": equipment.item_id})
        for component in COMPONENTS:
            grouped["components"].append({"kind": "component", "data": component, "id": component.item_id})
        for key, _label in GROUPS:
            self.records[key] = grouped.get(key, [])

    def enter(self, **kwargs):
        self.group_index = 0
        self.selected = 0

    @property
    def current_group(self):
        return GROUPS[self.group_index][0]

    @property
    def entries(self):
        return self.records.get(self.current_group, [])

    def handle_key(self, key):
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.game.set_state("menu")
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.group_index = (self.group_index - 1) % len(GROUPS)
            self.selected = 0
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.group_index = (self.group_index + 1) % len(GROUPS)
            self.selected = 0
        elif key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % max(1, len(self.entries))
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % max(1, len(self.entries))

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (45, 32, 1190, 736), border=(80, 174, 220), bw=3)
        TEXT.draw(surf, "ENCICLOPÉDIA ECO NAVE", 43, (138, 220, 255), (W // 2, 72), "center", bold=True,
                  outline=(12, 30, 62))
        total = sum(len(v) for v in self.records.values())
        unlocked = len(game.progress_store.discovered_ids.intersection(
            {entry["id"] for values in self.records.values() for entry in values}))
        TEXT.draw(surf, f"{unlocked} / {total} fichas descobertas", 17, (186, 220, 236),
                  (W // 2, 111), "center")

        # Navegação de categorias; a categoria atual fica visualmente destacada.
        group_label = GROUPS[self.group_index][1]
        TEXT.draw(surf, "‹", 40, (135, 220, 255), (90, 158), "center", bold=True)
        TEXT.draw(surf, group_label, 24, (255, 226, 126), (W // 2, 158), "center", bold=True)
        TEXT.draw(surf, "›", 40, (135, 220, 255), (1190, 158), "center", bold=True)

        Ui.panel(surf, (78, 198, 350, 505), border=(60, 110, 154))
        Ui.panel(surf, (452, 198, 750, 505), border=(60, 110, 154))
        entries = self.entries
        if not entries:
            TEXT.draw(surf, "Nenhum item nesta categoria.", 21, (200, 216, 236),
                      (253, 440), "center")
            return

        row_h = 70 if len(entries) <= 6 else 56
        start_y = 226
        for i, entry in enumerate(entries):
            y = start_y + i * row_h
            is_selected = i == self.selected
            is_unlocked = entry["id"] in game.progress_store.discovered_ids
            if is_selected:
                rr(surf, (30, 76, 78), (96, y, 314, row_h - 7), 9, (120, 232, 190), 2)
            elif i % 2 == 0:
                rr(surf, (15, 27, 48), (96, y, 314, row_h - 7), 8)
            number = "OK" if is_unlocked else "??"
            name = entry["data"].name if is_unlocked else "????????"
            TEXT.draw(surf, number, 19, (120, 240, 168) if is_unlocked else (144, 154, 174),
                      (113, y + (row_h - 7) // 2), "center", bold=True)
            TEXT.draw(surf, name, 17, (245, 250, 255) if is_unlocked else (120, 132, 154),
                      (139, y + (row_h - 7) // 2), "midleft", bold=is_selected, max_w=255)

        self._draw_record(surf, entries[self.selected])
        TEXT.draw(surf, "A/D ou ←/→ categoria · W/S ou ↑/↓ item · ESC menu", 16,
                  (166, 188, 216), (W // 2, 722), "center")

    def _draw_record(self, surf, entry):
        game = self.game
        data = entry["data"]
        unlocked = entry["id"] in game.progress_store.discovered_ids
        if not unlocked:
            TEXT.draw(surf, "FICHA BLOQUEADA", 27, (146, 162, 188), (827, 254), "center", bold=True)
            TEXT.draw(surf, "????????", 35, (220, 228, 242), (827, 320), "center", bold=True)
            TEXT.draw(surf, "Encontre este objeto durante uma partida ou na Oficina Circular para revelar sua ficha.",
                      20, (184, 202, 226), (827, 408), "center", max_w=620)
            D.circle(surf, (72, 88, 112), (827, 520), 45, 3)
            TEXT.draw(surf, "?", 58, (112, 140, 172), (827, 518), "center", bold=True)
            return

        TEXT.draw(surf, data.name, 29, (255, 255, 255), (827, 238), "center", bold=True, max_w=660)
        if entry["kind"] == "item":
            surf.blit(game.assets.sprite_for(data), (762, 270))
            category = data.category.upper()
            bin_text = ("Coleta específica / logística reversa" if data.reverse_logistics else
                        ("Lixeira " + BINS[data.bin_index].name if data.bin_index is not None else "Sem lixeira convencional"))
            destination = data.destination
            description = data.tip
            fact = data.fact
            reuse = data.reuse
        elif entry["kind"] == "equipment":
            surf.blit(render_equipment(data, 150), (752, 268))
            category = "ELETROELETRÔNICO"
            bin_text = "Não utilizar as dez lixeiras tradicionais"
            destination = data.destination
            description = data.description
            fact = data.note
            reuse = "Avalie primeiro a possibilidade de conserto, doação ou recondicionamento."
        else:
            surf.blit(render_component(data, 150), (752, 268))
            category = "COMPONENTE DE ELETROELETRÔNICO"
            bin_text = "Triagem por operador especializado"
            destination = {"reuse": "Reutilização após testes", "recovery": "Recuperação industrial de materiais",
                           "special": "Tratamento especializado"}[data.destination_key]
            description = data.description
            fact = data.fact
            reuse = "O reaproveitamento depende de avaliação técnica e compatibilidade."

        x = 932
        TEXT.draw(surf, category, 16, (132, 224, 194), (x, 290), "topleft", bold=True, max_w=260)
        TEXT.draw(surf, bin_text, 16, (255, 218, 130), (x, 320), "topleft", bold=True, max_w=260)
        lines = TEXT.wrap(description, 17, 650)
        TEXT.draw(surf, "INFORMAÇÃO", 15, (138, 204, 255), (500, 450), "topleft", bold=True)
        for i, line in enumerate(lines[:3]):
            TEXT.draw(surf, line, 17, (220, 230, 244), (500, 476 + i * 23), "topleft")
        TEXT.draw(surf, "DESTINAÇÃO", 15, (138, 204, 255), (500, 554), "topleft", bold=True)
        for i, line in enumerate(TEXT.wrap(destination, 16, 650)[:2]):
            TEXT.draw(surf, line, 16, (220, 230, 244), (500, 578 + i * 21), "topleft")
        TEXT.draw(surf, "CURIOSIDADE / REAPROVEITAMENTO", 14, (132, 224, 194), (500, 635), "topleft", bold=True)
        for i, line in enumerate(TEXT.wrap(fact + " " + reuse, 14, 650)[:2]):
            TEXT.draw(surf, line, 14, (198, 216, 232), (500, 655 + i * 18), "topleft")
