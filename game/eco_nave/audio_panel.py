# -*- coding: utf-8 -*-
"""Painel de áudio (tecla V): volume da música e dos efeitos, separados, e silenciar tudo."""
import os

import pygame

from .config import W
from .drawing import rr
from .facts import random_fact
from .icons import draw_icon
from .text import TEXT
from .ui import Ui


class AudioPanel:
    """Sobreposição desenhada por cima de qualquer tela. Enquanto está aberto, captura o teclado."""
    STEP = 0.1
    ROWS = ("music", "fx", "mute")

    def __init__(self, game):
        self.game = game
        self.visible = False
        self.row = 0

    def open(self):
        game = self.game
        if game.state_name == "playing":      # abrir o painel durante a partida pausa o jogo
            game.fact = random_fact()
            game.set_state("paused")
        self.visible = True
        self.row = 0

    def close(self):
        self.visible = False

    def handle_event(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        audio = self.game.audio
        k = ev.key
        if k in (pygame.K_ESCAPE, pygame.K_v, pygame.K_RETURN, pygame.K_KP_ENTER):
            self.close()
        elif k == pygame.K_m:
            audio.toggle_mute()
        elif k in (pygame.K_UP, pygame.K_w):
            self.row = (self.row - 1) % len(self.ROWS)
        elif k in (pygame.K_DOWN, pygame.K_s):
            self.row = (self.row + 1) % len(self.ROWS)
        elif k in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
            sign = 1 if k in (pygame.K_RIGHT, pygame.K_d) else -1
            which = self.ROWS[self.row]
            if which == "music":
                audio.adjust_music(sign * self.STEP)
            elif which == "fx":
                audio.adjust_fx(sign * self.STEP)
                self.game.snd.play("ok")        # prévia do volume dos efeitos
            else:
                audio.toggle_mute()

    def draw(self, surf):
        if not self.visible:
            return
        game, audio = self.game, self.game.audio
        surf.blit(game.assets.dim, (0, 0))
        px, py, pw, ph = W // 2 - 300, 220, 600, 330
        Ui.panel(surf, (px, py, pw, ph), alpha=252, border=(150, 190, 230), bw=3)
        draw_icon(surf, "speaker", px + 42, py + 44, 30, (150, 190, 230))
        TEXT.draw(surf, "ÁUDIO", 32, (210, 228, 250), (px + 74, py + 44), "midleft", bold=True)
        rows = (("Música", audio.music_volume), ("Efeitos", audio.fx_volume), ("Silenciar tudo", None))
        for i, (label, value) in enumerate(rows):
            y = py + 100 + i * 66
            sel = i == self.row
            rr(surf, (30, 60, 80) if sel else (14, 22, 42), (px + 24, y - 24, pw - 48, 52), 10,
               (130, 220, 200) if sel else (60, 88, 128), 2)
            TEXT.draw(surf, label, 19, (255, 255, 255), (px + 44, y), "midleft", bold=sel)
            if value is not None:
                bx, bw = px + 220, 250
                rr(surf, (40, 52, 84), (bx, y - 7, bw, 14), 7)
                if value > 0:
                    rr(surf, (110, 240, 150) if not audio.muted else (110, 120, 140),
                       (bx, y - 7, max(14, int(bw * value)), 14), 7)
                TEXT.draw(surf, f"{int(round(value * 100))}%", 18, (230, 238, 250), (bx + bw + 14, y), "midleft", bold=True)
            else:
                TEXT.draw(surf, "SIM" if audio.muted else "NÃO", 19, (255, 214, 120) if audio.muted else (186, 206, 228),
                          (px + 220, y), "midleft", bold=True)
        track = os.path.basename(audio.music_path) if audio.music_available else "sem música (arquivo não encontrado)"
        TEXT.draw(surf, "Faixa: " + track, 14, (170, 190, 216), (W // 2, py + 296), "center", max_w=pw - 50)
        Ui.hint_bar(surf, [("↑", "linha") if False else ("W/S", "linha"), ("A/D", "ajustar"), ("M", "mudo"),
                           ("ESC", "fechar")], py + ph + 28, 15)
