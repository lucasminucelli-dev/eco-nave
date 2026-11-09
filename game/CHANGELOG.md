# Changelog

## ECO NAVE 2.1 — Interface renovada

### Corrigido
- **Menu:** as teclas dos cartões (O, C, R, G) eram desenhadas como seta para baixo (`Ui.keycap` só conhecia setas); agora mostram a letra.
- **Menu:** a linha de atalhos ficava em cima das lixeiras e o texto de instruções ocupava metade da tela. Foi substituído por um hub limpo.
- **Oficina Circular:** o texto do cenário se sobrepunha à pergunta e às opções. Todo texto agora é medido antes de ser desenhado.
- **Oficina Circular:** o cenário era sempre o mesmo, a resposta certa era sempre a opção 2 e o próprio texto entregava a resposta. Há 4 cenários sorteados (reutilizar, manutenção ×2 e reciclagem), sem repetir o último.
- **Oficina Circular:** o feedback sumia em ~1,3 s, antes de dar tempo de ler. Agora espera o ENTER.
- **Oficina Circular:** uma escolha errada travava a peça até acertar (a precisão nunca caía de verdade). Agora a explicação aparece, a peça segue para o destino correto e a precisão reflete os erros.
- **Enciclopédia:** o texto de "Informação" e o de "Curiosidade" eram o mesmo; fichas usavam sprites pequenos e só havia setas para trocar de categoria.
- **Conquistas:** o cartão de título cobria o resíduo caindo por ~5 s. Agora fica atrás do lixo e é translúcido.
- **Sorteio:** nenhum item tinha peso maior, então o destaque ao lixo eletrônico/perigoso da versão 1 se perdeu. Pilhas, baterias, lâmpadas, cartuchos, fio de cobre e dissipador voltaram a ter peso 2, agora com a classificação correta (caixa de papelão, manual e capa de celular continuam peso 1).
- **Áudio:** `[` e `]` exigem AltGr em teclado ABNT2. Foi criado o painel de áudio (tecla V); os atalhos antigos continuam funcionando.
- **Progresso:** arquivo corrompido era sobrescrito sem aviso; agora é guardado como `.corrompido`.

### Adicionado
- Tela inicial (hub) com cartões: Jogar, Oficina Circular, Enciclopédia, Ranking, Descarte Real, Como Jogar e Áudio. Navegação por setas/WASD, ENTER, atalhos de letra e mouse. ESC pede confirmação para sair.
- Tela **Como jogar** (controles, regras e legenda das 10 lixeiras).
- Painel de **Áudio** (V): volume da música e dos efeitos separados e mudo. Abrir durante a partida pausa o jogo.
- Oficina: bancada com varredura, peças "saindo" do notebook, bandejas de destino com as peças já triadas, resultado com marcas ✓/✗, materiais recuperáveis e componentes reutilizáveis.
- `eco_nave/icons.py` (ícones por formas) e helpers `Ui.fit_block`, `Ui.bullets`, `Ui.hint_bar`, `Ui.chip`, `Ui.header`.
- `eco_nave/workshop_run.py`: regras da oficina separadas do desenho (testáveis).
- Estatísticas da oficina em `eco_progress.json` (melhor pontuação, rodadas perfeitas).
- `tests/test_layout.py`: detector de sobreposição, que desenha cada tela e falha se dois textos se cruzam, saem da janela ou invadem as lixeiras.
- `tests/test_v21.py`: regras da oficina, pesos do sorteio, RNG independente, persistência e ajuste de texto.

### Alterado
- `Effects` aceita um gerador aleatório próprio; a oficina usa um, então não interfere no sorteio da partida.
- `VERSION = "2.1"` em `config.py`.

## ECO NAVE 2.0 — 04/11/2026

### Adicionado
- Títulos especiais nos níveis 3, 5, 10, 15 e 20, com animação comemorativa e som próprio.
- Registro persistente de conquistas e itens descobertos em `eco_progress.json`.
- 18 novos resíduos tradicionais, ampliando o catálogo de 38 para 56 itens.
- Catálogo separado com oito eletroeletrônicos e oito componentes para a Oficina Circular.
- Estado `WorkshopState` com avaliação do notebook, triagem dos componentes, feedback, pontos, precisão e resumo.
- Estado `CodexState` com categorias e fichas bloqueadas/desbloqueadas.
- Estado `RealWorldState` com links para SINIR, Green Eletron e ABREE.
- Música chiptune instrumental original em OGG, com WAV de fallback.
- Controle independente de volume da música e dos efeitos; atalho M mantido.
- Resumo de fim de partida com título, acertos, erros, precisão, melhor combo e objetos descobertos.
- Testes automatizados das regras e persistência.

### Alterado
- `ItemDef` passou a separar identificação de eletrônico, componente, logística reversa e peso de aparição.
- A propriedade legada `ewaste` continua disponível para compatibilidade, mas deixou de determinar a frequência do sorteio.
- Removidas marcações indevidas de lixo eletrônico em caixa de papelão, manual de instruções e capa de celular.
- Música pausa na tela de pausa e retoma ao continuar, sem reiniciar em transições comuns de tela.
- Menu principal atualizado para os novos modos.
- README ampliado com controles, manutenção, créditos e referências educativas.

### Preservado
- Resolução interna 1280x800 e 60 FPS.
- Fórmula original de pontuação, combos, vidas e progressão de cinco acertos por nível.
- Sorteador tradicional e dez lixeiras.
- Formato tabulado do `ranking.txt` e ranking Top 10.
- Efeitos sonoros sintetizados originais.

### Limitações conhecidas
- A faixa CC0 indicada no pedido, de congusbongus, não pôde ser baixada durante a preparação; foi incluída uma trilha alternativa original, sem samples de terceiros.
- A validação gráfica completa com Pygame não pôde ser executada neste ambiente de preparação porque o pacote Pygame não estava instalado e a conexão para instalá-lo estava indisponível. A sintaxe e os testes independentes de Pygame foram executados.
