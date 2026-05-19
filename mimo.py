import numpy as np

def mmse_detector(H, noise_var):
    Nr, Nt = H.shape
    return np.linalg.inv(H.conj().T @ H + noise_var * np.eye(Nt)) @ H.conj().T

def zf_detector(H):
    return np.linalg.pinv(H)

def generate_symbols(num_antennas, N, modulation_order):
    if modulation_order == 2:
        bits = np.random.randint(0, 2, (num_antennas, N))
        s = 2 * bits - 1 + 0j
        return s, bits
    elif modulation_order == 4:
        bits = np.random.randint(0, 2, (num_antennas, N, 2))
        s = (2 * bits[:,:,0] - 1) + 1j * (2 * bits[:,:,1] - 1)
        s /= np.sqrt(2)
        return s, bits
    elif modulation_order == 16:
        bits = np.random.randint(0, 2, (num_antennas, N, 4))
        real_part = 2 * (2 * bits[:,:,0] + bits[:,:,1]) - 3
        imag_part = 2 * (2 * bits[:,:,2] + bits[:,:,3]) - 3
        s = real_part + 1j * imag_part
        s /= np.sqrt(10)
        return s, bits
    elif modulation_order == 64:
        bits = np.random.randint(0, 2, (num_antennas, N, 6))
        real_part = 2 * (4 * bits[:,:,0] + 2 * bits[:,:,1] + bits[:,:,2]) - 7
        imag_part = 2 * (4 * bits[:,:,3] + 2 * bits[:,:,4] + bits[:,:,5]) - 7
        s = real_part + 1j * imag_part
        s /= np.sqrt(42)
        return s, bits
    else:
        raise ValueError("Ordem de modulação não suportada (2, 4, 16, 64)")

def demodulate_symbols(s_hat, modulation_order):
    num_antennas, N = s_hat.shape
    
    if modulation_order == 2:
        b = (np.real(s_hat) > 0).astype(int)
        return b
    elif modulation_order == 4:
        b = np.zeros((num_antennas, N, 2), dtype=int)
        b[:,:,0] = (np.real(s_hat) > 0).astype(int)
        b[:,:,1] = (np.imag(s_hat) > 0).astype(int)
        return b
    elif modulation_order == 16:
        s_hat = s_hat * np.sqrt(10)
        b = np.zeros((num_antennas, N, 4), dtype=int)
        r = np.real(s_hat)
        b[:,:,0] = (r > 0).astype(int)
        b[:,:,1] = (np.abs(r) < 2).astype(int)
        
        r_level = np.clip(np.round((r + 3) / 2), 0, 3).astype(int)
        i_level = np.clip(np.round((np.imag(s_hat) + 3) / 2), 0, 3).astype(int)
        
        b[:,:,0] = r_level // 2
        b[:,:,1] = r_level % 2
        b[:,:,2] = i_level // 2
        b[:,:,3] = i_level % 2
        return b
    elif modulation_order == 64:
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
