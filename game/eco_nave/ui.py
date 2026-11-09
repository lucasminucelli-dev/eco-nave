# -*- coding: utf-8 -*-
"""Pecas de interface reutilizaveis (paineis e teclas desenhadas por formas)."""
import pygame

from .drawing import D
from .text import TEXT


class Ui:
    @staticmethod
    def panel(surf, rect, color=(8, 12, 30), alpha=215, border=None, radius=16, bw=2):
        rect = pygame.Rect(rect)
        p = pygame.Surface(rect.size, pygame.SRCALPHA)
        D.rect(p, (color[0], color[1], color[2], alpha), (0, 0, rect.w, rect.h), 0, border_radius=radius)
        if border is not None:
            D.rect(p, border, (0, 0, rect.w, rect.h), bw, border_radius=radius)
        surf.blit(p, rect.topleft)

    @staticmethod
    def keycap(surf, cx, cy, kind, size=34):
        """Tecla de seta desenhada por formas: kind = 'left' | 'right' | 'down'."""
        r = pygame.Rect(0, 0, size, size)
        r.center = (cx, cy)
        D.rect(surf, (28, 36, 64), r.move(0, 3), 0, border_radius=7)
        D.rect(surf, (226, 232, 246), r, 0, border_radius=7)
        D.rect(surf, (120, 132, 170), r, 2, border_radius=7)
        m = size * 0.24
        if kind == "left":
            pts = [(cx - m, cy), (cx + m * 0.8, cy - m), (cx + m * 0.8, cy + m)]
        elif kind == "right":
            pts = [(cx + m, cy), (cx - m * 0.8, cy - m), (cx - m * 0.8, cy + m)]
        else:
            pts = [(cx, cy + m), (cx - m, cy - m * 0.8), (cx + m, cy - m * 0.8)]
        D.polygon(surf, (40, 50, 86), pts)

    @staticmethod
    def keylabel(surf, label, x, y, size=16):
        """Tecla com texto (ENTER, R, ...). (x, y) = canto esquerdo/centro vertical. Devolve a largura."""
        t = TEXT.surface(label, size, (30, 38, 70), True)
        w = t.get_width() + 18
        r = pygame.Rect(x, y - 13, w, 26)
        D.rect(surf, (28, 36, 64), r.move(0, 2), 0, border_radius=6)
        D.rect(surf, (226, 232, 246), r, 0, border_radius=6)
        D.rect(surf, (120, 132, 170), r, 2, border_radius=6)
        surf.blit(t, t.get_rect(center=r.center))
        return w

    @staticmethod
    def keylabel_width(label, size=16):
        """Largura que 'keylabel' ocupa (para centralizar linhas de atalhos)."""
        return TEXT.surface(label, size, (30, 38, 70), True).get_width() + 18
