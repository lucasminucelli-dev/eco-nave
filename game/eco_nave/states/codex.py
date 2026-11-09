# -*- coding: utf-8 -*-
"""Enciclopédia ECO NAVE: fichas de resíduos, eletroeletrônicos e componentes (persistentes)."""
import pygame

from ..bins import BINS
from ..config import W
from ..drawing import rr
from ..icons import draw_icon
from ..items import ITEM_CATALOG
from ..text import TEXT
from ..ui import Ui
from ..workshop_catalog import COMPONENTS, EQUIPMENT_CATALOG, render_component, render_equipment
from .base import AttractState

GROUPS = [
    ("azul", "PAPEL E PAPELÃO"), ("vermelho", "PLÁSTICOS"), ("verde", "VIDROS"), ("amarelo", "METAIS"),
    ("preto", "MADEIRA"), ("marrom", "ORGÂNICOS"), ("cinza", "NÃO RECICLÁVEIS"), ("laranja", "PERIGOSOS"),
    ("branco", "RESÍDUOS DE SAÚDE"), ("roxo", "RADIOATIVOS"), ("equipment", "ELETROELETRÔNICOS"),
    ("components", "COMPONENTES"),
]
GROUP_COLORS = {"equipment": (70, 205, 175), "components": (255, 188, 118)}
GRID_COLS, CARD_W, CARD_H, CARD_GAP = 3, 132, 124, 10
DEST_TEXT = {"reuse": "Reutilização após testes funcionais.",
             "recovery": "Recuperação industrial de materiais, feita por operadores especializados.",
             "special": "Tratamento especializado: nunca vai para as lixeiras convencionais."}
LEFT_X, LEFT_W = 48, 240
GRID_X = 300
DET_X, DET_W = 730, 502
TOP, BOTTOM = 140, 692


