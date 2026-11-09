# -*- coding: utf-8 -*-
"""A classe Game: laco principal, troca de telas e objetos compartilhados entre elas."""
import random

import pygame

from .assets import Assets
from .audio_manager import AudioManager
from .backdrop import Backdrop
from .config import FPS, H, W
from .entities import Ship
from .events import FOCUS_LOST
from .facts import random_fact
from .ranking import RankingStore
from .progress_store import ProgressStore
from .session import Session
from .sound import SoundFx
from .states import (MenuState, NameEntryState, PausedState, PlayingState, RankingState,
                     WorkshopState, CodexState, RealWorldState)


class Game:
    def __init__(self, screen, ranking_path=None):
        self.screen = screen
        self.scene = pygame.Surface((W, H)).convert()
        self.assets = Assets()
        self.snd = SoundFx()
        self.audio = AudioManager(self.snd)
        self.ranking = RankingStore(ranking_path)
        self.progress_store = ProgressStore()
        self.running = True
        self.t = 0.0                       # tempo total (s), usado nas animacoes
        self.fact = random_fact()          # curiosidade mostrada na pausa e no fim de jogo
        self.backdrop = Backdrop()
        self.ship = Ship()
        self.session = Session(self.assets, self.snd, self.ship, self.progress_store)
        self.states = {
            "menu": MenuState(self),
            "playing": PlayingState(self),
            "paused": PausedState(self),
            "name": NameEntryState(self),
            "ranking": RankingState(self),
            "workshop": WorkshopState(self),
            "codex": CodexState(self),
            "real_world": RealWorldState(self),
        }
        self.state_name = None
        self.state = None
        self.set_state("menu")

    # ------------------------------------------------------------------ telas
    def set_state(self, name, **kwargs):
        """Troca de tela. Os argumentos vao para o enter() da nova tela."""
        if self.state is not None:
            self.state.exit()
        previous_name = self.state_name
        self.state_name = name
        self.state = self.states[name]
        self.state.enter(**kwargs)
        if name == "paused":
            self.audio.pause_music()
        else:
            if previous_name == "paused":
                self.audio.resume_music()
            else:
                self.audio.play_music()

    def start_game(self):
        self.set_state("playing", new_game=True)

    # ---------------------------------------------------------------- eventos
    def handle_event(self, ev):
        if ev.type == pygame.QUIT:
            self.running = False
        elif FOCUS_LOST is not None and ev.type == FOCUS_LOST:
            self.state.on_focus_lost()
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
            try:
                pygame.display.toggle_fullscreen()
            except Exception:
                pass
        else:
            self.state.handle_event(ev)

    # ------------------------------------------------------- atualizar e desenhar
    def update(self, dt):
        self.t += dt
        self.state.update(dt)

    def draw(self):
        surf = self.scene
        self.state.draw(surf)
        ox = oy = 0
        amp = self.state.shake_amplitude()
        if amp > 0:
            ox, oy = random.randint(-int(amp), int(amp)), random.randint(-int(amp), int(amp))
            self.screen.fill((0, 0, 0))
        self.screen.blit(surf, (ox, oy))

    # ---------------------------------------------------------------- laco principal
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = min(clock.tick(FPS) / 1000.0, 0.05)
            for ev in pygame.event.get():
                self.handle_event(ev)
            self.update(dt)
            self.draw()
            pygame.display.flip()
