# ECO NAVE 2.1 — Desafio do Descarte Consciente

Jogo educativo em Python + Pygame sobre coleta seletiva, reutilização, economia circular e logística reversa de eletroeletrônicos. A versão 2.0 preserva o arcade original da nave e das dez lixeiras e acrescenta conquistas, novos resíduos, Oficina Circular, Enciclopédia persistente e trilha sonora.

## Como instalar e executar

Requisitos de execução: Python 3.8+ e Pygame 2.x.

```bash
python -m pip install -r requirements.txt
python main.py
```

Não há dependências Python adicionais além do Pygame. A música e os sprites ficam dentro do próprio projeto. Se o mixer ou os arquivos de música não puderem ser carregados, o jogo continua sem trilha, preservando os demais recursos.

## Novidades da versão 2.0

- **Títulos por nível:** conquistas nos níveis 3, 5, 10, 15 e 20, com letreiro animado, partículas e efeito sonoro especial.
- **Catálogo ampliado:** 56 resíduos tradicionais, todos com identificador estável, desenho próprio e orientação educativa.
- **Oficina Circular:** atividade jogável de avaliação de notebook e classificação de oito componentes em reutilização, recuperação de materiais ou tratamento especializado.
- **Enciclopédia ECO NAVE:** fichas bloqueadas que são reveladas conforme resíduos, equipamento e componentes são encontrados; descobertas permanecem salvas.
- **Trilha sonora:** música chiptune instrumental original, em loop, com volume independente dos efeitos.
- **Guia de descarte real:** abre SINIR, Green Eletron e ABREE para consultar orientações e pontos de recebimento.
- **Resumo aprimorado:** nível, maior título, acertos, erros, precisão, melhor combo e novos objetos descobertos.

## Controles

### Partida arcade

| Tecla | Ação |
|---|---|
| ← → ou A / D | Mover o resíduo entre as faixas |
| ↓ ou S | Acelerar a queda |
| P / ESC | Pausar |
| M | Silenciar / restaurar música e efeitos |
| `[` / `]` | Diminuir / aumentar volume da música |
| `-` / `+` | Diminuir / aumentar volume dos efeitos |
| F11 | Alternar tela cheia |

### Menu principal (hub)

| Tecla / ação | Função |
|---|---|
| ← → ↑ ↓ (ou A / D / W / S) | mover a seleção entre os cartões |
| ENTER / ESPAÇO | abrir o cartão selecionado (começa em **Jogar**) |
| O / C / R / G / H | abrir direto Oficina, Enciclopédia, Ranking, Descarte real, Como jogar |
| V | painel de áudio (música e efeitos separados) |
| M | liga/desliga todo o áudio |
| F11 | tela cheia |
| ESC | sair (pede confirmação) |
| Mouse | passar por cima seleciona, clicar abre |

### Oficina Circular

- Na avaliação, use ← / → ou A / D para selecionar a destinação e ENTER para confirmar.
- Na bancada, use ← / →, A / D ou ↑ / ↓ para navegar entre os componentes.
- ENTER seleciona um componente; em seguida, as mesmas setas escolhem a destinação e ENTER confirma.
- BACKSPACE volta da escolha de destinação para a seleção do componente.
- ESC abre uma confirmação de saída; ENTER / Y confirma e ESC / N continua.

### Enciclopédia e guia

- Enciclopédia: ← / → ou A / D muda a categoria; ↑ / ↓ ou W / S navega pelos itens; ESC retorna.
- Guia de descarte: 1 abre o SINIR, 2 abre o localizador Green Eletron e 3 abre os pontos de recebimento ABREE; ESC retorna.

## Oficina Circular

A primeira atividade jogável usa um notebook antigo. O cenário apresenta um defeito recuperável na bateria, então a escolha adequada é encaminhar para manutenção profissional antes de reutilizar ou doar o aparelho.

Na etapa de triagem, o jogador classifica:

- **Reutilização após testes:** memória RAM, SSD e cooler.
- **Recuperação de materiais:** estrutura metálica, peças plásticas e cabos.
- **Tratamento especializado:** placa eletrônica e bateria.

