# -*- coding: utf-8 -*-
"""Itens da lixeira ROXO (radioativos)."""
import math

from ..drawing import D, rr
from .catalog import item


@item("roxo", "Detector de fumaça", "Alguns detectores de fumaça têm uma pequena fonte radioativa. Devolva ao fabricante.", True)
def _(s):
    D.circle(s, (196, 196, 192), (64, 64), 52)
    D.circle(s, (240, 240, 234), (64, 64), 48)
    D.circle(s, (214, 214, 208), (64, 64), 34)
    for k in range(16):
        a = math.radians(k * 22.5)
        D.line(s, (150, 150, 146), (64 + 38 * math.cos(a), 64 + 38 * math.sin(a)),
               (64 + 45 * math.cos(a), 64 + 45 * math.sin(a)), 4)
    D.circle(s, (248, 248, 244), (64, 64), 15)
    D.circle(s, (160, 160, 155), (64, 64), 15, 2)
    D.circle(s, (232, 44, 44), (64, 64), 5)


@item("roxo", "Fonte radioativa", "Materiais radioativos só podem ser descartados por órgãos especializados.")
def _(s):
    D.circle(s, (252, 218, 44), (64, 64), 54)
    D.circle(s, (30, 30, 34), (64, 64), 54, 5)
    r_out, r_in = 38, 15
    for k in range(3):
        base = math.radians(90 + k * 120)
        pts = []
        for j in range(11):
            a = base - math.radians(30) + math.radians(60) * j / 10
            pts.append((64 + r_out * math.cos(a), 64 - r_out * math.sin(a)))
        for j in range(10, -1, -1):
            a = base - math.radians(30) + math.radians(60) * j / 10
            pts.append((64 + r_in * math.cos(a), 64 - r_in * math.sin(a)))
        D.polygon(s, (30, 30, 34), pts)
    D.circle(s, (30, 30, 34), (64, 64), 8)


@item("roxo", "Relógio luminoso antigo", "Relógios antigos com tinta luminosa podiam ter rádio, um material radioativo.", True)
def _(s):
    rr(s, (124, 82, 50), (50, 6, 28, 46), 5, (80, 50, 30), 2)
    rr(s, (124, 82, 50), (50, 76, 28, 46), 5, (80, 50, 30), 2)
    D.circle(s, (192, 194, 200), (64, 64), 42)
    D.circle(s, (110, 112, 120), (64, 64), 42, 3)
    D.circle(s, (22, 48, 34), (64, 64), 35)
    for k in range(12):
        a = math.radians(k * 30)
        r1 = 24 if k % 3 == 0 else 28
        D.line(s, (150, 255, 160), (64 + r1 * math.cos(a), 64 + r1 * math.sin(a)),
               (64 + 31 * math.cos(a), 64 + 31 * math.sin(a)), 4 if k % 3 == 0 else 2)
    D.line(s, (190, 255, 196), (64, 64), (64, 42), 4)
    D.line(s, (190, 255, 196), (64, 64), (82, 72), 3)
    D.circle(s, (190, 255, 196), (64, 64), 4)
