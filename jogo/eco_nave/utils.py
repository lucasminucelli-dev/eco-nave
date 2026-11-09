# -*- coding: utf-8 -*-
"""Funcoes pequenas de matematica, cor e formatacao."""


def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    """Mistura duas cores RGB."""
    return (int(lerp(c1[0], c2[0], t)), int(lerp(c1[1], c2[1], t)), int(lerp(c1[2], c2[2], t)))


def shade(c, f):
    """Clareia (f > 1) ou escurece (f < 1) uma cor RGB."""
    return (clamp(int(c[0] * f), 0, 255), clamp(int(c[1] * f), 0, 255), clamp(int(c[2] * f), 0, 255))


def fmt(n):
    """Formata inteiro com ponto de milhar (padrao pt-BR)."""
    return f"{n:,}".replace(",", ".")
