# -*- coding: utf-8 -*-
"""Pecas de interface reutilizaveis (paineis e teclas desenhadas por formas)."""
import pygame

from .drawing import D
from .text import TEXT


class Ui:
    @staticmethod
    def panel(surf, rect, color=(8, 12, 30), alpha=215, border=None, radius=16, bw=2):
        rect = pygame.Rect(rect)
        p = pygame.Surface(rect.size, pygame.SRCALPHA)
        D.rect(p, (color[0], color[1], color[2], alpha), (0, 0, rect.w, rect.h), 0, border_radius=radius)
        if border is not None:
            D.rect(p, border, (0, 0, rect.w, rect.h), bw, border_radius=radius)
        surf.blit(p, rect.topleft)

    @staticmethod
    def keycap(surf, cx, cy, kind, size=34):
        """Tecla desenhada por formas. kind = 'left' | 'right' | 'up' | 'down' (setas) ou
        qualquer outro texto curto (ex.: 'O', 'ENTER'), que vira uma tecla com esse rotulo."""
        r = pygame.Rect(0, 0, size, size)
        r.center = (cx, cy)
        D.rect(surf, (28, 36, 64), r.move(0, 3), 0, border_radius=7)
        D.rect(surf, (226, 232, 246), r, 0, border_radius=7)
        D.rect(surf, (120, 132, 170), r, 2, border_radius=7)
        m = size * 0.24
        if kind == "left":
            pts = [(cx - m, cy), (cx + m * 0.8, cy - m), (cx + m * 0.8, cy + m)]
        elif kind == "right":
            pts = [(cx + m, cy), (cx - m * 0.8, cy - m), (cx - m * 0.8, cy + m)]
        elif kind == "up":
            pts = [(cx, cy - m), (cx - m, cy + m * 0.8), (cx + m, cy + m * 0.8)]
        elif kind == "down":
            pts = [(cx, cy + m), (cx - m, cy - m * 0.8), (cx + m, cy - m * 0.8)]
        else:
            TEXT.draw(surf, str(kind), max(11, int(size * 0.5)), (30, 38, 70), (cx, cy), "center", bold=True)
            return
        D.polygon(surf, (40, 50, 86), pts)

    @staticmethod
    def keylabel(surf, label, x, y, size=16):
        """Tecla com texto (ENTER, R, ...). (x, y) = canto esquerdo/centro vertical. Devolve a largura."""
        t = TEXT.surface(label, size, (30, 38, 70), True)
        w = t.get_width() + 18
        r = pygame.Rect(x, y - 13, w, 26)
        D.rect(surf, (28, 36, 64), r.move(0, 2), 0, border_radius=6)
        D.rect(surf, (226, 232, 246), r, 0, border_radius=6)
        D.rect(surf, (120, 132, 170), r, 2, border_radius=6)
        surf.blit(t, t.get_rect(center=r.center))
        return w

    @staticmethod
    def keylabel_width(label, size=16):
        """Largura que 'keylabel' ocupa (para centralizar linhas de atalhos)."""
        return TEXT.surface(label, size, (30, 38, 70), True).get_width() + 18


# ======================================================================================
# Ajudantes de layout: medem o texto antes de desenhar, para nada ficar em cima de nada.
# ======================================================================================
def _ellipsize(text, size, max_w, bold=False):
    """Corta 'text' (com reticencias) ate caber em max_w pixels."""
    if TEXT.width(text, size, bold) <= max_w:
        return text
    while len(text) > 1 and TEXT.width(text + "…", size, bold) > max_w:
        text = text[:-1]
    return text.rstrip() + "…"


def measure_block(text, w, size, bold=False, gap=3):
    """Altura (px) que um bloco de texto quebrado em linhas ocupa."""
    n = len(TEXT.wrap(text, size, w, bold))
    return n * TEXT.line_height(size, bold) + max(0, n - 1) * gap


