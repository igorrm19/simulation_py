import numpy as np

def rayleigh_channel(num_rx, num_tx):
    """
    Gera um canal Rayleigh flat-fading complexo.
    H ~ CN(0, I)
    
    Args:
        num_rx (int): Número de antenas receptoras.
        num_tx (int): Número de antenas transmissoras.
        
    Returns:
        H (np.ndarray): Matriz de canal num_rx x num_tx.
    """
    return (np.random.randn(num_rx, num_tx) + 1j * np.random.randn(num_rx, num_tx)) / np.sqrt(2)

def add_awgn(signal, noise_var):
    """
    Adiciona Ruído Branco Gaussiano Aditivo (AWGN) ao sinal.
    
    Args:
        signal (np.ndarray): Sinal transmitido/recebido.
        noise_var (float): Variância do ruído (potência do ruído).
        
    Returns:
        y (np.ndarray): Sinal ruidoso.
        n (np.ndarray): O ruído gerado.
    """
    shape = signal.shape
    noise = (np.random.randn(*shape) + 1j * np.random.randn(*shape)) * np.sqrt(noise_var / 2)
    return signal + noise, noise