class CodexState(AttractState):
    def __init__(self, game):
        super().__init__(game)
        self.group_index = 0
        self.selected = 0
        self.records = {}
        self._cache = {}
        self._build_records()

    def _build_records(self):
        grouped = {key: [] for key, _label in GROUPS}
        for idef in ITEM_CATALOG:
            grouped.setdefault(idef.category, []).append({"kind": "item", "data": idef, "id": idef.item_id})
        for equipment in EQUIPMENT_CATALOG:
            grouped["equipment"].append({"kind": "equipment", "data": equipment, "id": equipment.item_id})
        for component in COMPONENTS:
            grouped["components"].append({"kind": "component", "data": component, "id": component.item_id})
        self.records = {key: grouped.get(key, []) for key, _label in GROUPS}

    def enter(self, **kwargs):
        self.group_index = 0
        self.selected = 0

    @property
    def current_group(self):
        return GROUPS[self.group_index][0]

    @property
    def entries(self):
        return self.records.get(self.current_group, [])

    def _known(self, entry):
        return entry["id"] in self.game.progress_store.discovered_ids

    # ------------------------------------------------------------------ entrada
    def _set_group(self, delta):
        self.group_index = (self.group_index + delta) % len(GROUPS)
        self.selected = 0

    def handle_key(self, key):
        n = len(self.entries)
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.game.set_state("menu")
        elif key in (pygame.K_TAB, pygame.K_e, pygame.K_PAGEDOWN):
            self._set_group(1)
        elif key in (pygame.K_q, pygame.K_PAGEUP):
            self._set_group(-1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.selected = max(0, self.selected - 1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.selected = min(n - 1, self.selected + 1)
        elif key in (pygame.K_UP, pygame.K_w):
            self.selected = max(0, self.selected - GRID_COLS)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = min(n - 1, self.selected + GRID_COLS)

    # ------------------------------------------------------------------- dados
    def _sprite(self, entry, size):
        key = (entry["id"], size)
        spr = self._cache.get(key)
        if spr is None:
            data = entry["data"]
            if entry["kind"] == "item":
                spr = data.render(size)
            elif entry["kind"] == "equipment":
                spr = render_equipment(data, size)
            else:
                spr = render_component(data, size)
            self._cache[key] = spr
        return spr

    def _info(self, entry):
        """Normaliza os três tipos de ficha: nome, etiquetas e seções de texto."""
        d = entry["data"]
        if entry["kind"] == "item":
            if d.reverse_logistics:
                bin_chip = ("COLETA ESPECÍFICA", (255, 188, 118))
            else:
                b = BINS[d.bin_index]
                bin_chip = ("LIXEIRA " + b.name, b.color if sum(b.color) > 150 else (170, 170, 180))
            sections = [("O QUE FAZER", d.tip), ("DESTINAÇÃO", d.destination)]
            if d.fact and d.fact != d.tip:
                sections.append(("CURIOSIDADE", d.fact))
            sections.append(("REAPROVEITAMENTO", d.reuse))
        elif entry["kind"] == "equipment":
            bin_chip = ("NÃO VAI NAS 10 LIXEIRAS", (70, 205, 175))
            sections = [("O QUE É", d.description), ("DESTINAÇÃO", d.destination), ("CURIOSIDADE", d.note),
                        ("REAPROVEITAMENTO", "Avalie primeiro a possibilidade de conserto, doação ou recondicionamento.")]
        else:
            bin_chip = ("TRIAGEM ESPECIALIZADA", (255, 188, 118))
            sections = [("O QUE FAZER", d.description), ("DESTINAÇÃO", DEST_TEXT[d.destination_key]),
                        ("CURIOSIDADE", d.fact),
                        ("REAPROVEITAMENTO", "Depende de avaliação técnica e de compatibilidade.")]
        return d.name, bin_chip, sections

    # ------------------------------------------------------------------ desenho
    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (32, 24, 1216, 748), border=(80, 174, 220), bw=3)
        all_ids = {e["id"] for v in self.records.values() for e in v}
        known = len(game.progress_store.discovered_ids & all_ids)
        Ui.header(surf, "ENCICLOPÉDIA ECO NAVE", f"{known} de {len(all_ids)} fichas descobertas", (138, 220, 255),
                  (12, 30, 62), y=58, size=36)
        bw = 420
        rr(surf, (30, 44, 74), ((W - bw) // 2, 114, bw, 8), 4)
        if known:
            rr(surf, (110, 240, 150), ((W - bw) // 2, 114, max(8, int(bw * known / len(all_ids))), 8), 4)

        self._draw_groups(surf)
        self._draw_grid(surf)
        entries = self.entries
        if entries:
            self._draw_detail(surf, entries[self.selected])
        Ui.hint_bar(surf, [("SETAS", "escolher ficha"), ("Q / E", "categoria"), ("ESC", "menu")], 750, 15)

    def _draw_groups(self, surf):
        rr(surf, (10, 16, 32), (LEFT_X, TOP, LEFT_W, BOTTOM - TOP), 14, (60, 110, 154), 2)
        for i, (key, label) in enumerate(GROUPS):
            y = TOP + 10 + i * 45
            sel = i == self.group_index
            col = BINS[BINS.index_of(key)].color if key in {b.key for b in BINS} else GROUP_COLORS[key]
            if sel:
                rr(surf, (30, 76, 78), (LEFT_X + 6, y, LEFT_W - 12, 40), 9, (120, 232, 190), 2)
            rr(surf, col, (LEFT_X + 16, y + 9, 14, 22), 4, (230, 236, 248), 1)
            entries = self.records[key]
            got = sum(1 for e in entries if self._known(e))
            TEXT.draw(surf, label, 14, (255, 255, 255) if sel else (176, 194, 220), (LEFT_X + 40, y + 20), "midleft",
                      bold=sel, max_w=LEFT_W - 40 - 62)
            TEXT.draw(surf, f"{got}/{len(entries)}", 13, (130, 245, 160) if got == len(entries) else (150, 172, 200),
                      (LEFT_X + LEFT_W - 16, y + 20), "midright", bold=True)

    def _draw_grid(self, surf):
        entries = self.entries
        for i, entry in enumerate(entries):
            c, r = i % GRID_COLS, i // GRID_COLS
            x = GRID_X + c * (CARD_W + CARD_GAP)
            y = TOP + r * (CARD_H + CARD_GAP)
            known = self._known(entry)
            sel = i == self.selected
            rr(surf, (26, 78, 74) if sel else ((16, 28, 52) if known else (10, 14, 26)), (x, y, CARD_W, CARD_H), 12,
               (120, 245, 190) if sel else ((70, 110, 154) if known else (48, 60, 82)), 3 if sel else 1)
            if known:
                surf.blit(self._sprite(entry, 64), (x + (CARD_W - 64) // 2, y + 10))
                Ui.fit_block(surf, entry["data"].name, (x + 6, y + 80, CARD_W - 12, 38), (245, 250, 255), 14, 11,
                             bold=sel, align="center")
            else:
                draw_icon(surf, "lock", x + CARD_W // 2, y + 44, 34, (96, 112, 138))
                TEXT.draw(surf, "?????", 14, (110, 124, 148), (x + CARD_W // 2, y + 98), "center", bold=True)
        # legenda da categoria
        key = self.current_group
        ly = TOP + 3 * (CARD_H + CARD_GAP) + 6
        rr(surf, (12, 20, 38), (GRID_X, ly, 416, BOTTOM - ly), 12, (60, 110, 154), 1)
        if key in {b.key for b in BINS}:
            b = BINS[BINS.index_of(key)]
            rr(surf, b.color, (GRID_X + 14, ly + 14, 22, 32), 5, (230, 236, 248), 1)
            TEXT.draw(surf, "Lixeira " + b.name.title(), 16, (255, 255, 255), (GRID_X + 48, ly + 24), "midleft", bold=True)
            TEXT.draw(surf, b.material, 14, (190, 210, 232), (GRID_X + 48, ly + 44), "midleft", max_w=350)
            Ui.fit_block(surf, "Cores da coleta seletiva conforme a Resolução CONAMA 275/2001. "
                               "A aceitação pode variar de município para município.",
                         (GRID_X + 14, ly + 66, 388, BOTTOM - ly - 74), (160, 182, 210), 13, 11)
        else:
            Ui.fit_block(surf, "Aparelhos completos e suas peças não vão para as dez lixeiras: seguem para a "
                               "logística reversa de eletroeletrônicos. Descubra tudo na Oficina Circular.",
                         (GRID_X + 14, ly + 12, 388, BOTTOM - ly - 22), (200, 224, 240), 14, 11)

    def _draw_detail(self, surf, entry):
        rr(surf, (10, 16, 32), (DET_X, TOP, DET_W, BOTTOM - TOP), 14, (60, 110, 154), 2)
        cx = DET_X + DET_W // 2
        if not self._known(entry):
            draw_icon(surf, "lock", cx, TOP + 150, 90, (96, 112, 138))
            TEXT.draw(surf, "FICHA BLOQUEADA", 28, (160, 176, 200), (cx, TOP + 250), "center", bold=True)
            Ui.fit_block(surf, "Encontre este objeto durante uma partida ou na Oficina Circular para revelar a ficha.",
                         (DET_X + 50, TOP + 290, DET_W - 100, 90), (184, 202, 226), 18, 13, align="center")
            return
        name, (chip_text, chip_col), sections = self._info(entry)
        surf.blit(self._sprite(entry, 128), (cx - 64, TOP + 14))
        TEXT.draw(surf, name, 26, (255, 255, 255), (cx, TOP + 168), "center", bold=True, max_w=DET_W - 30)
        gl = GROUPS[self.group_index][1]
        w1 = TEXT.width(gl, 13, True) + 20
        w2 = TEXT.width(chip_text, 13, True) + 20
        x = cx - (w1 + w2 + 10) // 2
        Ui.chip(surf, gl, x, TOP + 190, (132, 224, 194), 13)
        Ui.chip(surf, chip_text, x + w1 + 10, TOP + 190, chip_col, 13, text_color=(240, 244, 252))
        y = TOP + 232
        avail = BOTTOM - 14 - y
        needs = [Ui.measure_block(t, DET_W - 44, 15) for _l, t in sections]
        extra = len(sections) * 24 + (len(sections) - 1) * 8
        scale = min(1.0, (avail - extra) / max(1, sum(needs)))
        for (label, text), need in zip(sections, needs):
            TEXT.draw(surf, label, 12, (138, 204, 255), (DET_X + 22, y), "topleft", bold=True)
            h = max(20, int(need * scale))
            bottom, _s = Ui.fit_block(surf, text, (DET_X + 22, y + 20, DET_W - 44, h), (222, 232, 246), 15, 11)
            y = bottom + 12