A oficina é uma simulação educativa de triagem profissional. Não é um manual de reparo doméstico. Baterias e placas devem ser encaminhadas a operadores especializados. Não abra, perfure, dobre, aqueça ou tente desmontar baterias.

Os oito equipamentos do catálogo estão em `eco_nave/workshop_catalog.py`. O notebook é o primeiro desafio completo; os outros equipamentos já têm ficha e representação visual para expansão futura.

## Enciclopédia e arquivos de progresso

As descobertas e os marcos de conquista ficam em `eco_progress.json`, na pasta do projeto (ou na pasta pessoal do usuário se a pasta do projeto não permitir gravação). O arquivo é independente do ranking.

O ranking antigo continua em `ranking.txt`, com os mesmos quatro campos separados por tabulação. O formato e o limite Top 10 não foram alterados.

O sistema de progresso grava identificadores, não nomes visíveis. Isso permite alterar textos e descrições sem perder as descobertas existentes. Se o JSON estiver ausente, o jogo cria um progresso novo; se estiver corrompido, inicia com um progresso vazio sem impedir a partida.

## Como adicionar conteúdo

### Novos resíduos

Adicione a função de desenho ao arquivo da categoria em `eco_nave/items/` e use o decorador `@item(...)` de `eco_nave/items/catalog.py`:

```python
@item("azul", "Novo resíduo", "Orientação educativa e destino correto.")
def _(surface):
    # Desenhe com as funções de eco_nave/drawing.py e pygame.draw.
    pass
```

O `item_id` é gerado a partir do nome quando não informado; para projetos publicados, mantenha os nomes estáveis ou informe um `item_id` explícito. Use metadados separados quando aplicável: `is_electronic`, `is_component`, `reverse_logistics`, `destination`, `fact`, `reuse` e `spawn_weight`. **`spawn_weight` controla o peso de aparição; a antiga flag `ewaste` é aceita apenas por compatibilidade e não altera mais o sorteio.**

Equipamentos eletrônicos completos e a atividade de oficina não devem ser inseridos no sorteador das dez lixeiras. Cadastre novos equipamentos e componentes em `eco_nave/workshop_catalog.py`, incluindo um tipo de desenho em `_draw_device` ou `render_component` e um cenário/etapa próprio em `eco_nave/states/workshop.py`.

### Música

Substitua `assets/audio/eco_nave_theme.ogg` por outro OGG compatível mantendo o mesmo nome. Um WAV com o mesmo nome-base é usado como fallback. Os parâmetros de volume e o gerenciamento da música ficam em `eco_nave/audio_manager.py`; os efeitos sintetizados ficam em `eco_nave/sound.py`.

A faixa incluída é uma trilha instrumental chiptune original, sintetizada para o ECO NAVE 2.0 sem gravações ou samples de terceiros. A música solicitada no OpenGameArt — “Keep your dream alive! (seamless loop)”, de congusbongus, consta na página do autor como CC0, mas o arquivo não pôde ser obtido no ambiente em que esta atualização foi preparada. A faixa incluída **não é** a obra de congusbongus.

Fonte da faixa solicitada: <https://opengameart.org/content/keep-your-dream-alive-seamless-loop> (autor: congusbongus; licença indicada na página: CC0).

## Tela inicial e navegação

```
            ┌──────────── MENU (hub) ────────────┐
   JOGAR    OFICINA CIRCULAR   ENCICLOPÉDIA   RANKING   DESCARTE REAL   COMO JOGAR   ÁUDIO
```

Todas as telas voltam ao hub com ESC. O painel de áudio (V) abre sobre qualquer tela; durante a partida
ele pausa o jogo. A Oficina nunca mexe na partida em andamento (ela tem sua própria sessão).

## Como evitar sobreposição ao criar telas

Não posicione texto por tentativa e erro. Use os helpers de `eco_nave/ui.py`:

