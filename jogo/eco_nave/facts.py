# -*- coding: utf-8 -*-
"""Curiosidades educativas exibidas na pausa e no fim de jogo."""
import random

FACTS = [
    "Celulares e computadores guardam metais valiosos, como cobre, prata e ouro, que podem ser reaproveitados.",
    "Pilhas e baterias têm metais pesados. Jogadas no lixo comum, podem contaminar o solo e a água.",
    "Muitas lojas e fabricantes recebem eletrônicos usados: é a chamada logística reversa.",
    "Consertar, doar ou vender um aparelho antigo evita a geração de lixo eletrônico.",
    "Antes de descartar um celular ou computador, apague todos os seus dados pessoais.",
    "Lâmpadas fluorescentes contêm mercúrio e precisam de descarte específico.",
    "Baterias de lítio danificadas podem pegar fogo. Nunca as jogue no lixo comum.",
    "Reciclar alumínio gasta bem menos energia do que produzir alumínio novo.",
    "O lixo eletrônico é um dos tipos de resíduo que mais crescem no mundo.",
]


def random_fact():
    return random.choice(FACTS)
