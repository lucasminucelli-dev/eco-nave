# -*- coding: utf-8 -*-
"""A partida em si."""
import pygame

from ..facts import random_fact
from .base import GameState


class PlayingState(GameState):
    def enter(self, new_game=False, **kwargs):
        """new_game=True comeca uma partida nova; False apenas retoma (saindo da pausa)."""
        if new_game:
            self.game.session.reset()
            self.game.snd.play("select")

    def handle_key(self, key):
        if key in (pygame.K_p, pygame.K_ESCAPE):
            self.game.fact = random_fact()
            self.game.set_state("paused")

    def on_focus_lost(self):
        self.game.set_state("paused")

    def update(self, dt):
        super().update(dt)
        keys = pygame.key.get_pressed()
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        fast = keys[pygame.K_DOWN] or keys[pygame.K_s]
        direction = (1 if right else 0) - (1 if left else 0)
        if self.game.session.update(dt, direction, fast):
            self.finish_round()

    def finish_round(self):
        """Acabaram as vidas: vai pedir o nome (ou direto ao ranking se nao pontuou)."""
        game = self.game
        game.snd.play("over")
        game.fact = random_fact()
        if game.session.progress.score <= 0:
            game.set_state("ranking", new_entry=None, note="Nenhum ponto desta vez. Tente de novo!")
        else:
            game.set_state("name")

    def draw(self, surf):
        game = self.game
        game.backdrop.draw(surf, game.assets, game.t)
        game.session.draw(surf, game.t)

    def shake_amplitude(self):
        return self.game.session.effects.shake_amplitude
