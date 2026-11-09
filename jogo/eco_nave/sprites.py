# -*- coding: utf-8 -*-
"""Fabrica de sprites procedurais: tudo e desenhado por formas, sem imagens externas."""
import pygame

from .config import BIN_BODY_TOP, H, LANES, LANE_W, PLATE_H, W
from .drawing import D, draw_recycle
from .text import TEXT
from .utils import lerp, mix, shade


class SpriteFactory:
    @staticmethod
    def glow(radius, color, max_alpha=90):
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        steps = max(8, radius // 2)
        for i in range(steps):
            r = radius - i * radius / steps
            a = int(max_alpha * ((i + 1) / steps) ** 2)
            D.circle(s, (color[0], color[1], color[2], a), (radius, radius), int(r))
        return s

    @classmethod
    def background(cls):
        bg = pygame.Surface((W, H))
        top, bot = (5, 8, 26), (34, 18, 62)
        for y in range(0, H, 2):
            c = mix(top, bot, (y / H) ** 1.2)
            D.line(bg, c, (0, y), (W, y), 2)
        for (x, y, r, col, a) in ((260, 250, 380, (60, 40, 140), 70), (980, 380, 420, (30, 90, 150), 55),
                                 (640, 120, 300, (110, 40, 120), 45)):
            g = cls.glow(r, col, a)
            bg.blit(g, (x - r, y - r))
        # lua
        mx, my = 1130, 190
        bg.blit(cls.glow(90, (200, 210, 255), 60), (mx - 90, my - 90))
        D.circle(bg, (226, 228, 240), (mx, my), 42)
        for (dx, dy, r) in ((-14, -10, 9), (12, 8, 12), (-6, 18, 6), (16, -18, 5)):
            D.circle(bg, (196, 198, 214), (mx + dx, my + dy), r)
        # chao / painel das lixeiras
        gy = BIN_BODY_TOP - 40
        panel = pygame.Surface((W, H - gy), pygame.SRCALPHA)
        for y in range(H - gy):
            a = int(lerp(0, 235, min(1.0, y / 60.0)))
            D.line(panel, (10, 14, 34, a), (0, y), (W, y))
        bg.blit(panel, (0, gy))
        D.line(bg, (70, 110, 190), (0, gy + 30), (W, gy + 30), 2)
        for i in range(1, LANES):
            D.line(bg, (40, 56, 100), (i * LANE_W, gy + 34), (i * LANE_W, H), 1)
        return bg

    @staticmethod
    def lane_glow(color):
        s = pygame.Surface((LANE_W, H), pygame.SRCALPHA)
        for y in range(0, H, 4):
            a = int(105 * (y / H) ** 1.6)
            D.rect(s, (color[0], color[1], color[2], a), (0, y, LANE_W, 4))
        D.line(s, (color[0], color[1], color[2], 150), (0, 0), (0, H), 2)
        D.line(s, (color[0], color[1], color[2], 150), (LANE_W - 1, 0), (LANE_W - 1, H), 2)
        return s

    @staticmethod
    def bin_body(b):
        k = 2
        color = b.color
        s = pygame.Surface((88 * k, 80 * k), pygame.SRCALPHA)
        dark = shade(color, 0.55) if b.key != "preto" else (110, 112, 130)
        light = mix(color, (255, 255, 255), 0.22)
        poly = [(8 * k, 0), (80 * k, 0), (72 * k, 80 * k), (16 * k, 80 * k)]
        D.polygon(s, color, poly)
        D.polygon(s, light, [(8 * k, 0), (21 * k, 0), (28 * k, 80 * k), (16 * k, 80 * k)])
        for f in (0.2, 0.8):
            x_top, x_bot = 8 + 72 * f, 16 + 56 * f
            D.line(s, shade(color, 0.8), (x_top * k, 4 * k), (x_bot * k, 76 * k), 2 * k)
        sym = (255, 255, 255) if b.key not in ("amarelo", "branco", "laranja") else (60, 60, 66)
        if b.key == "branco":
            sym = (170, 172, 180)
        draw_recycle(s, 44 * k, 42 * k, 15 * k, sym, 3.4 * k)
        D.polygon(s, dark, poly, 3 * k)
        return pygame.transform.smoothscale(s, (88, 80))

    @staticmethod
    def bin_lid(b):
        k = 2
        color = b.color
        s = pygame.Surface((96 * k, 18 * k), pygame.SRCALPHA)
        lid = mix(color, (255, 255, 255), 0.12)
        dark = shade(color, 0.55) if b.key != "preto" else (110, 112, 130)
        D.rect(s, lid, (0, 7 * k, 96 * k, 11 * k), 0, border_radius=4 * k)
        D.rect(s, dark, (0, 7 * k, 96 * k, 11 * k), 2 * k, border_radius=4 * k)
        D.rect(s, lid, (34 * k, 0, 28 * k, 11 * k), 0, border_radius=3 * k)
        D.rect(s, dark, (34 * k, 0, 28 * k, 11 * k), 2 * k, border_radius=3 * k)
        return pygame.transform.smoothscale(s, (96, 18))

    @staticmethod
    def plate(b):
        s = pygame.Surface((116, PLATE_H), pygame.SRCALPHA)
        edge = mix(b.color, (255, 255, 255), 0.35)
        D.rect(s, b.color, (0, 0, 116, PLATE_H), 0, border_radius=7)
        D.rect(s, edge, (0, 0, 116, PLATE_H), 2, border_radius=7)
        TEXT.draw(s, b.name, 16, b.text_color, (58, 14), "center", bold=True, max_w=104)
        TEXT.draw(s, b.material, 13, b.text_color, (58, 32), "center", max_w=106)
        return s

    @staticmethod
    def ship():
        k = 2
        w, h = 180, 110
        s = pygame.Surface((w * k, h * k), pygame.SRCALPHA)

        def E(x, y, ww, hh):
            return (x * k, y * k, ww * k, hh * k)

        cx = 90
        # cupula de vidro
        D.ellipse(s, (150, 214, 240), E(cx - 34, 6, 68, 64))
        D.ellipse(s, (96, 160, 200), E(cx - 34, 6, 68, 64), 3 * k)
        D.ellipse(s, (214, 244, 255), E(cx - 24, 12, 22, 26))
        # alienigena piloto
        D.ellipse(s, (128, 226, 116), E(cx - 14, 30, 28, 32))
        D.ellipse(s, (60, 140, 60), E(cx - 14, 30, 28, 32), 2 * k)
        D.ellipse(s, (20, 40, 20), E(cx - 10, 41, 8, 6))
        D.ellipse(s, (20, 40, 20), E(cx + 2, 41, 8, 6))
        D.line(s, (60, 140, 60), (cx * k, 30 * k), ((cx + 4) * k, 20 * k), 2 * k)
        D.circle(s, (255, 90, 90), ((cx + 4) * k, 19 * k), 3 * k)
        # casco
        D.ellipse(s, (98, 108, 134), E(cx - 60, 62, 120, 40))
        D.ellipse(s, (162, 172, 194), E(cx - 84, 44, 168, 44))
        D.ellipse(s, (230, 236, 248), E(cx - 84, 44, 168, 44), 2 * k)
        D.ellipse(s, (120, 130, 156), E(cx - 84, 62, 168, 22))
        D.ellipse(s, (180, 190, 210), E(cx - 84, 44, 168, 34))
        D.ellipse(s, (232, 238, 250), E(cx - 84, 44, 168, 34), 2 * k)
        # escotilha (por onde cai o lixo)
        D.ellipse(s, (44, 50, 70), E(cx - 16, 88, 32, 12))
        return pygame.transform.smoothscale(s, (w, h))

    @staticmethod
    def beam():
        length, top_w = 150, 30
        s = pygame.Surface((140, length), pygame.SRCALPHA)
        for y in range(length):
            half = top_w / 2 + 50 * y / length
            a = int(120 * (1 - y / length) ** 1.3)
            D.line(s, (190, 255, 215, a), (70 - half, y), (70 + half, y))
        return s

    @staticmethod
    def heart(size, color, outline):
        k = 3
        s = pygame.Surface((size * k, size * k), pygame.SRCALPHA)
        r = size * 0.27 * k
        cx, cy = size * k / 2, size * k * 0.42
        D.circle(s, color, (cx - r, cy - r * 0.35), r)
        D.circle(s, color, (cx + r, cy - r * 0.35), r)
        D.polygon(s, color, [(cx - 2 * r + 1, cy - r * 0.05), (cx + 2 * r - 1, cy - r * 0.05), (cx, size * k * 0.9)])
        return pygame.transform.smoothscale(s, (size, size))
