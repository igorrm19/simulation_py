import numpy as np

def mmse_detector(H, noise_var):
    """
    Calcula a matriz de equalização MMSE para o canal H.
    W = (H^H * H + sigma^2 * I)^-1 * H^H
    
    Args:
        H (np.ndarray): Matriz do Canal.
        noise_var (float): Variância do ruído (N0).
        
    Returns:
        W (np.ndarray): Matriz do detector MMSE.
    """
    Nr, Nt = H.shape
    # (H^H * H + sigma^2 * I)^-1 * H^H
    return np.linalg.inv(H.conj().T @ H + noise_var * np.eye(Nt)) @ H.conj().T

def zf_detector(H):
    """
    Calcula a matriz de equalização Zero-Forcing (ZF) para o canal H.
    W = (H^H * H)^-1 * H^H = pinv(H)
    """
    return np.linalg.pinv(H)

def generate_symbols(num_antennas, N, modulation_order):
    """
    Gera símbolos complexos para a transmissão baseados na ordem de modulação M-QAM/PSK.
    Retorna os símbolos e os bits correspondentes.
    
    Suporta: 2 (BPSK), 4 (QPSK), 16 (16-QAM), 64 (64-QAM)
    
    Args:
        num_antennas (int): Número de antenas Tx.
        N (int): Tamanho do bloco GFDM.
        modulation_order (int): 2, 4, 16, 64.
        
    Returns:
        s (np.ndarray): Símbolos complexos gerados de dimensão (num_antennas, N).
        bits (np.ndarray): Array de bits gerados (apenas para referência de BER, para QPSK gera 2 bits por símb).
    """
    # Simplificação: mapeamento aleatório direto em constelações padronizadas
    # Para o BER, a forma mais precisa é mapear e desmapear bits, mas
    # podemos gerar inteiros e comparar diretamente os símbolos ou bits.
    # Vamos gerar os bits explicitamente para BPSK e QPSK, e inteiros para ordens maiores
    
    if modulation_order == 2: # BPSK
        bits = np.random.randint(0, 2, (num_antennas, N))
        s = 2 * bits - 1 + 0j
        return s, bits
        
    elif modulation_order == 4: # QPSK
        bits = np.random.randint(0, 2, (num_antennas, N, 2))
        s = (2 * bits[:,:,0] - 1) + 1j * (2 * bits[:,:,1] - 1)
        s /= np.sqrt(2) # Normaliza
        return s, bits
        
    elif modulation_order == 16: # 16-QAM (simplificado)
        # Amplitudes -3, -1, 1, 3
        bits = np.random.randint(0, 2, (num_antennas, N, 4))
        real_part = 2 * (2 * bits[:,:,0] + bits[:,:,1]) - 3
        imag_part = 2 * (2 * bits[:,:,2] + bits[:,:,3]) - 3
        s = real_part + 1j * imag_part
        s /= np.sqrt(10) # Normaliza (potência média do 16QAM é 10)
        return s, bits
        
    elif modulation_order == 64: # 64-QAM (simplificado)
        bits = np.random.randint(0, 2, (num_antennas, N, 6))
        real_part = 2 * (4 * bits[:,:,0] + 2 * bits[:,:,1] + bits[:,:,2]) - 7
        imag_part = 2 * (4 * bits[:,:,3] + 2 * bits[:,:,4] + bits[:,:,5]) - 7
        s = real_part + 1j * imag_part
        s /= np.sqrt(42) # Normaliza (potência média do 64QAM é 42)
        return s, bits
    else:
        raise ValueError("Ordem de modulação não suportada (2, 4, 16, 64)")

def demodulate_symbols(s_hat, modulation_order):
    """
    Desmapeia os símbolos recebidos de volta para bits.
    """
    num_antennas, N = s_hat.shape
    
    if modulation_order == 2: # BPSK
        b = (np.real(s_hat) > 0).astype(int)
        return b
        
    elif modulation_order == 4: # QPSK
        b = np.zeros((num_antennas, N, 2), dtype=int)
        b[:,:,0] = (np.real(s_hat) > 0).astype(int)
        b[:,:,1] = (np.imag(s_hat) > 0).astype(int)
        return b
        
    elif modulation_order == 16: # 16-QAM
        s_hat = s_hat * np.sqrt(10)
        b = np.zeros((num_antennas, N, 4), dtype=int)
        # Região de decisão simplificada para real
        r = np.real(s_hat)
        b[:,:,0] = (r > 0).astype(int)
        b[:,:,1] = (np.abs(r) < 2).astype(int) # -2 a 2 = bit 1 (se invertido ou não, depende do map, mas vamos ser consistentes)
        # Vamos usar uma aproximação de hard decision mais simples
        # Voltando para os níveis 0, 1, 2, 3 que mapeiam para -3, -1, 1, 3
        r_level = np.clip(np.round((r + 3) / 2), 0, 3).astype(int)
        i_level = np.clip(np.round((np.imag(s_hat) + 3) / 2), 0, 3).astype(int)
        
        b[:,:,0] = r_level // 2
        b[:,:,1] = r_level % 2
        b[:,:,2] = i_level // 2
        b[:,:,3] = i_level % 2
        return b
        
    elif modulation_order == 64: # 64-QAM
        s_hat = s_hat * np.sqrt(42)
        b = np.zeros((num_antennas, N, 6), dtype=int)
        
        r_level = np.clip(np.round((np.real(s_hat) + 7) / 2), 0, 7).astype(int)
        i_level = np.clip(np.round((np.imag(s_hat) + 7) / 2), 0, 7).astype(int)
        
        b[:,:,0] = r_level // 4
        b[:,:,1] = (r_level % 4) // 2
        b[:,:,2] = r_level % 2
        
        b[:,:,3] = i_level // 4
        b[:,:,4] = (i_level % 4) // 2
        b[:,:,5] = i_level % 2
        return b
        
    return None
