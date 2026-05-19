import numpy as np

def generate_gfdm_matrix(M, K):
    N = M * K
    n = np.arange(N)
    g = np.exp(-0.5 * ((n - N/2)/(N/(2*M)))**2) 
    g = g / np.sqrt(np.sum(np.abs(g)**2))
    g = np.fft.ifftshift(g)
    
    A = np.zeros((N, N), dtype=complex)
    for m in range(M):
        for k in range(K):
            col_idx = k + m * K
            pulse = np.roll(g, k * M) * np.exp(1j * 2 * np.pi * m * np.arange(N) / M)
            A[:, col_idx] = pulse
    return A

def gfdm_modulate(A, s):
    return A @ s

def gfdm_demodulate_zf(A_inv, rx_signal):
    return A_inv @ rx_signal
