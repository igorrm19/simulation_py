# Documentação Técnica: `channel.py`

## 1. Fundamentação Teórica
Em sistemas de comunicações móveis como o 5G NR, o canal de rádio é o meio físico de propagação. Devido a reflexões, refrações e espalhamentos no ambiente (prédios, árvores, veículos), o sinal transmitido chega ao receptor através de múltiplos caminhos (Multipath Fading). O módulo `channel.py` abstrai matematicamente essas imperfeições do canal, incorporando Desvanecimento de Rayleigh e Adição de Ruído AWGN.

## 2. Detalhamento de Funções e Matemática

### 2.1. `rayleigh_channel(num_rx, num_tx)`
**Propósito:** Instanciar a Matriz de Canal (Channel State Information - CSI) modelada por uma distribuição de Rayleigh, essencial para a análise espacial de múltiplas antenas (MIMO).

- **Estrutura de Dados (Input/Output):**
  - **Entradas:** `num_rx` (Inteiro, número de antenas de recepção), `num_tx` (Inteiro, número de antenas de transmissão).
  - **Saída:** $H \in \mathbb{C}^{N_r \times N_t}$, uma matriz Numpy 2D de números complexos.

- **Equacionamento Físico-Matemático:**
  A envolvente complexa do desvanecimento de canal base (Flat Fading) é modelada de forma que as partes em fase (Real) e em quadratura (Imaginária) do coeficiente do canal sigam distribuições normais Gaussianas independentes com média zero e variância $1/2$.
  
  $$H_{i,j} = \frac{X + jY}{\sqrt{2}} \quad \text{onde} \quad X, Y \sim \mathcal{N}(0, 1)$$
  
  Dessa forma, a amplitude do ganho de canal $|H_{i,j}|$ segue uma **Distribuição de Rayleigh** pura e a potência (seu quadrado) possui média unitária $\mathbb{E}[|H_{i,j}|^2] = 1$. O escalonamento por $\sqrt{2}$ garante que o canal não adicione ou subtraia energia na média teórica, apenas distorça a fase e amplitude.

### 2.2. `add_awgn(signal, noise_var)`
**Propósito:** Emular a interferência eletromagnética randômica e térmica inerente ao *hardware* de radiofrequência e ambiente natural (Ruído Branco Gaussiano Aditivo).

- **Estrutura de Dados:**
  - **Entradas:** `signal` (Array Numpy contendo os símbolos pré-processados que atravessaram o canal MIMO), `noise_var` (Float representando a potência do ruído $N_0$).
  - **Saídas:** A tupla `(y, n)`, onde `y` é o sinal contaminado e `n` é a matriz pura de ruído que foi injetada, devolvida para checagens ou cálculos posteriores de energia.

- **Equacionamento Físico-Matemático:**
  Dado um sinal transmitido complexo vetorial $x$, a recepção em banda base é modelada pela equação matricial fundamental:
  
  $$\mathbf{y} = \mathbf{H}\mathbf{x} + \mathbf{n}$$
  
  O vetor de ruído $\mathbf{n}$ possui distribuição Gaussiana Circular Simétrica complexa: $\mathbf{n} \sim \mathcal{CN}(0, \sigma^2 \mathbf{I})$, onde $\sigma^2$ é igual a `noise_var`.
  O código simula isso dividindo a variância em duas metades (Real e Imaginária):
  
  $$n = \left( \mathcal{N}(0,1) + j\mathcal{N}(0,1) \right) \cdot \sqrt{\frac{\sigma^2}{2}}$$

  Essa precisão na injeção do ruído é vital, pois a Relação Sinal-Ruído (SNR) depende que a energia deste AWGN seja cravada em cima do logaritmo planejado pela simulação global.
