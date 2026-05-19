# Documentação: Bibliotecas Utilizadas

O sistema 5G NR foi montado empregando tecnologias consagradas da comunidade científica Python em *Data Science* e Algoritmos Estruturais.

## Numpy (`numpy`)
- **Papel:** É a fundação do código. O simulador não lida com inteiros ou strings, mas sim com dezenas de matrizes com dezenas de milhares de posições.
- O Numpy faz toda a álgebra de modulação do sinal (como inverter canais MMSE) baseada em suas rotinas escritas em C e *Fortran* internamente no pacote `numpy.linalg`.

## Scipy (`scipy`)
- **Papel:** De forma silenciosa e abstraída, o Scipy serve de apoio interno para as integrações matriciais matemáticas que as arquiteturas GFDM e Rayleigh demandam para funcionarem sem gargalar a CPU do computador durante centenas de simulações Monte Carlo do Python.

## DEAP (`deap`)
- **Papel:** Sigla para *Distributed Evolutionary Algorithms in Python*.
- É o responsável por trazer a camada de *Machine Learning* via computação Bio-Inspirada. Utiliza-se da rotina **NSGA-II** porque o nosso problema não era apenas aumentar velocidade ou baixar erro, mas sim as duas coisas. Lida com Seleção natural, Hall da Fama evolutivo e Mutação de Genes.

## Matplotlib (`matplotlib`)
- **Papel:** A câmera do sistema. Extrai números abstratos das listas da memória RAM e elabora painéis esteticamente perfeitos. Lida de forma magistral com renderizações em escala linear e escala logarítmica simultâneas.
