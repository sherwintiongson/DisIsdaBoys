import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft

# sampling rate 340KHz, nyquist is 340KHz / 2 = 170KHz
SamplingRate = 357000             # Must matched the ADC Scan Rate
NyquistRate = 357000 * 2             # Minimum NyquistRate = SamplingRate/2
SampleSize = 540000 + 1             # SampleSize = NyquistRate + 1
t = np.linspace(0, 1, SampleSize)

# generate 5Hz sine wave sine(2*pi*f*t)
#voffset = 0
voffset = 2062

VdemFreq = 2500
VdemScaleFactor = 1700
Vdem = (np.sin(2*np.pi*VdemFreq*t) * VdemScaleFactor) + voffset

Noise1Freq = 12500
Noise1ScaleFactor = 1000
Noise1 = np.sin(2 * np.pi * Noise1Freq * t) * Noise1ScaleFactor

Noise2Freq = 32000
Noise2ScaleFactor = 1000
Noise2 = np.sin(2 * np.pi * Noise2Freq * t) * Noise2ScaleFactor

np.random.seed(0)
Noise3 = np.random.randn(SampleSize) * Noise2ScaleFactor

sig_combined = Vdem + Noise2 + Noise1 + Noise3

# Design a lowpass Butterworth Digital filter
order = 2
cutoff_freq = 3000  # Hz
b, a = signal.butter(order, cutoff_freq, fs=SamplingRate, btype='low', analog=False, output='ba')
print('\n b =',b)
print('\n a =',a)

w, h = signal.freqz(b, a)
plt.figure()
plt.title("Digital filter frequency response")
plt.plot(0.5 * SamplingRate * w / np.pi, np.abs(h), "b")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Gain")
plt.grid(True)
plt.axvline(2500,color='green', label='2.5KHz')
plt.axvline(cutoff_freq,color='red', label='Fc')
plt.axhline(0.7071,color='green')
plt.show()

# Apply the filter to the data
filtered_output = signal.lfilter(b, a, sig_combined)

freq_domain_in = fft(sig_combined)
in_magnitude = np.abs(freq_domain_in)

freq_domain_out = fft(filtered_output)
output_magnitude = np.abs(freq_domain_out)

f, plt_arr = plt.subplots(8, figsize=(15, 9), sharex=True)
f.suptitle('Scipy IIR Low Pass Filter Simulation using float number')
plt_arr[0].plot(Vdem, label='Vdem(Green) vs. Filtered Signal(Red)', color='g')
plt_arr[0].plot(filtered_output, label='Filtered Signal', color='r')
plt_arr[1].plot(Noise1, label='Noise1', color='b')
plt_arr[2].plot(Noise2, label='Noise2', color='b')
plt_arr[3].plot(Noise3, label='Noise2', color='b')
plt_arr[4].plot(sig_combined, label='Vdem with noise', color='m')
plt_arr[5].plot(filtered_output, label='Filtered Signal', color='r')
plt_arr[6].plot(in_magnitude, label='Vdem Input FFT', color='b')
plt_arr[7].plot(output_magnitude, label='Vdem Input FFT', color='b')

f.legend(loc='outside upper right')
plt.autoscale()
plt.legend()
plt.show()
