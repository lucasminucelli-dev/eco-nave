# -*- coding: utf-8 -*-
"""Itens da lixeira MARROM (organicos)."""
import math

from ..drawing import D, blob, rr
from .catalog import item


@item("marrom", "Casca de banana", "Restos de comida viram adubo na compostagem.")
def _(s):
    Y, YO = (246, 212, 62), (190, 146, 22)
    px, py, ry = 64, 22, 46
    for ang in (-42, 42, 0):
        a = math.radians(ang)
        pts = blob(px + math.sin(a) * ry, py + math.cos(a) * ry, 13, ry, ang)
        D.polygon(s, Y, pts)
        D.polygon(s, YO, pts, 3)
        D.line(s, (150, 100, 30), (px + math.sin(a) * ry * 1.7, py + math.cos(a) * ry * 1.7),
               (px + math.sin(a) * ry * 1.85, py + math.cos(a) * ry * 1.85), 5)
    rr(s, (110, 74, 30), (57, 8, 14, 24), 4)
    for (x, y) in ((50, 70), (80, 66), (64, 92), (66, 60)):
        D.circle(s, (170, 120, 40), (x, y), 3)


@item("marrom", "Miolo de maçã", "Orgânicos podem virar adubo. Menos lixo no aterro, mais vida no solo!")
def _(s):
    core = [(44, 24), (84, 24), (70, 64), (84, 104), (44, 104), (58, 64)]
    D.polygon(s, (246, 238, 192), core)
    D.polygon(s, (204, 182, 120), core, 3)
    D.ellipse(s, (212, 52, 52), (34, 12, 60, 32))
    D.ellipse(s, (212, 52, 52), (34, 86, 60, 32))
    D.ellipse(s, (150, 30, 34), (34, 12, 60, 32), 3)
    D.ellipse(s, (150, 30, 34), (34, 86, 60, 32), 3)
    D.ellipse(s, (96, 56, 30), (57, 52, 7, 13))
    D.ellipse(s, (96, 56, 30), (66, 56, 7, 13))
    D.line(s, (96, 66, 34), (64, 14), (72, 2), 4)


@item("marrom", "Folhas", "Folhas e restos de poda são ótimos para a compostagem.")
def _(s):
    def leaf(cx, cy, rx, ry, ang, col, out):
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        left, right = [], []
        for i in range(21):
            t = -1 + i * 0.1
            half = rx * (1 - t * t) ** 0.7
            u, v = half, t * ry
            left.append((cx + u * ca + v * sa, cy - u * sa + v * ca))
            u = -half
            right.append((cx + u * ca + v * sa, cy - u * sa + v * ca))
        pts = left + right[::-1]
        D.polygon(s, col, pts)
        D.polygon(s, out, pts, 3)
        D.line(s, out, (cx - math.sin(a) * ry, cy - math.cos(a) * ry),
               (cx + math.sin(a) * ry * 1.25, cy + math.cos(a) * ry * 1.25), 3)
    leaf(46, 62, 24, 46, 32, (96, 178, 72), (52, 116, 46))
    leaf(84, 64, 22, 40, -38, (196, 150, 60), (128, 86, 30))


@item("marrom", "Casca de ovo", "Cascas de ovo são ricas em cálcio e ótimas para a compostagem.")
def _(s):
    D.ellipse(s, (246, 240, 224), (26, 22, 76, 92))
    D.ellipse(s, (196, 184, 156), (26, 22, 76, 92), 3)
    zig = [(130, 56)]
    x = 118
    i = 0
    while x > -6:
        zig.append((x, 54 + (10 if i % 2 else -8)))
        x -= 12
        i += 1
    D.polygon(s, (0, 0, 0, 0), [(0, 0), (130, 0)] + zig + [(-2, 56)])
    D.lines(s, (196, 184, 156), False, zig[1:], 3)
