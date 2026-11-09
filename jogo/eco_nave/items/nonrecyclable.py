# -*- coding: utf-8 -*-
"""Itens da lixeira CINZA (nao reciclaveis)."""
import math
import random

from ..drawing import D, rr
from .catalog import item


@item("cinza", "Guardanapo sujo", "Papel sujo de gordura ou comida não é reciclável. Vai no lixo comum.")
def _(s):
    rnd = random.Random(7)
    pts = []
    for i in range(15):
        a = 2 * math.pi * i / 15
        r = 40 + rnd.randint(-9, 5)
        pts.append((64 + r * math.cos(a), 64 + r * math.sin(a)))
    D.polygon(s, (230, 230, 224), pts)
    D.polygon(s, (150, 150, 146), pts, 3)
    for _i in range(6):
        p1 = (64 + rnd.randint(-28, 28), 64 + rnd.randint(-28, 28))
        p2 = (p1[0] + rnd.randint(-22, 22), p1[1] + rnd.randint(-22, 22))
        D.line(s, (176, 176, 170), p1, p2, 2)
    D.circle(s, (214, 176, 112), (80, 50), 10)
    D.circle(s, (196, 150, 84), (80, 50), 10, 2)
    D.circle(s, (214, 176, 112), (50, 82), 6)


@item("cinza", "Chiclete mascado", "Chiclete não é reciclável: embrulhe em papel e jogue no lixo comum.")
def _(s):
    P = (240, 142, 188)
    blobs = ((58, 68, 34), (86, 58, 24), (44, 92, 20))
    for (x, y, r) in blobs:
        D.circle(s, (176, 84, 128), (x, y), r + 3)
    D.line(s, (176, 84, 128), (100, 78), (120, 102), 9)
    D.line(s, P, (100, 78), (120, 102), 5)
    for (x, y, r) in blobs:
        D.circle(s, P, (x, y), r)
    D.circle(s, (255, 214, 232), (48, 54), 9)
    D.circle(s, (255, 214, 232), (80, 50), 5)


@item("cinza", "Esponja de cozinha", "Esponjas de cozinha são feitas de materiais misturados e não recicláveis.")
def _(s):
    rr(s, (238, 208, 52), (16, 30, 96, 46), 8, (170, 140, 20))
    rr(s, (72, 152, 82), (16, 72, 96, 28), 8, (40, 100, 50))
    for (x, y) in ((32, 44), (56, 54), (84, 42), (98, 58), (44, 64), (72, 66)):
        D.circle(s, (204, 172, 30), (x, y), 4)
    for x in range(26, 104, 10):
        D.line(s, (100, 180, 108), (x, 80), (x + 5, 94), 2)


@item("cinza", "Fita adesiva", "Fita adesiva mistura cola e plástico e não é reciclável.")
def _(s):
    D.polygon(s, (240, 220, 132), [(88, 96), (124, 108), (120, 124), (80, 112)])
    D.polygon(s, (200, 180, 92), [(88, 96), (124, 108), (120, 124), (80, 112)], 2)
    D.circle(s, (240, 220, 132), (58, 60), 46)
    D.circle(s, (0, 0, 0, 0), (58, 60), 24)
    D.circle(s, (200, 180, 92), (58, 60), 46, 3)
    D.circle(s, (200, 180, 92), (58, 60), 24, 3)
    D.circle(s, (255, 246, 196), (58, 60), 37, 3)
