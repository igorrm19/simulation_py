import random
import numpy as np
from deap import base, creator, tools, algorithms
from simulation import run_single_simulation

# Configurações do Problema (Maximização de Throughput e Minimização de BER)
# Pesos: Throughput (+1.0), BER (-1.0)
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def eval_system(individual, snr_db=15):
    """
    Função de avaliação do Indivíduo.
    Indivíduo: [tx_power, relay_gain, num_subcarriers_idx, modulation_idx]
    """
    tx_power = individual[0]
    relay_gain = individual[1]
    
    # Mapeamento discreto
    M_options = [4, 8, 16]
    mod_options = [2, 4, 16, 64]
    
    M = M_options[int(individual[2])]
    mod_order = mod_options[int(individual[3])]
    K = 4 # Mantemos fixo para não explodir a complexidade
    
    ber, throughput, _ = run_single_simulation(
        snr_db=snr_db,
        tx_power=tx_power,
        relay_gain=relay_gain,
        M=M,
        K=K,
        modulation_order=mod_order,
        num_blocks=20, # Reduzido para acelerar o GA
        use_relay=True
    )
    
    # Penalização extrema para BER inaceitável
    if ber > 0.3:
        throughput = 0.0
        
    return throughput, ber

def run_genetic_algorithm(snr_db=15, ngen=10, pop_size=20):
    toolbox = base.Toolbox()
    
    # Atributos:
    # 0: tx_power (0.5 a 2.0)
    # 1: relay_gain (0.5 a 3.0)
    # 2: M_idx (0, 1, 2)
    # 3: mod_idx (0, 1, 2, 3)
    toolbox.register("attr_power", random.uniform, 0.5, 2.0)
    toolbox.register("attr_gain", random.uniform, 0.5, 3.0)
    toolbox.register("attr_M", random.randint, 0, 2)
    toolbox.register("attr_mod", random.randint, 0, 3)
    
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (toolbox.attr_power, toolbox.attr_gain, toolbox.attr_M, toolbox.attr_mod), n=1)
                     
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", eval_system, snr_db=snr_db)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
    toolbox.register("select", tools.selNSGA2) # Seleção multiobjetivo
    
    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    
    # Algoritmo genético simples
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen, 
                                       stats=stats, halloffame=hof, verbose=True)
                                       
    best_ind = hof[0]
    return best_ind, logbook

