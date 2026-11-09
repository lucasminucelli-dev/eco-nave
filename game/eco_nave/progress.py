# -*- coding: utf-8 -*-
"""Pontuacao, vidas, sequencia de acertos e nivel de uma partida."""
from dataclasses import dataclass

from .config import ITEMS_PER_LEVEL, MAX_LIVES, START_LIVES
from .achievements import title_for_level, highest_title_for_level


@dataclass
class HitResult:
    points: int
    leveled_up: bool
    extra_life: bool
    title_unlocked: object = None


class Progress:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = START_LIVES
        self.streak = 0
        self.best_streak = 0
        self.correct = 0
        self.wrong = 0
        self.level = 1
        self.highest_title = "Ainda não conquistado"

    @property
    def combo(self):
        """Multiplicador de pontos: +1 a cada 5 acertos seguidos (maximo x5)."""
        return 1 + min(self.streak // 5, 4)

    @property
    def level_progress(self):
        """Fracao (0 a 1) do caminho ate o proximo nivel."""
        return (self.correct % ITEMS_PER_LEVEL) / ITEMS_PER_LEVEL

    @property
    def accuracy(self):
        """Percentual de acertos (0 a 100)."""
        total = self.correct + self.wrong
        return int(100 * self.correct / total) if total else 0

    @property
    def game_over(self):
        return self.lives <= 0

    def register_hit(self):
        old_level = self.level
        self.correct += 1
        self.streak += 1
        self.best_streak = max(self.best_streak, self.streak)
        points = (100 + 10 * (old_level - 1)) * self.combo
        self.score += points
        self.level = 1 + self.correct // ITEMS_PER_LEVEL
        extra_life = False
        if self.streak % 10 == 0 and self.lives < MAX_LIVES:
            self.lives += 1
            extra_life = True
        title = title_for_level(self.level) if self.level > old_level else None
        if title:
            self.highest_title = title["title"]
        elif self.level >= 3:
            self.highest_title = highest_title_for_level(self.level)
        return HitResult(points, self.level > old_level, extra_life, title)

    def register_miss(self):
        self.wrong += 1
        self.streak = 0
        self.lives -= 1
