# -*- coding: utf-8 -*-
"""Fundo animado: estrelas caindo e (no menu) residuos flutuando."""
import math
import random

import pygame

from .config import H, W
from .items import ITEM_CATALOG


class StarField:
    def __init__(self, count=130):
        # cada estrela: [x, y, tamanho, velocidade, fase, brilho]
        self.stars = [[random.uniform(0, W), random.uniform(0, H), random.choice((1, 1, 2, 2, 3)),
                       random.uniform(6, 26), random.uniform(0, 6.28), random.randint(110, 230)]
                      for _ in range(count)]

    def update(self, dt):
        for s in self.stars:
            s[1] += s[3] * dt
            if s[1] > H:
                s[1] = 0
                s[0] = random.uniform(0, W)

    def draw(self, surf, t):
        for x, y, sz, _sp, ph, base in self.stars:
            b = int(base * (0.65 + 0.35 * math.sin(t * 2.0 + ph)))
            surf.fill((b, b, min(255, b + 25)), (int(x), int(y), sz, sz))


class FloatingItem:
    """Residuo que cai devagar, girando, no fundo do menu e do ranking."""

    def __init__(self, y):
        self.respawn(y)

    def respawn(self, y):
        self.index = random.randrange(len(ITEM_CATALOG))
        self.x = random.uniform(40, W - 40)
        self.y = y
        self.vy = random.uniform(30, 80)
        self.rot = random.uniform(0, 360)
        self.vr = random.uniform(-40, 40)

    def update(self, dt):
        self.y += self.vy * dt
        self.rot += self.vr * dt
        if self.y > H + 60:
            self.respawn(-60)

    def draw(self, surf, assets):
        img = pygame.transform.rotate(assets.items[self.index], self.rot)
        img.set_alpha(120)
        surf.blit(img, img.get_rect(center=(int(self.x), int(self.y))))


class Backdrop:
    """Fundo completo: imagem de fundo + estrelas (+ residuos flutuantes, se pedido)."""

    def __init__(self):
        self.stars = StarField()
        self.floaters = [FloatingItem(random.uniform(-100, H)) for _ in range(10)]

    def update_stars(self, dt):
        self.stars.update(dt)

    def update_floaters(self, dt):
        for f in self.floaters:
            f.update(dt)

    def draw(self, surf, assets, t, with_floaters=False):
        surf.blit(assets.background, (0, 0))
        self.stars.draw(surf, t)
        if with_floaters:
            for f in self.floaters:
                f.draw(surf, assets)
