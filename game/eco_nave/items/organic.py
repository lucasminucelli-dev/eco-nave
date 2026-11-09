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


@item("marrom", "Borra de café", "A borra de café pode ser compostada em quantidades equilibradas e misturada a outros materiais secos.")
def _(s):
    rr(s, (104, 70, 44), (18, 32, 92, 72), 12, (62, 40, 28), 4)
    D.ellipse(s, (70, 44, 30), (24, 24, 80, 30))
    D.ellipse(s, (164, 116, 72), (31, 30, 66, 18))
    for x, y in ((44, 63), (66, 76), (88, 58), (72, 91)):
        D.circle(s, (58, 36, 24), (x, y), 4)
    D.arc(s, (222, 192, 142), (18, 32, 92, 72), 0, 3.14, 3)


@item("marrom", "Cascas de legumes", "Cascas de legumes sem contaminação podem ser destinadas à compostagem doméstica ou comunitária.")
def _(s):
    D.polygon(s, (226, 166, 62), [(20, 90), (34, 40), (62, 28), (78, 66), (54, 108)])
    D.polygon(s, (84, 162, 72), [(56, 90), (70, 28), (98, 18), (112, 64), (84, 104)])
    D.polygon(s, (176, 114, 48), [(20, 90), (34, 40), (62, 28), (78, 66), (54, 108)], 3)
    D.polygon(s, (54, 120, 52), [(56, 90), (70, 28), (98, 18), (112, 64), (84, 104)], 3)
    D.line(s, (240, 206, 110), (34, 48), (56, 88), 3)


@item("marrom", "Restos de vegetais", "Restos vegetais crus podem virar composto; evite incluir materiais que atraiam vetores e siga as orientações da composteira.")
def _(s):
    D.ellipse(s, (76, 142, 66), (18, 52, 56, 54))
    D.ellipse(s, (116, 176, 84), (48, 32, 64, 64))
    D.ellipse(s, (54, 116, 52), (18, 52, 56, 54), 3)
    D.ellipse(s, (76, 138, 62), (48, 32, 64, 64), 3)
    D.line(s, (222, 236, 138), (54, 58), (54, 94), 3)
    D.line(s, (202, 228, 136), (80, 46), (80, 82), 3)
