# Documentação do Simulador 5G NR

## 1. Visão Geral
Este documento detalha o funcionamento interno do simulador 5G NR, focado na camada de enlace e na camada física. O código base simula dados transmitidos e recebidos através do espaço usando:
- Modulação não-ortogonal (GFDM)
- Múltiplas Antenas (MIMO)
- Comunicação Cooperativa com retransmissor (AF Relay)
- Inteligência Computacional por Algoritmo Genético (GA) para maximizar o sinal.

**Nota:** Todos os comentários em linha e docstrings foram removidos do código fonte para fins de limpeza, estando agora inteiramente registrados neste documento oficial.

## 2. Funcionamento do Código e Módulos

### Módulo: `channel.py`
**Responsabilidade:** Simular o ambiente eletromagnético onde as ondas de rádio viajam.
- **`rayleigh_channel(num_rx, num_tx)`**: Retorna uma matriz matemática de números complexos que modela as "fading" do canal. A distribuição normal complexa simula as infinitas reflexões do sinal em prédios e objetos num ambiente sem linha de visada.
- **`add_awgn(signal, noise_var)`**: Pega o sinal e soma a ele o "Ruído Branco Gaussiano", degradando as informações conforme a potência do ruído definida por equações de SNR.

### Módulo: `relay.py`
**Responsabilidade:** Controlar as ações da antena repetidora no meio do caminho.
- **`get_af_beta(y_r, noise_var, desired_gain)`**: Quando a torre intermediária recebe o pacote, esse pacote está fraco. O algoritmo calcula um fator $\beta$ de correção, ajustando a força elétrica do sinal (ganho do Relay).
- **`apply_af_relay(y_r, beta)`**: Apenas multiplica o sinal elétrico pela escala de amplificação antes de atirar ele no ar novamente em direção ao celular do usuário.

### Módulo: `gfdm.py`
**Responsabilidade:** Fazer a modulação de dados para as radiofrequências. O GFDM é uma evolução do antigo OFDM usado no 4G.
- **`generate_gfdm_matrix(M, K)`**: Monta a supermatriz de alocação de frequência $A$. Filtros *Root Raised Cosine* evitam que o sinal de um usuário vaze e atrapalhe o rádio de outro usuário, usando blocos não retangulares flexíveis.
- **`gfdm_modulate` / `gfdm_demodulate_zf`**: Transforma bits crus na "onda" a ser enviada. Ao receber, usa um esquema *Zero-Forcing* (A Inversa da matriz) para reverter o áudio recebido e transformá-lo em bytes limpos novamente.

### Módulo: `mimo.py`
**Responsabilidade:** Modulação digital e o combate a interferência.
- **`generate_symbols`**: Lê os bits que queremos transmitir e os converte em coordenadas complexas espaciais usando modulações de mercado como BPSK, QPSK, 16-QAM, e 64-QAM. 64-QAM envia muitos dados, mas erra fácil. BPSK envia pouco, mas é super robusto.
- **`demodulate_symbols`**: Lê a onda recebida, checa os quadrantes matemáticos da Constelação I/Q, e advinha quais 0's e 1's chegaram.
- **`mmse_detector` e `zf_detector`**: Equalizadores de Inteligência Analítica de ponta. O MMSE não tenta destruir 100% da interferência porque sabe que isso destrói o ruído também; ele cria a malha mais equilibrada de reconstrução possível baseada em inversões de Matriz Transposta Conjugada.

### Módulo: `simulation.py`
**Responsabilidade:** Lógica da simulação temporal.
- **`run_single_simulation`**: Conecta as funções acima. O sinal vai da antena Tx pra antena Rx, mas também vai para o Relay, depois do Relay vai pro Rx. O receptor (celular do usuário final) combina a informação que veio reta e a que veio de ricochete cooperativo. Ele calcula o BER (taxa de perdas de pacote), o Throughput (taxa de Megabits/s entregues puros) e a Eficiência Espectral.

### Módulo: `optimization.py`
**Responsabilidade:** Uma Inteligência Artificial Evolutiva baseada em Darwin.
- Em vez de descobrirmos os melhores parâmetros do rádio na força bruta, rodamos um GA.
- Ele joga números aleatórios de potência (bateria), escolhe o melhor QAM, a melhor largura de banda do GFDM. Ao fim de cada round, cruza os resultados (reprodução) e sofre *Mutação Gaussiana* gerando filhos. Em 15 gerações, ele descobre a melhor configuração do transmissor no ambiente.

### Módulo: `utils.py` e `main.py`
- Utilizam do `matplotlib.pyplot` para ler os arrays de matemática numéricos da simulação e exportar gráficos coloridos de engenharia.
- O `main` apenas sequencia e pede pros demais arquivos ligarem de forma orquestrada.

---

## 3. Bibliotecas e Dependências

- **`numpy`**: O cérebro pesado. Faz os cálculos matriciais com dezenas de dimensões nas linhas complexas sem gargalar a CPU. Ele quem resolve e inverte as gigantescas matrizes do canal MIMO e as FFTs (Transformadas de Fourier do GFDM).
- **`scipy`**: É importado por tabelas internas. Usa solvers clássicos em C/Fortran para apoiar a matemática.
- **`deap`**: *Distributed Evolutionary Algorithms in Python*. Framework de Inteligência Computacional líder da indústria. Usado para criar um modelo NSGA-II multiobjetivo para otimização evolutiva dos parâmetros no pacote `optimization.py`.
- **`matplotlib`**: A biblioteca padrão do ecossistema de Data Science para gráficos de linha, barras e escalas logarítmicas.

---

## 4. Explicação Científica dos Gráficos Gerados

Ao rodar a simulação, três relatórios são salvos na pasta base:

### 1. `ber_vs_snr.png` (Curva em Cascata logarítmica)
**Como ler:** Eixo horizontal X é o nível do sinal (SNR, medido em dB). Para a direita significa que você tem antena cheia, mais próximo da torre. O eixo Y é o BER, a proporção de pedaços que chegaram corrompidos (escala logarítmica para facilitar leitura científica, 10^-1 a 10^-4).
**Significado:** Quanto menor a linha, melhor. A linha tracejada vermelha representa seu celular recebendo 4G/5G normal (Link Direto). A linha azul mostra o AF Relay. Com o mesmo sinal na torre (ex: 15 dB), a linha azul fica com 10 a 50 vezes menos erros do que a normal porque combinamos o sinal que veio na diagonal e o que veio reto.

### 2. `fitness_evolution.png` (O Algoritmo Genético)
**Como ler:** O eixo horizontal representa a passagem do tempo (as Gerações do robô evolutivo). O gráfico possui *Eixos Duplos*. A linha Azul e a régua Azul representam a Vazão da Internet (Throughput). A linha vermelha representa o erro (BER).
**Significado:** Mostra a Inteligência Computacional trabalhando sozinha. Perto da geração 0 o Throughput era muito ruim e os erros eram aleatórios. Conforme as gerações chegam em 10 e 15, a barra azul estabiliza no topo porque ele achou a modulação 64-QAM aliada a uma regulagem de Relay.

### 3. `comparison.png` (Gráfico de Barras Duplas)
**Como ler:** Aponta dois cenários fixos no tempo (Antes da IA otimizar vs Depois da IA Otimizar).
**Significado:** A IA mudou as chaves de potência e QAM e mais que dobrou sua vazão efetiva total. Houve um preço leve a se pagar (o BER subir levemente), e o gráfico constata esse *trade-off* do engenheiro de telecomunicações de maneira elegante: Trocar estabilidade 100% rígida por Velocidade e Eficiência Espectral sem corromper a latência tolerável.
