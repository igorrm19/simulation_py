# Documentação: `mimo.py`

## Visão Geral
Este módulo foca na inteligência das múltiplas antenas (MIMO) e nas modulações de mercado utilizadas em celulares digitais. A modulação converte zeros e uns em coordenadas no plano real/imaginário (Fase e Amplitude).

## Funções

### `generate_symbols(num_antennas, N, modulation_order)`
**Objetivo:** Criar os bits binários de teste e convertê-los na modulação física QAM/PSK.

- **Parâmetros:**
  - `num_antennas`: Para suportar diversidade espacial (ex: 2 antenas enviando streams diferentes).
  - `N`: Quantidade de amostras.
  - `modulation_order`: Ordem da constelação (2=BPSK, 4=QPSK, 16=16-QAM, 64=64-QAM).
- **Funcionamento:** Sorteia uma corrente de números binários. Depois, agrupa os binários e os "plota" num gráfico complexo. Em QPSK, dois bits `(0, 1)` viram o número `-1 + 1j`. No 64-QAM, seis bits viram coordenadas mais refinadas, exigindo precisão na sintonia.
- **Retorno:** Os símbolos complexos ajustados de energia normalizada e os bits corretos originais.

### `demodulate_symbols(s_hat, modulation_order)`
**Objetivo:** Reverter as coordenadas complexas afetadas por ruído de volta para bits discretos.

- **Parâmetros:**
  - `s_hat`: Os símbolos recebidos.
  - `modulation_order`: O mapa que foi usado na origem.
- **Funcionamento:** Corta o plano cartesiano em "quadrantes de decisão" (Hard Decision). Ex: Em BPSK, se o número tem parte Real maior que zero, ele é lido como bit 1, se for menor, bit 0. O algoritmo executa lógicas avançadas de aproximação aritmética para desmapear 16-QAM e 64-QAM.

### Detecção Espacial (Equalizadores)

- **`zf_detector(H)`:** Detector *Zero-Forcing*. Apenas inverte o canal de rádio ($H^{-1}$). Zera a interferência, mas no processo acaba explodindo qualquer ruído presente no fundo.
- **`mmse_detector(H, noise_var)`:** Minimum Mean Square Error. O estado da arte de receivers em modens de Wi-Fi e 5G. Ele incorpora a variância do ruído na matriz de ponderação para conseguir o melhor meio-termo matemático entre "diminuir a interferência" e "não amplificar o ruído".
