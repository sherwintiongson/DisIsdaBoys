import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import cmsisdsp as dsp

# Very Good Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html

# sampling rate 340KHz, nyquist is 340KHz / 2 = 170KHz
SamplingRate = 357000             # Must matched the ADC Scan Rate
NyquistRate = 357000 * 2             # Minimum NyquistRate = SamplingRate/2
SampleSize = 540000 + 1             # SampleSize = NyquistRate + 1
t = np.linspace(0, 1, SampleSize)

# generate 5Hz sine wave sine(2*pi*f*t)
#voffset = 0
voffset = 2062

VdemFreq = 2500
VdemScaleFactor = 1500
Vdem = (np.sin(2*np.pi*VdemFreq*t) * VdemScaleFactor) + voffset

Noise1Freq = 12500
Noise1ScaleFactor = 900
Noise1 = np.sin(2 * np.pi * Noise1Freq * t) * Noise1ScaleFactor

Noise2Freq = 32000
Noise2ScaleFactor = 800
Noise2 = np.sin(2 * np.pi * Noise2Freq * t) * Noise2ScaleFactor

np.random.seed(0)
Noise3ScaleFactor = 400
Noise3 = np.random.randn(SampleSize) * Noise3ScaleFactor

sig_combined = Vdem + Noise2 + Noise1 + Noise3

# Design a lowpass Butterworth Digital filter
filter_order = 2  # Only filter order = 2, will work. Refer to https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html.
cutoff_freq = 3000  # Hz
b, a = signal.butter(filter_order, cutoff_freq, fs=SamplingRate, btype='low', analog=False, output='ba')
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

# For use in CMSIS, denominator coefs 'a' must be negated and first coef A0 which is always 1 must be removed
# Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html
last_index = len(a)
filter_coeff = np.hstack((b,-a[1:last_index]))
print('\n filter_coeff =',filter_coeff)

# IIR Digital Filter
numStages = 1   # this is not the same with filter order. Higher order filters are realized as a cascade of second order sections. numStages refers to the number of second order stages used
state=np.zeros(numStages*4)
Iirf32 = dsp.arm_biquad_casd_df1_inst_f32()
dsp.arm_biquad_cascade_df1_init_f32(Iirf32, numStages, filter_coeff, state)
filtered_output = dsp.arm_biquad_cascade_df1_f32(Iirf32, sig_combined)

# Plot
freq_domain_in = fft(sig_combined)
in_magnitude = np.abs(freq_domain_in)

freq_domain_out = fft(filtered_output)
output_magnitude = np.abs(freq_domain_out)

f, plt_arr = plt.subplots(8, figsize=(15, 9), sharex=True)
f.suptitle('CMSIS DSP IIR Low Pass Filter Simulation using float number')
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
