# Documentação: `channel.py`

## Visão Geral
Este módulo é responsável por simular o ambiente de propagação dos sinais eletromagnéticos sem fio, inserindo características reais como desvanecimento (fading) e ruído.

## Funções

### `rayleigh_channel(num_rx, num_tx)`
**Objetivo:** Gerar a matriz do canal MIMO considerando um modelo de desvanecimento de Rayleigh.

- **Parâmetros:**
  - `num_rx`: Número de antenas receptoras.
  - `num_tx`: Número de antenas transmissoras.
- **Funcionamento:** Cria uma matriz complexa onde as partes real e imaginária seguem uma distribuição normal padrão $\mathcal{N}(0, 1/\sqrt{2})$. Este modelo é ideal para cenários urbanos onde não há linha de visada direta (NLOS) entre o transmissor e o receptor, fazendo com que o sinal sofra múltiplas reflexões.
- **Retorno:** Matriz complexa `num_rx` $\times$ `num_tx`.

### `add_awgn(signal, noise_var)`
**Objetivo:** Adicionar Ruído Branco Gaussiano Aditivo (AWGN) ao sinal transmitido.

- **Parâmetros:**
  - `signal`: O sinal eletromagnético transmitido (array numpy).
  - `noise_var`: A potência (variância) do ruído a ser adicionado, inversamente proporcional ao SNR.
- **Funcionamento:** Gera ruído térmico aleatório, modelado como um processo Gaussiano complexo. A potência do ruído é escalonada baseada no parâmetro `noise_var` para emular diferentes níveis de degradação da comunicação.
- **Retorno:** 
  - `signal + noise`: O sinal ruidoso final que chega à antena.
  - `noise`: A matriz de ruído puro gerada (para fins de debug/registro).
