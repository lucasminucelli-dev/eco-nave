# -*- coding: utf-8 -*-
"""Itens da lixeira VERDE (vidro)."""

from ..drawing import D, rr
from ..utils import shade
from .catalog import item


@item("verde", "Garrafa de vidro", "O vidro pode ser reciclado várias vezes sem perder qualidade.")
def _(s):
    G = (46, 150, 80)
    D.rect(s, G, (38, 56, 52, 58), 0, border_radius=8)
    D.polygon(s, G, [(38, 62), (90, 62), (74, 36), (54, 36)])
    D.rect(s, G, (54, 12, 20, 34))
    D.rect(s, shade(G, 0.7), (51, 8, 26, 9), 0, border_radius=3)
    D.rect(s, (238, 236, 214), (38, 76, 52, 20))
    D.rect(s, (130, 215, 150), (45, 64, 7, 44), 0, border_radius=3)
    D.rect(s, shade(G, 0.55), (38, 56, 52, 58), 3, border_radius=8)


@item("verde", "Pote de vidro", "Potes de vidro limpos são recicláveis. Retire a tampa antes de descartar.")
def _(s):
    rr(s, (175, 226, 206), (26, 36, 76, 74), 10, (68, 150, 120))
    rr(s, (150, 206, 186), (32, 24, 64, 16), 4, (68, 150, 120))
    D.rect(s, (232, 252, 242), (35, 48, 8, 50), 0, border_radius=4)
    rr(s, (245, 240, 220), (50, 62, 42, 26), 3)


@item("verde", "Frasco de perfume", "Frascos de vidro são recicláveis. Retire tampa e borrifador antes de descartar.")
def _(s):
    rr(s, (160, 206, 240), (28, 50, 72, 62), 8, (80, 130, 182))
    rr(s, (240, 150, 192), (34, 72, 60, 34), 6)
    rr(s, (50, 50, 62), (50, 20, 28, 28), 4)
    D.rect(s, (190, 192, 204), (56, 46, 16, 8))
    D.rect(s, (232, 246, 255), (37, 56, 6, 44), 0, border_radius=3)


@item("verde", "Pote de conserva", "Potes de vidro podem ser reciclados; remova resíduos e separe a tampa metálica quando a coleta orientar.")
def _(s):
    rr(s, (178, 226, 202), (26, 35, 76, 78), 10, (62, 142, 104), 4)
    rr(s, (190, 202, 158), (23, 26, 82, 15), 4, (112, 126, 82), 3)
    D.rect(s, (242, 248, 222), (37, 52, 10, 50), 0, border_radius=5)
    D.rect(s, (116, 168, 108), (48, 64, 40, 24), 0, border_radius=4)


@item("verde", "Frasco de molho", "Frascos de vidro limpos podem retornar à reciclagem; tampas e rótulos seguem a orientação do serviço local.")
def _(s):
    D.rect(s, (180, 68, 52), (40, 49, 48, 65), 0, border_radius=10)
    D.polygon(s, (180, 68, 52), [(40, 55), (88, 55), (76, 34), (52, 34)])
    D.rect(s, (180, 68, 52), (53, 14, 22, 25))
    rr(s, (204, 208, 216), (50, 7, 28, 10), 3, (112, 118, 128), 2)
    rr(s, (244, 238, 220), (45, 72, 38, 23), 4)
    D.line(s, (240, 255, 245), (47, 58), (47, 98), 3)
