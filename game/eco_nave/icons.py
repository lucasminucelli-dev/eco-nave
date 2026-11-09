# -*- coding: utf-8 -*-
"""Icones simples desenhados por formas (nenhuma imagem externa).

Todos usam o mesmo contrato: draw_icon(surf, nome, cx, cy, tamanho, cor).
Assim a informacao nunca depende so da cor: cada opcao tem um simbolo proprio.
"""
import math

from .drawing import D, draw_recycle
from .text import TEXT


def _arc(cx, cy, r, a0, a1, n=18):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _gear(surf, cx, cy, r, color, bg):
    pts = []
    for i in range(8):
        a = i * math.pi / 4
        for da, rad in ((-0.2, r * 0.78), (-0.13, r), (0.13, r), (0.2, r * 0.78)):
            pts.append((cx + rad * math.cos(a + da), cy + rad * math.sin(a + da)))
    D.polygon(surf, color, pts)
    D.circle(surf, bg, (int(cx), int(cy)), max(2, int(r * 0.32)))


def draw_icon(surf, name, cx, cy, size, color, bg=(10, 16, 32)):
    s = size / 2.0
    w = max(2, int(size * 0.11))
    if name == "play":
        D.polygon(surf, color, [(cx - s * 0.5, cy - s * 0.7), (cx - s * 0.5, cy + s * 0.7), (cx + s * 0.75, cy)])
    elif name == "gear":
        _gear(surf, cx, cy, s * 0.9, color, bg)
    elif name == "book":
        D.polygon(surf, color, [(cx - s * 0.9, cy - s * 0.6), (cx - s * 0.05, cy - s * 0.4),
                                (cx - s * 0.05, cy + s * 0.75), (cx - s * 0.9, cy + s * 0.55)])
        D.polygon(surf, color, [(cx + s * 0.9, cy - s * 0.6), (cx + s * 0.05, cy - s * 0.4),
                                (cx + s * 0.05, cy + s * 0.75), (cx + s * 0.9, cy + s * 0.55)])
        D.line(surf, bg, (cx - s * 0.5, cy - s * 0.2), (cx - s * 0.2, cy - s * 0.15), 2)
        D.line(surf, bg, (cx + s * 0.5, cy - s * 0.2), (cx + s * 0.2, cy - s * 0.15), 2)
    elif name == "trophy":
        D.polygon(surf, color, [(cx - s * 0.55, cy - s * 0.8), (cx + s * 0.55, cy - s * 0.8),
                                (cx + s * 0.4, cy + s * 0.1), (cx - s * 0.4, cy + s * 0.1)])
        D.lines(surf, color, False, _arc(cx - s * 0.55, cy - s * 0.4, s * 0.35, 90, 270), w)
        D.lines(surf, color, False, _arc(cx + s * 0.55, cy - s * 0.4, s * 0.35, 90, -90), w)
        D.rect(surf, color, (cx - s * 0.12, cy + s * 0.1, s * 0.24, s * 0.45))
        D.rect(surf, color, (cx - s * 0.5, cy + s * 0.55, s * 1.0, s * 0.25), 0, border_radius=3)
    elif name == "pin":
        D.circle(surf, color, (int(cx), int(cy - s * 0.2)), int(s * 0.62))
        D.polygon(surf, color, [(cx - s * 0.5, cy + s * 0.1), (cx + s * 0.5, cy + s * 0.1), (cx, cy + s * 0.95)])
        D.circle(surf, bg, (int(cx), int(cy - s * 0.2)), max(2, int(s * 0.25)))
    elif name == "help":
        D.circle(surf, color, (int(cx), int(cy)), int(s * 0.9), w)
        TEXT.draw(surf, "?", max(10, int(size * 0.7)), color, (cx, cy + 1), "center", bold=True)
    elif name == "speaker":
        D.polygon(surf, color, [(cx - s * 0.8, cy - s * 0.3), (cx - s * 0.35, cy - s * 0.3), (cx + s * 0.15, cy - s * 0.75),
                                (cx + s * 0.15, cy + s * 0.75), (cx - s * 0.35, cy + s * 0.3), (cx - s * 0.8, cy + s * 0.3)])
        D.lines(surf, color, False, _arc(cx + s * 0.1, cy, s * 0.5, -50, 50), w)
        D.lines(surf, color, False, _arc(cx + s * 0.1, cy, s * 0.85, -50, 50), w)
    elif name == "recycle":
        draw_recycle(surf, int(cx), int(cy), s * 0.72, color, max(2.0, size * 0.1))
    elif name == "reuse":      # seta circular: voltar ao uso
        D.lines(surf, color, False, _arc(cx, cy, s * 0.7, 40, 330), w)
        ex, ey = cx + s * 0.7 * math.cos(math.radians(40)), cy - s * 0.7 * math.sin(math.radians(40))
        D.polygon(surf, color, [(ex - s * 0.4, ey - s * 0.12), (ex + s * 0.45, ey - s * 0.1), (ex + s * 0.15, ey + s * 0.45)])
    elif name == "wrench":
        D.line(surf, color, (cx - s * 0.7, cy + s * 0.7), (cx + s * 0.25, cy - s * 0.25), max(3, int(size * 0.17)))
        D.circle(surf, color, (int(cx + s * 0.4), int(cy - s * 0.4)), int(s * 0.48))
        D.polygon(surf, bg, [(cx + s * 0.4, cy - s * 0.4), (cx + s * 0.95, cy - s * 0.95), (cx + s * 0.95, cy - s * 0.2)])
    elif name == "shield":
        D.polygon(surf, color, [(cx - s * 0.7, cy - s * 0.75), (cx + s * 0.7, cy - s * 0.75), (cx + s * 0.7, cy + s * 0.1),
                                (cx, cy + s * 0.95), (cx - s * 0.7, cy + s * 0.1)])
        D.line(surf, bg, (cx, cy - s * 0.45), (cx, cy + s * 0.1), w)
        D.circle(surf, bg, (int(cx), int(cy + s * 0.38)), max(2, w // 2 + 1))
    elif name == "check":
        D.lines(surf, color, False, [(cx - s * 0.7, cy), (cx - s * 0.2, cy + s * 0.55), (cx + s * 0.75, cy - s * 0.55)], w + 1)
    elif name == "cross":
        D.line(surf, color, (cx - s * 0.6, cy - s * 0.6), (cx + s * 0.6, cy + s * 0.6), w + 1)
        D.line(surf, color, (cx - s * 0.6, cy + s * 0.6), (cx + s * 0.6, cy - s * 0.6), w + 1)
    elif name == "lock":
        D.rect(surf, color, (cx - s * 0.6, cy - s * 0.05, s * 1.2, s * 0.9), 0, border_radius=3)
        D.lines(surf, color, False, _arc(cx, cy - s * 0.05, s * 0.4, 0, 180), w)
        D.circle(surf, bg, (int(cx), int(cy + s * 0.4)), max(2, int(s * 0.14)))
    elif name == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rad = s * (0.95 if i % 2 == 0 else 0.4)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
        D.polygon(surf, color, pts)
    else:
        D.circle(surf, color, (int(cx), int(cy)), int(s * 0.8), w)
