#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECO NAVE - Desafio do Descarte
==============================
Ponto de entrada do jogo. Para jogar:

    pip install pygame        (precisa do pygame 2.x)
    python main.py

Teclas
------
    <- ->  (ou A / D)   mover o lixo
    v      (ou S)       acelerar a queda
    P / ESC             pausar
    M                   ligar/desligar o som
    F11                 tela cheia
    ENTER               confirmar / jogar

O ranking fica salvo em "ranking.txt", na mesma pasta deste arquivo.
Nenhuma imagem ou som externo e necessario: tudo e desenhado/gerado no codigo.
"""
import sys

try:
    import pygame
except ImportError:  # pragma: no cover
    print("O pygame nao esta instalado. Instale com:  pip install pygame")
    sys.exit(1)

from eco_nave import Game
from eco_nave.config import H, TITLE, W


def create_window():
    """Abre a janela (escalavel, com vsync quando possivel)."""
    flags = pygame.SCALED | pygame.RESIZABLE
    try:
        return pygame.display.set_mode((W, H), flags, vsync=1)
    except Exception:
        try:
            return pygame.display.set_mode((W, H), flags)
        except Exception:
            return pygame.display.set_mode((W, H))


def main():
    if pygame.version.vernum[0] < 2:
        print("Este jogo precisa do pygame 2.x. Atualize com:  pip install --upgrade pygame")
        sys.exit(1)
    try:
        pygame.mixer.pre_init(22050, -16, 1, 512)
    except Exception:
        pass
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = create_window()
    Game(screen).run()
    pygame.quit()


if __name__ == "__main__":
    main()
