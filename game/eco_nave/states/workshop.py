# -*- coding: utf-8 -*-
"""Oficina Circular: avaliação e triagem simulada de um notebook."""
import math
import pygame

from ..config import H, W
from ..drawing import D, rr
from ..text import TEXT
from ..ui import Ui
from ..workshop_catalog import COMPONENTS, DESTINATIONS, EQUIPMENT_CATALOG, render_component, render_equipment
from .base import AttractState


ASSESSMENT_OPTIONS = [
    ("Reutilizar ou doar imediatamente", "Ainda é preciso corrigir a falha conhecida antes de repassar o equipamento."),
    ("Encaminhar para manutenção", "Correto! Um profissional pode substituir a bateria e testar o notebook antes de doar ou reutilizar."),
    ("Logística reversa / reciclagem especializada", "Essa é a rota adequada quando o equipamento não pode ser recuperado. Neste cenário, a bateria pode ser substituída, então vale reparar primeiro."),
]


class WorkshopState(AttractState):
    """Desafio modular de oficina; novos equipamentos podem ganhar cenários próprios."""

    def __init__(self, game):
        super().__init__(game)
        self.equipment = EQUIPMENT_CATALOG[0]
        self.stage = "assessment"
        self.selected = 0
        self.destination_selected = 0
        self.mode = "select"
        self.feedback = ""
        self.feedback_ok = False
        self.feedback_timer = 0.0
        self.pending_action = None
        self.correct = 0
        self.wrong = 0
        self.score = 0
        self.component_index = 0
        self.confirm_exit = False
        self.elapsed = 0.0
        self.new_discoveries = set()

    def enter(self, equipment_id="equip_notebook_antigo", **kwargs):
        self.equipment = next((x for x in EQUIPMENT_CATALOG if x.item_id == equipment_id), EQUIPMENT_CATALOG[0])
        self.stage = "assessment"
        self.selected = 0
        self.destination_selected = 0
        self.mode = "select"
        self.feedback = ""
        self.feedback_ok = False
        self.feedback_timer = 0.0
        self.pending_action = None
        self.correct = self.wrong = self.score = 0
        self.component_index = 0
        self.confirm_exit = False
        self.elapsed = 0.0
        self.new_discoveries = set()
        self._discover(self.equipment.item_id)

    def _discover(self, item_id):
        if self.game.progress_store.discover(item_id):
            self.new_discoveries.add(item_id)

    def handle_key(self, key):
        if self.confirm_exit:
            if key in (pygame.K_y, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.game.set_state("menu")
            elif key in (pygame.K_n, pygame.K_ESCAPE):
                self.confirm_exit = False
            return

        if key == pygame.K_ESCAPE:
            self.confirm_exit = True
            return

        if self.feedback_timer > 0:
            return

        if self.stage == "assessment":
            if key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP):
                self.selected = (self.selected - 1) % len(ASSESSMENT_OPTIONS)
            elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN):
                self.selected = (self.selected + 1) % len(ASSESSMENT_OPTIONS)
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self._check_assessment()
            return

        if self.stage == "components":
            if self.mode == "select":
                if key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP):
                    self.component_index = (self.component_index - 1) % len(COMPONENTS)
                elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN):
                    self.component_index = (self.component_index + 1) % len(COMPONENTS)
                elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._discover(COMPONENTS[self.component_index].item_id)
                    self.mode = "destination"
                    self.destination_selected = 0
            else:
                if key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP):
                    self.destination_selected = (self.destination_selected - 1) % len(DESTINATIONS)
                elif key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN):
                    self.destination_selected = (self.destination_selected + 1) % len(DESTINATIONS)
                elif key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self._check_component()
                elif key == pygame.K_BACKSPACE:
                    self.mode = "select"
            return

        if self.stage == "summary" and key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_ESCAPE):
            self.game.set_state("menu")

    def _check_assessment(self):
        if self.selected == 1:
            self.correct += 1
            self.score += 150
            self.feedback_ok = True
            self.feedback = ASSESSMENT_OPTIONS[1][1]
            self.pending_action = "components"
            self.game.snd.play("achievement")
        else:
            self.wrong += 1
            self.feedback_ok = False
            self.feedback = ASSESSMENT_OPTIONS[self.selected][1]
            self.pending_action = None
            self.game.snd.play("bad")
        self.feedback_timer = 1.65

    def _check_component(self):
        component = COMPONENTS[self.component_index]
        selected_key = DESTINATIONS[self.destination_selected][0]
        if selected_key == component.destination_key:
            self.correct += 1
            self.score += 100
            self.feedback_ok = True
            self.feedback = "Correto! " + component.description
            self.pending_action = "next_component"
            self.game.snd.play("ok")
        else:
            self.wrong += 1
            self.feedback_ok = False
            correct_name = next(x[1] for x in DESTINATIONS if x[0] == component.destination_key)
            self.feedback = "Destino inadequado. A classificação correta é: " + correct_name + ". " + component.description
            self.pending_action = None
            self.game.snd.play("bad")
        self.feedback_timer = 1.35

    def update(self, dt):
        super().update(dt)
        self.elapsed += dt
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                if self.pending_action == "components":
                    self.stage = "components"
                    self.mode = "select"
                    self.component_index = 0
                elif self.pending_action == "next_component":
                    self.component_index += 1
                    self.mode = "select"
                    if self.component_index >= len(COMPONENTS):
                        self._finish()
                self.pending_action = None
                self.feedback = ""

    def _finish(self):
        self.stage = "summary"
        self.game.progress_store.register_workshop_completion()
        self.game.snd.play("achievement")

    @property
    def accuracy(self):
        total = self.correct + self.wrong
        return int(round(100 * self.correct / total)) if total else 0

    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.panel(surf, (50, 38, 1180, 720), border=(70, 188, 170), bw=3)
        TEXT.draw(surf, "OFICINA CIRCULAR", 48, (130, 245, 190), (W // 2, 78), "center", bold=True,
                  outline=(12, 42, 42))
        TEXT.draw(surf, "LABORATÓRIO DE REUTILIZAÇÃO TECNOLÓGICA", 17, (190, 218, 232),
                  (W // 2, 116), "center", bold=True)

        if self.stage == "assessment":
            self._draw_assessment(surf)
        elif self.stage == "components":
            self._draw_components(surf)
        else:
            self._draw_summary(surf)

        if self.feedback:
            col = (132, 245, 170) if self.feedback_ok else (255, 154, 132)
            box = pygame.Surface((1040, 80), pygame.SRCALPHA)
            rr(box, (6, 14, 28, 235), (0, 0, 1040, 80), 12, col, 2)
            lines = TEXT.wrap(self.feedback, 18, 990)[:2]
            for i, line in enumerate(lines):
                TEXT.draw(box, line, 18, col if i == 0 else (230, 236, 244), (520, 23 + i * 27), "center", bold=(i == 0))
            surf.blit(box, (120, 646))

        if self.confirm_exit:
            surf.blit(game.assets.dim, (0, 0))
            Ui.panel(surf, (260, 290, 760, 210), border=(255, 190, 100), bw=3)
            TEXT.draw(surf, "SAIR DA OFICINA?", 38, (255, 220, 150), (W // 2, 345), "center", bold=True)
            TEXT.draw(surf, "ENTER / Y: sair     ESC / N: continuar", 24, (240, 244, 252),
                      (W // 2, 420), "center")

    def _draw_assessment(self, surf):
        Ui.panel(surf, (105, 154, 1070, 450), border=(70, 130, 170))
        TEXT.draw(surf, "ETAPA 1 · AVALIAÇÃO DO EQUIPAMENTO", 24, (255, 226, 126),
                  (145, 184), "topleft", bold=True)
        icon = render_equipment(self.equipment, 230)
        surf.blit(icon, (148, 245))
        TEXT.draw(surf, self.equipment.name, 25, (255, 255, 255), (263, 488), "center", bold=True)
        TEXT.draw(surf, "CENÁRIO", 17, (130, 245, 190), (438, 240), "topleft", bold=True)
        scenario = ("O notebook liga e funciona, mas a bateria perdeu autonomia. Um diagnóstico profissional confirmou que "
                    "a bateria pode ser substituída. Em um aparelho funcional, considere reutilização/doação; "
                    "quando há defeito recuperável, priorize reparo; se não houver recuperação viável, use logística reversa.")
        for i, line in enumerate(TEXT.wrap(scenario, 20, 650)):
            TEXT.draw(surf, line, 20, (225, 234, 246), (438, 274 + i * 29), "topleft")
        TEXT.draw(surf, "Qual é a destinação mais adequada neste caso?", 21, (255, 225, 130),
                  (438, 366), "topleft", bold=True)
        for i, (title, _desc) in enumerate(ASSESSMENT_OPTIONS):
            y = 414 + i * 54
            selected = i == self.selected
            bg = (30, 76, 78) if selected else (18, 30, 54)
            border = (120, 245, 190) if selected else (72, 104, 144)
            rr(surf, bg, (430, y, 670, 42), 9, border, 2)
            TEXT.draw(surf, ("› " if selected else "  ") + title, 19,
                      (255, 255, 255) if selected else (194, 208, 226), (448, y + 21), "midleft", bold=selected)
        TEXT.draw(surf, "← → ou A/D para escolher · ENTER para avaliar · ESC para sair", 17,
                  (165, 184, 212), (W // 2, 612), "center")

    def _draw_components(self, surf):
        Ui.panel(surf, (92, 150, 1096, 454), border=(70, 130, 170))
        TEXT.draw(surf, "ETAPA 2 · TRIAGEM DE COMPONENTES", 24, (255, 226, 126),
                  (132, 180), "topleft", bold=True)
        TEXT.draw(surf, f"COMPONENTE {self.component_index + 1} / {len(COMPONENTS)}", 16,
                  (140, 236, 200), (1150, 182), "topright", bold=True)
        comp = COMPONENTS[self.component_index]
        icon = render_component(comp, 150)
        surf.blit(icon, (150, 254))
        TEXT.draw(surf, comp.name, 28, (255, 255, 255), (225, 430), "center", bold=True)
        for i, line in enumerate(TEXT.wrap(comp.description, 19, 350)[:4]):
            TEXT.draw(surf, line, 18, (202, 218, 238), (225, 472 + i * 24), "center")

        if self.mode == "select":
            TEXT.draw(surf, "Selecione o componente na bancada e pressione ENTER para escolher o destino.",
                      19, (222, 234, 246), (690, 260), "center", max_w=660)
            for i, item in enumerate(COMPONENTS):
                x = 430 + (i % 4) * 175
                y = 310 + (i // 4) * 126
                active = i == self.component_index
                rr(surf, (26, 78, 74) if active else (16, 28, 48), (x, y, 154, 104), 10,
                   (120, 245, 190) if active else (66, 100, 142), 3 if active else 1)
                mini = render_component(item, 54)
                surf.blit(mini, (x + 50, y + 4))
                TEXT.draw(surf, item.name, 15, (255, 255, 255) if active else (190, 204, 226),
                          (x + 77, y + 80), "center", bold=active, max_w=144)
            TEXT.draw(surf, "← → / A-D ou ↑ ↓ navega · ENTER seleciona · ESC sai", 17,
                      (165, 184, 212), (W // 2, 610), "center")
        else:
            TEXT.draw(surf, "Para onde este componente deve seguir?", 23, (255, 226, 126),
                      (785, 300), "center", bold=True)
            for i, (key, title, subtitle) in enumerate(DESTINATIONS):
                y = 354 + i * 70
                active = i == self.destination_selected
                rr(surf, (26, 78, 74) if active else (16, 28, 48), (470, y, 625, 56), 10,
                   (120, 245, 190) if active else (66, 100, 142), 3 if active else 1)
                TEXT.draw(surf, title, 19, (255, 255, 255) if active else (190, 204, 226),
                          (492, y + 17), "topleft", bold=active)
                TEXT.draw(surf, subtitle, 15, (184, 202, 224), (492, y + 40), "topleft")
            TEXT.draw(surf, "← → / A-D escolhe destino · ENTER confirma · BACKSPACE retorna", 17,
                      (165, 184, 212), (W // 2, 586), "center")

    def _draw_summary(self, surf):
        Ui.panel(surf, (140, 160, 1000, 490), border=(116, 238, 164), bw=3)
        pulse = 0.5 + 0.5 * math.sin(self.elapsed * 5)
        col = (int(120 + 70 * pulse), 255, int(170 + 50 * pulse))
        TEXT.draw(surf, "TRIAGEM CONCLUÍDA!", 48, col, (W // 2, 214), "center", bold=True,
                  outline=(12, 42, 32))
        TEXT.draw(surf, f"{self.correct} classificações corretas · {self.wrong} escolhas inadequadas · {self.accuracy}% de acerto",
                  22, (228, 238, 248), (W // 2, 280), "center")
        TEXT.draw(surf, f"PONTUAÇÃO DA OFICINA: {self.score}", 30, (255, 222, 112),
                  (W // 2, 328), "center", bold=True)
        reuse = [x.name for x in COMPONENTS if x.destination_key == "reuse"]
        recovery = [x.name for x in COMPONENTS if x.destination_key == "recovery"]
        special = [x.name for x in COMPONENTS if x.destination_key == "special"]
        sections = [("REUTILIZAÇÃO", reuse, (124, 240, 174)),
                    ("RECUPERAÇÃO DE MATERIAIS", recovery, (130, 202, 255)),
                    ("TRATAMENTO ESPECIALIZADO", special, (255, 188, 118))]
        for col_idx, (title, names, color) in enumerate(sections):
            x = 205 + col_idx * 300
            rr(surf, (18, 30, 52), (x, 378, 270, 150), 10, color, 2)
            TEXT.draw(surf, title, 16, color, (x + 135, 400), "center", bold=True, max_w=250)
            for i, name in enumerate(names):
                TEXT.draw(surf, "• " + name, 16, (224, 234, 246), (x + 18, 432 + i * 25), "topleft")
        TEXT.draw(surf, "Curiosidade: trocar uma bateria desgastada pode prolongar a vida útil do notebook e evitar a substituição do aparelho inteiro.",
                  16, (190, 224, 244), (W // 2, 548), "center", max_w=900)
        TEXT.draw(surf, "Baterias e placas exigem operadores especializados. Não tente abri-las ou manipulá-las em casa.",
                  16, (255, 190, 140), (W // 2, 574), "center", max_w=900)
        TEXT.draw(surf, "ENTER para voltar ao menu", 22, (255, 255, 255), (W // 2, 612), "center", bold=True)
