import numpy as np

def get_af_beta(y_r, noise_var, desired_gain=None):
    p_rx = np.mean(np.abs(y_r)**2)
    if desired_gain is None:
        desired_gain = 1.0
    beta = np.sqrt(desired_gain / p_rx)
    return beta

def apply_af_relay(y_r, beta):
    return beta * y_r
