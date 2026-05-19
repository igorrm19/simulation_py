# Documentação: `gfdm.py`

## Visão Geral
Implementa as rotinas da forma de onda GFDM (*Generalized Frequency Division Multiplexing*), uma alternativa avançada ao OFDM do 4G, utilizando blocos de símbolos filtrados para diminuir as emissões fora de banda.

## Funções

### `generate_gfdm_matrix(M, K)`
**Objetivo:** Construir a matriz central de modulação do modelo.

- **Parâmetros:**
  - `M`: Número de subportadoras (alocação no domínio da frequência).
  - `K`: Número de subsímbolos por subportadora (alocação no domínio do tempo).
- **Funcionamento:** O tamanho total do pacote gerado é $N = M \times K$. O algoritmo cria um pulso formador "em formato de sino" (uma versão Gaussian/Root-Raised Cosine) para modelar o sinal no tempo. Então, ele preenche a matriz `A` aplicando um deslocamento (shift) no tempo (`np.roll`) e na frequência (`np.exp`) em cada um dos pulsos.
- **Retorno:** Matriz $A$ de dimensões $N \times N$, no domínio dos números complexos.

### `gfdm_modulate(A, s)`
**Objetivo:** Transportar os bits para a estrutura GFDM.

- **Parâmetros:**
  - `A`: A matriz base gerada na função acima.
  - `s`: Símbolos puros oriundos da modulação (ex: QAM).
- **Funcionamento:** Multiplicação matricial direta $x = A \times s$. Cada símbolo ganha uma frequência e um slot de tempo.

### `gfdm_demodulate_zf(A_inv, rx_signal)`
**Objetivo:** Retirar os dados da estrutura da onda ao chegar no receptor.

- **Parâmetros:**
  - `A_inv`: A pseudo-inversa ou inversa da matriz de modulação $A$.
  - `rx_signal`: O vetor de sinal amostrado do ar.
- **Funcionamento:** Aplica a regra de detecção *Zero-Forcing*. Multiplicar a onda que chegou pela matriz inversa da qual a gerou desfaz as rotações de fase, anulando a interferência interna imposta pela modulação GFDM.
