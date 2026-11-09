# -*- coding: utf-8 -*-
"""Efeitos visuais passageiros: confete, faiscas, textos flutuantes e lixo voando."""
import math
import random

import pygame

from .config import ITEM_SIZE
from .text import TEXT
from .utils import clamp, lerp, mix


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "color", "size", "max_life")

    def __init__(self, x, y, vx, vy, life, color, size, max_life):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.life, self.color, self.size, self.max_life = life, color, size, max_life

    def update(self, dt):
        self.life -= dt
        self.vy += 520 * dt           # gravidade
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surf):
        k = clamp(self.life / self.max_life, 0.0, 1.0)
        s = max(1, int(self.size * k + 1))
        surf.fill(self.color, (int(self.x), int(self.y), s, s))


class Popup:
    """Texto que sobe e some (ex.: +100, Errou!)."""

    def __init__(self, text, x, y, duration, color, size):
        self.text, self.x, self.y = text, x, y
        self.t = duration
        self.duration = duration
        self.color, self.size = color, size

    def update(self, dt):
        self.t -= dt
        self.y -= 46 * dt

    def draw(self, surf):
        k = clamp(self.t / self.duration, 0.0, 1.0)
        TEXT.draw(surf, self.text, self.size, self.color, (self.x, self.y), "center", bold=True,
                  outline=(10, 14, 30), alpha=255 * min(1.0, k * 2.5))


class ItemEffect:
    """Animacao do lixo depois de resolvido: entra na lixeira (acerto) ou quica para fora (erro)."""

    def __init__(self, sprite, x, y, tx, ty, duration, ok, vx=0.0):
        self.sprite = sprite
        self.x, self.y = x, y
        self.tx, self.ty = tx, ty
        self.duration = duration
        self.ok = ok
        self.vx = vx
        self.t = 0.0

    def update(self, dt):
        self.t += dt

    @property
    def finished(self):
        return self.t >= self.duration

    def draw(self, surf):
        p = clamp(self.t / self.duration, 0.0, 1.0)
        if self.ok:
            e = p * p * (3 - 2 * p)
            x = lerp(self.x, self.tx, e)
            y = lerp(self.y, self.ty, e)
            sz = max(4, int(ITEM_SIZE * lerp(1.0, 0.35, e)))
            img = pygame.transform.smoothscale(self.sprite, (sz, sz))
        else:
            t = self.t
            x = self.x + self.vx * t
            y = self.y - 300 * t + 760 * t * t
            img = pygame.transform.rotate(self.sprite, t * 420)
            img.set_alpha(int(255 * (1 - p)))
        surf.blit(img, img.get_rect(center=(int(x), int(y))))


class Effects:
    """Gerencia todos os efeitos ativos e o tremor de tela."""
    SHAKE_TIME = 0.35

    def __init__(self):
        self.reset()

    def reset(self):
        self.particles = []
        self.popups = []
        self.item_fx = []
        self.shake = 0.0

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]
        for pop in self.popups:
            pop.update(dt)
        self.popups = [p for p in self.popups if p.t > 0]
        for fx in self.item_fx:
            fx.update(dt)
        self.item_fx = [f for f in self.item_fx if not f.finished]
        self.shake = max(0.0, self.shake - dt)

    # ---- criacao
    def start_shake(self):
        self.shake = self.SHAKE_TIME

    @property
    def shake_amplitude(self):
        """Amplitude (px) do tremor atual; 0 se nao ha tremor."""
        if self.shake <= 0:
            return 0.0
        return 9 * min(1.0, self.shake / self.SHAKE_TIME)

    def popup(self, text, x, y, duration, color, size):
        self.popups.append(Popup(text, x, y, duration, color, size))

    def confetti(self, x, y, color, n):
        cols = (color, (255, 255, 255), mix(color, (255, 255, 255), 0.5), (255, 230, 90))
        for _ in range(n):
            a = math.radians(random.uniform(-165, -15))
            sp = random.uniform(140, 430)
            self.particles.append(Particle(x + random.uniform(-20, 20), y, math.cos(a) * sp, math.sin(a) * sp,
                                           random.uniform(0.6, 1.1), random.choice(cols), random.randint(4, 8), 1.1))

    def sparks(self, x, y, color, n):
        for _ in range(n):
            a = math.radians(random.uniform(-170, -10))
            sp = random.uniform(120, 360)
            self.particles.append(Particle(x + random.uniform(-16, 16), y, math.cos(a) * sp, math.sin(a) * sp,
                                           random.uniform(0.4, 0.8),
                                           random.choice((color, (255, 190, 90), (90, 90, 96))),
                                           random.randint(3, 6), 0.8))

    def fly_into_bin(self, sprite, x, y, tx, ty):
        self.item_fx.append(ItemEffect(sprite, x, y, tx, ty, 0.28, True))

    def bounce_away(self, sprite, x, y):
        self.item_fx.append(ItemEffect(sprite, x, y, x, y, 0.7, False, vx=random.uniform(-170, 170)))

    # ---- desenho
    def draw_items(self, surf):
        for fx in self.item_fx:
            fx.draw(surf)

    def draw_particles(self, surf):
        for p in self.particles:
            p.draw(surf)

    def draw_popups(self, surf):
        for p in self.popups:
            p.draw(surf)
