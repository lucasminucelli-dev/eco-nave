# -*- coding: utf-8 -*-
"""Catalogo de itens de lixo. Importar os modulos abaixo registra os itens (a ordem importa)."""
from .catalog import ITEM_CATALOG, ItemCatalog, ItemDef, item  # noqa: F401

from . import paper  # noqa: F401
from . import plastic  # noqa: F401
from . import glass  # noqa: F401
from . import metal  # noqa: F401
from . import wood  # noqa: F401
from . import hazardous  # noqa: F401
from . import health  # noqa: F401
from . import radioactive  # noqa: F401
from . import organic  # noqa: F401
from . import nonrecyclable  # noqa: F401
