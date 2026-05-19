# Documentação: `optimization.py`

## Visão Geral
Cérebro de Inteligência Computacional e Machine Learning do simulador baseado no pacote DEAP (Distributed Evolutionary Algorithms in Python). É desenhado para sintonizar dinamicamente todas as engrenagens da antena de forma a extrair as melhores taxas de rede no deserto do mundo real.

## Lógica Evolutiva 
Configurado sob NSGA-II, possui uma arquitetura de múltiplos objetivos, porque queremos ao mesmo tempo a taxa de internet **mais rápida possível** com o **menor volume de perdas**.

- O Cromossomo (Indivíduo) do projeto é um vetor numérico:
  `[potência, ganho do relay, índice GFDM, índice QAM]`

## Funções

### `eval_system(individual, snr_db)`
**Objetivo:** É a famosa Função de Aptidão (Fitness Function) de Darwin.
- Ela lê as opções escolhidas pelo cromossomo.
- Injeta esses parâmetros dentro de `simulation.py` para um rápido test-drive.
- Analisa a performance da tentativa. Se for um sucesso de vazão de dados, recebe alta nota. Contudo, possui uma punição severa se a configuração de QAM foi imprudente e resultou num BER maior que 30% (onde a conexão do celular literalmente seria descartada na vida real).

### `run_genetic_algorithm`
**Objetivo:** Orquestra a "Natureza" sob as leis da evolução.
- `toolbox.register`: Sorteia randomicamente os genes nas primeiras baterias.
- **Tamanho da População (`pop_size`)**: Cria X combinações de rádio e bota os rádios para "competirem" quem transmite melhor no SNR estipulado.
- **Processos Evolutivos**: 
  - *Cruzamento (Mate)*: Pega metade das configs de um vencedor e mistura com a metade de outro.
  - *Mutação*: Adiciona saltos Gaussianos para criar configurações inovadoras nas antenas acidentalmente.
  - *Seleção*: Mata os piores test-drives do monte.
- **Retorno**: Devolve ao final do loop o "Cromossomo Superior" com as melhores estatísticas absolutas no `Hall of Fame` e um livro de registro (`logbook`) das gerações.
