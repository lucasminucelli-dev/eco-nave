# -*- coding: utf-8 -*-
"""A fileira de 10 lixeiras na base da tela, com tampas animadas."""
import math

from .bins import BINS
from .config import BIN_BODY_TOP, LANE_W, LANES, PLATE_H, PLATE_Y
from .drawing import D, blit_rotated
from .utils import mix


class BinRow:
    HINT_TIME = 2.2

    def __init__(self):
        self.reset()

    def reset(self):
        self.open = [0.0] * LANES      # 0 = tampa fechada, 1 = aberta
        self.bounce = [0.0] * LANES    # pulinho ao acertar
        self.shake = [0.0] * LANES     # tremida ao errar
        self.hint_bin = None           # lixeira certa, destacada depois de um erro
        self.hint_time = 0.0

    @staticmethod
    def center_x(i):
        return i * LANE_W + LANE_W // 2

    def pulse_ok(self, i):
        self.bounce[i] = 1.0

    def pulse_bad(self, i):
        self.shake[i] = 1.0

    def show_hint(self, i):
        self.hint_bin = i
        self.hint_time = self.HINT_TIME

    def update(self, dt):
        """Esmaece pulinhos, tremidas e a dica."""
        for i in range(LANES):
            self.bounce[i] = max(0.0, self.bounce[i] - dt * 3.2)
            self.shake[i] = max(0.0, self.shake[i] - dt * 2.6)
        if self.hint_bin is not None:
            self.hint_time -= dt
            if self.hint_time <= 0:
                self.hint_bin = None

    def ease_open(self, dt, hover):
        """Abre a tampa da lixeira sob o lixo (hover) e fecha as outras."""
        for i in range(LANES):
            target = 1.0 if hover == i else 0.0
            self.open[i] += (target - self.open[i]) * min(1.0, dt * 14)

    def draw(self, surf, assets, t, hover=None):
        for i in range(LANES):
            cx = self.center_x(i)
            ox = math.sin(t * 70) * 7 * self.shake[i]
            oy = -abs(math.sin(self.bounce[i] * math.pi)) * 9
            top = BIN_BODY_TOP + oy
            surf.blit(assets.bin_body[i], (cx - 44 + ox, top))
            op = self.open[i]
            if op > 0.05:
                D.ellipse(surf, (6, 8, 12), (cx - 31 + ox, top - 5, 62, 12))
            blit_rotated(surf, assets.bin_lid[i], (cx - 45 + ox, top + 1), (3, 15), op * 62)
            surf.blit(assets.plate[i], (cx - 58, PLATE_Y))
            if hover == i:
                D.rect(surf, (255, 255, 255), (cx - 58, PLATE_Y, 116, PLATE_H), 3, border_radius=7)
        if self.hint_bin is not None:
            i = self.hint_bin
            cx = self.center_x(i)
            pulse = 0.5 + 0.5 * math.sin(t * 12)
            col = mix(BINS[i].glow, (255, 255, 255), pulse)
            D.rect(surf, col, (cx - 62, BIN_BODY_TOP - 30, 124, PLATE_Y + PLATE_H - BIN_BODY_TOP + 36), 4,
                   border_radius=14)
