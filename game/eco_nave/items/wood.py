# -*- coding: utf-8 -*-
"""Itens da lixeira PRETO (madeira)."""

from ..drawing import D, rr
from ..utils import lerp, shade
from .catalog import item


@item("preto", "Tábuas de madeira", "Sobras de madeira podem ser reutilizadas em móveis, artesanato e reformas.")
def _(s):
    for i, y in enumerate((24, 52, 80)):
        c = shade((156, 104, 60), 0.88 + 0.12 * (i % 2))
        rr(s, c, (10, y, 108, 26), 3, shade(c, 0.62))
        D.line(s, shade(c, 0.75), (22, y + 9), (72, y + 9), 2)
        D.line(s, shade(c, 0.75), (54, y + 18), (104, y + 18), 2)
        D.circle(s, (86, 88, 96), (20, y + 13), 2)
        D.circle(s, (86, 88, 96), (108, y + 13), 2)


@item("preto", "Caixote de madeira", "Caixotes podem ganhar novo uso. Se não der, a madeira segue para reciclagem.")
def _(s):
    D.rect(s, (170, 120, 70), (14, 22, 100, 86))
    for y in (22, 50, 78):
        D.rect(s, (192, 140, 84), (14, y, 100, 30))
        D.rect(s, (112, 72, 40), (14, y, 100, 30), 3)
    D.polygon(s, (146, 98, 56), [(14, 26), (26, 22), (114, 104), (102, 108)])
    D.polygon(s, (112, 72, 40), [(14, 26), (26, 22), (114, 104), (102, 108)], 2)
    D.rect(s, (112, 72, 40), (14, 22, 100, 86), 4)


@item("preto", "Palete de madeira", "Paletes de madeira são muito reaproveitados em móveis e decoração.")
def _(s):
    top = [(22, 16), (108, 16), (118, 34), (10, 34)]
    D.polygon(s, (206, 164, 104), top)
    for k in (0.33, 0.66):
        x0 = lerp(22, 10, 0) + (108 - 22) * k
        D.line(s, (140, 100, 56), (lerp(22, 10, k) + (86 * 0), 16), (lerp(22, 10, k), 34), 1)
    for x in (44, 66, 88):
        D.line(s, (140, 100, 56), (x, 16), (x - 8 + (x - 66) * 0.1, 34), 2)
    D.polygon(s, (140, 100, 56), top, 3)
    D.rect(s, (192, 148, 90), (10, 34, 108, 14))
    D.rect(s, (130, 92, 50), (10, 34, 108, 14), 3)
    for x in (14, 55, 96):
        D.rect(s, (170, 124, 70), (x, 48, 18, 28))
        D.rect(s, (120, 84, 46), (x, 48, 18, 28), 3)
    D.rect(s, (192, 148, 90), (10, 76, 108, 14))
    D.rect(s, (130, 92, 50), (10, 76, 108, 14), 3)


@item("preto", "Tronco de madeira", "Restos de madeira podem ser reaproveitados. Não queime: a fumaça polui o ar.")
def _(s):
    bark = (112, 72, 40)
    D.ellipse(s, shade(bark, 0.9), (10, 32, 26, 64))
    D.rect(s, bark, (22, 32, 66, 64))
    for y in (46, 62, 78):
        D.line(s, shade(bark, 0.7), (26, y), (82, y + 3), 2)
    D.line(s, shade(bark, 0.6), (22, 32), (94, 32), 3)
    D.line(s, shade(bark, 0.6), (22, 96), (94, 96), 3)
    D.ellipse(s, (216, 174, 114), (76, 32, 36, 64))
    D.ellipse(s, (146, 100, 58), (76, 32, 36, 64), 3)
    D.ellipse(s, (172, 126, 74), (83, 41, 22, 46), 2)
    D.ellipse(s, (172, 126, 74), (89, 54, 10, 20), 2)


@item("preto", "Retalhos de madeira", "Retalhos limpos podem ser reaproveitados em pequenos projetos; madeira tratada ou contaminada exige orientação específica.", reuse="Use peças em bom estado em reparos, artesanato ou pequenos móveis.")
def _(s):
    for i, y in enumerate((24, 48, 72)):
        D.polygon(s, (184 - i * 9, 132 - i * 7, 80 - i * 5), [(12, y), (108, y + 6), (116, y + 25), (18, y + 19)])
        D.polygon(s, (112, 74, 42), [(12, y), (108, y + 6), (116, y + 25), (18, y + 19)], 3)
        D.line(s, (224, 184, 124), (26, y + 7), (90, y + 12), 2)


@item("preto", "Sobras de madeira de móveis", "Peças de móveis podem ser consertadas ou reaproveitadas. Verifique tratamentos, tintas e contaminantes antes da destinação.", reuse="Avalie doação, reparo ou reaproveitamento antes de encaminhar a madeira para reciclagem.")
def _(s):
    rr(s, (150, 98, 56), (16, 24, 96, 82), 5, (88, 56, 34), 4)
    D.rect(s, (190, 138, 82), (24, 32, 80, 18))
    D.rect(s, (112, 72, 42), (24, 62, 80, 36))
    D.line(s, (220, 178, 118), (30, 42), (96, 42), 2)
    for x in (28, 96):
        D.circle(s, (216, 184, 128), (x, 80), 3)
    D.rect(s, (88, 56, 34), (16, 24, 96, 82), 3, border_radius=5)