def fit_block(surf, text, rect, color, size_max=20, size_min=12, bold=False, align="left", gap=3):
    """Desenha 'text' quebrado em linhas dentro de 'rect' (x, y, w, h).

    Usa a maior fonte entre size_max e size_min que cabe na altura; se nem a menor couber,
    corta as linhas que sobram e termina com reticencias. Devolve (y_final, tamanho_usado).
    """
    x, y, w, h = rect
    size = size_max
    while True:
        lines = TEXT.wrap(text, size, w, bold)
        lh = TEXT.line_height(size, bold)
        total = len(lines) * lh + max(0, len(lines) - 1) * gap
        if total <= h or size <= size_min:
            break
        size -= 1
    if total > h:
        keep = max(1, (h + gap) // (lh + gap))
        if keep < len(lines):
            lines = lines[:keep]
            lines[-1] = _ellipsize(lines[-1] + " …", size, w, bold)
        total = len(lines) * lh + max(0, len(lines) - 1) * gap
    for i, line in enumerate(lines):
        ly = y + i * (lh + gap)
        if align == "center":
            TEXT.draw(surf, line, size, color, (x + w // 2, ly), "midtop", bold=bold)
        elif align == "right":
            TEXT.draw(surf, line, size, color, (x + w, ly), "topright", bold=bold)
        else:
            TEXT.draw(surf, line, size, color, (x, ly), "topleft", bold=bold)
    return y + total, size


Ui.measure_block = staticmethod(measure_block)
Ui.fit_block = staticmethod(fit_block)
Ui.ellipsize = staticmethod(_ellipsize)


def _hint_bar(surf, hints, y, size=15, max_w=1160, color=(196, 210, 232)):
    """Linha centralizada de atalhos [(tecla, texto), ...]. Reduz a fonte se nao couber."""
    from .config import W
    while True:
        widths = [Ui.keylabel_width(k, size) + 8 + TEXT.width(t, size) for k, t in hints]
        total = sum(widths) + 26 * (len(hints) - 1)
        if total <= max_w or size <= 11:
            break
        size -= 1
    x = (W - total) // 2
    for (k, t), wd in zip(hints, widths):
        kw = Ui.keylabel(surf, k, x, y, size)
        TEXT.draw(surf, t, size, color, (x + kw + 8, y), "midleft")
        x += wd + 26
    return y + 14


def _chip(surf, text, x, y, color, size=14, fill=True, text_color=None):
    """Etiqueta arredondada com o canto esquerdo-superior em (x, y). Devolve a largura."""
    from .drawing import rr
    tw = TEXT.width(text, size, True)
    w, h = tw + 20, size + 12
    rr(surf, (color[0] // 4, color[1] // 4, color[2] // 4) if fill else (10, 16, 32), (x, y, w, h), h // 2,
       color, 2)
    TEXT.draw(surf, text, size, text_color or color, (x + w // 2, y + h // 2), "center", bold=True)
    return w


def _header(surf, title, subtitle, color=(138, 220, 255), outline=(12, 30, 62), y=58, size=40):
    """Titulo de tela centralizado + subtitulo. Devolve o y logo abaixo do cabecalho."""
    from .config import W
    TEXT.draw(surf, title, size, color, (W // 2, y), "center", bold=True, outline=outline, max_w=W - 160)
    bottom = y + size // 2 + 6
    if subtitle:
        TEXT.draw(surf, subtitle, 16, (190, 214, 232), (W // 2, bottom + 12), "center", max_w=W - 160)
        bottom += 26
    return bottom


Ui.hint_bar = staticmethod(_hint_bar)
Ui.chip = staticmethod(_chip)
Ui.header = staticmethod(_header)


def _bullets(surf, items, rect, color, size_max=19, size_min=13, gap=8, bullet=(130, 245, 160)):
    """Lista com marcadores; reduz a fonte ate toda a lista caber em 'rect'. Devolve o y final."""
    x, y, w, h = rect
    size = size_max
    while size > size_min:
        total = sum(measure_block(t, w - 22, size) for t in items) + gap * (len(items) - 1)
        if total <= h:
            break
        size -= 1
    cy = y
    for t in items:
        hgt = measure_block(t, w - 22, size)
        D.circle(surf, bullet, (x + 6, cy + TEXT.line_height(size) // 2), 4)
        fit_block(surf, t, (x + 22, cy, w - 22, hgt + 2), color, size, size)
        cy += hgt + gap
    return cy - gap


Ui.bullets = staticmethod(_bullets)
