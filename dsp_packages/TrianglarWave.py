import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
from matplotlib import style

def moving_average_filter(data, window_size):
    """
    Applies a moving average FIR filter to the input data.
    Parameters:
    - data: Input data (1D array or list)
    - window_size: Size of the moving average window
    Returns:
    - filtered_data: Output data after applying the moving average filter
    """
    filtered_data = []
    for i in range(len(data) - window_size + 1):
        window = data[i : i + window_size]
        average = sum(window) / window_size
        filtered_data.append(average)
    return filtered_data

# sampling rate 2KHz, nyquist is 2KHz / 2 = 1KHz
t = np.linspace(0, 1, 5001)

# create the square wave fundamental frequency
sig1_Hz = np.sin(2*np.pi*100*t)

# create the square wave harmonic frequency
sig2_Hz = np.sin(2*np.pi*100*t) * (1/9)
sig3_Hz = np.sin(2*np.pi*300*t) * (1/25)
sig4_Hz = np.sin(2*np.pi*500*t) * (1/49)
sig5_Hz = np.sin(2*np.pi*700*t) * (1/81)
sig6_Hz = np.sin(2*np.pi*900*t) * (1/121)
sig7_Hz = np.sin(2*np.pi*1100*t) * (1/169)
sig8_Hz = np.sin(2*np.pi*1300*t) * (1/225)
sig9_Hz = np.sin(2*np.pi*1500*t) * (1/289)
sig10_Hz = np.sin(2*np.pi*1700*t) * (1/361)

# combine signals to form a square wave
sig_combined = sig1_Hz + sig2_Hz + sig3_Hz + sig4_Hz + sig5_Hz + sig6_Hz + sig7_Hz + sig8_Hz + sig9_Hz + sig10_Hz

# filter to smooth out the ripple
lpf_out = moving_average_filter(sig_combined, 12)

# plot
plt.plot(lpf_out,label ='lpf_out')
plt.xlabel('time')
plt.title('Combined Waves')
plt.legend()
plt.show()