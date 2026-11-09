# -*- coding: utf-8 -*-
"""As 10 lixeiras da coleta seletiva (na ordem da imagem de referencia)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BinType:
    key: str          # identificador interno
    name: str         # nome da cor, exibido na placa
    material: str     # o que vai nessa lixeira
    color: tuple      # cor do corpo
    glow: tuple       # cor do brilho/destaque
    text_color: tuple  # cor do texto da placa


class BinCatalog:
    """Colecao ordenada de lixeiras; a posicao na lista e a faixa (lane) da tela."""

    def __init__(self, types):
        self._types = list(types)
        self._index = {b.key: i for i, b in enumerate(self._types)}

    def __len__(self):
        return len(self._types)

    def __iter__(self):
        return iter(self._types)

    def __getitem__(self, i):
        return self._types[i]

    def index_of(self, key):
        return self._index[key]


BINS = BinCatalog([
    BinType("azul",     "AZUL",     "papel/papelão",      (30, 80, 195),   (80, 140, 255),  (255, 255, 255)),
    BinType("vermelho", "VERMELHO", "plástico/isopor",    (212, 38, 46),   (255, 96, 96),   (255, 255, 255)),
    BinType("verde",    "VERDE",    "vidro",              (22, 128, 62),   (70, 225, 120),  (255, 255, 255)),
    BinType("amarelo",  "AMARELO",  "metal",              (244, 198, 22),  (255, 232, 90),  (70, 50, 0)),
    BinType("preto",    "PRETO",    "madeira",            (34, 34, 40),    (160, 160, 185), (255, 255, 255)),
    BinType("laranja",  "LARANJA",  "perigosos",          (245, 138, 30),  (255, 185, 90),  (60, 30, 0)),
    BinType("branco",   "BRANCO",   "serviços de saúde",  (242, 242, 244), (255, 255, 255), (40, 40, 46)),
    BinType("roxo",     "ROXO",     "radioativos",        (124, 80, 170),  (195, 145, 255), (255, 255, 255)),
    BinType("marrom",   "MARROM",   "orgânicos",          (148, 88, 48),   (215, 145, 95),  (255, 255, 255)),
    BinType("cinza",    "CINZA",    "não recicláveis",    (106, 108, 114), (195, 197, 205), (255, 255, 255)),
])
