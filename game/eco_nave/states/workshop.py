# -*- coding: utf-8 -*-
"""Oficina Circular: avaliação do equipamento, triagem de componentes e resultado.

A tela usa regiões fixas (cabeçalho, bancada, área de trabalho, painel de feedback e barra de
atalhos) e mede todo texto antes de desenhar, então nada se sobrepõe em nenhuma fonte.
"""
import math
import random

import pygame

from ..config import W
from ..drawing import D, rr
from ..effects import Effects
from ..icons import draw_icon
from ..text import TEXT
from ..ui import Ui
from ..utils import clamp, mix, shade
from ..workshop_catalog import (ASSESSMENT_OPTIONS, COMPONENTS, DESTINATIONS, EQUIPMENT_CATALOG, REUSE_NOTE,
                                SAFETY_NOTE, render_component, render_equipment)
from ..workshop_run import WorkshopRun
from .base import AttractState

GREEN, GOLD, BLUE, ORANGE, RED = (130, 245, 190), (255, 226, 126), (130, 202, 255), (255, 188, 118), (255, 150, 130)
DEST_STYLE = {"reuse": ("reuse", (124, 240, 174)), "recovery": ("recycle", (130, 202, 255)),
              "special": ("shield", (255, 188, 118))}
PX, PY, PW, PH = 40, 128, 1200, 580          # painel principal
LEFT_X, LEFT_W = 64, 320                     # coluna da bancada
RIGHT_X, RIGHT_W = 408, 808                  # área de trabalho
STEPS = ("AVALIAÇÃO", "TRIAGEM", "RESULTADO")
CURIOSITY = ("Trocar uma bateria desgastada, ou reaproveitar memória e SSD depois de testes, pode prolongar a "
             "vida útil de um notebook e evitar a produção de um aparelho novo.")


