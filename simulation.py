import numpy as np
from channel import rayleigh_channel, add_awgn
from relay import get_af_beta, apply_af_relay
from gfdm import generate_gfdm_matrix, gfdm_modulate, gfdm_demodulate_zf
from mimo import generate_symbols, demodulate_symbols, mmse_detector

def run_single_simulation(snr_db, tx_power, relay_gain, M, K, modulation_order, num_blocks=100, use_relay=True):
    """
    Roda uma simulação do sistema MIMO-GFDM com/sem Relay AF para um SNR específico.
    
    Args:
        snr_db (float): SNR em dB.
        tx_power (float): Fator de escala de potência de transmissão.
        relay_gain (float): Ganho de potência do relay.
        M (int): Número de subportadoras GFDM.
        K (int): Número de subsímbolos GFDM.
        modulation_order (int): Ordem de modulação (2, 4, 16, 64).
        num_blocks (int): Número de blocos a serem simulados.
        use_relay (bool): Se True, usa o AF Relay. Se False, apenas link direto.
        
    Returns:
        ber (float): Taxa de Erro de Bit.
        throughput (float): Throughput em bits por segundo (aproximado).
        spectral_eff (float): Eficiência Espectral (bits/s/Hz).
    """
    N = M * K
    num_tx = 2
    num_rx = 2
    
    A = generate_gfdm_matrix(M, K)
    A_inv = np.linalg.pinv(A)
    
    snr_linear = 10**(snr_db / 10)
    
    total_bits = 0
    total_errors = 0
    
    # Bits por símbolo baseado na modulação
    if modulation_order == 2: bits_per_sym = 1
    elif modulation_order == 4: bits_per_sym = 2
    elif modulation_order == 16: bits_per_sym = 4
    elif modulation_order == 64: bits_per_sym = 6
    else: bits_per_sym = 2
    
    for _ in range(num_blocks):
        # 1. Geração de Símbolos MIMO
        s, bits = generate_symbols(num_tx, N, modulation_order)
        s = s * np.sqrt(tx_power) # Aplica controle de potência
        
        # 2. Modulação GFDM
        x_tx = np.zeros((num_tx, N), dtype=complex)
        for i in range(num_tx):
            x_tx[i] = gfdm_modulate(A, s[i])
            
        # Potência do sinal e variância do ruído
        p_signal = np.mean(np.abs(x_tx)**2)
        noise_var = p_signal / snr_linear if snr_linear > 0 else 1.0
        
        # 3. Canais Rayleigh
        H_sd = rayleigh_channel(num_rx, num_tx) # Source -> Destination
        
        # Link Direto
        y_d1, n_d1 = add_awgn(H_sd @ x_tx, noise_var)
        
        if use_relay:
            H_sr = rayleigh_channel(num_rx, num_tx) # Source -> Relay
            H_rd = rayleigh_channel(num_rx, num_tx) # Relay -> Destination
            
            # Source -> Relay
            y_r, n_r = add_awgn(H_sr @ x_tx, noise_var)
            
            # Fase Relay AF
            beta = get_af_beta(y_r, noise_var, desired_gain=relay_gain)
            x_r = apply_af_relay(y_r, beta)
            
            # Relay -> Destination
            y_d2, n_d2 = add_awgn(H_rd @ x_r, noise_var)
            
            # Combinação no Destino (Cooperative Diversity)
            # Y_eq = [y_d1; y_d2]
            # H_eq = [H_sd; H_rd * beta * H_sr]
            H_eq = np.vstack([H_sd, H_rd @ (beta * H_sr)])
            y_combined = np.vstack([y_d1, y_d2])
            
            # Detecção MMSE Combinada
            W = mmse_detector(H_eq, noise_var)
            s_hat_gfdm = W @ y_combined
        else:
            # Apenas Link Direto
            W = mmse_detector(H_sd, noise_var)
            s_hat_gfdm = W @ y_d1
            
        # 4. Demodulação GFDM e desmapeamento
        s_hat = np.zeros((num_tx, N), dtype=complex)
        for i in range(num_tx):
            s_hat[i] = gfdm_demodulate_zf(A_inv, s_hat_gfdm[i])
            
        # Desfaz o ganho de potência para desmapeamento correto
        s_hat = s_hat / np.sqrt(tx_power)
        bits_hat = demodulate_symbols(s_hat, modulation_order)
        
        # Contagem de Erros
        total_errors += np.sum(bits != bits_hat)
        total_bits += bits.size
        
    ber = total_errors / total_bits
    
    # Cálculos de Throughput e Eficiência
    # Assume uma banda B arbitrária, ex: 10 MHz
    B = 10e6
    T_sym = 1 / B # Tempo base de símbolo
    T_block = N * T_sym # Duração do bloco
    
    # Throughput real = (bits transmitidos corretos) / Tempo
    # Simplificação: Taxa de símbolos * (1 - BER)
    # Como o MIMO é 2x2, transmitimos num_tx * N símbolos por bloco
    success_rate = 1.0 - ber
    bits_per_block = total_bits / num_blocks
    
    throughput = (bits_per_block * success_rate) / T_block
    
    # Penalidade por uso do Relay (Half-Duplex) - O tempo de transmissão dobra (2 slots)
    if use_relay:
        throughput /= 2.0
        
    spectral_eff = throughput / B
    
    return ber, throughput, spectral_eff

