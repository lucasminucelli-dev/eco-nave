# -*- coding: utf-8 -*-
"""Elementos de interface durante a partida: placar, vidas, mensagem e aviso de nivel."""
import pygame

from .config import START_LIVES, W
from .drawing import D
from .text import TEXT
from .utils import clamp, fmt


class Hud:
    """Placar, combo, nivel, barra de progresso e coracoes de vida."""

    def draw(self, surf, assets, progress):
        TEXT.draw(surf, "PONTOS", 15, (150, 172, 214), (24, 8), "topleft", bold=True)
        sc = fmt(progress.score)
        TEXT.draw(surf, sc, 40, (255, 255, 255), (24, 22), "topleft", bold=True, shadow=(0, 0, 0))
        mult = progress.combo
        if mult > 1:
            w = TEXT.surface(sc, 40, (255, 255, 255), True).get_width()
            TEXT.draw(surf, f"COMBO x{mult}", 20, (255, 214, 80), (24 + w + 14, 40), "topleft",
                      bold=True, shadow=(0, 0, 0))
        TEXT.draw(surf, f"NÍVEL {progress.level}", 26, (255, 255, 255), (W - 24, 8), "topright", bold=True,
                  shadow=(0, 0, 0))
        bw = 118
        bx, by = W - 24 - bw, 44
        D.rect(surf, (40, 50, 84), (bx, by, bw, 9), 0, border_radius=4)
        prog = progress.level_progress
        if prog > 0:
            D.rect(surf, (110, 240, 150), (bx, by, int(bw * prog), 9), 0, border_radius=4)
        n = max(START_LIVES, progress.lives)
        hx = bx - 18 - n * 30
        for i in range(n):
            surf.blit(assets.heart_full if i < progress.lives else assets.heart_empty, (hx + i * 30, 10))


class MessageBox:
    """Caixa no topo com o resultado do ultimo lixo e a dica educativa."""
    WIDTH, HEIGHT = 620, 58

    def __init__(self):
        self.clear()

    def clear(self):
        self.title = self.tip = self.kind = None
        self.t = 0.0

    @property
    def visible(self):
        return self.title is not None

    def show(self, title, tip, kind, duration):
        """kind: 'ok' (verde) ou 'bad' (vermelho)."""
        self.title, self.tip, self.kind, self.t = title, tip, kind, duration

    def update(self, dt):
        if self.visible:
            self.t -= dt
            if self.t <= 0:
                self.clear()

    def draw(self, surf):
        if not self.visible:
            return
        alpha = 1.0 if self.t > 0.5 else max(0.0, self.t / 0.5)
        col = (130, 245, 160) if self.kind == "ok" else (255, 130, 130)
        pw, ph = self.WIDTH, self.HEIGHT
        pill = pygame.Surface((pw, ph), pygame.SRCALPHA)
        D.rect(pill, (8, 12, 30, 220), (0, 0, pw, ph), 0, border_radius=14)
        D.rect(pill, col, (0, 0, pw, ph), 2, border_radius=14)
        TEXT.draw(pill, self.title, 20, col, (pw // 2, 18), "center", bold=True, max_w=pw - 30)
        TEXT.draw(pill, self.tip, 16, (222, 230, 246), (pw // 2, 41), "center", max_w=pw - 24)
        pill.set_alpha(int(255 * alpha))
        surf.blit(pill, ((W - pw) // 2, 6))


class LevelBanner:
    """Letreiro grande 'NIVEL N' que aparece ao subir de nivel."""
    DURATION = 1.8

    def __init__(self):
        self.clear()

    def clear(self):
        self.text = self.sub = None
        self.t = 0.0

    @property
    def visible(self):
        return self.text is not None

    def show(self, text, sub):
        self.text, self.sub, self.t = text, sub, self.DURATION

    def update(self, dt):
        if self.visible:
            self.t -= dt
            if self.t <= 0:
                self.clear()

    def draw(self, surf):
        if not self.visible:
            return
        p = clamp(self.t / self.DURATION, 0.0, 1.0)
        al = 255 * min(1.0, p * 3.0)
        y = 290 - (1 - p) * 30
        TEXT.draw(surf, self.text, 84, (255, 236, 110), (W // 2, y), "center", bold=True,
                  outline=(20, 16, 40), alpha=al)
        TEXT.draw(surf, self.sub, 28, (255, 255, 255), (W // 2, y + 58), "center", bold=True,
                  outline=(20, 16, 40), alpha=al)
