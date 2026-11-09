# -*- coding: utf-8 -*-
"""Objetos que existem no mundo do jogo: o lixo em queda e a nave."""
import math
import random

import pygame

from .config import (BIN_MOUTH_Y, Difficulty, HALF, ITEM_SIZE, LANE_W, LANES, W)
from .drawing import D
from .text import TEXT
from .utils import clamp


class Trash:
    """Um residuo caindo. O jogador o empurra para os lados ate a lixeira certa."""

    def __init__(self, idef, x, y):
        self.idef = idef
        self.x = x
        self.y = y
        self.age = 0.0
        self.tilt = 0.0
        self.lane = self._lane_at(x)

    @staticmethod
    def _lane_at(x):
        return clamp(int(x // LANE_W), 0, LANES - 1)

    @property
    def reached_mouth(self):
        """True quando chegou na boca das lixeiras (hora de contar acerto/erro)."""
        return self.y >= BIN_MOUTH_Y - 20

    def update(self, dt, direction, fast, level):
        """direction: -1 esquerda, 0 parado, 1 direita. fast: acelerar a queda."""
        self.age += dt
        self.x = clamp(self.x + direction * Difficulty.move_speed(level) * dt, HALF, W - HALF)
        self.tilt += (direction * 12 - self.tilt) * min(1.0, dt * 10)
        self.y += Difficulty.fall_speed(level) * (3.2 if fast else 1.0) * dt
        self.lane = self._lane_at(self.x)

    def draw(self, surf, assets):
        spr = assets.sprite_for(self.idef)
        scale = min(1.0, 0.45 + self.age * 3.0)
        img = spr
        if scale < 1.0:
            sz = max(4, int(ITEM_SIZE * scale))
            img = pygame.transform.smoothscale(spr, (sz, sz))
        if abs(self.tilt) > 0.6:
            img = pygame.transform.rotate(img, -self.tilt)
        surf.blit(img, img.get_rect(center=(int(self.x), int(self.y))))
        TEXT.draw(surf, self.idef.name, 17, (255, 255, 255), (self.x, self.y + HALF + 12), "center",
                  bold=True, shadow=(0, 0, 0), max_w=190)


class Ship:
    """A nave alienigena que despeja o lixo. Tambem aparece no menu."""
    BEAM_TIME = 0.35
    LIGHT_COLORS = ((255, 224, 90), (110, 240, 255), (255, 120, 190))

    def __init__(self):
        self.bob = 0.0            # fase da oscilacao (continua entre menu e jogo)
        self.reset()

    def reset(self):
        self.x = W / 2
        self.target = W / 2
        self.beam_t = 0.0

    def tick(self, dt):
        self.bob += dt

    def sway(self, t):
        """Vai e volta pela tela (usado no menu)."""
        self.x = W / 2 + math.sin(t * 0.6) * 430

    def follow_target(self, dt, level):
        """Desliza ate o ponto alvo; quanto maior o nivel, mais rapido."""
        rate = 4.0 + 0.15 * level
        self.x += (self.target - self.x) * min(1.0, dt * rate)
        if self.beam_t > 0:
            self.beam_t -= dt

    @property
    def aligned(self):
        """Chegou perto do alvo e ja pode soltar o proximo lixo."""
        return abs(self.target - self.x) < 40

    def choose_target(self):
        """Sorteia a proxima posicao (longe da atual)."""
        for _ in range(8):
            t = random.uniform(160, W - 160)
            if abs(t - self.x) > 240:
                break
        self.target = t

    def fire_beam(self):
        self.beam_t = self.BEAM_TIME

    def draw(self, surf, assets, t, cy, with_beam=True):
        cx = self.x
        if with_beam and self.beam_t > 0:
            p = clamp(self.beam_t / self.BEAM_TIME, 0.0, 1.0)
            assets.beam.set_alpha(int(255 * p))
            surf.blit(assets.beam, (int(cx) - 70, int(cy) + 38))
        surf.blit(assets.ship, (int(cx) - 90, int(cy) - 55))
        for i in range(7):
            dx = -60 + i * 20
            ly = 64 + 10 * (1 - (dx / 88.0) ** 2) ** 0.5
            on = (int(t * 4) + i) % 2 == 0
            col = self.LIGHT_COLORS[i % 3] if on else (90, 96, 120)
            D.circle(surf, col, (int(cx + dx), int(cy - 55 + ly)), 4)
