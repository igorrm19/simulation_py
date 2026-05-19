import matplotlib.pyplot as plt
import numpy as np

def plot_fitness_evolution(logbook, filename="fitness_evolution.png"):
    """
    Plota a evolução da fitness (Throughput e BER) ao longo das gerações.
    """
    gen = logbook.select("gen")
    fit_maxs = np.array(logbook.select("max"))
    fit_avgs = np.array(logbook.select("avg"))
    
    # O GA otimiza (Throughput, -BER). Então extraímos os componentes:
    # Máximos da população
    throughput_max = fit_maxs[:, 0]
    # O BER foi negado na fitness, então invertemos para plotar o valor real do menor BER encontrado
    ber_min = -fit_maxs[:, 1]
    
    # Médias da população
    throughput_avg = fit_avgs[:, 0]
    ber_avg = -fit_avgs[:, 1]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Gerações')
    ax1.set_ylabel('Throughput Máximo (bps)', color=color)
    ax1.plot(gen, throughput_max, 'b-', label='Throughput Max')
    ax1.plot(gen, throughput_avg, 'b--', alpha=0.5, label='Throughput Médio')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('BER Mínimo', color=color)  
    ax2.plot(gen, ber_min, 'r-', label='BER Min')
    ax2.plot(gen, ber_avg, 'r--', alpha=0.5, label='BER Médio')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_yscale('log')
    ax2.legend(loc='upper right')

    fig.tight_layout()  
    plt.title('Evolução da Fitness (GA)')
    plt.savefig(filename)
    plt.close()


def plot_ber_vs_snr(snr_db_range, ber_direct, ber_af, filename="ber_vs_snr.png"):
    """
    Plota a curva BER vs SNR para os casos com e sem Relay AF.
    """
    plt.figure(figsize=(10, 6))
    plt.semilogy(snr_db_range, ber_direct, 'r--o', label='MIMO-GFDM (Link Direto)')
    plt.semilogy(snr_db_range, ber_af, 'b-s', label='MIMO-GFDM (AF Relay)')
    plt.grid(True, which='both')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Taxa de Erro de Bit (BER)')
    plt.title('Performance do Sistema: BER vs SNR')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_comparison(throughput_before, throughput_after, ber_before, ber_after, filename="comparison.png"):
    """
    Plota barras comparativas antes e depois da otimização.
    """
    labels = ['Antes (Default)', 'Depois (Otimizado)']
    throughputs = [throughput_before, throughput_after]
    bers = [ber_before, ber_after]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(8, 6))
    
    rects1 = ax1.bar(x - width/2, throughputs, width, label='Throughput (bps)', color='blue')
    ax1.set_ylabel('Throughput', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, bers, width, label='BER', color='red')
    ax2.set_ylabel('BER', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_yscale('log')
    
    fig.tight_layout()
    plt.title('Comparação de Performance (SNR fixo)')
    plt.savefig(filename)
    plt.close()

