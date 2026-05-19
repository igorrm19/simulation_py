import numpy as np
from src.simulation import run_single_simulation
from src.optimization import run_genetic_algorithm
from src.utils import plot_fitness_evolution, plot_ber_vs_snr, plot_comparison

def main():
    print("Iniciando Simulação 5G NR MIMO-GFDM-AF...")
    
    print("\n--- 1. Avaliação do Sistema Padrão ---")
    snr_range = np.arange(0, 21, 5)
    
    tx_power_def = 1.0
    relay_gain_def = 1.0
    M_def = 8
    K_def = 4
    mod_order_def = 4
    
    ber_direct_list = []
    ber_af_list = []
    
    print("Calculando BER vs SNR...")
    for snr in snr_range:
        ber_d, _, _ = run_single_simulation(snr, tx_power_def, 1.0, M_def, K_def, mod_order_def, use_relay=False)
        ber_direct_list.append(ber_d)
        
        ber_r, _, _ = run_single_simulation(snr, tx_power_def, relay_gain_def, M_def, K_def, mod_order_def, use_relay=True)
        ber_af_list.append(ber_r)
        print(f"SNR: {snr}dB | BER Direct: {ber_d:.4f} | BER AF: {ber_r:.4f}")
        
    plot_ber_vs_snr(snr_range, ber_direct_list, ber_af_list)
    print("Gráfico BER vs SNR salvo.")
    
    snr_opt = 15
    ber_before, th_before, _ = run_single_simulation(snr_opt, tx_power_def, relay_gain_def, M_def, K_def, mod_order_def, num_blocks=50)
    print(f"\nDesempenho Default (SNR={snr_opt}dB): Throughput={th_before:.2e} bps, BER={ber_before:.4e}")
    
    print("\n--- 2. Executando Algoritmo Genético ---")
    print("Otimizando: tx_power, relay_gain, Num_Subcarriers, Modulation...")
    best_ind, logbook = run_genetic_algorithm(snr_db=snr_opt, ngen=15, pop_size=30)
    
    plot_fitness_evolution(logbook)
    print("Gráfico da evolução do GA salvo.")
    
    M_options = [4, 8, 16]
    mod_options = [2, 4, 16, 64]
    
    tx_power_opt = best_ind[0]
    relay_gain_opt = abs(best_ind[1])
    M_opt = M_options[abs(int(best_ind[2])) % len(M_options)]
    mod_order_opt = mod_options[abs(int(best_ind[3])) % len(mod_options)]
    
    print(f"\nMelhor Indivíduo Encontrado:")
    print(f"Tx Power: {tx_power_opt:.2f}")
    print(f"Relay Gain: {relay_gain_opt:.2f}")
    print(f"Subcarriers (M): {M_opt}")
    print(f"Modulation (QAM): {mod_order_opt}")
    
    print("\n--- 3. Avaliação Final ---")
    ber_after, th_after, _ = run_single_simulation(snr_opt, tx_power_opt, relay_gain_opt, M_opt, K_def, mod_order_opt, num_blocks=100)
    print(f"Desempenho Otimizado (SNR={snr_opt}dB): Throughput={th_after:.2e} bps, BER={ber_after:.4e}")
    
    plot_comparison(th_before, th_after, ber_before, ber_after)
    print("Gráfico de comparação salvo.")
    print("\nSimulação Concluída!")

if __name__ == "__main__":
    main()
