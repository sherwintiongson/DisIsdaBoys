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
sig1_Hz = np.sin(2*np.pi*50*t)

# create the square wave harmonic frequency
sig2_Hz = np.sin(2*np.pi*150*t) * (1/3)
sig3_Hz = np.sin(2*np.pi*250*t) * (1/5)
sig4_Hz = np.sin(2*np.pi*350*t) * (1/7)
sig5_Hz = np.sin(2*np.pi*450*t) * (1/9)
sig6_Hz = np.sin(2*np.pi*550*t) * (1/11)
sig7_Hz = np.sin(2*np.pi*650*t) * (1/13)
sig8_Hz = np.sin(2*np.pi*750*t) * (1/15)
sig9_Hz = np.sin(2*np.pi*850*t) * (1/17)
sig10_Hz = np.sin(2*np.pi*950*t) * (1/19)

# combine signals to form a square wave
sig_combined = sig1_Hz + sig2_Hz + sig3_Hz + sig4_Hz + sig5_Hz + sig6_Hz + sig7_Hz + sig8_Hz + sig9_Hz + sig10_Hz

# filter to smooth out the ripple
lpf_out = moving_average_filter(sig_combined, 20)

# generate noise
noise = np.random.normal(0, 0.08, len(lpf_out))

# add noise
with_noise = lpf_out + noise

# plot
f, plt_arr = plt.subplots(4, figsize=(15, 9), sharex=True)
f.suptitle("Fourier Series Demo")

plt_arr[0].plot(sig_combined, color='red')
plt_arr[0].set_title("sig_combined", color='red')

plt_arr[1].plot(lpf_out, color='blue')
plt_arr[1].set_title("lpf_out", color='blue')

plt_arr[2].plot(noise, color='blue')
plt_arr[2].set_title("noise", color='blue')

plt_arr[3].plot(with_noise, color='blue')
plt_arr[3].set_title("with_noise", color='blue')

plt.legend()
plt.show()