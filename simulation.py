import numpy as np
from channel import rayleigh_channel, add_awgn
from relay import get_af_beta, apply_af_relay
from gfdm import generate_gfdm_matrix, gfdm_modulate, gfdm_demodulate_zf
from mimo import generate_symbols, demodulate_symbols, mmse_detector

def run_single_simulation(snr_db, tx_power, relay_gain, M, K, modulation_order, num_blocks=100, use_relay=True):
    N = M * K
    num_tx = 2
    num_rx = 2
    
    A = generate_gfdm_matrix(M, K)
    A_inv = np.linalg.pinv(A)
    
    snr_linear = 10**(snr_db / 10)
    total_bits = 0
    total_errors = 0
    
    for _ in range(num_blocks):
        s, bits = generate_symbols(num_tx, N, modulation_order)
        s = s * np.sqrt(tx_power)
        
        x_tx = np.zeros((num_tx, N), dtype=complex)
        for i in range(num_tx):
            x_tx[i] = gfdm_modulate(A, s[i])
            
        p_signal = np.mean(np.abs(x_tx)**2)
        noise_var = p_signal / snr_linear if snr_linear > 0 else 1.0
        
        H_sd = rayleigh_channel(num_rx, num_tx)
        y_d1, n_d1 = add_awgn(H_sd @ x_tx, noise_var)
        
        if use_relay:
            H_sr = rayleigh_channel(num_rx, num_tx)
            H_rd = rayleigh_channel(num_rx, num_tx)
            
            y_r, n_r = add_awgn(H_sr @ x_tx, noise_var)
            
            beta = get_af_beta(y_r, noise_var, desired_gain=relay_gain)
            x_r = apply_af_relay(y_r, beta)
            
            y_d2, n_d2 = add_awgn(H_rd @ x_r, noise_var)
            
            H_eq = np.vstack([H_sd, H_rd @ (beta * H_sr)])
            y_combined = np.vstack([y_d1, y_d2])
            
            W = mmse_detector(H_eq, noise_var)
            s_hat_gfdm = W @ y_combined
        else:
            W = mmse_detector(H_sd, noise_var)
            s_hat_gfdm = W @ y_d1
            
        s_hat = np.zeros((num_tx, N), dtype=complex)
        for i in range(num_tx):
            s_hat[i] = gfdm_demodulate_zf(A_inv, s_hat_gfdm[i])
            
        s_hat = s_hat / np.sqrt(tx_power)
        bits_hat = demodulate_symbols(s_hat, modulation_order)
        
        total_errors += np.sum(bits != bits_hat)
        total_bits += bits.size
        
    ber = total_errors / total_bits
    
    B = 10e6
    T_sym = 1 / B
    T_block = N * T_sym
    
    success_rate = 1.0 - ber
    bits_per_block = total_bits / num_blocks
    
    throughput = (bits_per_block * success_rate) / T_block
    
    if use_relay:
        throughput /= 2.0
        
    spectral_eff = throughput / B
    
    return ber, throughput, spectral_eff
