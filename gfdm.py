import numpy as np

def generate_gfdm_matrix(M, K):
    """
    Gera a Matriz de Modulação A (N x N) do GFDM, onde N = M * K.
    M: Número de subportadoras.
    K: Número de subsímbolos por subportadora.
    
    Usa um filtro Root Raised Cosine aproximado para o pulso formador.
    """
    N = M * K
    n = np.arange(N)
    
    # Filtro de pulso Gaussiano ou RRC aproximado (forma de sino)
    g = np.exp(-0.5 * ((n - N/2)/(N/(2*M)))**2) 
    g = g / np.sqrt(np.sum(np.abs(g)**2)) # Normaliza energia
    g = np.fft.ifftshift(g) # Shift para centrar no zero
    
    A = np.zeros((N, N), dtype=complex)
    for m in range(M):
        for k in range(K):
            col_idx = k + m * K
            # Deslocamento no tempo (k*M) e frequência (m*N/M)
            pulse = np.roll(g, k * M) * np.exp(1j * 2 * np.pi * m * np.arange(N) / M)
            A[:, col_idx] = pulse
    return A

def gfdm_modulate(A, s):
    """
    Modula os dados usando a matriz GFDM A.
    
    Args:
        A (np.ndarray): Matriz GFDM NxN.
        s (np.ndarray): Vetor de dados de tamanho N (símbolos QAM/QPSK).
        
    Returns:
        x (np.ndarray): Sinal transmitido de tamanho N.
    """
    return A @ s

def gfdm_demodulate_zf(A_inv, rx_signal):
    """
    Demodula o sinal GFDM utilizando Zero-Forcing (Inversa de A).
    
    Args:
        A_inv (np.ndarray): Pseudo-inversa ou inversa de A.
        rx_signal (np.ndarray): Sinal recebido estimado.
        
    Returns:
        s_hat (np.ndarray): Símbolos estimados de tamanho N.
    """
    return A_inv @ rx_signal
