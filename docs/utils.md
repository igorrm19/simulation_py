# Documentação: `utils.py`

## Visão Geral
Este script é o painel de leitura do sistema. Ele usa a matemática e a extrai para um formato visual. Lida majoritariamente em converter matrizes brutas do `numpy` para os gráficos `matplotlib`.

## Funções

### `plot_fitness_evolution(logbook, filename)`
Acessa o Logbook diário gerado pela inteligência artificial a cada geração rodada, traça uma linha histórica e imprime no disco uma figura com dois eixos. Ela constrói linhas sólidas e tracejadas identificando as estatísticas médias e as máximas.

### `plot_ber_vs_snr(snr_db_range, ber_direct, ber_af, filename)`
Construção clássica em engenharia de telecomunicações, um gráfico de cascata ou Waterfall. Trata a dimensão logarítmica (pois erros caem muito abruptamente, da casa dos décimos para casa de milionésimos) para desenhar quão superior a antena 2 é contra a antena 1.

### `plot_comparison(throughput_before, ...)`
Plota colunas comparativas mostrando quão maior (Bps) as transferências ficaram depois de todas as otimizações, permitindo auditorias visuais de Trade-Offs (velocidade contra erros).
