# -*- coding: utf-8 -*-
"""Itens da lixeira AZUL (papel e papelao)."""

from ..drawing import D, rr
from .catalog import item


@item("azul", "Caixa de papelão", "Papelão limpo e seco é reciclável. Achate a caixa antes de descartar.", True)
def _(s):
    top = [(14, 38), (114, 38), (104, 18), (24, 18)]
    D.rect(s, (190, 140, 85), (14, 38, 100, 72), 0, border_radius=5)
    D.polygon(s, (212, 165, 105), top)
    D.rect(s, (232, 208, 150), (54, 18, 20, 92))
    D.rect(s, (140, 98, 55), (14, 38, 100, 72), 4, border_radius=5)
    D.polygon(s, (140, 98, 55), top, 4)
    rr(s, (245, 240, 225), (80, 76, 26, 22), 2)
    D.line(s, (120, 120, 125), (84, 83), (102, 83), 2)
    D.line(s, (120, 120, 125), (84, 90), (98, 90), 2)


@item("azul", "Manual de instruções", "Manuais em papel podem ser reciclados. Prefira consultar a versão digital!", True)
def _(s):
    rr(s, (240, 238, 228), (28, 12, 72, 104), 5)
    rr(s, (70, 120, 210), (28, 12, 72, 32), 5)
    D.rect(s, (70, 120, 210), (28, 30, 72, 14))
    D.circle(s, (255, 255, 255), (64, 28), 8, 3)
    for i in range(5):
        D.line(s, (150, 150, 158), (40, 58 + i * 11), (88 - (i % 2) * 16, 58 + i * 11), 4)
    D.rect(s, (105, 105, 118), (28, 12, 72, 104), 3, border_radius=5)


@item("azul", "Jornal velho", "Jornais são recicláveis, desde que não estejam molhados nem engordurados.")
def _(s):
    rr(s, (228, 228, 220), (16, 16, 96, 96), 4)
    D.rect(s, (45, 45, 50), (24, 24, 80, 14))
    D.rect(s, (125, 125, 135), (24, 46, 36, 30))
    for i in range(3):
        D.line(s, (95, 95, 100), (66, 50 + i * 10), (104, 50 + i * 10), 3)
    for i in range(4):
        D.line(s, (95, 95, 100), (24, 84 + i * 7), (104, 84 + i * 7), 3)
    D.rect(s, (100, 100, 108), (16, 16, 96, 96), 3, border_radius=4)


@item("azul", "Envelope", "Envelopes de papel comum vão para a reciclagem.")
def _(s):
    rr(s, (246, 242, 226), (12, 30, 104, 70), 5)
    D.polygon(s, (228, 220, 198), [(12, 30), (116, 30), (64, 72)])
    D.line(s, (160, 150, 130), (14, 98), (54, 64), 3)
    D.line(s, (160, 150, 130), (114, 98), (74, 64), 3)
    D.rect(s, (160, 150, 130), (12, 30, 104, 70), 3, border_radius=5)
    D.rect(s, (215, 70, 70), (88, 38, 18, 18))
    D.rect(s, (255, 255, 255), (91, 41, 12, 12), 2)
