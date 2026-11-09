# -*- coding: utf-8 -*-
"""Classe base das telas (estados) do jogo."""
import pygame


class GameState:
    """Uma tela do jogo (menu, partida, pausa...). Cada subclasse cuida de seus proprios eventos,
    atualizacao e desenho. O objeto 'game' da acesso ao que e compartilhado entre telas."""

    allow_mute = True      # a tecla M liga/desliga o som nesta tela?

    def __init__(self, game):
        self.game = game

    # ---- ciclo de vida
    def enter(self, **kwargs):
        """Chamado quando a tela passa a ser a ativa."""

    def exit(self):
        """Chamado quando a tela deixa de ser a ativa."""

    # ---- entrada
    def handle_event(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if self.allow_mute:
            if ev.key == pygame.K_m:
                self.game.audio.toggle_mute()
                return
            if ev.key == pygame.K_LEFTBRACKET:
                self.game.audio.adjust_music(-0.05)
                return
            if ev.key == pygame.K_RIGHTBRACKET:
                self.game.audio.adjust_music(0.05)
                return
            if ev.key == pygame.K_MINUS:
                self.game.audio.adjust_fx(-0.05)
                return
            if ev.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.game.audio.adjust_fx(0.05)
                return
        self.handle_key(ev.key)

    def handle_key(self, key):
        """Tecla pressionada (ja descontada a tecla M)."""

    def on_focus_lost(self):
        """A janela perdeu o foco."""

    # ---- atualizacao e desenho
    def update(self, dt):
        """Por padrao, so as estrelas do fundo se mexem."""
        self.game.backdrop.update_stars(dt)

    def draw(self, surf):
        raise NotImplementedError

    def shake_amplitude(self):
        """Tremor de tela em pixels (0 = sem tremor)."""
        return 0.0


class AttractState(GameState):
    """Telas com fundo animado e a nave passeando (menu e ranking)."""

    def update(self, dt):
        super().update(dt)
        game = self.game
        game.ship.tick(dt)
        game.backdrop.update_floaters(dt)
        game.ship.sway(game.t)

    def draw_backdrop(self, surf):
        game = self.game
        game.backdrop.draw(surf, game.assets, game.t, with_floaters=True)
