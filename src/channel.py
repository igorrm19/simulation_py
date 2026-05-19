import numpy as np

def rayleigh_channel(num_rx, num_tx):
    return (np.random.randn(num_rx, num_tx) + 1j * np.random.randn(num_rx, num_tx)) / np.sqrt(2)

def add_awgn(signal, noise_var):
    shape = signal.shape
    noise = (np.random.randn(*shape) + 1j * np.random.randn(*shape)) * np.sqrt(noise_var / 2)
    return signal + noise, noise
