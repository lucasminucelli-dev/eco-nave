# -*- coding: utf-8 -*-
"""Definicao e registro dos itens de lixo.

Cada item tem um desenho feito so com formas do pygame num canvas de 128x128 px,
depois reduzido (com suavizacao) para ITEM_SIZE. Os desenhos ficam nos arquivos
desta pasta, um por lixeira, e se registram aqui com o decorador @item.
"""
import pygame
import re
import unicodedata

from ..bins import BINS
from ..config import ITEM_SIZE

CANVAS = 128


class ItemDef:
    """Um tipo de residuo: nome, dica educativa, lixeira correta e desenho."""

    def __init__(self, bin_index, name, tip, draw, item_id=None, category=None,
                 destination=None, fact=None, reuse=None, is_electronic=False,
                 is_component=False, spawn_weight=1, reverse_logistics=False):
        self.bin_index = bin_index
        self.name = name
        self.tip = tip
        self.draw = draw
        self.item_id = item_id or self.make_id(name)
        self.category = category or BINS[bin_index].key
        if destination:
            self.destination = destination
        elif reverse_logistics:
            self.destination = "Ponto de recebimento do sistema de logística reversa; confirme quais produtos são aceitos."
        else:
            self.destination = ("Lixeira " + BINS[bin_index].name.lower() +
                                " — confirme as regras da coleta local.")
        self.fact = fact or tip
        self.reuse = reuse or "Avalie se o objeto pode ser reutilizado antes do descarte."
        self.is_electronic = bool(is_electronic)
        self.is_component = bool(is_component)
        self.spawn_weight = max(1, int(spawn_weight))
        self.reverse_logistics = bool(reverse_logistics)

    @staticmethod
    def make_id(name):
        normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[^a-z0-9]+", "_", normalized.lower()).strip("_")

    @property
    def ewaste(self):
        """Compatibilidade com código antigo. Não controla o peso do sorteio."""
        return self.is_electronic or self.is_component

    def render(self, size=ITEM_SIZE):
        """Desenha o item e devolve a imagem ja reduzida para 'size' px."""
        canvas = pygame.Surface((CANVAS, CANVAS), pygame.SRCALPHA)
        self.draw(canvas)
        return pygame.transform.smoothscale(canvas, (size, size))


class ItemCatalog:
    """Lista de todos os itens do jogo, na ordem em que foram registrados."""

    def __init__(self):
        self._items = []

    def register(self, bin_key, name, tip, ewaste=False, **metadata):
        """Decorador de registro.

        O argumento legado ``ewaste`` é aceito para não quebrar módulos antigos,
        mas não altera o sorteio. Use os metadados explícitos para descrever
        equipamentos/componentes e ``spawn_weight`` para ponderar aparições.
        """
        def deco(fn):
            self._items.append(ItemDef(
                BINS.index_of(bin_key), name, tip, fn,
                item_id=metadata.pop("item_id", None),
                category=metadata.pop("category", bin_key),
                destination=metadata.pop("destination", None),
                fact=metadata.pop("fact", None),
                reuse=metadata.pop("reuse", None),
                is_electronic=metadata.pop("is_electronic", False),
                is_component=metadata.pop("is_component", False),
                spawn_weight=metadata.pop("spawn_weight", 1),
                reverse_logistics=metadata.pop("reverse_logistics", False),
            ))
            if metadata:
                unknown = ", ".join(sorted(metadata))
                raise TypeError("Metadados desconhecidos para item: " + unknown)
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

    def by_id(self, item_id):
        return next((it for it in self._items if it.item_id == item_id), None)

    def ids(self):
        return {it.item_id for it in self._items}


ITEM_CATALOG = ItemCatalog()
item = ITEM_CATALOG.register
