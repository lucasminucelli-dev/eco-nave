# -*- coding: utf-8 -*-
"""Pre-renderiza todos os sprites uma unica vez (precisa de janela ja criada)."""
import pygame

from .bins import BINS
from .config import H, W
from .items import ITEM_CATALOG
from .sprites import SpriteFactory


class Assets:
    def __init__(self):
        f = SpriteFactory
        self.background = f.background().convert()
        self.dim = pygame.Surface((W, H), pygame.SRCALPHA)
        self.dim.fill((2, 4, 14, 175))
        self.lane_glow = [f.lane_glow(b.glow).convert_alpha() for b in BINS]
        self.bin_body = [f.bin_body(b).convert_alpha() for b in BINS]
        self.bin_lid = [f.bin_lid(b).convert_alpha() for b in BINS]
        self.plate = [f.plate(b).convert_alpha() for b in BINS]
        self.ship = f.ship().convert_alpha()
        self.beam = f.beam().convert_alpha()
        self.heart_full = f.heart(28, (240, 70, 90), (120, 20, 40)).convert_alpha()
        self.heart_empty = f.heart(28, (70, 78, 108), (40, 44, 64)).convert_alpha()
        # um sprite por item, na mesma ordem do catalogo
        self.items = [idef.render().convert_alpha() for idef in ITEM_CATALOG]
        self._by_item = {id(idef): spr for idef, spr in zip(ITEM_CATALOG, self.items)}

    def sprite_for(self, idef):
        """Sprite pronto de um ItemDef."""
        return self._by_item[id(idef)]
