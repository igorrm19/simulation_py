# Simulação 5G NR: MIMO-GFDM com AF Relay e Algoritmo Genético

Este projeto implementa uma simulação simplificada de um sistema de comunicação da camada física (PHY) inspirado no 5G NR. Ele integra as tecnologias:
- **MIMO (Multiple-Input Multiple-Output)**: Transmissão por múltiplas antenas (2x2).
- **GFDM (Generalized Frequency Division Multiplexing)**: Modulação não-ortogonal.
- **AF Relay (Amplify-and-Forward)**: Comunicação cooperativa.
- **Algoritmo Genético (GA)**: Otimização de enlace.

## Requisitos
As dependências do projeto são: `numpy`, `scipy`, `matplotlib` e `deap`.
Você pode instalá-las com:
```bash
pip install numpy scipy matplotlib deap
```

## Como Executar
Basta rodar o arquivo principal:
```bash
python main.py
```
O script gerará três gráficos no diretório atual:
1. `ber_vs_snr.png`: Comparação do BER vs SNR com e sem o AF Relay.
2. `fitness_evolution.png`: Evolução da aptidão (Throughput e BER) ao longo das gerações do GA.
3. `comparison.png`: Comparação de desempenho antes e depois da otimização para um SNR específico.

## Modelagem Matemática

### 1. Modulação GFDM
No GFDM, os dados são organizados em uma matriz onde temos $M$ subportadoras e $K$ subsímbolos. O número total de símbolos por bloco é $N = M \times K$.
A matriz de modulação $A$ de dimensão $N \times N$ é construída a partir de pulsos deslocados no tempo e na frequência:
$$g_{m,k}[n] = g[(n - kM) \bmod N] \cdot e^{j 2 \pi \frac{m n}{M}}$$
O sinal transmitido é dado por $x = A \mathbf{s}$, onde $\mathbf{s}$ é o vetor de símbolos de dados.

### 2. MIMO e Canal Rayleigh
Utilizamos um modelo de canal plano (flat-fading) com desvanecimento de Rayleigh: $H \sim \mathcal{CN}(0, 1)$.
Para um sistema 2x2, $H$ é uma matriz $2 \times 2$. O sinal recebido no destino através do link direto é:
$$y_{d1} = H_{sd} x + n_{d1}$$
Onde $n_{d1}$ é o ruído AWGN com variância $N_0$.

### 3. Relay Cooperativo Amplify-and-Forward (AF)
Na fase 1, o relay também recebe o sinal:
$$y_r = H_{sr} x + n_r$$
Na fase 2, o relay amplifica o sinal com um fator $\beta$ e o retransmite:
$$\beta = \sqrt{\frac{G}{P_r}}$$
Onde $G$ é o ganho do relay e $P_r$ é a potência do sinal recebido no relay.
O sinal recebido no destino via relay é:
$$y_{d2} = H_{rd} (\beta y_r) + n_{d2}$$

### 4. Receptor e Detecção MMSE Combinada
O destino combina os sinais $y_{d1}$ e $y_{d2}$ para decodificar $x$.
$$y = \begin{bmatrix} y_{d1} \\ y_{d2} \end{bmatrix} = \begin{bmatrix} H_{sd} \\ \beta H_{rd} H_{sr} \end{bmatrix} x + \tilde{n}$$
A equalização é feita usando o detector Minimum Mean Square Error (MMSE):
$$W = (H_{eq}^H H_{eq} + N_0 I)^{-1} H_{eq}^H$$
E os símbolos estimados do GFDM são recuperados usando Zero-Forcing (pseudo-inversa de $A$).

### 5. Algoritmo Genético
O GA (`deap`) busca otimizar a camada de enlace alterando:
- **Tx Power**: Potência de transmissão $\in [0.5, 2.0]$.
- **Relay Gain**: Fator de ganho de amplificação $G \in [0.5, 3.0]$.
- **Subportadoras ($M$)**: $\{4, 8, 16\}$.
- **Modulação**: $\{BPSK, QPSK, 16QAM, 64QAM\}$.

A **função objetivo** visa maximizar o Throughput e minimizar o BER, ponderados internamente no DEAP. Se o BER for excessivamente alto, aplica-se uma forte penalidade no Throughput.
