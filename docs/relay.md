# Documentação Técnica: `relay.py`

## 1. Fundamentação Teórica
As comunicações cooperativas são essenciais em Redes 5G para aumentar a cobertura e combater bloqueios (Shadowing). O protocolo **Amplify-and-Forward (AF)** é o protocolo cooperativo com a menor latência de hardware possível: o *relay node* não demodula, não decodifica nem aplica correção de erro de FEC aos dados recebidos. Ele atua na camada analógica (ou digital de baixo nível), captando o sinal sujo de banda base e aplicando um ganho eletrônico de potência antes de dispará-lo na direção do nó destino.

## 2. Detalhamento de Funções e Matemática

### 2.1. `get_af_beta(y_r, noise_var, desired_gain)`
**Propósito:** Extrair o Fator Escalar de Ganho de Potência ($\beta$). Esta é a métrica mais crítica de um Relay AF, responsável por respeitar as regulamentações de controle de energia (Power Constraint) do rádio retransmissor.

- **Estrutura de Dados:**
  - **Entradas:** `y_r` (Array Complexo: O sinal matricial recebido pelo Relay na fase de transmissão 1), `noise_var` (Variância do canal AWGN), `desired_gain` (Potência alvo exigida de transmissão da antena do relay $P_r$).
  - **Saída:** Escalar real $\beta$.

- **Equacionamento Físico-Matemático:**
  Um nó Relay recebe um sinal $y_r$ que é governado por $y_r = H_{sr}x + n_{sr}$. 
  Se ele meramente amplificasse isso com um valor arbitrário alto, a potência irradiada explodiria as limitações da antena, pois ele retransmite o sinal e o ruído $n_{sr}$ amplificados.

  A energia total média instantânea que chega ao receptor do Relay é:
  $$P_{rx} = \mathbb{E}[|y_r|^2]$$
  *(Implementado no código via `np.mean(np.abs(y_r)**2)`)*

  Para assegurar que o Relay lance no ar uma potência restrita e estabilizada igual ao Fator `desired_gain` ($G$), determinamos a razão da raiz quadrada:
  $$\beta = \sqrt{\frac{G}{\mathbb{E}[|y_r|^2]}}$$

### 2.2. `apply_af_relay(y_r, beta)`
**Propósito:** Efetivar a fase cooperativa aplicando a multiplicação espacial algébrica da energia sobre a matriz complexa recebida.

- **Estrutura de Dados:**
  - **Entradas:** Array complexo `y_r` e Escalar real `beta`.
  - **Saída:** Sinal `x_r` (O que será irradiado pela antena repetidora).

- **Equacionamento:**
  A transmissão subsequente, na fase do tempo slot 2, do Relay ($R$) para o Destino ($D$) é:
  $$x_{relay} = \beta y_r$$
  A matemática da amplificação ocorre linearmente, preservando todas as fases e deslocamentos da modulação GFDM (que não são perturbadas, o que é mandatório na camada PHY para evitar rotações de fase corrompidas no Equalizador final). O receptor final receberá $y_{d2} = H_{rd}(\beta (H_{sr}x + n_{sr})) + n_{rd}$.
