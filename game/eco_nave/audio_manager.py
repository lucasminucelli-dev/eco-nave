# -*- coding: utf-8 -*-
"""Gerencia música de fundo e efeitos em canais independentes."""
import os
import pygame


class AudioManager:
    def __init__(self, sound_fx, music_path=None):
        self.sound_fx = sound_fx
        self.music_path = music_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "audio", "eco_nave_theme.ogg")
        self.music_volume = 0.28
        self.fx_volume = 0.65
        self.muted = False
        self.music_loaded = False
        self.music_available = False
        self.music_paused = False
        self._load_music()
        self.sound_fx.set_volume(self.fx_volume)

    def _load_music(self):
        try:
            if not pygame.mixer.get_init():
                return
            candidates = [self.music_path]
            wav_fallback = os.path.splitext(self.music_path)[0] + ".wav"
            if wav_fallback != self.music_path:
                candidates.append(wav_fallback)
            for candidate in candidates:
                if not os.path.isfile(candidate):
                    continue
                try:
                    pygame.mixer.music.load(candidate)
                    self.music_path = candidate
                    pygame.mixer.music.set_volume(self.music_volume)
                    self.music_loaded = True
                    self.music_available = True
                    return
                except Exception:
                    continue
        except Exception:
            pass
        self.music_loaded = False
        self.music_available = False

    def play_music(self):
        if not self.music_loaded:
            return False
        try:
            if not pygame.mixer.get_init():
                return False
            if self.music_paused:
                pygame.mixer.music.unpause()
            else:
                busy = pygame.mixer.music.get_busy()
                if not busy:
                    pygame.mixer.music.play(-1, fade_ms=900)
            self.music_paused = False
            self._apply_music_volume()
            return True
        except Exception:
            self.music_available = False
            return False

    def pause_music(self):
        if not self.music_loaded:
            return
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.music_paused = True
        except Exception:
            pass

    def resume_music(self):
        if self.music_loaded:
            self.play_music()

    def stop_music(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.fadeout(450)
        except Exception:
            pass
        self.music_paused = False

    def _apply_music_volume(self):
        try:
            pygame.mixer.music.set_volume(0.0 if self.muted else self.music_volume)
        except Exception:
            pass

    def set_music_volume(self, value):
        self.music_volume = max(0.0, min(1.0, float(value)))
        self._apply_music_volume()

    def set_fx_volume(self, value):
        self.fx_volume = max(0.0, min(1.0, float(value)))
        self.sound_fx.set_volume(self.fx_volume)

    def adjust_music(self, delta):
        self.set_music_volume(self.music_volume + delta)

    def adjust_fx(self, delta):
        self.set_fx_volume(self.fx_volume + delta)

    def toggle_mute(self):
        self.muted = not self.muted
        self.sound_fx.muted = self.muted
        self._apply_music_volume()
        return self.muted
