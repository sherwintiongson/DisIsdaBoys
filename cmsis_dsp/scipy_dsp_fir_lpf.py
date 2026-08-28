import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
from matplotlib import style




# sampling rate 2KHz, nyquist is 2KHz / 2 = 1KHz
t = np.linspace(0, 1, 2001)

# generate 5Hz sine wave sine(2*pi*f*t)
voffset = 0
#voffset = 2062
sig_5Hz = np.sin(2*np.pi*5*t) * 100
sig_50Hz = np.sin(2*np.pi*50*t) * 100
sig_250Hz = np.sin(2*np.pi*250*t) * 100
sig_combined = voffset + sig_5Hz + sig_250Hz + sig_50Hz

# filter specifications
number_of_taps = 101    # number of filter coef
cutoff_lpf = 7          # in hz
cutoff_hpf = 100        # in hz
cutoff_low_bpf = 15     # in hz
cutoff_high_bpf = 90   # in hz
nyquist = 1000          # sampling rate 2KHz, nyquist is 2KHz / 2 = 1KHz

lpf_coef = signal.firwin(number_of_taps, cutoff_lpf, fs =nyquist)
filtered_output = signal.lfilter( lpf_coef, 1.0, sig_combined)

f, plt_arr = plt.subplots(5, figsize=(15, 9), sharex=True)
f.suptitle('FIR Filter Waves')

plt_arr[0].plot(sig_5Hz, label='sig_5Hz')
plt_arr[0].set_title('5Hz Signal')

plt_arr[1].plot(sig_50Hz, label='sig_50Hz')
plt_arr[1].set_title('50Hz Signal')

plt_arr[2].plot(sig_250Hz, label='sig_250Hz')
plt_arr[2].set_title('250Hz Signal')

plt_arr[3].plot(sig_combined, label='sig_combined')
plt_arr[3].set_title('Combined 5Hz, 50Hz and 250Hz')

plt_arr[4].plot(filtered_output, label='filtered_output')
plt_arr[4].set_title('Filtered Output')

plt.show()