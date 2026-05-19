# Documentação Técnica: `gfdm.py`

## 1. Fundamentação Teórica
O **GFDM** (*Generalized Frequency Division Multiplexing*) é um esquema de modulação multi-portadora não-ortogonal concebido como uma evolução de onda flexível perante o OFDM (LTE/4G). Ele ataca o principal problema do OFDM: A enorme emissão fora de banda (Out-of-Band Emission). Através da aplicação matemática de filtros de conformação de pulso (Pulse Shaping Filters) circulares nas subportadoras, o GFDM confina a energia, essencial para comunicações IoT de espectro fragmentado e baixa latência no 5G.

## 2. Detalhamento de Funções e Matemática

### 2.1. `generate_gfdm_matrix(M, K)`
**Propósito:** Sintetizar a Matriz de Modulação (Transmissor) do bloco GFDM. O GFDM opera em dados em formato de blocos de tamanho $N = K \times M$.

- **Estrutura de Dados:**
  - **Entradas:** `M` (Total de Subportadoras no domínio da Frequência), `K` (Total de Subsímbolos no domínio do Tempo).
  - **Saída:** A matriz central de alocação $A$, onde $A \in \mathbb{C}^{N \times N}$.

- **Equacionamento Físico-Matemático:**
  No GFDM, diferentemente do OFDM, a base do sinal de transmissão é modelada não apenas por uma Transformada de Fourier retangular, mas pela translação de uma função filtro pulso $g[n]$. O código usa uma aproximação gaussiana de *Root-Raised Cosine*. O pulso base para o sub-símbolo $k$ na subportadora $m$ é gerado por:
  
  $$g_{k,m}[n] = g[(n - kM) \bmod N] \cdot \exp\left(j 2 \pi \frac{m}{M} n\right)$$

  onde $n = 0, 1, \dots, N-1$. A translação temporal é garantida por convolução circular (na programação em `numpy`, utilizamos a função `np.roll(g, k * M)`). O pulso de filtro base $g$ é calculado por:
  $$g[n] = \exp\left( -0.5 \left( \frac{n - N/2}{N / (2M)} \right)^2 \right)$$
  E escalonado por energia unitária via norma Euclidiana. Essa matriz construída em blocos contém o emaranhado das subportadoras. 

### 2.2. `gfdm_modulate(A, s)`
**Propósito:** Mapeamento paralelo maciço do bloco de símbolos numéricos para as frequências aéreas base.

- **Equacionamento:**
  A modulação GFDM em banda base discreta é expressa puramente como uma operação matricial:
  $$\mathbf{x} = \mathbf{A}\mathbf{s}$$
  Onde $\mathbf{s}$ é o vetor coluna $N \times 1$ contendo os dados empacotados (símbolos QAM complexos). Se o sistema usar antena MIMO, essa função rodará $N_t$ vezes para cada array de símbolos e cada antena propagará seu bloco $\mathbf{x}$.

### 2.3. `gfdm_demodulate_zf(A_inv, rx_signal)`
**Propósito:** Demodulação em bloco no estágio receptor.

- **Estrutura de Dados:**
  - **Entradas:** `A_inv` (A Pseudo-inversa calculada analiticamente de $A$), `rx_signal` (Sinal pós-equalizador MMSE, após a torre já ter cancelado o ruído espacial).
  - **Saída:** Vetor de símbolos $\hat{s}$ (Valores complexos QAM que ainda flutuam devido aos resquícios de distorção não mitigada).

- **Equacionamento Físico-Matemático:**
  Como o GFDM perde a ortogonalidade (uma subportadora vaza um pouco para a do vizinho de propósito para cortar os lóbulos laterais e suavizar a OOBE), a simples FFT clássica não funciona. Nós mitigamos essa Interferência Inter-Portadora Inerente (ICI) usando uma matriz inversa linear:
  $$\hat{\mathbf{s}}_{ZF} = \mathbf{A}^{-1} \mathbf{y}$$
  Essa operação recupera perfeitamente os símbolos sob a ótica de canal ideal (Zero-Forcing).
