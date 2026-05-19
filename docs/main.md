# Documentação: `main.py`

## Visão Geral
O script condutor principal que um usuário de terminal rodaria ao operar a simulação. Em termos práticos, é o programa cliente que acopla todos os módulos.

## Fluxo Lógico (main)

O código funciona em 3 passos progressivos:

1. **A Ferramenta Base:**
   Dá ignição nas funções sem a interferência da Inteligência Artificial. Ele faz uma *Varredura (Sweep)*. Aumenta a potência da torre progressivamente e manda o `simulation.py` testar as respostas até ter dados suficientes para construir a primeira imagem (Relay vs Sem Relay).
   No final da etapa, ele marca uma posição de referência para SNR = 15 dB.

2. **O Momento Evolutivo:**
   O script convoca o `optimization.py` e liga o modelo DEAP. Ao terminar a simulação, que demora devido ao peso matemático brutal das matrizes do GFDM cruzadas com Múltiplas Antenas MIMO repetidamente, ele obtém a resposta da evolução natural e plota a curva.

3. **Validação Final:**
   Rodando na vida real para validar, o script pluga o que o robô achou nas simulações base, computa a última bateria final e sobrepõe no gráfico de barras para gerar o `comparison.png`, provando ao engenheiro humano as conclusões do software.
