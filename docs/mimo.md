# Documentação Técnica: `mimo.py`

## 1. Fundamentação Teórica
O Múltiplas-Entradas Múltiplas-Saídas (MIMO) é o coração das altas velocidades desde o LTE. Multiplicar antenas não apenas concentra feixes elétricos (Beamforming), mas cria **Diversidade Espacial** e **Multiplexação Espacial**. O módulo `mimo.py` lida com o mapeamento e desmapeamento na Constelação Digital (Digital Modulation) e com os algoritmos de Equalização e separação dos streams que se colidiram no ar.

## 2. Detalhamento de Funções e Matemática

### 2.1. Equalizadores (`mmse_detector` e `zf_detector`)
**Propósito:** Inverter os efeitos do desvanecimento do Canal $H$ nas matrizes recebidas do ar. Quando os sinais são transmitidos pelas antenas, eles se emaranham.

- **`zf_detector(H)` (Zero-Forcing):**
  A forma mais agressiva e simples de separar os dados das antenas. Consiste na pseudo-inversa de Moore-Penrose:
  $$\mathbf{W}_{ZF} = (\mathbf{H}^H \mathbf{H})^{-1}\mathbf{H}^H$$
  O ZF forçosamente zera a interferência, mas no limite de $H \to 0$ ele explode o ruído matemático do AWGN (Noise Enhancement).

- **`mmse_detector(H, noise_var)` (Minimum Mean Square Error):**
  O padrão da indústria. Ele minimiza o erro médio quadrático $\mathbb{E}[||\mathbf{s} - \hat{\mathbf{s}}||^2]$. Ao incluir o conhecimento de quanta energia de ruído $\sigma^2$ existe no ambiente, ele cria um balanço entre a eliminação de interferência co-canal e a manutenção do ruído:
  $$\mathbf{W}_{MMSE} = (\mathbf{H}^H \mathbf{H} + \sigma^2 \mathbf{I})^{-1}\mathbf{H}^H$$
  - **Entradas:** Matriz de desvanecimento complexa $H$, variância real do AWGN $\sigma^2$.
  - **Saída:** A matriz de equalização corretiva $\mathbf{W}$. O sinal recuperado será $\hat{\mathbf{y}} = \mathbf{W}\mathbf{y}_{rx}$.

### 2.2. Geração e Mapeamento de Símbolos (`generate_symbols`)
**Propósito:** Instanciar a Carga Útil (Payload) digital e inseri-la no domínio RF via Modulação de Amplitude em Quadratura (QAM).

- **Mapeamentos Suportados:**
  - **BPSK (1 bit/símbolo):** Mapeamento físico unidimensional $\{-1, 1\}$.
  - **QPSK (2 bits/símbolo):** Mapeamento 2D fase-amplitude nas raízes da unidade (normalizado para manter potência 1 via divisão por $\sqrt{2}$).
  - **16-QAM (4 bits/símbolo):** Mapeamento de matriz $4\times4$. Valores base reais $\{-3, -1, 1, 3\}$. Fator de normalização em $\sqrt{10}$.
  - **64-QAM (6 bits/símbolo):** Mapeamento ultra-denso. Níveis de amplitude complexa variando de -7 a 7, e o fator estrito de normalização energética global de $\sqrt{42}$.
- **Retorno:** A função produz dois DataFrames: O vetor analógico Complexo com a onda perfeitamente moldada, e o Buffer de bits lógicos (para contagem de erros futura).

### 2.3. Demodulação (`demodulate_symbols`)
**Propósito:** A transição reversa. Converter a "sopa complexa" que sobrou depois do MMSE em bits lógicos firmes ("Hard Decision" Slicer).

- **Mecânica Aritmética:** O algoritmo retira a normalização do QAM e insere as aproximações do receptor de Limites de Decisão. Em vez de calcular as distâncias euclidianas (Minimum Distance Rule), nós aplicamos matemática booleana sobre eixos em clipes (ex: `np.clip(np.round((r + 3) / 2), 0, 3)`) que fatia a malha IQ em caixas de tolerância rigorosa. Os bits originais são reconstruídos a partir destas localizações espaciais quantizadas.
