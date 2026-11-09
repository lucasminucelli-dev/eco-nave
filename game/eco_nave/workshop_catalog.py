# -*- coding: utf-8 -*-
"""Catálogo separado de eletroeletrônicos e componentes da Oficina Circular."""
from dataclasses import dataclass
import pygame

from .drawing import D, rr


@dataclass(frozen=True)
class EquipmentDef:
    item_id: str
    name: str
    kind: str
    description: str
    destination: str = "Logística reversa de eletroeletrônicos: ponto de recebimento habilitado."
    note: str = "Apague dados pessoais e verifique previamente o que o ponto de coleta aceita."


@dataclass(frozen=True)
class ComponentDef:
    item_id: str
    name: str
    destination_key: str
    description: str
    fact: str
    kind: str


EQUIPMENT_CATALOG = [
    EquipmentDef("equip_notebook_antigo", "Notebook antigo", "notebook",
                 "Computador portátil que pode ser avaliado para doação, recondicionamento, reparo ou reciclagem especializada."),
    EquipmentDef("equip_computador_mesa", "Computador de mesa", "desktop",
                 "Gabinete e periféricos que podem ter peças reaproveitáveis após avaliação técnica."),
    EquipmentDef("equip_celular_antigo", "Celular antigo", "phone",
                 "Aparelho que pode voltar ao uso, ser recondicionado ou seguir para logística reversa."),
    EquipmentDef("equip_teclado", "Teclado", "keyboard",
                 "Periférico com componentes plásticos e eletrônicos que não deve ser misturado aos recicláveis comuns."),
    EquipmentDef("equip_mouse", "Mouse", "mouse",
                 "Periférico pequeno que pode ser reparado ou encaminhado ao sistema de eletroeletrônicos."),
    EquipmentDef("equip_roteador", "Roteador", "router",
                 "Equipamento de rede com placa e fonte que exigem triagem adequada ao fim da vida útil."),
    EquipmentDef("equip_controle_videogame", "Controle de videogame", "controller",
                 "Controle eletrônico que pode ser consertado, doado ou encaminhado à logística reversa."),
    EquipmentDef("equip_pequeno_eletrodomestico", "Pequeno eletrodoméstico", "appliance",
                 "Aparelho doméstico que deve ser separado de resíduos comuns e levado a ponto que aceite a categoria."),
]

COMPONENTS = [
    ComponentDef("comp_memoria_ram", "Memória RAM", "reuse",
                 "Pode ser reaproveitada depois de testes funcionais e verificação de compatibilidade.",
                 "Módulos de memória têm formatos e gerações diferentes; compatibilidade importa.", "ram"),
    ComponentDef("comp_ssd", "SSD", "reuse",
                 "Pode ser reutilizado depois de testes de saúde e apagamento seguro dos dados.",
                 "Antes de doar ou reaproveitar unidades de armazenamento, remova os dados com método adequado.", "ssd"),
    ComponentDef("comp_cooler", "Cooler", "reuse",
                 "Ventoinhas podem ser reaproveitadas se estiverem íntegras e passarem por teste técnico.",
                 "Um cooler em bom estado pode prolongar a vida útil de outro computador.", "cooler"),
    ComponentDef("comp_estrutura_metalica", "Estrutura metálica", "recovery",
                 "A carcaça pode fornecer metais recuperáveis em uma linha de manufatura reversa.",
                 "A recuperação depende de triagem e separação feita por operadores especializados.", "metal"),
    ComponentDef("comp_pecas_plasticas", "Peças plásticas", "recovery",
                 "Plásticos de carcaças podem ser separados por tipo de polímero para recuperação industrial.",
                 "Plásticos diferentes nem sempre podem ser reciclados juntos; a identificação do polímero é importante.", "plastic"),
    ComponentDef("comp_cabos", "Cabos", "recovery",
                 "Cabos podem conter cobre e polímeros recuperáveis em processamento especializado.",
                 "Não queime nem descasque cabos em casa para retirar cobre.", "cable"),
    ComponentDef("comp_placa_eletronica", "Placa eletrônica", "special",
                 "Placas devem seguir para tratamento especializado; não vão para lixeiras convencionais.",
                 "Placas podem conter metais valiosos e substâncias que exigem controle ambiental.", "board"),
    ComponentDef("comp_bateria", "Bateria", "special",
                 "Baterias devem ser encaminhadas intactas a operadores e pontos que aceitem esse resíduo.",
                 "Não abra, perfure, dobre, aqueça ou tente remover células de bateria. A triagem é profissional.", "battery"),
]

