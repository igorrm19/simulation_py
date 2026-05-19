# Documentação: `relay.py`

## Visão Geral
Modela um nó de comunicação cooperativa do tipo *Amplify-and-Forward* (AF). Um nó relay AF não decodifica a mensagem; ele apenas recebe o sinal elétrico e o amplifica antes de retransmitir.

## Funções

### `get_af_beta(y_r, noise_var, desired_gain=None)`
**Objetivo:** Calcular o fator de escalonamento dinâmico $\beta$ (ganho de potência) para o relay.

- **Parâmetros:**
  - `y_r`: Sinal completo recebido pelo relay (incluindo desvanecimento e ruído).
  - `noise_var`: Variância do ruído inserido no canal.
  - `desired_gain`: Ganho de potência alvo que o relay tentará alcançar.
- **Funcionamento:** Como o relay amplifica também o ruído, é crucial que a potência da transmissão não estoure limites físicos do hardware. A potência de entrada é aferida (`p_rx`), e o ganho $\beta$ é extraído tirando a raiz quadrada da divisão entre a potência que se quer e a que se tem.
- **Retorno:** `beta` (float) - o escalar de amplificação.

### `apply_af_relay(y_r, beta)`
**Objetivo:** Realizar a etapa física de amplificação no hardware do relay.

- **Parâmetros:**
  - `y_r`: O sinal captado pela antena.
  - `beta`: O escalar calculado por `get_af_beta`.
- **Funcionamento:** Simplesmente multiplica as amplitudes e fases do sinal vetorial recebido pelo fator de ganho ajustado, construindo o sinal que será atirado no espaço novamente.
- **Retorno:** Sinal complexo amplificado (array numpy).
