# -*- coding: utf-8 -*-
"""Sorteio do proximo residuo, com regras de justica."""
import random

from .config import BIN_MOUTH_Y, Difficulty, LANE_W, LANES, SHIP_Y


class ItemSpawner:
    def __init__(self, catalog):
        self.catalog = catalog
        self.reset()

    def reset(self):
        self.last_item = None
        self.last_bins = []

    @staticmethod
    def reach(level):
        """Distancia lateral (px) que da tempo de percorrer antes do lixo chegar embaixo.
        Usa so 70% do tempo teorico: sobra margem para o tempo de reacao."""
        fall_time = (BIN_MOUTH_Y - 20 - (SHIP_Y + 50)) / Difficulty.fall_speed(level)
        return Difficulty.move_speed(level) * fall_time * 0.7

    def pick(self, x, level):
        """Escolhe um item cuja lixeira ainda e alcancavel a partir de 'x'."""
        choices = list(range(LANES))
        # Justica: so sorteia lixeiras que ainda sao alcancaveis a partir de onde o lixo nasce.
        r = self.reach(level)
        near = [i for i in choices if abs((i * LANE_W + LANE_W / 2) - x) - LANE_W / 2 <= r]
        if near:
            choices = near
        # evita 3 lixeiras iguais seguidas
        if len(self.last_bins) >= 2 and self.last_bins[-1] == self.last_bins[-2] and len(choices) > 1 \
                and self.last_bins[-1] in choices:
            choices.remove(self.last_bins[-1])
        b = random.choice(choices)
        candidates = self.catalog.for_bin(b)
        pool = [it for it in candidates if it is not self.last_item]
        if not pool:
            pool = candidates
        # Cada item usa seu peso explicito; a flag legada ewaste nao altera o sorteio.
        idef = random.choices(pool, weights=[it.spawn_weight for it in pool])[0]
        self.last_item = idef
        self.last_bins = (self.last_bins + [b])[-3:]
        return idef
