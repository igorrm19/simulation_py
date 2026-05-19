# Documentação: `simulation.py`

## Visão Geral
A espinha dorsal (Core) do projeto. Este módulo amarra a lógica matemática de todos os blocos construtores. Ele passa uma corrente de bits pela montagem GFDM, cruza as camadas de antenas MIMO e afere os resultados no receptor final.

## Funções

### `run_single_simulation`
**Objetivo:** Roda um pacote completo no ambiente e afere o que sobreviveu à comunicação sem fio.

- **Parâmetros:**
  - `snr_db`: SNR (Signal to Noise Ratio) injetado na simulação em Decibéis.
  - `tx_power`: Nível de energia escalonado do transmissor móvel.
  - `relay_gain`: O ganho de recepção e disparo na antena relê.
  - `M`, `K`: Parâmetros de modulação espectral do GFDM.
  - `modulation_order`: Bits por Hertz do QAM.
  - `num_blocks`: Quantidade de pacotes que o Monte Carlo rodará para tirar a média estatística.
  - `use_relay`: Booleano para usar a matriz Cooperativa ou apenas atirar em linha reta.
  
- **Funcionamento em Blocos:**
  1. Cria os símbolos binários virtuais e aplica controle de energia Tx Power (`mimo.py`).
  2. Modula as ondas aplicando o filtro Roll do GFDM em cima dos arrays QAM criados (`gfdm.py`).
  3. Despacha o sinal para dois caminhos virtuais. O Link Direto sofre um fading H_sd.
  4. (Bloco Relay): Se ativo, ele envia o sinal pra um canal secundário H_sr, sofre interferência e amplifica beta (`relay.py`). Depois envia pro caminho H_rd.
  5. O software empilha (Concatena) o que veio do link direto com o que veio do relay, forjando um sinal rico com diversidade espacial.
  6. Injeta tudo no equalizador MMSE para destruir as multipaths.
  7. Desfaz a forma da onda GFDM e re-lê o QAM voltando a ter bits.

- **Métricas de Retorno Calculadas:**
  - `ber`: Bit Error Rate. Taxa de pacotes falhos contabilizados após tudo isso.
  - `throughput`: Capacidade estimada em Bits por Segundo (Bps). Penalizado pela metade (Half-Duplex) caso use relay porque consome 2 timeslots.
  - `spectral_eff`: Eficiência que compara Throughput perante a banda em Mhz configurada (10Mhz default).
