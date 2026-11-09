# -*- coding: utf-8 -*-
"""Tela inicial (hub): de aqui o jogador vai para o jogo e para todas as outras telas."""
import math

import pygame

from ..config import VERSION, W
from ..drawing import rr
from ..icons import draw_icon
from ..items import ITEM_CATALOG
from ..text import TEXT
from ..ui import Ui
from ..utils import mix, shade
from ..workshop_catalog import COMPONENTS, EQUIPMENT_CATALOG
from .base import AttractState

CX = W // 2
CARD_X = CX - 308          # o bloco de cartoes tem 616 px de largura e fica centralizado
COL_W, GAP = 300, 16


class HubItem:
    """Um cartao do menu."""

    def __init__(self, action, title, subtitle, hotkey, color, icon, rect):
        self.action = action
        self.title = title
        self.subtitle = subtitle
        self.hotkey = hotkey
        self.color = color
        self.icon = icon
        self.rect = pygame.Rect(rect)


# Posicao de cada cartao na grade (linha, coluna). 'play' ocupa as duas colunas da linha 0.
GRID = [["play", "play"], ["workshop", "codex"], ["ranking", "real"], ["help", "audio"]]


def _build_items():
    row_y = {0: 268, 1: 356, 2: 436, 3: 516}
    row_h = {0: 74, 1: 68, 2: 68, 3: 46}
    xs = (CARD_X, CARD_X + COL_W + GAP)
    spec = {
        "play": ("JOGAR", "Separe cada resíduo na lixeira certa", "ENTER", (112, 244, 158), "play"),
        "workshop": ("OFICINA CIRCULAR", "Avalie e reaproveite eletrônicos", "O", (70, 205, 175), "gear"),
        "codex": ("ENCICLOPÉDIA", "", "C", (96, 172, 240), "book"),
        "ranking": ("RANKING", "Os 10 melhores jogadores", "R", (190, 140, 240), "trophy"),
        "real": ("DESCARTE REAL", "Onde levar seus eletrônicos", "G", (130, 210, 110), "pin"),
        "help": ("COMO JOGAR", "Controles e regras", "H", (236, 200, 110), "help"),
        "audio": ("ÁUDIO", "Música e efeitos", "V", (150, 190, 230), "speaker"),
    }
    items = {}
    for r, row in enumerate(GRID):
        for c, action in enumerate(row):
            if action in items:
                continue
            title, sub, key, color, icon = spec[action]
            if action == "play":
                rect = (CARD_X, row_y[0], 2 * COL_W + GAP, row_h[0])
            else:
                rect = (xs[c], row_y[r], COL_W, row_h[r])
            items[action] = HubItem(action, title, sub, key, color, icon, rect)
    return items


