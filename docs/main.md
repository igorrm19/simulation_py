# Documentação Técnica: `main.py`

## 1. Fundamentação Teórica
Sistemas computacionais estocásticos pesados exigem uma sequência determinística de chamadas em script (Entrypoint). O módulo `main.py` não executa modelagem eletromagnética; ele atua puramente como o *Facade* ou Orquestrador arquitetural da execução. É aqui que todos os dados fixos e hiperparâmetros determinísticos (Parâmetros Independentes de Sistema) são cravados antes de acionar a carga computacional das matrizes.

## 2. Detalhamento Estrutural do Fluxo

A estrutura funcional do roteiro ocorre de cima para baixo através da verificação protetora `if __name__ == "__main__":`. Ele dispara três Fases Distintas de Execução Cronológica:

### Fase 1: Avaliação de Base (Baseline System Assessment)
- **Declaração Paramétrica:** Inicializamos as constantes estáticas de fábrica (e.g. `tx_power_def = 1.0`, `relay_gain_def = 1.0`, modulação engessada em `QPSK` (índice 4)).
- **Varredura (SNR Sweep):** O laço `for snr in snr_range:` dispara uma matriz variando em passos fixos as Relações Sinal-Ruído em $0, 5, 10, 15, \text{e} \ 20\text{ dB}$. Isso avalia o limite de *Shannon* imposto na linha de transmissão sem inteligência. As amostras salvam o resultado em listas globais que são enviadas na sequência imediata para a renderização no arquivo secundário da biblioteca.

### Fase 2: Despertar do Algoritmo Genético (Cognitive Machine Learning Phase)
- **Chamada Assíncrona Lógica:** Nós focamos a análise analítica unicamente no SNR $15 \text{ dB}$ arbitrário. O módulo aciona `run_genetic_algorithm(...)` repassando o tamanho da população computacional.
- **Desempacotamento Re-Discreto:** Como o GA devolve índices inteiros normalizados gerados pelo processador randômico e mutações de campânula gaussiana corrompidas (podendo ser negativos por erro normal estatístico), usamos o tratamento aritmético em modulo (`%`) sobre as listas *Lookup* reais:
  ```python
  M_options = [4, 8, 16]
  M_opt = M_options[abs(int(best_ind[2])) % len(M_options)]
  ```
  Essa instrução prova-de-falhas impede índices foragidos gerados pela seleção Darwiniana de cracharem o script e devolve instâncias perfeitas de arquitetura (ex: $16$, $64$).

### Fase 3: Benchmark e Validação Cruzada Otimizada
- Utilizando a decodificação cirúrgica obtida do dicionário `best_ind`, recarregamos uma nova bateria pesada de testes no arquivo `simulation.py` instanciando exatos `100` blocos simulados. Isso não ensina a IA; apenas submete o rádio configurado que ela nos deu na vida real do simulador final, consolidando os comparativos em barras e declarando o fim da simulação complexa da PHY layer via Exit Point nulo.