DESTINATIONS = [
    ("reuse", "REUTILIZAÇÃO", "Testar e aproveitar novamente"),
    ("recovery", "RECUPERAÇÃO", "Separar materiais para a cadeia produtiva"),
    ("special", "TRATAMENTO ESPECIAL", "Encaminhar a operador especializado"),
]


def _draw_device(surf, kind, rect):
    x, y, w, h = rect
    cx, cy = x + w // 2, y + h // 2
    dark = (18, 28, 48)
    edge = (94, 140, 190)
    screen = (42, 92, 132)
    light = (136, 224, 210)

    def R(rx, ry, rw, rh):
        return (int(x + w * rx), int(y + h * ry), max(1, int(w * rw)), max(1, int(h * rh)))

    def P(rx, ry):
        return (int(x + w * rx), int(y + h * ry))

    if kind == "notebook":
        body = pygame.Rect(R(.15, .10, .70, .62))
        rr(surf, dark, body, 9, edge, 3)
        rr(surf, screen, (body.x + 7, body.y + 7, body.w - 14, body.h - 14), 4, (42, 70, 104), 1)
        D.line(surf, light, (body.centerx - 18, body.centery), (body.centerx + 18, body.centery), 3)
        D.polygon(surf, (116, 138, 166), [P(.08, .76), P(.92, .76), P(.82, .91), P(.18, .91)])
        D.line(surf, edge, P(.08, .76), P(.92, .76), 3)
    elif kind == "desktop":
        rr(surf, dark, R(.10, .08, .52, .70), 8, edge, 3)
        rr(surf, screen, R(.16, .15, .40, .56), 4)
        D.circle(surf, light, P(.20, .68), 3)
        rr(surf, dark, R(.68, .14, .24, .76), 6, edge, 3)
        D.circle(surf, light, P(.80, .76), 4)
    elif kind == "phone":
        rr(surf, dark, R(.30, .04, .40, .92), 13, edge, 4)
        rr(surf, screen, R(.34, .12, .32, .72), 5)
        D.circle(surf, light, P(.50, .90), 4)
        D.line(surf, (240, 246, 255), P(.43, .28), P(.57, .28), 3)
    elif kind == "keyboard":
        rr(surf, dark, R(.06, .28, .88, .48), 8, edge, 3)
        for row in range(3):
            for col in range(10):
                rr(surf, (106, 132, 164), R(.12 + col * .078, .35 + row * .105, .052, .06), 2)
        rr(surf, (106, 132, 164), R(.32, .67, .36, .035), 2)
    elif kind == "mouse":
        rr(surf, dark, R(.32, .12, .36, .74), 24, edge, 3)
        D.line(surf, edge, P(.50, .15), P(.50, .48), 2)
        D.rect(surf, light, (*P(.50, .25), 6, max(4, int(h * .14))), 0, border_radius=3)
    elif kind == "router":
        rr(surf, dark, R(.12, .42, .76, .38), 8, edge, 3)
        D.line(surf, edge, P(.27, .42), P(.18, .08), 4)
        D.line(surf, edge, P(.73, .42), P(.82, .08), 4)
        for col in range(4):
            D.circle(surf, light, P(.30 + col * .13, .67), 4)
    elif kind == "controller":
        D.ellipse(surf, dark, R(.08, .34, .84, .48))
        D.ellipse(surf, edge, R(.08, .34, .84, .48), 3)
        D.rect(surf, light, R(.25, .49, .20, .06), 0, border_radius=3)
        D.rect(surf, light, R(.32, .42, .06, .20), 0, border_radius=3)
        for px, py in ((.70, .48), (.78, .60)):
            D.circle(surf, (255, 192, 106), P(px, py), 5)
    else:  # pequeno eletrodoméstico
        rr(surf, dark, R(.18, .12, .64, .76), 12, edge, 3)
        D.circle(surf, screen, P(.50, .48), int(min(w, h) * .18))
        D.circle(surf, light, P(.50, .48), int(min(w, h) * .18), 3)
        for dx in (-.18, .18):
            D.circle(surf, (180, 190, 205), P(.50 + dx, .80), 4)


def render_equipment(equipment, size=160):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    _draw_device(surf, equipment.kind, (8, 8, size - 16, size - 16))
    return surf


