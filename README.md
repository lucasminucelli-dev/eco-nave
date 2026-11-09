# ECO NAVE – Desafio do Descarte

Jogo educativo em Python/pygame sobre coleta seletiva e lixo eletrônico.
Uma nave alienígena solta resíduos do alto da tela; guie cada um até a lixeira da cor certa.

## Como rodar

```
pip install -r requirements.txt     # pygame 2.x
python main.py
```

O ranking fica salvo em `ranking.txt` (um jogador por linha, campos separados por tabulação), na mesma pasta do `main.py`.
Nenhuma imagem ou som externo é usado: tudo é desenhado/gerado no código.

## Teclas

| Tecla | Ação |
|---|---|
| ← → (ou A / D) | mover o lixo |
| ↓ (ou S) | acelerar a queda |
| P / ESC | pausar |
| M | liga/desliga o som |
| F11 | tela cheia |
| ENTER | confirmar / jogar |

## Estrutura do projeto

```
main.py                  ← ponto de entrada: abre a janela e roda o Game
eco_nave/
  game.py                Game: laço principal, troca de telas e objetos compartilhados
  session.py             Session: uma partida (lixo, nave, lixeiras, acerto/erro)
  progress.py            Progress: pontos, vidas, combo, nível
  spawner.py             ItemSpawner: sorteio do próximo lixo (com regras de justiça)
  entities.py            Trash (lixo em queda) e Ship (nave)
  bin_row.py             BinRow: fileira de lixeiras e suas animações
  effects.py             Effects, Particle, Popup, ItemEffect: confete, faíscas, textos
  hud.py                 Hud, MessageBox, LevelBanner: placar, dica educativa, aviso de nível
  backdrop.py            Backdrop, StarField, FloatingItem: fundo animado
  ranking.py             RankingStore e RankEntry: leitura/gravação do ranking
  sound.py               SoundFx: sons sintetizados
  assets.py / sprites.py Assets e SpriteFactory: sprites desenhados por formas
  text.py / ui.py        TextRenderer (fontes e cache) e Ui (painéis e teclas)
  bins.py                BinType e BinCatalog: as 10 lixeiras e suas cores
  facts.py               curiosidades educativas
  config.py              tamanho da tela, vidas, Difficulty (curvas de dificuldade)
  utils.py / drawing.py  funções auxiliares de cor, formatação e desenho
  items/                 catálogo de resíduos (um arquivo por lixeira)
    catalog.py           ItemDef e ItemCatalog
    paper.py plastic.py glass.py metal.py wood.py
    hazardous.py health.py radioactive.py organic.py nonrecyclable.py
  states/                uma classe por tela
    base.py              GameState (base) e AttractState (menu/ranking)
    menu.py playing.py paused.py name_entry.py ranking_screen.py
```

## Onde mexer para…

| Quero… | Arquivo |
|---|---|
| mudar tamanho da tela, vidas, nível | `eco_nave/config.py` |
| deixar o jogo mais fácil/difícil | `Difficulty` em `eco_nave/config.py` |
| mudar a pontuação ou o combo | `eco_nave/progress.py` |
| adicionar um novo resíduo | o arquivo da lixeira em `eco_nave/items/` (copie um bloco `@item(...)`) |
| mudar cores/nomes das lixeiras | `eco_nave/bins.py` |
| editar as curiosidades | `eco_nave/facts.py` |
| mudar o visual do menu, pausa ou ranking | o arquivo correspondente em `eco_nave/states/` |
| criar uma nova tela | nova classe em `eco_nave/states/` herdando de `GameState` e registrada em `Game.states` |
| trocar o formato do ranking | `eco_nave/ranking.py` |

## Como as telas funcionam

Cada tela é uma classe que herda de `GameState` e implementa `enter()`, `handle_key()`,
`update(dt)` e `draw(surf)`. O `Game` guarda a tela ativa e troca com
`game.set_state("nome", **dados)`; os dados chegam no `enter()` da nova tela
(por exemplo, `RankingState.enter(new_entry=..., note=...)`).
