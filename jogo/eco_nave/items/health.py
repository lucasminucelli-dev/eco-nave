# -*- coding: utf-8 -*-
"""Itens da lixeira BRANCO (servicos de saude)."""

from ..drawing import D, blob, drawn_rotated, rr
from ..utils import shade
from .catalog import item


@item("branco", "Seringa", "Seringas e agulhas são resíduos de saúde e exigem descarte seguro e especial.")
def _(s):
    def fn(t):
        D.rect(t, (150, 156, 168), (4, 62, 26, 6))
        rr(t, (170, 176, 188), (2, 54, 6, 22), 2)
        rr(t, (244, 246, 250), (28, 50, 64, 28), 6, (100, 110, 124), 2)
        D.rect(t, (120, 202, 232), (36, 57, 46, 14))
        for x in range(42, 88, 9):
            D.line(t, (90, 100, 112), (x, 50), (x, 56 if (x // 9) % 2 else 54), 2)
        rr(t, (244, 246, 250), (24, 44, 6, 40), 2, (100, 110, 124), 2)
        D.polygon(t, (200, 206, 216), [(92, 58), (92, 70), (104, 64)])
        D.line(t, (170, 176, 188), (104, 64), (126, 64), 2)
    drawn_rotated(s, fn, 32)


@item("branco", "Máscara cirúrgica", "Máscaras usadas em serviços de saúde têm descarte próprio, separado do lixo comum.")
def _(s):
    D.ellipse(s, (232, 234, 240), (2, 46, 32, 34), 3)
    D.ellipse(s, (232, 234, 240), (94, 46, 32, 34), 3)
    rr(s, (158, 208, 234), (22, 36, 84, 60), 8, (98, 152, 188))
    for y in (50, 63, 76):
        D.line(s, (118, 170, 206), (24, y), (104, y), 3)
        D.line(s, (196, 232, 248), (24, y + 3), (104, y + 3), 1)
    D.line(s, (240, 242, 248), (40, 40), (88, 40), 3)


@item("branco", "Curativo usado", "Curativos usados em unidades de saúde vão no lixo de serviços de saúde.")
def _(s):
    def fn(t):
        rr(t, (234, 198, 152), (6, 44, 116, 40), 20, (196, 156, 110))
        D.rect(t, (250, 236, 210), (46, 44, 36, 40))
        D.rect(t, (196, 156, 110), (46, 44, 36, 40), 2)
        for x in (22, 32, 42, 86, 96, 106):
            for y in (54, 74):
                D.circle(t, (200, 160, 114), (x, y), 2)
    drawn_rotated(s, fn, 30)


@item("branco", "Luva descartável", "Luvas usadas em atendimentos de saúde exigem descarte separado.")
def _(s):
    C = (122, 192, 232)
    O = (70, 130, 175)
    D.polygon(s, C, blob(28, 76, 10, 18, -50))
    D.polygon(s, O, blob(28, 76, 10, 18, -50), 3)
    for x, top in ((34, 30), (48, 18), (62, 14), (76, 26)):
        rr(s, C, (x, top, 15, 74 - top), 7, O)
    rr(s, C, (34, 60, 57, 46), 12, O)
    D.rect(s, C, (37, 60, 51, 16))
    rr(s, shade(C, 0.82), (34, 102, 57, 16), 4, O)