def render_component(component, size=96):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    s = size / 128.0
    def p(v): return int(v * s)
    kind = component.kind
    if kind == "ram":
        rr(surf, (34, 88, 68), (p(12), p(45), p(104), p(34)), p(5), (100, 220, 160), max(1, p(3)))
        for i in range(8):
            D.rect(surf, (215, 198, 106), (p(22 + i * 12), p(35), p(7), p(13)), 0)
            D.rect(surf, (215, 198, 106), (p(22 + i * 12), p(78), p(7), p(13)), 0)
        D.rect(surf, (230, 190, 70), (p(20), p(49), p(88), p(26)), 2)
    elif kind == "ssd":
        rr(surf, (40, 58, 92), (p(18), p(28), p(92), p(72)), p(7), (130, 180, 224), max(1, p(3)))
        D.circle(surf, (224, 190, 98), (p(30), p(40)), p(4))
        TEXT_COLOR = (160, 222, 240)
        D.line(surf, TEXT_COLOR, (p(44), p(50)), (p(94), p(50)), max(1, p(3)))
        D.line(surf, TEXT_COLOR, (p(44), p(64)), (p(84), p(64)), max(1, p(3)))
    elif kind == "cooler":
        D.circle(surf, (72, 104, 140), (p(64), p(64)), p(48))
        D.circle(surf, (160, 194, 220), (p(64), p(64)), p(48), max(1, p(4)))
        for angle in range(0, 360, 90):
            v = pygame.math.Vector2(p(28), 0).rotate(angle)
            D.ellipse(surf, (120, 174, 208), (p(64) + int(v.x) - p(12), p(64) + int(v.y) - p(7), p(30), p(14)))
        D.circle(surf, (34, 52, 82), (p(64), p(64)), p(12))
    elif kind == "metal":
        D.polygon(surf, (144, 158, 178), [(p(18), p(32)), (p(96), p(20)), (p(110), p(94)), (p(30), p(108))])
        D.polygon(surf, (216, 224, 236), [(p(18), p(32)), (p(96), p(20)), (p(110), p(94)), (p(30), p(108))], max(1, p(4)))
        D.line(surf, (255, 255, 255), (p(35), p(48)), (p(92), p(42)), max(1, p(3)))
    elif kind == "plastic":
        rr(surf, (64, 148, 180), (p(26), p(18), p(76), p(92)), p(10), (128, 218, 236), max(1, p(4)))
        for y in (42, 60, 78):
            D.line(surf, (182, 232, 242), (p(38), p(y)), (p(90), p(y)), max(1, p(3)))
    elif kind == "cable":
        for i in range(3):
            D.arc(surf, (210, 138, 76), (p(14 + i * 8), p(20 + i * 14), p(98 - i * 10), p(86 - i * 8)), 0.4, 5.8, max(1, p(7)))
        D.rect(surf, (180, 188, 202), (p(88), p(78), p(24), p(14)), 0, border_radius=p(3))
    elif kind == "board":
        rr(surf, (38, 104, 76), (p(16), p(16), p(96), p(96)), p(5), (114, 218, 160), max(1, p(3)))
        for x, y in ((38, 38), (84, 38), (42, 84), (86, 82)):
            rr(surf, (34, 52, 66), (p(x), p(y), p(22), p(18)), p(2), (196, 206, 212), max(1, p(2)))
        D.lines(surf, (220, 192, 92), False, [(p(24), p(68)), (p(54), p(68)), (p(54), p(56)), (p(104), p(56))], max(1, p(3)))
    else:  # bateria: pictograma fechado; nunca desenhar processo de abertura
        rr(surf, (56, 66, 82), (p(22), p(24), p(84), p(80)), p(8), (238, 180, 80), max(1, p(4)))
        D.rect(surf, (224, 180, 72), (p(52), p(14), p(24), p(10)), 0, border_radius=p(2))
        D.polygon(surf, (255, 218, 84), [(p(72), p(34)), (p(54), p(64)), (p(68), p(64)), (p(58), p(94)), (p(84), p(56)), (p(70), p(56))])
    return surf


# ======================================================================================
# Avaliação do equipamento (Etapa 1): cenários variados, opções fixas.
# ======================================================================================
@dataclass(frozen=True)
class AssessmentOption:
    key: str
    title: str
    subtitle: str
    icon: str


ASSESSMENT_OPTIONS = (
    AssessmentOption("reuse", "REUTILIZAR / DOAR", "Funciona: segue em uso, é doado ou recondicionado", "reuse"),
    AssessmentOption("repair", "MANUTENÇÃO", "Defeito recuperável: assistência técnica qualificada", "wrench"),
    AssessmentOption("recycle", "RECICLAGEM ESPECIALIZADA", "Sem conserto viável: logística reversa", "recycle"),
)