- `Ui.fit_block(surf, texto, (x, y, w, h), cor, tamanho_max, tamanho_min)`: quebra o texto e reduz a fonte até caber.
- `Ui.bullets(...)`: lista com marcadores que se ajusta ao espaço.
- `Ui.hint_bar(surf, [("ENTER", "confirmar"), ...], y)`: linha de atalhos centralizada.
- `Ui.header`, `Ui.chip`, `Ui.panel` e `eco_nave/icons.py` para o resto.

Depois rode `python run_tests.py`: `tests/test_layout.py` desenha todas as telas e acusa textos sobrepostos.
Para incluir uma tela nova no teste, acrescente-a em `tests/test_layout.py`.

## Estrutura principal

```text
main.py
README.md
CHANGELOG.md
requirements.txt
ranking.txt                 criado quando o ranking for usado
eco_progress.json           criado ao iniciar o progresso
assets/audio/               música OGG e fallback WAV
eco_nave/
  achievements.py           marcos e títulos
  audio_manager.py          música e volumes independentes
  progress_store.py         persistência JSON
  workshop_catalog.py       catálogo de equipamentos e componentes
  game.py                   gerenciamento das telas e objetos compartilhados
  session.py                partida arcade
  progress.py               pontuação, combos, vidas e nível
  hud.py                    HUD, mensagens e conquistas
  sound.py                  efeitos sintetizados
  items/                    56 resíduos tradicionais
  states/
    workshop.py             Oficina Circular
    codex.py                Enciclopédia
    real_world.py           guia de pontos oficiais de coleta
    menu.py playing.py paused.py name_entry.py ranking_screen.py
```

## Precisão educativa e referências

O jogo utiliza como referência o padrão de cores da Resolução CONAMA nº 275/2001. A aceitação real de materiais depende da coleta seletiva e da estrutura de cada município; as cores do jogo são uma ferramenta didática, não uma garantia de que todo material será recebido em qualquer coletor.

Para eletroeletrônicos, a orientação é separar os aparelhos dos resíduos comuns e consultar pontos de recebimento que aceitem a categoria. O sistema de logística reversa pode envolver recebimento, armazenamento, transporte, triagem, reutilização, reciclagem, recuperação e destinação dos rejeitos. Apague os dados pessoais de dispositivos antes da entrega e não viole o equipamento.

Referências consultadas:

- [Resolução CONAMA nº 275/2001 — padrão de cores](https://www.siam.mg.gov.br/sla/download.pdf?idNorma=291)
- [SINIR — logística reversa de eletroeletrônicos](https://sinir.gov.br/perfis/logistica-reversa/logistica-reversa/eletroeletronicos)
- [Ministério das Comunicações — reaproveitamento de equipamentos eletrônicos (16/07/2026)](https://www.gov.br/mcom/pt-br/noticias/2026/copy_of_julho/logistica-reversa-entenda-como-funciona-o-reaproveitamento-de-equipamentos-eletronicos)
- [Ministério das Comunicações — reusar, recondicionar e reciclar (09/07/2026)](https://www.gov.br/mcom/pt-br/noticias/noticias_alt/2026/julho/reciclar-recondicionar-e-reusar-diferencas-entre-as-formas-de-prolongar-a-vida-util-de-equipamentos-eletronicos)
- [Global E-waste Monitor 2024 — ITU](https://www.itu.int/en/ITU-D/Environment/Pages/Publications/The-Global-E-Waste-Monitor-2024.aspx). O relatório estima que 62 milhões de toneladas de lixo eletrônico foram geradas no mundo em 2022; 22,3% foram documentadas como formalmente coletadas e recicladas de maneira ambientalmente adequada.
- [Green Eletron — localizador](https://greeneletron.org.br/localizador)
- [ABREE — pontos de recebimento](https://abree.org.br/pontos-de-recebimento)

Sempre verifique materiais aceitos, condições e horários diretamente com o ponto de recebimento antes de levar o resíduo.

## Testes

Execute os testes de regras sem abrir a janela do jogo:

```bash
python run_tests.py
```

Os testes cobrem progressão e marcos, combos e vidas, persistência JSON, compatibilidade de leitura/gravação do ranking antigo, identificadores do catálogo, catálogo da oficina e presença/assinatura dos arquivos de áudio.
