# Documentação Técnica: `simulation.py`

## 1. Fundamentação Teórica
O modelo da camada física em comunicações não é avaliado em base a um único pacote, pois o ruído térmico AWGN e o Fading são variáveis estocásticas randômicas (mudam a cada nanossegundo). Para termos dados estatisticamente válidos da engenharia, utilizamos o método de Simulação de *Monte Carlo*. O módulo `simulation.py` é responsável por fazer o loop de milhares de quadros (frames) de dados dentro das condições geradas, aplicar a combinatória espacial e computar as métricas chaves de qualidade de serviço (QoS).

## 2. Detalhamento de Funções e Matemática

### 2.1. `run_single_simulation`
**Propósito:** Orquestrar o empacotamento completo de ponta a ponta para um ponto fixo de SNR e configuração de rádio, aferindo o *Bit Error Rate* (BER) e as Vazões informacionais.

- **Fluxo Causal Interno:**
  1. Cria os Arrays base via módulo `mimo.generate_symbols`. O número total de símbolos transmitidos em paralelo pelas 2 antenas será $2 \times N$.
  2. Ajusta a energia cinética via multiplicação por escalonamento `tx_power`.
  3. Despacha o vetor de rádio em direção ao ar. O módulo invoca `channel.rayleigh_channel` três vezes consecutivas gerando matrizes de interferências únicas $H_{sd}, H_{sr}, H_{rd}$ simulando uma malha tridimensional de roteamento.
  4. Executa a Matemática Cooperativa do AF Relay (`use_relay=True`):
     A junção de sinais vindos de direções diferentes é o chamado *Cooperative Diversity*. O vetor de observação no Destino recebe um empilhamento matricial (*stacking*):
     $$\mathbf{y}_{eq} = \begin{bmatrix} \mathbf{y}_{d1} \\ \mathbf{y}_{d2} \end{bmatrix} = \begin{bmatrix} \mathbf{H}_{sd} \\ \mathbf{H}_{rd} \beta \mathbf{H}_{sr} \end{bmatrix} \mathbf{x} + \mathbf{\tilde{n}}$$
     Onde $\mathbf{y}_{eq}$ é então empurrado para dentro do estimador Equalizador `mmse_detector`.
  5. Desfaz o GFDM do MMSE via filtro inverso `gfdm_demodulate_zf`.
  6. Quantiza as malhas contínuas de volta em Bits Booleanos.

- **Métricas Matemáticas Aferidas:**
  - **$BER$ (Bit Error Rate):** $\frac{\text{Erros Totais}}{\text{Bits Totais}}$. Mede a Confiabilidade.
  - **Tempo de Bloco ($T_{block}$):** Sendo $B$ a banda espectral estipulada em 10 MHz, o tempo do símbolo em Nyquist é $T_s = 1/B$. O tempo consumido na transmissão é $N \times T_s$.
  - **Throughput ($T_h$):** A quantidade de Bits Válidos empurrados pelo tempo gasto:
    $$T_h = \frac{\text{Bits} \times (1 - BER)}{T_{block}}$$
    *Observação de Hardware:* Operações AF Relay exigem 2 fatias de tempo (*Time Slots*) para que não exista interferência destrutiva na antena do meio do caminho (*Half-Duplex constraint*). Por isso o throughput num teste Relay deve ser dividido rigorosamente por 2.
  - **Eficiência Espectral ($\eta$):** O suprassumo do 5G. Quantos bits você espremeu por segundo em cada hertz locado do governo:
    $$\eta = \frac{T_h}{B} \quad \text{(bits/s/Hz)}$$
