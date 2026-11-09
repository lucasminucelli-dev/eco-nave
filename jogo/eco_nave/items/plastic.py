# -*- coding: utf-8 -*-
"""Itens da lixeira VERMELHO (plastico e isopor)."""

from ..drawing import D, rr
from .catalog import item


@item("vermelho", "Isopor de embalagem", "O isopor leva muito tempo para se decompor. Leve-o a um ponto de reciclagem.")
def _(s):
    D.polygon(s, (238, 238, 242), [(14, 44), (96, 44), (114, 24), (32, 24)])
    D.polygon(s, (196, 198, 206), [(96, 44), (114, 24), (114, 84), (96, 104)])
    D.rect(s, (250, 250, 252), (14, 44, 82, 60))
    rr(s, (218, 220, 228), (28, 56, 54, 36), 4)
    D.rect(s, (170, 172, 182), (14, 44, 82, 60), 3)
    D.polygon(s, (170, 172, 182), [(96, 44), (114, 24), (114, 84), (96, 104)], 3)
    D.polygon(s, (170, 172, 182), [(14, 44), (96, 44), (114, 24), (32, 24)], 3)
    for (x, y) in ((24, 50), (46, 50), (70, 50), (88, 98), (22, 98), (44, 98)):
        D.circle(s, (205, 207, 215), (x, y), 2)


@item("vermelho", "Capa de celular", "Antes de descartar a capa, veja se dá para reutilizar ou doar.", True)
def _(s):
    rr(s, (232, 84, 112), (34, 10, 60, 108), 12, (176, 44, 76), 4)
    rr(s, (58, 22, 34), (42, 18, 28, 28), 8)
    D.circle(s, (130, 130, 145), (52, 28), 6)
    D.circle(s, (130, 130, 145), (60, 38), 6)
    D.rect(s, (255, 160, 180), (80, 30, 6, 52), 0, border_radius=3)


@item("vermelho", "Plástico-bolha", "Plástico de embalagem limpo e seco pode ser reciclado.")
def _(s):
    rr(s, (190, 225, 245), (12, 26, 104, 76), 8)
    for r in range(3):
        for c in range(4):
            cx, cy = 30 + c * 23, 44 + r * 22
            D.circle(s, (218, 240, 253), (cx, cy), 10)
            D.circle(s, (140, 185, 218), (cx, cy), 10, 2)
            D.circle(s, (255, 255, 255), (cx - 3, cy - 3), 3)
    D.rect(s, (120, 165, 200), (12, 26, 104, 76), 3, border_radius=8)


@item("vermelho", "Garrafa PET", "Garrafas PET são muito recicladas. Esvazie e amasse antes de descartar.")
def _(s):
    B = (170, 222, 245)
    O = (90, 150, 185)
    D.rect(s, B, (38, 54, 52, 60), 0, border_radius=8)
    D.polygon(s, B, [(38, 58), (90, 58), (74, 36), (54, 36)])
    D.rect(s, B, (54, 16, 20, 26))
    D.rect(s, (40, 110, 200), (51, 8, 26, 12), 0, border_radius=3)
    D.rect(s, (60, 170, 90), (38, 72, 52, 22))
    D.rect(s, (235, 250, 255), (44, 60, 6, 48), 0, border_radius=3)
    D.rect(s, O, (38, 54, 52, 60), 3, border_radius=8)
    D.polygon(s, O, [(38, 58), (54, 36), (74, 36), (90, 58)], 3)
