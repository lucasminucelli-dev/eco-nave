# -*- coding: utf-8 -*-
"""Regras da Oficina Circular, sem nada de desenho (assim podem ser testadas sozinhas)."""
import random

from .workshop_catalog import (ASSESSMENT_OPTIONS, COMPONENTS, SCENARIOS, component_materials, destination_label)

EVAL_POINTS = 150
PART_POINTS = 100


class WorkshopRun:
    """Uma rodada da oficina: 1 avaliação do equipamento + a triagem de cada componente."""

    def __init__(self, equipment, scenario=None, rng=None, components=COMPONENTS, avoid_key=None):
        self.equipment = equipment
        self.components = list(components)
        self.rng = rng or random.Random()
        if scenario is None:
            pool = [s for s in SCENARIOS if s.key != avoid_key] or list(SCENARIOS)
            scenario = self.rng.choice(pool)
        self.scenario = scenario
        self.eval_choice = None
        self.eval_correct = None
        self.results = {}          # item_id do componente -> (destino escolhido, acertou?)
        self.score = 0

    # ---------------------------------------------------------------- etapa 1
    def evaluate(self, option_key):
        """Registra a avaliação. Devolve (acertou, texto educativo)."""
        if option_key not in {o.key for o in ASSESSMENT_OPTIONS}:
            raise ValueError("opcao desconhecida: " + str(option_key))
        if self.eval_choice is not None:
            raise RuntimeError("avaliacao ja registrada")
        self.eval_choice = option_key
        self.eval_correct = option_key == self.scenario.answer
        if self.eval_correct:
            self.score += EVAL_POINTS
            return True, "Correto! " + self.scenario.explanation
        return False, "Quase. " + self.scenario.wrong[option_key] + " Resposta adequada: " + \
            next(o.title for o in ASSESSMENT_OPTIONS if o.key == self.scenario.answer) + "."

    # ---------------------------------------------------------------- etapa 2
    def classify(self, component, destination_key):
        """Registra a triagem de um componente. Devolve (acertou, texto educativo)."""
        if component.item_id in self.results:
            raise RuntimeError("componente ja triado")
        ok = destination_key == component.destination_key
        self.results[component.item_id] = (destination_key, ok)
        if ok:
            self.score += PART_POINTS
            return True, "Correto! " + component.description
        return False, ("Não é esse o destino. O adequado é " + destination_label(component.destination_key) +
                       ". " + component.description)

    def is_classified(self, component):
        return component.item_id in self.results

    # --------------------------------------------------------------- resultado
    @property
    def parts_done(self):
        return len(self.results)

    @property
    def finished(self):
        return self.eval_choice is not None and self.parts_done == len(self.components)

    @property
    def correct_parts(self):
        return sum(1 for _d, ok in self.results.values() if ok)

    @property
    def wrong_parts(self):
        return self.parts_done - self.correct_parts

    @property
    def decisions(self):
        return self.parts_done + (1 if self.eval_choice is not None else 0)

    @property
    def correct_decisions(self):
        return self.correct_parts + (1 if self.eval_correct else 0)

    @property
    def accuracy(self):
        return int(round(100 * self.correct_decisions / self.decisions)) if self.decisions else 0

    @property
    def perfect(self):
        return self.finished and self.correct_decisions == self.decisions

    def reusable(self):
        """Componentes que podem ser reutilizados (após testes)."""
        return [c for c in self.components if c.destination_key == "reuse"]

    def recoverable_materials(self):
        """Materiais que podem voltar à cadeia produtiva, sem repetir."""
        seen = []
        for c in self.components:
            if c.destination_key == "recovery":
                for m in component_materials(c):
                    if m not in seen:
                        seen.append(m)
        return seen
