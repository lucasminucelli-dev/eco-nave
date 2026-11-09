# -*- coding: utf-8 -*-
"""Renderizacao de texto com cache de fontes e de imagens de texto."""
import pygame


class TextRenderer:
    FONT_NAMES = "segoeui,helveticaneue,arial,dejavusans,liberationsans,freesans"
    MAX_CACHED_TEXTS = 700

    def __init__(self):
        self._fonts = {}
        self._texts = {}

    def font(self, size, bold=False):
        key = (size, bold)
        f = self._fonts.get(key)
        if f is None:
            try:
                f = pygame.font.SysFont(self.FONT_NAMES, size, bold=bold)
            except Exception:
                f = pygame.font.Font(None, int(size * 1.25))
            self._fonts[key] = f
        return f

    def surface(self, text, size, color, bold=False):
        """Imagem do texto (em cache)."""
        key = (text, size, color, bold)
        s = self._texts.get(key)
        if s is None:
            if len(self._texts) > self.MAX_CACHED_TEXTS:
                self._texts.clear()
            s = self.font(size, bold).render(text, True, color)
            self._texts[key] = s
        return s

    def width(self, text, size, bold=False):
        return self.surface(text, size, (0, 0, 0), bold).get_width()

    def draw(self, surf, text, size, color, pos, anchor="center", bold=False,
             shadow=None, outline=None, alpha=None, max_w=None):
        """Desenha texto (com cache). Devolve o retangulo ocupado."""
        if max_w:
            while size > 9 and self.surface(text, size, color, bold).get_width() > max_w:
                size -= 1
        img = self.surface(text, size, color, bold)
        rect = img.get_rect()
        setattr(rect, anchor, (int(pos[0]), int(pos[1])))
        if alpha is not None and alpha < 255:
            img = img.copy()
            img.set_alpha(max(0, int(alpha)))
        if outline is not None:
            o = self.surface(text, size, outline, bold)
            if alpha is not None and alpha < 255:
                o = o.copy()
                o.set_alpha(max(0, int(alpha)))
            for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)):
                surf.blit(o, (rect.x + dx, rect.y + dy))
        elif shadow is not None:
            o = self.surface(text, size, shadow, bold)
            if alpha is not None and alpha < 255:
                o = o.copy()
                o.set_alpha(max(0, int(alpha)))
            surf.blit(o, (rect.x + 2, rect.y + 2))
        surf.blit(img, rect)
        return rect

    def wrap(self, text, size, max_w, bold=False):
        """Quebra 'text' em linhas que cabem em 'max_w' pixels."""
        font = self.font(size, bold)
        lines, cur = [], ""
        for word in text.split():
            test = word if not cur else cur + " " + word
            if font.size(test)[0] <= max_w or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


# Instancia unica usada pelo jogo inteiro.
TEXT = TextRenderer()
