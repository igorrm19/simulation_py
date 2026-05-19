# Documentação Científica: Interpretação de Gráficos

Ao rodar a simulação, três relatórios visuais são salvos na pasta base:

## 1. `ber_vs_snr.png` (Curva em Cascata Logarítmica)
- **O Eixo X (Horizontal)** é a força do sinal em relação ao ruído ambiente (SNR, medido em dB). Andar para a direita significa possuir um equipamento melhor com menos interferência estática no ar.
- **O Eixo Y (Vertical)** é o BER (Bit Error Rate), ou a proporção de pacotes arruinados na conexão. Está numa escala de Log10 para facilitar a visualização que decai muito severamente.
- **Explicação:** A comparação exibe que a linha azul (com AF Relay Cooperativo ligado) decai muito mais rápido que a vermelha (Link direto sem relay), provando empiricamente o **Ganho de Diversidade Espacial** que um repetidor inteligente fornece, mitigando o problema do desvanecimento profundo sem precisar estourar a bateria do celular.

## 2. `fitness_evolution.png` (O Algoritmo Genético)
- **O Eixo X (Horizontal)** representa o relógio biológico-evolutivo, as passagens de Gerações.
- **Múltiplos Eixos:** A linha Azul contínua e tracejada pontuam a Vazão absoluta de dados (Throughput) para os melhores e a média, respectivamente. A linha Vermelha mede os erros persistentes durante a comunicação.
- **Explicação:** Mostra o Computador resolvendo o problema não-linear de otimização no escuro. Repare que perto das primeiras rodadas, o software tenta forçar sinais com Throughput altíssimos mas que geram taxas de perdas imensas porque ele usa parâmetros errados. Em meados da geração 10 e diante, as linhas vermelhas desmoronam de nível e o throughput atinge o nível mais alto suportável matematicamente pelo ambiente sem corromper a comunicação de forma fatal, indicando convergência e maturidade celular.

## 3. `comparison.png` (Gráfico de Barras Duplas)
- Exibe dezenas de barras de medição mostrando o Antes versus o Depois.
- **Explicação:** Demonstra visivelmente os conceitos abstratos de compensação (o "Trade-Off"). O computador foi capaz de aumentar sua transmissão para velocidades assustadoras ao encontrar chaves ideais de potência e arranjos QAM perfeitos para aquele instante. Contudo, essa velocidade extra gera mais perdas parciais (O BER no otimizado é discretamente mais elevado, mas contido no nível de restrição exigido pela função de custo). Isso é a Engenharia operando em prol do aproveitamento de eficiência espectral!
