# -*- coding: utf-8 -*-
"""Itens da lixeira LARANJA (residuos perigosos: pilhas, baterias, lampadas...)."""

from ..drawing import D, rr
from .catalog import item


@item("laranja", "Pilha", "Pilhas podem conter substâncias que exigem coleta específica. Use pontos de entrega do sistema de logística reversa.", reverse_logistics=True)
def _(s):
    rr(s, (200, 202, 208), (56, 8, 16, 16), 3)
    rr(s, (32, 34, 40), (40, 20, 48, 100), 8)
    rr(s, (226, 142, 40), (40, 20, 48, 36), 8)
    D.rect(s, (226, 142, 40), (40, 42, 48, 14))
    D.rect(s, (255, 212, 64), (40, 62, 48, 7))
    D.line(s, (255, 255, 255), (64, 82), (64, 102), 4)
    D.line(s, (255, 255, 255), (54, 92), (74, 92), 4)
    D.rect(s, (96, 98, 108), (46, 28, 6, 86), 0, border_radius=3)


@item("laranja", "Bateria de celular", "Baterias de lítio podem incendiar se danificadas. Não amasse, perfure ou abra; encaminhe a um ponto de recebimento.", is_component=True, reverse_logistics=True)
def _(s):
    rr(s, (74, 84, 100), (20, 26, 88, 76), 8, (42, 50, 62))
    rr(s, (100, 112, 132), (27, 33, 74, 62), 6)
    for x in (34, 58, 82):
        D.rect(s, (232, 192, 62), (x, 102, 12, 10))
    D.polygon(s, (255, 222, 52), [(74, 38), (48, 68), (63, 68), (56, 92), (82, 60), (67, 60), (78, 38)])


@item("laranja", "Lâmpada fluorescente", "Lâmpadas fluorescentes podem conter mercúrio e exigem logística reversa ou coleta especializada.", reverse_logistics=True)
def _(s):
    D.circle(s, (255, 250, 200), (64, 50), 46)
    for x in (44, 64, 84):
        D.line(s, (222, 224, 200), (x, 80), (x, 28), 14)
        D.circle(s, (222, 224, 200), (x, 28), 7)
        D.line(s, (255, 255, 240), (x, 80), (x, 28), 10)
        D.circle(s, (255, 255, 240), (x, 28), 5)
    rr(s, (236, 236, 226), (34, 74, 60, 22), 4, (150, 150, 140), 2)
    rr(s, (196, 198, 204), (42, 94, 44, 14), 3)
    for x in (48, 58, 68, 78):
        D.line(s, (120, 122, 130), (x, 95), (x, 107), 2)
    rr(s, (60, 62, 68), (54, 108, 20, 10), 3)


@item("laranja", "Cartucho de tinta", "Cartuchos e toners podem ter sistema de devolução próprio. Consulte o fabricante, a loja ou o serviço local.", reverse_logistics=True)
def _(s):
    rr(s, (60, 62, 76), (22, 24, 84, 68), 6, (36, 38, 48))
    for i, c in enumerate(((0, 190, 232), (232, 44, 142), (250, 222, 34))):
        rr(s, c, (30 + i * 26, 34, 20, 46), 4)
    rr(s, (208, 172, 62), (44, 92, 40, 14), 3)
    D.rect(s, (255, 255, 255), (34, 38, 4, 30), 0, border_radius=2)
