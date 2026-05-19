# Documentação Técnica: `optimization.py`

## 1. Fundamentação Teórica
Nas telecomunicações da vida real (Cognitive Radio Systems / CRN), a antena deve se adaptar instantaneamente às condições da atmosfera. Se ela transmitir na força e modulação máximas o tempo todo com ruído, ela perde todos os pacotes e gasta bateria inútil. Se ela transmitir em BPSK num dia limpo, ela desperdiça um *link* imenso. 
Para resolver dezenas de equações não-lineares, não temos fórmula fechada simples, por isso aplicamos **Inteligência Computacional**. O módulo usa o DEAP para instanciar um **Algoritmo Genético (GA)** voltado ao Pareto (Múltiplos Objetivos).

## 2. Detalhamento de Funções e Matemática

### 2.1. O Cromossomo do Indivíduo (Representation)
No DEAP, um indivíduo é uma array de características lógicas (Genes):
$\text{Cromossomo} = [\text{Potência_{Tx}}, \text{Ganho_{Relay}}, \text{Subportadoras_Index}, \text{Modulação_Index}]$

As funções da rotina `toolbox.register` determinam que a mutação operará em limites randômicos contínuos e discretos (ex: modulação possui índice restrito a 0, 1, 2, 3 correspondentes a 2, 4, 16 e 64-QAM).

### 2.2. A Função de Custo / Aptidão (`eval_system`)
**Propósito:** Modelar o Fitness do gene. O GA é alimentado pela maximização de $f(x)$.

- **Estrutura Bi-Direcional (Multi-Objective):**
  Definimos no topo via `creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))`. Isso diz ao robô: Quero escalar (1.0 positivo) o primeiro retorno ($T_h$), mas quero afundar (-1.0 negativo) o segundo retorno ($BER$).

- **O Paradigma das Punições de Máquina (Penalty Method):**
  Como a busca heurística às vezes escolhe QAM muito denso e o pacote é corrompido de forma irreparável em SNR's terríveis, nós usamos restrições rígidas no escopo da aptidão:
  ```python
  if ber > 0.3:
      throughput = 0.0
  ```
  Isso gera um gradiente mortal para esse gene. Ao ser testado e passar de 30% de pacotes mortos, a recompensa de rede despenca a zero de imediato. Aquele espécime jamais deixará descendentes, forçando as gerações evolutivas a sempre procurarem combinações em que o erro resida abaixo dos trinta por cento críticos.

### 2.3. Operadores Evolutivos (`run_genetic_algorithm`)
**Propósito:** Processamento final da topologia bio-inspirada NSGA-II.
- **`cxTwoPoint` (Cruzamento de Dois Pontos):** Mistura genes numéricas trocando segmentos de pais estocásticos.
- **`mutGaussian` (Mutação):** Adiciona ruído derivado da distribuição Normal com $\mu = 0$ e desvio padrão fixo em $0.2$, com $20\%$ de chance de alterar o genótipo da próxima bateria de simulações.
- **`selNSGA2` (Seleção Multi-Objetivo):** Utiliza a distância de Crowding para classificar as topologias ideais na Fronteira de Pareto.

Ao término das 15 gerações exaustivas, o log devolve o **Hall of Fame** contendo a solução ótima unificada (Sintonia automática do rádio celular do usuário final).
