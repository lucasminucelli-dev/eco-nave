# -*- coding: utf-8 -*-
"""Definicao e registro dos itens de lixo.

Cada item tem um desenho feito so com formas do pygame num canvas de 128x128 px,
depois reduzido (com suavizacao) para ITEM_SIZE. Os desenhos ficam nos arquivos
desta pasta, um por lixeira, e se registram aqui com o decorador @item.
"""
import pygame

from ..bins import BINS
from ..config import ITEM_SIZE

CANVAS = 128


class ItemDef:
    """Um tipo de residuo: nome, dica educativa, lixeira correta e desenho."""

    def __init__(self, bin_index, name, tip, draw, ewaste):
        self.bin_index = bin_index
        self.name = name
        self.tip = tip
        self.draw = draw
        self.ewaste = ewaste          # True = lixo eletronico (aparece mais no sorteio)

    def render(self, size=ITEM_SIZE):
        """Desenha o item e devolve a imagem ja reduzida para 'size' px."""
        canvas = pygame.Surface((CANVAS, CANVAS), pygame.SRCALPHA)
        self.draw(canvas)
        return pygame.transform.smoothscale(canvas, (size, size))


class ItemCatalog:
    """Lista de todos os itens do jogo, na ordem em que foram registrados."""

    def __init__(self):
        self._items = []

    def register(self, bin_key, name, tip, ewaste=False):
        """Decorador: registra a funcao de desenho como um novo item."""
        def deco(fn):
            self._items.append(ItemDef(BINS.index_of(bin_key), name, tip, fn, ewaste))
            return fn
        return deco

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def for_bin(self, bin_index):
        """Itens que pertencem a uma lixeira."""
        return [it for it in self._items if it.bin_index == bin_index]


ITEM_CATALOG = ItemCatalog()
item = ITEM_CATALOG.register
