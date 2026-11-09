# Changelog

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
