# -*- coding: utf-8 -*-
"""Itens da lixeira AMARELO (metal)."""

from ..drawing import D, hexagon, rr
from ..utils import shade
from .catalog import item


@item("amarelo", "Lata de alumínio", "O alumínio pode ser reciclado muitas vezes, poupando energia e recursos.")
def _(s):
    S = (198, 204, 214)
    D.ellipse(s, shade(S, 0.75), (36, 96, 56, 20))
    D.rect(s, S, (36, 28, 56, 78))
    D.rect(s, (210, 50, 56), (36, 50, 56, 38))
    D.rect(s, (248, 248, 250), (36, 62, 56, 12))
    D.rect(s, (238, 242, 248), (43, 30, 6, 72))
    D.ellipse(s, S, (36, 18, 56, 22))
    D.ellipse(s, (150, 156, 168), (42, 22, 44, 14))
    D.circle(s, (118, 124, 136), (64, 29), 3)


@item("amarelo", "Porca e parafuso", "Sucata de metal pode ser derretida e reaproveitada pela indústria.")
def _(s):
    D.rect(s, (150, 156, 168), (50, 88, 66, 14), 0, border_radius=3)
    for x in range(58, 114, 8):
        D.line(s, (98, 104, 116), (x, 88), (x + 4, 102), 2)
    D.polygon(s, (188, 194, 206), hexagon(38, 95, 20))
    D.polygon(s, (108, 114, 126), hexagon(38, 95, 20), 3)
    D.circle(s, (108, 114, 126), (38, 95), 8, 3)
    nut = hexagon(60, 42, 30, 0.5)
    D.polygon(s, (172, 178, 190), nut)
    D.polygon(s, (108, 114, 126), nut, 3)
    D.circle(s, (0, 0, 0, 0), (60, 42), 13)
    D.circle(s, (108, 114, 126), (60, 42), 13, 3)


@item("amarelo", "Fio de cobre", "O cobre dos fios e cabos é valioso e pode ser reaproveitado.")
def _(s):
    C, C2 = (214, 128, 64), (150, 80, 36)
    for i in range(5):
        y = 16 + i * 15
        D.ellipse(s, C2, (14, y, 92, 44), 9)
        D.ellipse(s, C, (14, y, 92, 44), 5)
    D.lines(s, C, False, [(104, 82), (116, 96), (100, 116)], 5)


@item("amarelo", "Dissipador de calor", "Peças de alumínio limpas e separadas podem ser recuperadas como metal; placas e aparelhos inteiros seguem para logística reversa especializada.")
def _(s):
    for i in range(9):
        x = 12 + i * 11
        D.rect(s, (178, 184, 196), (x, 16, 8, 74), 0, border_radius=2)
        D.rect(s, (118, 124, 138), (x + 6, 16, 2, 74))
    rr(s, (152, 158, 170), (8, 86, 112, 24), 4, (100, 106, 120))


@item("amarelo", "Lata de aço", "Embalagens de aço limpas e vazias podem ser recicladas. Evite deixar resíduos de alimento.")
def _(s):
    D.ellipse(s, (148, 154, 166), (30, 20, 68, 20))
    D.rect(s, (176, 182, 194), (30, 30, 68, 78))
    D.ellipse(s, (130, 136, 148), (30, 96, 68, 20))
    D.rect(s, (220, 224, 232), (40, 34, 8, 68), 0, border_radius=4)
    D.rect(s, (74, 116, 164), (30, 54, 68, 24))
    D.rect(s, (108, 114, 126), (30, 30, 68, 78), 3)


@item("amarelo", "Bandeja de alumínio", "Bandejas de alumínio sem excesso de gordura podem ser recicláveis; confira as regras locais.")
def _(s):
    D.polygon(s, (190, 198, 210), [(16, 48), (108, 48), (94, 108), (30, 108)])
    D.polygon(s, (228, 232, 240), [(26, 56), (98, 56), (86, 98), (38, 98)])
    D.polygon(s, (116, 124, 140), [(16, 48), (30, 108), (38, 98), (26, 56)], 3)
    D.polygon(s, (116, 124, 140), [(108, 48), (94, 108), (86, 98), (98, 56)], 3)
    D.line(s, (255, 255, 255), (34, 60), (86, 60), 3)


@item("amarelo", "Tampa metálica", "Tampas metálicas podem ser recicladas junto aos metais quando limpas; evite misturá-las a vidro quebrado solto.")
def _(s):
    D.ellipse(s, (148, 154, 166), (18, 34, 92, 60))
    D.ellipse(s, (214, 220, 230), (24, 28, 80, 54))
    D.ellipse(s, (112, 120, 136), (24, 28, 80, 54), 4)
    D.ellipse(s, (244, 246, 250), (36, 39, 56, 32), 2)
    for x in (32, 48, 64, 80, 96):
        D.line(s, (162, 168, 180), (x, 34), (x + 3, 48), 2)
