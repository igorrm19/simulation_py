# Documentação Técnica: `utils.py`

## 1. Fundamentação Teórica
Nas simulações de camada física, as abstrações matriciais extraídas de milhares de simulações iterativas (Monte Carlo) só adquirem significado técnico real através da Visualização de Dados (Data Visualization). Este módulo não computa simulações analíticas; ao invés disso, serve para a conversão vetorial da biblioteca `numpy` para os *plots* dimensionais da biblioteca `matplotlib`, lidando com transformações de escala e *warning silencers*.

## 2. Detalhamento de Funções e Lógica Visual

### 2.1. Ocultação de Erros de Escala (Warnings)
- No início do arquivo usamos o `warnings.filterwarnings("ignore")`. Como as simulações em alto SNR produzem uma taxa de erro que pode chegar a $0.0$ cravado matematicamente, o `matplotlib` reclama ao tentar forçar uma escala `log` em cima de zero (matematicamente infinito negativo). Esta camada garante que o software não polua o terminal com notificações se as antenas apresentarem perfomance 100% livre de defeitos temporariamente.

### 2.2. `plot_fitness_evolution(logbook, filename)`
**Propósito:** Modelar a curva convergente da Inteligência Biológica em dois eixos perpendiculares.
- **Estrutura de Entrada:** Recebe o dicionário `logbook`, uma estrutura nativa do framework DEAP preenchida contendo médias, mínimos e máximos vetoriais extraídos a cada *snapshot* das passagens dos séculos (gerações).
- **Tratamento Matemático:** O eixo da esquerda da figura (Azul) é mantido em Linear pois a Velocidade (Throughput) escala puramente. Contudo, o módulo instancia o código vital `ax1.twinx()`, criando uma dimensão virtual Y secundária (Vermelha) atrelada à mesma linha do tempo (eixo X), cuja a escala é convertida em notação científica algorítmica ($10^{-x}$) para abarcar a volatilidade massiva dos índices fracionários do BER usando:
  ```python
  if np.any(ber_min > 0) or np.any(ber_avg > 0):
      ax2.set_yscale('log')
  ```

### 2.3. `plot_ber_vs_snr(...)` e `plot_comparison(...)`
**Propósito:** Geração das figuras fixas clássicas da IEEE.
- O Waterfall plot em cascata do `plot_ber_vs_snr` sobrepõe vetores que percorrem SNRs (Relação de Energia) num plot `plt.semilogy()`. Essa função converte nativamente a renderização em grades dimensionais, essenciais para mostrar que ganhar de 3 dB para 6 dB na torre corta a taxa de erros pela metade de forma logarítmica descendente.
- O `plot_comparison` usa álgebra posicional simples (`x - width/2` e `x + width/2`) gerando uma barra composta lado a lado, isolando a performance humana teórica versus o resultado estocástico encontrado pela sintonia do algoritmo genético do DEAP.
