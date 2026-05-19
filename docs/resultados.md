# 📈 Interpretação dos Resultados da Simulação

Este documento detalha as conclusões e os fenômenos observados a partir dos resultados gráficos gerados pelo simulador da rede 5G NR (MIMO-GFDM com AF Relay e IA). O objetivo do sistema é encontrar o melhor ponto de equilíbrio (*trade-off*) entre a eficiência espectral (Vazão) e a confiabilidade do link (Taxa de Erro de Bit).

Após a execução do cenário principal (`main.py`), três artefatos visuais são gerados:

## 1. O Ganho da Comunicação Cooperativa (AF Relay)
**Gráfico correspondente:** `ber_vs_snr.png`

O primeiro resultado crítico que a simulação demonstra é o impacto da utilização da técnica de *Amplify-and-Forward* (AF) em um nó Relay.
- **O Desafio do Fading:** Em um link de rádio direto (Transmissor ➡️ Receptor), o sinal frequentemente sofre desvanecimento de Rayleigh (quedas profundas de potência devido a múltiplos caminhos e obstáculos).
- **O Comportamento Observado:** A curva "Waterfall" de BER (eixo Y logarítmico) versus o SNR (eixo X em dB) mostra que a inclusão do nó Relay diminui substancialmente os erros de transmissão sob os mesmos níveis de ruído. 
- **Conclusão:** O algoritmo equalizador do receptor consegue somar a energia do caminho direto com o caminho cooperativo do Relay. O gráfico comprova matematicamente a melhoria da confiabilidade, garantindo o funcionamento do sistema mesmo em regiões de cobertura mais fracas (Baixo SNR).

## 2. A Evolução e o Aprendizado da Inteligência Artificial
**Gráfico correspondente:** `fitness_evolution.png`

O segundo resultado tangível do sistema diz respeito ao processo cognitivo do Algoritmo Genético (NSGA-II) durante a busca da calibração ideal da rede.
- **Otimização Multiobjetivo:** A rede possui duas métricas de sucesso conflitantes. Se aumentarmos indiscriminadamente a potência de transmissão ou a ordem de modulação (ex: usando 64-QAM em vez de 4-QAM), a vazão de dados sobe muito, mas o índice de erro (BER) também explode. 
- **O Comportamento Observado:** O gráfico temporal de evolução mostra as gerações da IA no eixo X. Nos eixos Y (Y1 para *Throughput*, Y2 para *BER*), vemos que, nas gerações iniciais, o algoritmo testa parâmetros muito caóticos e subótimos. Com o passar do tempo evolutivo, as curvas estabilizam, o sistema converge e encontra configurações precisas.
- **Conclusão:** A simulação atesta que o uso de Machine Learning para alocação de recursos da camada PHY é extremamente vantajoso. A IA encontra autonomamente a potência, o ganho do Relay e a ordem de modulação exatos que extraem a maior velocidade de conexão sem estourar o limite aceitável de perdas de pacotes.

## 3. O Impacto Direto: Sistema Não-Otimizado vs. Otimizado
**Gráfico correspondente:** `comparison.png`

O resultado final traduz as descobertas da IA em ganhos absolutos para a telecomunicação através de um comparativo "Antes e Depois".
- **O Cenário Padrão:** Antes da otimização, sistemas convencionais utilizam parâmetros fixos (potência e modulação hard-coded) que ignoram as condições dinâmicas e reais do canal de rádio no instante da transmissão.
- **O Comportamento Observado:** O gráfico de barras evidencia duas métricas lado a lado (Vazão e BER). O comparativo revela uma discrepância nítida. O sistema retroalimentado pela IA não apenas entrega consideravelmente mais dados, como mantém os erros controlados.
- **Conclusão:** Os dados finais atestam que infraestruturas de rádio avançadas (MIMO + Relay + GFDM) precisam ser orquestradas ativamente. A adoção da inteligência artificial permite extrair o desempenho máximo das frequências de rádio disponíveis, provando o valor das redes auto-otimizáveis (*Self-Organizing Networks*) no ecossistema 5G NR e tecnologias futuras.

---
*Este relatório reflete o comportamento médio esperado ao se executar a rotina principal Monte Carlo configurada na raiz do repositório (`main.py`).*
