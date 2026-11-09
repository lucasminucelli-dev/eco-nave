# -*- coding: utf-8 -*-
"""Configuracoes gerais do jogo: tela, faixas das lixeiras, vidas e dificuldade."""

TITLE = "ECO NAVE - Desafio do Descarte"
W, H = 1280, 800
FPS = 60

LANES = 10
LANE_W = W // LANES              # largura da "faixa" de cada lixeira (128)
ITEM_SIZE = 84                   # tamanho do lixo na tela
HALF = ITEM_SIZE // 2
PLATE_H = 46                     # placa com o nome da lixeira
PLATE_Y = H - PLATE_H - 8
BIN_BODY_TOP = PLATE_Y - 4 - 80  # topo do corpo da lixeira
BIN_MOUTH_Y = BIN_BODY_TOP - 6   # boca da lixeira
SHIP_Y = 100

START_LIVES = 3
MAX_LIVES = 5
ITEMS_PER_LEVEL = 5              # acertos para subir de nivel
RANKING_SIZE = 10
NAME_MAX = 12


class Difficulty:
    """Curvas de dificuldade: tudo cresce aos poucos com o nivel, com um teto."""

    @staticmethod
    def fall_speed(level):
        """Velocidade de queda (px/s)."""
        return min(130 + 10 * (level - 1), 420)

    @staticmethod
    def move_speed(level):
        """Velocidade lateral do lixo (px/s)."""
        return min(470 + 5 * (level - 1), 620)

    @staticmethod
    def spawn_delay(level):
        """Pausa (s) entre um lixo e o proximo."""
        return max(0.35, 0.9 - 0.03 * (level - 1))