@dataclass(frozen=True)
class Scenario:
    key: str
    title: str
    symptoms: tuple
    answer: str             # chave de AssessmentOption
    explanation: str        # mostrada quando o jogador acerta
    wrong: dict             # chave da opção errada -> explicação
    triage_intro: str


SAFETY_NOTE = ("Baterias e placas eletrônicas só devem ser manipuladas por profissionais e operadores "
               "especializados. Não tente abrir, perfurar ou cortar.")

REUSE_NOTE = "Reutilizar e prolongar a vida útil costuma ser melhor do que descartar."

_NEXT_BATCH = "Agora um notebook do mesmo lote, sem conserto, chega à bancada para triagem de componentes."

SCENARIOS = (
    Scenario(
        "slow", "Lento, mas funcionando",
        ("Liga normalmente e abre os programas.", "Tela, teclado e portas funcionam bem.",
         "Está lento: tem pouca memória e um disco antigo.", "Ainda guarda arquivos pessoais do antigo dono."),
        "reuse",
        "O notebook funciona, então o melhor destino é continuar em uso: ele pode ser doado, vendido ou "
        "recondicionado. Antes de passar adiante, os dados pessoais devem ser apagados com método seguro.",
        {"repair": "Não há defeito a consertar: o aparelho só está lento. O primeiro passo é reaproveitar o "
                   "equipamento inteiro, por doação ou recondicionamento.",
         "recycle": "Reciclar um aparelho que ainda funciona desperdiça a vida útil que ele tem. A reciclagem "
                    "fica para quando não há mais uso possível."},
        _NEXT_BATCH),
    Scenario(
        "battery", "Bateria sem autonomia",
        ("Liga e funciona normalmente na tomada.", "A bateria perdeu a autonomia e desliga em poucos minutos.",
         "Um técnico confirmou que a bateria pode ser substituída."),
        "repair",
        "É um defeito recuperável: um profissional pode substituir a bateria e testar o notebook antes de doar "
        "ou reutilizar. Consertar prolonga a vida útil e evita gerar lixo eletrônico.",
        {"reuse": "O defeito é conhecido e tem solução. Corrija antes de repassar o equipamento, para que ele "
                  "seja realmente útil a quem receber.",
         "recycle": "A bateria pode ser substituída, então o notebook ainda tem conserto. A reciclagem "
                    "especializada é para quando não há recuperação viável."},
        _NEXT_BATCH),
    Scenario(
        "keyboard", "Teclado com falhas",
        ("Liga e funciona, mas várias teclas não respondem.", "Tela e demais partes estão em bom estado.",
         "A assistência técnica informou que o teclado é substituível."),
        "repair",
        "Uma única peça com defeito, que um técnico pode substituir, não justifica descartar o notebook inteiro. "
        "A manutenção devolve o aparelho ao uso.",
        {"reuse": "Doar com defeito transfere o problema para outra pessoa. Conserte antes, e ele poderá ser "
                  "usado por muito mais tempo.",
         "recycle": "Como existe conserto viável, a reciclagem seria precoce: o aparelho ainda pode voltar ao uso."},
        _NEXT_BATCH),
    Scenario(
        "liquid", "Sem conserto",
        ("Não liga mais depois de contato com líquido.", "Há sinais de oxidação e a tela está trincada.",
         "O laudo técnico indica placa danificada e reparo inviável."),
        "recycle",
        "Sem possibilidade de recuperação, o equipamento segue para a logística reversa: um ponto de recebimento "
        "o encaminha a recicladores especializados, que separam peças reutilizáveis, materiais e o que exige "
        "tratamento específico.",
        {"reuse": "O aparelho não funciona e não tem reparo viável, então não serve para doação. O caminho é a "
                  "reciclagem especializada.",
         "repair": "O laudo diz que o reparo é inviável. Insistir em consertar gasta tempo e recursos; encaminhe "
                   "à reciclagem especializada."},
        "O notebook segue para a triagem profissional de componentes."),
)

COMPONENT_MATERIALS = {
    "comp_estrutura_metalica": ("metais",),
    "comp_pecas_plasticas": ("plásticos",),
    "comp_cabos": ("cobre", "plásticos"),
}


def component_materials(component):
    """Materiais que voltam à cadeia produtiva quando o componente é corretamente triado."""
    return COMPONENT_MATERIALS.get(component.item_id, ())


def destination_label(key):
    return next(d[1] for d in DESTINATIONS if d[0] == key)