class WorkshopState(AttractState):
    """Desafio modular: novos equipamentos podem ganhar cenários e componentes próprios."""

    def __init__(self, game):
        super().__init__(game)
        self.equipment = EQUIPMENT_CATALOG[0]
        self.rng = random.Random()               # sorteio próprio: não interfere no sorteio do jogo
        self.last_scenario = None
        self.fx = Effects(self.rng)
        self._sprites = {}
        self._reset()

    # ------------------------------------------------------------------ ciclo
    def _reset(self):
        self.run = None
        self.stage = "assess"                    # assess | triage | summary
        self.opt_sel = 0
        self.part_sel = 0
        self.tray_sel = 0
        self.mode = "select"                     # assess: select | feedback / triage: select | choose | feedback
        self.feedback = ("", True)
        self.t = 0.0
        self.stage_t = 0.0
        self.flight = None
        self.trays = {k: [] for k, _l, _s in DESTINATIONS}
        self.confirm_exit = False
        self.fx.reset()
        self.burst_t = 0.0

    def enter(self, equipment_id=None, **kwargs):
        self.equipment = next((x for x in EQUIPMENT_CATALOG if x.item_id == equipment_id), EQUIPMENT_CATALOG[0])
        self._reset()
        self.run = WorkshopRun(self.equipment, rng=self.rng, avoid_key=self.last_scenario)
        self.last_scenario = self.run.scenario.key
        self.game.progress_store.discover(self.equipment.item_id)

    # ------------------------------------------------------------------ entrada
    def handle_key(self, key):
        enter = key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)
        left = key in (pygame.K_LEFT, pygame.K_a)
        right = key in (pygame.K_RIGHT, pygame.K_d)
        up, down = key in (pygame.K_UP, pygame.K_w), key in (pygame.K_DOWN, pygame.K_s)
        if self.confirm_exit:
            if key in (pygame.K_y, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.game.set_state("menu")
            elif key in (pygame.K_n, pygame.K_ESCAPE):
                self.confirm_exit = False
            return
        if self.stage == "summary":
            if enter:
                self.enter(self.equipment.item_id)           # nova rodada, com outro cenário
            elif key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.game.set_state("menu")
            return
        if key == pygame.K_ESCAPE:
            if self.stage == "triage" and self.mode == "choose":
                self.mode = "select"
            else:
                self.confirm_exit = True
            return
        if self.stage == "assess":
            self._key_assess(enter, left or up, right or down)
        else:
            self._key_triage(key, enter, left, right, up, down)

    def _key_assess(self, enter, prev, nxt):
        if self.mode == "select":
            if prev:
                self.opt_sel = (self.opt_sel - 1) % len(ASSESSMENT_OPTIONS)
            elif nxt:
                self.opt_sel = (self.opt_sel + 1) % len(ASSESSMENT_OPTIONS)
            elif enter:
                ok, text = self.run.evaluate(ASSESSMENT_OPTIONS[self.opt_sel].key)
                self.feedback = (text, ok)
                self.mode = "feedback"
                self.game.snd.play("achievement" if ok else "bad")
        elif enter:
            self.stage, self.mode, self.stage_t = "triage", "select", 0.0
            self.part_sel = 0
            self.feedback = ("", True)

    def _free_parts(self):
        return [i for i, c in enumerate(COMPONENTS) if not self.run.is_classified(c)]

    def _step_part(self, delta):
        free = self._free_parts()
        if free:
            pos = free.index(self.part_sel) if self.part_sel in free else 0
            self.part_sel = free[(pos + delta) % len(free)]

    def _key_triage(self, key, enter, left, right, up, down):
        if self.mode == "select":
            if self.stage_t < 1.4:
                return                                        # espera a desmontagem terminar
            if left or up:
                self._step_part(-1)
            elif right or down:
                self._step_part(1)
            elif enter and self._free_parts():
                self.mode, self.tray_sel = "choose", 0
                self.game.progress_store.discover(COMPONENTS[self.part_sel].item_id)
        elif self.mode == "choose":
            if left:
                self.tray_sel = (self.tray_sel - 1) % len(DESTINATIONS)
            elif right:
                self.tray_sel = (self.tray_sel + 1) % len(DESTINATIONS)
            elif key == pygame.K_BACKSPACE:
                self.mode = "select"
            elif enter:
                self._confirm_part()
        elif enter:                                           # feedback -> continuar
            self._finish_flight()
            if self.run.finished:
                self._to_summary()
            else:
                self.mode = "select"
                self._step_part(0)
                self.feedback = ("", True)

    def _confirm_part(self):
        comp = COMPONENTS[self.part_sel]
        dest_key = DESTINATIONS[self.tray_sel][0]
        ok, text = self.run.classify(comp, dest_key)
        self.feedback = (text, ok)
        self.mode = "feedback"
        self.game.snd.play("ok" if ok else "bad")
        target = comp.destination_key                         # a peça sempre termina no destino correto
        self.flight = {"comp": comp, "t": 0.0, "dur": 0.55, "ok": ok, "dest": target,
                       "from": self._slot_rect(self.part_sel).center, "to": self._tray_rect(target).center}

    def _finish_flight(self):
        if self.flight:
            self.trays[self.flight["dest"]].append(self.flight["comp"])
            self.flight = None

    def _to_summary(self):
        self.stage, self.mode, self.stage_t = "summary", "select", 0.0
        run = self.run
        self.game.progress_store.register_workshop_completion(run.score, run.perfect)
        self.game.snd.play("achievement")
        self.burst_t = 0.0

    # ------------------------------------------------------------- atualização
    def update(self, dt):
        super().update(dt)
        self.t += dt
        self.stage_t += dt
        self.fx.update(dt)
        if self.flight:
            self.flight["t"] += dt
            if self.flight["t"] >= self.flight["dur"]:
                self._finish_flight()
        if self.stage == "summary" and self.stage_t < 2.4:
            self.burst_t -= dt
            if self.burst_t <= 0:
                self.burst_t = 0.45
                for x in (260, 640, 1020):
                    self.fx.confetti(x, 190, (130, 245, 190), 14)

    # --------------------------------------------------------------- geometria
    def _slot_rect(self, i):
        c, r = i % 4, i // 4
        return pygame.Rect(RIGHT_X + c * 204, PY + 20 + r * 126, 190, 112)

    def _tray_rect(self, key):
        i = [d[0] for d in DESTINATIONS].index(key)
        return pygame.Rect(RIGHT_X + i * 274, PY + 276, 260, 138)

    def _sprite(self, kind, obj, size):
        key = (kind, obj.item_id, size)
        s = self._sprites.get(key)
        if s is None:
            s = (render_component if kind == "c" else render_equipment)(obj, size)
            self._sprites[key] = s
        return s

    # ------------------------------------------------------------------ desenho
    def draw(self, surf):
        game = self.game
        self.draw_backdrop(surf)
        surf.blit(game.assets.dim, (0, 0))
        Ui.header(surf, "OFICINA CIRCULAR", "Laboratório de reutilização tecnológica", GREEN, (12, 42, 42), y=44,
                  size=36)
        self._draw_steps(surf)
        Ui.panel(surf, (PX, PY, PW, PH), border=(70, 188, 170), bw=3)
        if self.stage == "assess":
            self._draw_assess(surf)
        elif self.stage == "triage":
            self._draw_triage(surf)
        else:
            self._draw_summary(surf)
        self._draw_footer(surf)
        if self.confirm_exit:
            surf.blit(game.assets.dim, (0, 0))
            Ui.panel(surf, (W // 2 - 280, 290, 560, 200), alpha=252, border=(255, 190, 100), bw=3)
            TEXT.draw(surf, "SAIR DA OFICINA?", 36, (255, 220, 150), (W // 2, 340), "center", bold=True)
            TEXT.draw(surf, "O progresso desta rodada será perdido.", 17, (214, 224, 244), (W // 2, 384), "center")
            Ui.hint_bar(surf, [("ENTER", "sair"), ("ESC", "continuar")], 440, 17)

    def _draw_steps(self, surf):
        idx = {"assess": 0, "triage": 1, "summary": 2}[self.stage]
        widths = [TEXT.width(f"{i + 1}  {n}", 14, True) + 24 for i, n in enumerate(STEPS)]
        x = (W - (sum(widths) + 16 * 2)) // 2
        for i, (name, wd) in enumerate(zip(STEPS, widths)):
            on = i == idx
            rr(surf, mix((10, 16, 32), GREEN, 0.35) if on else (10, 16, 32), (x, 94, wd, 26), 13,
               GREEN if on else (60, 90, 120), 2)
            TEXT.draw(surf, f"{i + 1}  {name}", 14, (255, 255, 255) if on else (150, 172, 196), (x + wd // 2, 107),
                      "center", bold=on)
            x += wd + 16

    def _draw_footer(self, surf):
        if self.stage == "assess":
            hints = [("A/D", "escolher"), ("ENTER", "continuar" if self.mode == "feedback" else "avaliar"),
                     ("ESC", "sair")]
        elif self.stage == "triage":
            if self.mode == "select":
                hints = [("A/D", "escolher peça"), ("ENTER", "selecionar"), ("ESC", "sair")]
            elif self.mode == "choose":
                hints = [("A/D", "escolher destino"), ("ENTER", "confirmar"), ("ESC", "voltar")]
            else:
                hints = [("ENTER", "continuar"), ("ESC", "sair")]
        else:
            hints = [("ENTER", "nova rodada"), ("ESC", "menu")]
        Ui.hint_bar(surf, hints, 744, 15)

    # ---- bancada (coluna esquerda)
    def _draw_bench(self, surf, rect, device_size, caption):
        x, y, w, h = rect
        rr(surf, (10, 22, 38), rect, 14, (60, 120, 150), 2)
        cx, cy = x + w // 2, y + 22 + device_size // 2
        pad = pygame.Surface((w - 40, 40), pygame.SRCALPHA)
        D.ellipse(pad, (70, 205, 175, 60), (0, 0, w - 40, 40))
        D.ellipse(pad, (130, 245, 200, 150), (0, 0, w - 40, 40), 2)
        surf.blit(pad, (x + 20, cy + device_size // 2 - 22))
        surf.blit(self._sprite("e", self.equipment, device_size), (cx - device_size // 2, cy - device_size // 2))
        sy = cy - device_size // 2 + (self.t * 70) % device_size          # linha de varredura (usa dt)
        D.line(surf, (130, 245, 200), (cx - device_size // 2, sy), (cx + device_size // 2, sy), 2)
        TEXT.draw(surf, self.equipment.name, 22, (255, 255, 255), (cx, y + h - 38), "center", bold=True, max_w=w - 24)
        TEXT.draw(surf, caption, 13, (150, 200, 210), (cx, y + h - 16), "center", max_w=w - 24)

    # ---- etapa 1
    def _draw_assess(self, surf):
        run, sc = self.run, self.run.scenario
        self._draw_bench(surf, (LEFT_X, PY + 20, LEFT_W, 300), 190, "Equipamento em avaliação")
        rr(surf, (12, 24, 30), (LEFT_X, PY + 336, LEFT_W, 224), 14, (90, 140, 90), 2)
        TEXT.draw(surf, "LEMBRE-SE", 15, GREEN, (LEFT_X + 18, PY + 356), "midleft", bold=True)
        Ui.fit_block(surf, REUSE_NOTE, (LEFT_X + 18, PY + 376, LEFT_W - 36, 90), (226, 236, 246), 18, 13)
        Ui.fit_block(surf, "Quando não há conserto, o destino é a logística reversa, com operadores especializados.",
                     (LEFT_X + 18, PY + 470, LEFT_W - 36, 80), (186, 206, 228), 15, 12)

        rr(surf, (12, 20, 38), (RIGHT_X, PY + 20, RIGHT_W, 226), 14, (70, 130, 170), 2)
        Ui.chip(surf, "ETAPA 1 · LAUDO TÉCNICO", RIGHT_X + 18, PY + 34, GOLD, 14)
        TEXT.draw(surf, sc.title, 24, (255, 255, 255), (RIGHT_X + 18, PY + 82), "midleft", bold=True,
                  max_w=RIGHT_W - 36)
        Ui.bullets(surf, list(sc.symptoms), (RIGHT_X + 18, PY + 108, RIGHT_W - 36, 126), (226, 236, 246), 19, 13)

        TEXT.draw(surf, "Qual é a destinação mais adequada?", 20, GOLD, (RIGHT_X, PY + 266), "midleft", bold=True)
        ow, gap = 260, 14
        for i, opt in enumerate(ASSESSMENT_OPTIONS):
            r = pygame.Rect(RIGHT_X + i * (ow + gap), PY + 286, ow, 150)
            sel = i == self.opt_sel
            border = GREEN if sel else (72, 104, 144)
            mark = None
            if self.mode == "feedback":
                if opt.key == sc.answer:
                    border, mark = (132, 245, 170), "check"
                elif i == self.opt_sel:
                    border, mark = RED, "cross"
            rr(surf, (26, 78, 74) if sel else (16, 28, 54), r, 12, border, 3 if sel or mark else 1)
            draw_icon(surf, opt.icon, r.centerx, r.y + 34, 40, GREEN if sel else (170, 196, 224))
            TEXT.draw(surf, opt.title, 16, (255, 255, 255) if sel else (200, 214, 232), (r.centerx, r.y + 72),
                      "center", bold=True, max_w=ow - 20)
            Ui.fit_block(surf, opt.subtitle, (r.x + 14, r.y + 88, ow - 28, 54), (186, 206, 228), 14, 11,
                         align="center")
            if mark:
                draw_icon(surf, mark, r.right - 20, r.y + 20, 20, border)
        self._draw_feedback(surf, (RIGHT_X, PY + 452, RIGHT_W, 108), idle=None)

    # ---- painel de feedback (único para todas as etapas)
    def _draw_feedback(self, surf, rect, idle):
        x, y, w, h = rect
        text, ok = self.feedback
        if not text:
            if idle:
                rr(surf, (22, 18, 12), rect, 12, (150, 110, 60), 1)
                Ui.fit_block(surf, idle, (x + 16, y + 10, w - 32, h - 20), ORANGE, 15, 11, align="center")
            return
        col = (132, 245, 170) if ok else RED
        rr(surf, (6, 16, 28), rect, 12, col, 3)
        draw_icon(surf, "check" if ok else "cross", x + 34, y + 36, 30, col)
        Ui.fit_block(surf, text, (x + 70, y + 12, w - 90, h - 44), (232, 238, 246), 18, 12)
        if (self.t * 2) % 2 < 1.4:
            TEXT.draw(surf, "ENTER para continuar", 13, col, (x + w - 16, y + h - 14), "midright", bold=True)

    # ---- etapa 2
    def _draw_triage(self, surf):
        run = self.run
        self._draw_bench(surf, (LEFT_X, PY + 20, LEFT_W, 250), 150, "Triagem profissional")
        comp = COMPONENTS[self.part_sel]
        sel_idx = self.part_sel
        # painel da peça selecionada
        rr(surf, (12, 20, 38), (LEFT_X, PY + 286, LEFT_W, 274), 14, (70, 130, 170), 2)
        Ui.chip(surf, "ETAPA 2 · PEÇA " + f"{min(run.parts_done + 1, len(COMPONENTS))}/{len(COMPONENTS)}",
                LEFT_X + 16, PY + 300, GOLD, 13)
        surf.blit(self._sprite("c", comp, 72), (LEFT_X + 16, PY + 336))
        TEXT.draw(surf, comp.name, 22, (255, 255, 255), (LEFT_X + 100, PY + 360), "midleft", bold=True,
                  max_w=LEFT_W - 116)
        sub = "Para onde vai esta peça?" if self.mode == "choose" else "Selecione e pressione ENTER."
        TEXT.draw(surf, sub, 14, GREEN, (LEFT_X + 100, PY + 388), "midleft", max_w=LEFT_W - 116)
        Ui.fit_block(surf, comp.description, (LEFT_X + 16, PY + 424, LEFT_W - 32, 128), (214, 226, 242), 17, 12)

        # peças (entram voando a partir do notebook)
        origin = (LEFT_X + LEFT_W // 2, PY + 20 + 100)
        for i, c in enumerate(COMPONENTS):
            slot = self._slot_rect(i)
            done = run.is_classified(c)
            fly = self.flight and self.flight["comp"] is c
            k = clamp((self.stage_t - i * 0.12) / 0.7, 0.0, 1.0)
            e = 1 - (1 - k) ** 3
            cx = origin[0] + (slot.centerx - origin[0]) * e
            cy = origin[1] + (slot.centery - origin[1]) * e
            sc_ = 0.35 + 0.65 * e
            w, h = int(slot.w * sc_), int(slot.h * sc_)
            r = pygame.Rect(0, 0, w, h)
            r.center = (int(cx), int(cy))
            if done or fly:
                rr(surf, (12, 18, 30), r, 10, (44, 60, 84), 1)
                continue
            active = i == sel_idx and self.mode in ("select", "choose") and k >= 1.0
            rr(surf, (26, 78, 74) if active else (16, 28, 52), r, 10, GREEN if active else (66, 100, 142),
               3 if active else 1)
            if k >= 0.6:
                spr = self._sprite("c", c, 54)
                surf.blit(spr, (r.centerx - 27, r.y + 8))
                TEXT.draw(surf, c.name, 15, (255, 255, 255) if active else (190, 204, 226), (r.centerx, r.bottom - 17),
                          "center", bold=active, max_w=r.w - 12)

        # bandejas de destino
        for key, label, subtitle in DESTINATIONS:
            r = self._tray_rect(key)
            icon, col = DEST_STYLE[key]
            idx = [d[0] for d in DESTINATIONS].index(key)
            hot = self.mode == "choose" and idx == self.tray_sel
            rr(surf, mix((10, 16, 32), col, 0.28 if hot else 0.08), r, 12, col if hot else shade(col, 0.55), 4 if hot else 2)
            draw_icon(surf, icon, r.x + 30, r.y + 30, 30, col)
            TEXT.draw(surf, label, 16, (255, 255, 255), (r.x + 56, r.y + 22), "midleft", bold=True, max_w=r.w - 66)
            Ui.fit_block(surf, subtitle, (r.x + 56, r.y + 38, r.w - 68, 34), (186, 206, 228), 13, 11)
            for j, c in enumerate(self.trays[key][:5]):
                surf.blit(self._sprite("c", c, 36), (r.x + 12 + j * 46, r.bottom - 54))
        if self.flight:                                        # peça voando até a bandeja
            f = self.flight
            p = clamp(f["t"] / f["dur"], 0.0, 1.0)
            e = p * p * (3 - 2 * p)
            fx_ = f["from"][0] + (f["to"][0] - f["from"][0]) * e
            fy_ = f["from"][1] + (f["to"][1] - f["from"][1]) * e - math.sin(p * math.pi) * 40
            size = int(54 - 20 * e)
            spr = self._sprite("c", f["comp"], 54)
            surf.blit(pygame.transform.smoothscale(spr, (size, size)), (int(fx_) - size // 2, int(fy_) - size // 2))
        self._draw_feedback(surf, (RIGHT_X, PY + 428, RIGHT_W, 132), idle=run.scenario.triage_intro + "  " + SAFETY_NOTE)

    # ---- resultado
    def _draw_summary(self, surf):
        run = self.run
        self.fx.draw_particles(surf)
        pulse = 0.5 + 0.5 * math.sin(self.t * 5)
        col = (int(120 + 70 * pulse), 255, int(170 + 50 * pulse))
        TEXT.draw(surf, "OFICINA CONCLUÍDA!", 42, col, (W // 2, PY + 38), "center", bold=True, outline=(12, 42, 32))
        TEXT.draw(surf, f"{self.equipment.name}  ·  {run.scenario.title}", 17, (214, 228, 242), (W // 2, PY + 76),
                  "center", max_w=PW - 80)
        tiles = [("PONTUAÇÃO", str(run.score), GOLD), ("COMPONENTES", f"{run.correct_parts} / {len(COMPONENTS)}", GREEN),
                 ("AVALIAÇÃO", "Correta" if run.eval_correct else "A melhorar", GREEN if run.eval_correct else ORANGE),
                 ("PRECISÃO", f"{run.accuracy}%", BLUE)]
        tw, gap = 270, 16
        x0 = (W - (4 * tw + 3 * gap)) // 2
        for i, (lab, val, c) in enumerate(tiles):
            r = pygame.Rect(x0 + i * (tw + gap), PY + 100, tw, 70)
            rr(surf, (12, 22, 40), r, 12, c, 2)
            TEXT.draw(surf, lab, 13, (160, 184, 212), (r.centerx, r.y + 17), "center", bold=True)
            TEXT.draw(surf, val, 28, c, (r.centerx, r.y + 46), "center", bold=True, max_w=tw - 20)
        cw = 376
        for i, (key, label, _s) in enumerate(DESTINATIONS):
            icon, c = DEST_STYLE[key]
            r = pygame.Rect(LEFT_X + i * (cw + 16), PY + 190, cw, 188)
            rr(surf, (14, 24, 44), r, 12, c, 2)
            draw_icon(surf, icon, r.x + 26, r.y + 24, 24, c)
            TEXT.draw(surf, label, 15, c, (r.x + 48, r.y + 24), "midleft", bold=True, max_w=cw - 60)
            row = 0
            for comp in COMPONENTS:
                if comp.destination_key != key:
                    continue
                ok = run.results.get(comp.item_id, (None, False))[1]
                yy = r.y + 56 + row * 30
                draw_icon(surf, "check" if ok else "cross", r.x + 24, yy, 16, (132, 245, 170) if ok else RED)
                TEXT.draw(surf, comp.name, 17, (232, 238, 246), (r.x + 46, yy), "midleft", max_w=cw - 60)
                row += 1
        mats = ", ".join(run.recoverable_materials())
        reuse = ", ".join(c.name for c in run.reusable())
        lines = [("MATERIAIS QUE VOLTAM À CADEIA PRODUTIVA: " + mats + ".", BLUE),
                 ("COMPONENTES REUTILIZÁVEIS, APÓS TESTES: " + reuse + ".", GREEN),
                 ("CURIOSIDADE: " + CURIOSITY, (200, 224, 244)),
                 (SAFETY_NOTE, ORANGE)]
        y = PY + 392
        for text, c in lines:
            bottom, _sz = Ui.fit_block(surf, text, (LEFT_X, y, PW - 48, 34), c, 15, 11, bold=text.startswith("MATERIAIS") or
                                       text.startswith("COMPONENTES"))
            y += 42 if text.startswith("CURIOSIDADE") else 34
