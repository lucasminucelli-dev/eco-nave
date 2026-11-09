# -*- coding: utf-8 -*-
"""Uma partida: junta nave, lixo, lixeiras, pontuacao e efeitos, e resolve acertos e erros."""
import math

from .bin_row import BinRow
from .bins import BINS
from .config import BIN_BODY_TOP, BIN_MOUTH_Y, Difficulty, HALF, LANE_W, SHIP_Y, W
from .effects import Effects
from .entities import Trash
from .hud import Hud, LevelBanner, MessageBox
from .items import ITEM_CATALOG
from .progress import Progress
from .spawner import ItemSpawner
from .utils import clamp, fmt


class Session:
    START_DELAY = 1.1      # pausa antes do primeiro lixo
    DEATH_DELAY = 1.4      # pausa entre a ultima vida e a tela de fim de jogo

    def __init__(self, assets, sound, ship):
        self.assets = assets
        self.sound = sound
        self.ship = ship
        self.progress = Progress()
        self.spawner = ItemSpawner(ITEM_CATALOG)
        self.bins = BinRow()
        self.effects = Effects()
        self.hud = Hud()
        self.message = MessageBox()
        self.banner = LevelBanner()
        self.reset()

    def reset(self):
        """Comeca uma partida nova."""
        self.progress.reset()
        self.spawner.reset()
        self.bins.reset()
        self.effects.reset()
        self.message.clear()
        self.banner.clear()
        self.ship.reset()
        self.trash = None
        self.spawn_timer = self.START_DELAY
        self.dying = False
        self.end_timer = 0.0

    # ------------------------------------------------------------ atualizacao
    def update_effects(self, dt):
        """Parte da atualizacao que continua rodando ate depois do fim de jogo."""
        self.effects.update(dt)
        self.bins.update(dt)
        self.message.update(dt)
        self.banner.update(dt)

    def update(self, dt, direction=0, fast=False):
        """Avanca a partida. Devolve True no instante em que ela termina."""
        level = self.progress.level
        self.ship.tick(dt)
        self.ship.follow_target(dt, level)
        self.update_effects(dt)
        hover = None
        finished = False
        if self.dying:
            self.end_timer -= dt
            if self.end_timer <= 0:
                self.dying = False
                finished = True
        elif self.trash is None:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0 and self.ship.aligned:
                self.spawn()
        else:
            it = self.trash
            it.update(dt, direction, fast, level)
            hover = it.lane
            if it.reached_mouth:
                self.resolve(it)
                hover = None
        self.bins.ease_open(dt, hover)
        return finished

    def spawn(self):
        x = clamp(self.ship.x, HALF, W - HALF)
        idef = self.spawner.pick(x, self.progress.level)
        self.trash = Trash(idef, x, SHIP_Y + 50)
        self.ship.fire_beam()
        self.sound.play("spawn")

    # ---------------------------------------------------------------- resolucao
    def resolve(self, it):
        """O lixo chegou na boca das lixeiras: conta acerto ou erro."""
        lane = it.lane
        idef = it.idef
        cx = BinRow.center_x(lane)
        sprite = self.assets.sprite_for(idef)
        if lane == idef.bin_index:
            self._on_hit(it, lane, cx, sprite)
        else:
            self._on_miss(it, lane, cx, sprite)
        self.trash = None
        if self.progress.game_over:
            self.dying = True
            self.end_timer = self.DEATH_DELAY
        else:
            self.spawn_timer = Difficulty.spawn_delay(self.progress.level)
            self.ship.choose_target()

    def _on_hit(self, it, lane, cx, sprite):
        idef = it.idef
        result = self.progress.register_hit()
        self.bins.pulse_ok(lane)
        self.effects.confetti(cx, BIN_MOUTH_Y, BINS[lane].glow, 30)
        self.effects.popup(f"+{fmt(result.points)}", cx, BIN_MOUTH_Y - 34, 1.0, (150, 255, 170), 30)
        self.message.show(f"Certo! {idef.name} vai na lixeira {BINS[lane].name}.", idef.tip, "ok", 4.2)
        self.sound.play("ok")
        if result.leveled_up:
            self.banner.show(f"NÍVEL {self.progress.level}", "A nave está mais rápida!")
            self.sound.play("level")
        if result.extra_life:
            self.effects.popup("+1 vida", cx, BIN_MOUTH_Y - 70, 1.4, (255, 140, 170), 26)
        self.effects.fly_into_bin(sprite, it.x, it.y, cx, BIN_BODY_TOP + 34)

    def _on_miss(self, it, lane, cx, sprite):
        idef = it.idef
        self.progress.register_miss()
        right_bin = idef.bin_index
        self.bins.pulse_bad(lane)
        self.effects.start_shake()
        self.effects.sparks(cx, BIN_MOUTH_Y, (255, 90, 90), 22)
        self.effects.popup("Errou!", cx, BIN_MOUTH_Y - 34, 1.0, (255, 120, 120), 30)
        self.message.show(f"Ops! {idef.name} vai na lixeira {BINS[right_bin].name}.", idef.tip, "bad", 5.0)
        self.bins.show_hint(right_bin)
        self.sound.play("bad")
        self.effects.bounce_away(sprite, it.x, it.y)

    # ------------------------------------------------------------------ desenho
    def draw(self, surf, t):
        """Desenha tudo da partida (o fundo e as estrelas ficam por conta de quem chama)."""
        a = self.assets
        it = self.trash
        hover = None
        if it is not None:
            hover = it.lane
            surf.blit(a.lane_glow[it.lane], (it.lane * LANE_W, 0))
        cy = SHIP_Y + math.sin(self.ship.bob * 2.4) * 4
        self.ship.draw(surf, a, t, cy)
        if it is not None:
            it.draw(surf, a)
        self.effects.draw_items(surf)
        self.bins.draw(surf, a, t, hover)
        self.effects.draw_particles(surf)
        self.effects.draw_popups(surf)
        self.hud.draw(surf, a, self.progress)
        self.message.draw(surf)
        self.banner.draw(surf)
