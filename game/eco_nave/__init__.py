# -*- coding: utf-8 -*-
"""ECO NAVE. Game é importado sob demanda para permitir testes de regras sem Pygame."""
__all__ = ["Game"]


def __getattr__(name):
    if name == "Game":
        from .game import Game
        return Game
    raise AttributeError(name)
