# -*- coding: utf-8 -*-
"""Itens da lixeira AZUL (papel e papelao)."""

from ..drawing import D, rr
from .catalog import item


@item("azul", "Caixa de papelão", "Papelão limpo e seco é reciclável. Achate a caixa antes de descartar.")
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


@item("azul", "Manual de instruções", "Manuais em papel podem ser reciclados. Prefira consultar a versão digital!")
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


@item("azul", "Revista", "Revistas limpas e secas podem ser encaminhadas à reciclagem de papel.", fact="Papéis plastificados ou com laminação especial podem ter aceitação diferente na coleta local.")
def _(s):
    rr(s, (238, 236, 224), (22, 14, 84, 102), 5, (92, 98, 116), 3)
    rr(s, (48, 154, 126), (22, 14, 84, 30), 5)
    D.circle(s, (246, 210, 90), (64, 59), 23)
    D.polygon(s, (80, 130, 196), [(35, 92), (64, 68), (92, 92)])
    D.line(s, (255, 255, 255), (32, 104), (96, 104), 3)


@item("azul", "Livro antigo", "Livros em bom estado podem ser doados; os sem condição de uso podem seguir para reciclagem, conforme aceitação local.", reuse="Doe ou compartilhe o livro se ainda puder ser lido.")
def _(s):
    rr(s, (50, 92, 158), (24, 14, 80, 100), 7, (28, 52, 100), 4)
    D.rect(s, (232, 218, 174), (34, 22, 62, 84), 0, border_radius=3)
    D.line(s, (255, 250, 220), (44, 28), (44, 100), 4)
    for y in (42, 54, 66, 78, 90):
        D.line(s, (130, 136, 146), (54, y), (86, y), 2)
    D.rect(s, (28, 52, 100), (24, 14, 80, 100), 3, border_radius=7)


@item("azul", "Caixa de ovos de papelão", "Embalagens de papel moldado podem ser recicláveis ou compostadas; verifique se estão limpas e secas e confirme a regra local.")
def _(s):
    rr(s, (188, 150, 98), (15, 36, 98, 68), 8, (112, 78, 42), 3)
    for row in range(2):
        for col in range(3):
            x, y = 34 + col * 31, 52 + row * 29
            D.ellipse(s, (224, 194, 142), (x - 11, y - 12, 22, 25))
            D.ellipse(s, (126, 88, 48), (x - 11, y - 12, 22, 25), 2)
    D.line(s, (150, 110, 66), (16, 70), (112, 70), 2)
