# -*- coding: utf-8 -*-
"""Marcos de conhecimento e títulos da progressão do ECO NAVE."""

TITLE_MILESTONES = {
    3: {
        "title": "Aprendiz Consciente",
        "message": "Cada escolha correta ajuda a construir um futuro mais sustentável!",
    },
    5: {
        "title": "Agente da Reciclagem",
        "message": "Você já reconhece muitos materiais e sabe encaminhá-los melhor.",
    },
    10: {
        "title": "Especialista em Resíduos",
        "message": "Seu conhecimento sobre reciclagem está evoluindo. Continue fazendo a diferença!",
    },
    15: {
        "title": "Mestre da Economia Circular",
        "message": "Você entende que reutilizar e recuperar materiais mantém recursos em circulação.",
    },
    20: {
        "title": "Guardião do Planeta",
        "message": "Sua jornada inspira escolhas responsáveis do começo ao fim do ciclo.",
    },
}


def title_for_level(level):
    """Retorna os dados do título do nível, ou None quando não há marco."""
    return TITLE_MILESTONES.get(int(level))


def highest_title_for_level(level):
    """Retorna o maior título já alcançado até o nível informado."""
    candidates = [(n, data["title"]) for n, data in TITLE_MILESTONES.items() if n <= int(level)]
    return max(candidates, default=(0, "Ainda não conquistado"))[1]
