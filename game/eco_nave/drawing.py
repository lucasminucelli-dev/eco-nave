# -*- coding: utf-8 -*-
"""Helpers de desenho por formas (usados pelos sprites e pelos itens de lixo)."""
import math

import pygame

D = pygame.draw


def blob(cx, cy, rx, ry, ang_deg, n=32):
    """Pontos de uma elipse rotacionada (eixo 'ry' inclinado 'ang' a partir da vertical)."""
    a = math.radians(ang_deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        u, v = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + u * ca + v * sa, cy - u * sa + v * ca))
    return pts


def hexagon(cx, cy, r, rot=0.0):
    return [(cx + r * math.cos(math.radians(60 * i) + rot), cy + r * math.sin(math.radians(60 * i) + rot))
            for i in range(6)]


def draw_recycle(surf, cx, cy, r, color, width):
    """Simbolo de reciclagem (tres setas em circulo)."""
    for k in range(3):
        a0 = k * 120 + 12
        a1 = a0 + 78
        pts = []
        for a in range(a0, a1 + 1, 6):
            rad = math.radians(a)
            pts.append((cx + r * math.cos(rad), cy - r * math.sin(rad)))
        D.lines(surf, color, False, pts, max(1, int(width)))
        for p in pts:
            D.circle(surf, color, (int(p[0]), int(p[1])), max(1, int(width / 2)))
        ex, ey = pts[-1]
        ang = math.radians(a1)
        tx, ty = -math.sin(ang), -math.cos(ang)
        nx, ny = -ty, tx
        head = width * 1.9
        tip = (ex + tx * head * 1.3, ey + ty * head * 1.3)
        p1 = (ex + nx * head, ey + ny * head)
        p2 = (ex - nx * head, ey - ny * head)
        D.polygon(surf, color, [tip, p1, p2])


def blit_rotated(surf, image, pos, pivot, angle):
    """Desenha 'image' girada 'angle' graus (anti-horario) em torno do ponto 'pivot' da imagem,
    que fica fixo em 'pos' na tela."""
    image_rect = image.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
    offset = pygame.math.Vector2(pos) - pygame.math.Vector2(image_rect.center)
    rotated_offset = offset.rotate(-angle)
    center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated = pygame.transform.rotate(image, angle)
    surf.blit(rotated, rotated.get_rect(center=center))


def rr(s, color, rect, radius=6, outline=None, width=3):
    """Retangulo arredondado com contorno opcional."""
    D.rect(s, color, rect, 0, border_radius=radius)
    if outline is not None:
        D.rect(s, outline, rect, width, border_radius=radius)


def drawn_rotated(s, fn, angle):
    """Executa 'fn' num canvas 128x128 e cola o resultado girado em 's'."""
    t = pygame.Surface((128, 128), pygame.SRCALPHA)
    fn(t)
    r = pygame.transform.rotate(t, angle)
    s.blit(r, r.get_rect(center=(64, 64)))
