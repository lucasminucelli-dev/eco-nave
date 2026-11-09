# -*- coding: utf-8 -*-
"""Efeitos sonoros sintetizados no codigo (nenhum arquivo de audio e necessario)."""
import array
import math

import pygame


class SoundFx:
    def __init__(self):
        self.enabled = False
        self.muted = False
        self.volume = 0.65
        self.fx = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 1, 512)
            info = pygame.mixer.get_init()
            if not info or info[1] != -16:
                return
            self.rate, _fmt, self.channels = info
            self.fx = {
                "ok": self._tone([(660, 0.07), (880, 0.13)], "tri", 0.30),
                "bad": self._tone([(190, 0.12), (130, 0.24)], "square", 0.22),
                "level": self._tone([(523, 0.08), (659, 0.08), (784, 0.08), (1046, 0.20)], "tri", 0.30),
                "over": self._tone([(392, 0.18), (330, 0.18), (262, 0.18), (196, 0.45)], "square", 0.20),
                "spawn": self._tone([(360, 0.05), (480, 0.06)], "sine", 0.22),
                "select": self._tone([(620, 0.05)], "tri", 0.25),
                "achievement": self._tone([(523, 0.10), (659, 0.10), (784, 0.10),
                                           (1046, 0.14), (1318, 0.25)], "tri", 0.32),
            }
            self.enabled = True
        except Exception:
            self.enabled = False

    def _tone(self, notes, wave, vol):
        data = array.array("h")
        for freq, dur in notes:
            n = max(1, int(self.rate * dur))
            attack = max(1, int(self.rate * 0.004))
            for i in range(n):
                ph = (i * freq / self.rate) % 1.0
                if wave == "square":
                    v = 1.0 if ph < 0.5 else -1.0
                elif wave == "tri":
                    v = 4 * abs(ph - 0.5) - 1
                else:
                    v = math.sin(2 * math.pi * ph)
                env = min(1.0, i / attack) * (1 - i / n) ** 0.8
                smp = int(32767 * vol * v * env)
                for _c in range(self.channels):
                    data.append(smp)
        return pygame.mixer.Sound(buffer=data.tobytes())

    def set_volume(self, value):
        self.volume = max(0.0, min(1.0, float(value)))
        for sound in self.fx.values():
            try:
                sound.set_volume(self.volume)
            except Exception:
                pass

    def play(self, name):
        if self.enabled and not self.muted:
            try:
                sound = self.fx.get(name)
                if sound is not None:
                    sound.play()
            except Exception:
                pass

    def toggle(self):
        self.muted = not self.muted
        if not self.muted:
            self.play("select")