class MenuState(AttractState):
    """Hub de navegação. Setas/WASD movem a seleção, ENTER abre, atalhos de letra abrem direto."""

    HOTKEYS = {pygame.K_o: "workshop", pygame.K_c: "codex", pygame.K_r: "ranking",
               pygame.K_g: "real", pygame.K_h: "help"}

    def __init__(self, game):
        super().__init__(game)
        self.items = _build_items()
        self.row, self.col = 0, 0
        self.confirm_quit = False

    # ------------------------------------------------------------ navegação
    @property
    def selected(self):
        return GRID[self.row][self.col]

    def _select(self, action):
        for r, row in enumerate(GRID):
            if action in row:
                self.row, self.col = r, row.index(action) if row[self.col] != action else self.col
                return

    def _move(self, dx, dy):
        self.row = (self.row + dy) % len(GRID)
        self.col = (self.col + dx) % 2

    def enter(self, **kwargs):
        self.game.ship.beam_t = 0.0
        self.confirm_quit = False

    def activate(self, action):
        game = self.game
        game.snd.play("select")
        if action == "play":
            game.start_game()
        elif action == "ranking":
            game.set_state("ranking", new_entry=None, note="")
        elif action == "real":
            game.set_state("real_world")
        elif action == "audio":
            game.audio_panel.open()
        else:
            game.set_state(action)

    def handle_key(self, key):
        if self.confirm_quit:
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_y):
                self.game.running = False
            elif key in (pygame.K_ESCAPE, pygame.K_n):
                self.confirm_quit = False
            return
        if key in (pygame.K_LEFT, pygame.K_a):
            self._move(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self._move(1, 0)
        elif key in (pygame.K_UP, pygame.K_w):
            self._move(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self._move(0, 1)
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.activate(self.selected)
        elif key in self.HOTKEYS:
            self.activate(self.HOTKEYS[key])
        elif key == pygame.K_ESCAPE:
            self.confirm_quit = True

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEMOTION and not self.confirm_quit:
            hit = self._item_at(ev.pos)
            if hit:
                self._select(hit)
        elif ev.type == pygame.MOUSEBUTTONDOWN and getattr(ev, "button", 1) == 1 and not self.confirm_quit:
            hit = self._item_at(ev.pos)
            if hit:
                self._select(hit)
                self.activate(hit)
        else:
            super().handle_event(ev)

    def _item_at(self, pos):
        for action, item in self.items.items():
            if item.rect.collidepoint(pos):
                return action
        return None

    # ------------------------------------------------------------- desenho
    def _codex_subtitle(self):
        ids = self.game.progress_store.discovered_ids
        total = len(ITEM_CATALOG) + len(EQUIPMENT_CATALOG) + len(COMPONENTS)
        known = len(ids & (ITEM_CATALOG.ids() | {e.item_id for e in EQUIPMENT_CATALOG} |
                           {c.item_id for c in COMPONENTS}))
        return f"{known} de {total} fichas descobertas"

    def _draw_card(self, surf, item, selected, t):
        r = item.rect
        col = item.color
        big = item.action == "play"
        if selected:
            pulse = 0.5 + 0.5 * math.sin(t * 5)
            glow = pygame.Surface((r.w + 24, r.h + 24), pygame.SRCALPHA)
            rr(glow, (col[0], col[1], col[2], int(40 + 40 * pulse)), (0, 0, r.w + 24, r.h + 24), 22)
            surf.blit(glow, (r.x - 12, r.y - 12))
        Ui.panel(surf, r, color=mix((10, 16, 34), col, 0.22 if selected else 0.06), alpha=240,
                 border=col if selected else shade(col, 0.55), radius=16, bw=3 if selected else 2)
        ir = r.h * 0.33
        icx, icy = r.x + 14 + ir, r.centery
        rr(surf, mix((10, 16, 34), col, 0.35), (int(icx - ir), int(icy - ir), int(ir * 2), int(ir * 2)),
           int(ir), shade(col, 0.8), 2)
        draw_icon(surf, item.icon, icx, icy, ir * 1.15, col, bg=mix((10, 16, 34), col, 0.35))
        kw = Ui.keylabel_width(item.hotkey, 15 if not big else 17)
        text_x = int(icx + ir + 14)
        max_w = r.right - kw - 26 - text_x
        sub = item.subtitle or self._codex_subtitle()
        TEXT.draw(surf, item.title, 26 if big else 19, (255, 255, 255), (text_x, r.centery - (11 if r.h > 60 else 0)),
                  "midleft", bold=True, max_w=max_w)
        if r.h > 60:
            TEXT.draw(surf, sub, 15 if big else 14, (186, 206, 228), (text_x, r.centery + 15), "midleft", max_w=max_w)
        Ui.keylabel(surf, item.hotkey, r.right - kw - 12, r.centery, 15 if not big else 17)

    def draw(self, surf):
        game = self.game
        t = game.t
        self.draw_backdrop(surf)
        ship = game.ship
        ship.draw(surf, game.assets, t, 62 + math.sin(ship.bob * 2.4) * 4, with_beam=False)

        # título
        tr = TEXT.draw(surf, "ECO NAVE", 84, (112, 244, 158), (CX, 166), "center", bold=True, outline=(8, 40, 30))
        Ui.chip(surf, VERSION, tr.right + 12, tr.top + 12, (255, 226, 126), 15)
        TEXT.draw(surf, "Desafio do Descarte Consciente", 26, (226, 236, 255), (CX, 228), "center", bold=True,
                  shadow=(0, 0, 0))

        sel = self.selected
        for action, item in self.items.items():
            if action != sel:
                self._draw_card(surf, item, False, t)
        self._draw_card(surf, self.items[sel], True, t)

        state = "mudo" if game.audio.muted else "ativo"
        Ui.hint_bar(surf, [("M", "áudio " + state), ("V", "volume"), ("F11", "tela cheia"), ("ESC", "sair")],
                    590, 14)
        game.session.bins.draw(surf, game.assets, t, None)

        if self.confirm_quit:
            surf.blit(game.assets.dim, (0, 0))
            Ui.panel(surf, (CX - 270, 290, 540, 190), alpha=252, border=(255, 190, 100), bw=3)
            TEXT.draw(surf, "SAIR DO JOGO?", 38, (255, 220, 150), (CX, 340), "center", bold=True)
            TEXT.draw(surf, "Seu ranking e suas descobertas já estão salvos.", 17, (214, 224, 244), (CX, 384),
                      "center")
            Ui.hint_bar(surf, [("ENTER", "sair"), ("ESC", "continuar")], 436, 17)
