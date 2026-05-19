import numpy as np

def get_af_beta(y_r, noise_var, desired_gain=None):
    """
    Calcula o fator de amplificação beta para o relay Amplify-and-Forward.
    O fator garante que a potência transmitida pelo relay não exceda uma certa restrição.
    
    A potência recebida no relay é P_r = E[|y_r|^2].
    beta = sqrt( G / P_r ), onde G é o ganho de potência desejado do relay.
    Se G não for especificado, assume-se que o relay normaliza a energia para 1 (ou mantém a mesma).
    
    Args:
        y_r (np.ndarray): Sinal recebido pelo relay.
        noise_var (float): Potência do ruído (para fins teóricos, se usarmos o sinal recebido real,
                           ele já inclui o ruído).
        desired_gain (float, opcional): Fator de ganho de potência.
        
    Returns:
        beta (float): Fator de escala.
    """
    # Potência média do sinal recebido pelo relay
    p_rx = np.mean(np.abs(y_r)**2)
    
    if desired_gain is None:
        desired_gain = 1.0 # Sem amplificação de potência, apenas normaliza
        
    # beta = sqrt(Ganho / (Potência Sinal Recebido + Potência Ruído))
    # Note que p_rx já é a estimativa de (Potência Sinal + Potência Ruído)
    beta = np.sqrt(desired_gain / p_rx)
    return beta

def apply_af_relay(y_r, beta):
    """
    Aplica o ganho do relay Amplify-and-Forward no sinal recebido.
    
    Args:
        y_r (np.ndarray): Sinal recebido pelo relay (S -> R).
        beta (float): Fator de ganho de amplificação.
        
    Returns:
        x_r (np.ndarray): Sinal transmitido pelo relay (R -> D).
    """
    return beta * y_r
