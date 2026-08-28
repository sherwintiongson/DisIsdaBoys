import numpy as np
import cmsisdsp as dsp
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
import cmsisdsp.fixedpoint as cmsis_dsp_fpoint

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
sig_combined = Vdem + Noise2 + Noise1

# filter specifications
number_of_taps = 64    # number of filter coef
cutoff_lpf = 3200          # in hz
cutoff_hpf = 100        # in hz
cutoff_low_bpf = 15     # in hz
cutoff_high_bpf = 90   # in hz
firStateF32 = [0] * 900000

# Create filter coefficient using Scipy
lpf_coef = signal.firwin(number_of_taps, cutoff_lpf, fs =NyquistRate)
print(lpf_coef)

# FIR Digital Filter
firf32 = dsp.arm_fir_instance_f32()
dsp.arm_fir_init_f32(firf32, number_of_taps, lpf_coef, firStateF32)
filtered_output = dsp.arm_fir_f32(firf32, sig_combined)

freq_domain_in = fft(sig_combined)
in_magnitude = np.abs(freq_domain_in)

freq_domain_out = fft(filtered_output)
output_magnitude = np.abs(freq_domain_out)



f, plt_arr = plt.subplots(7, figsize=(15, 9), sharex=True)
f.suptitle('CMSIS DSP FIR Low Pass Filter Simulation using float number')

plt_arr[0].plot(Vdem, label='Vdem(Green) vs. Filtered Signal(Red)', color='g')
plt_arr[0].plot(filtered_output, label='Filtered Signal', color='r')
plt_arr[1].plot(Noise1, label='Noise1', color='b')
plt_arr[2].plot(Noise2, label='Noise2', color='b')
plt_arr[3].plot(sig_combined, label='Vdem with noise', color='m')
plt_arr[4].plot(filtered_output, label='Filtered Signal', color='r')
plt_arr[5].plot(in_magnitude, label='Vdem Input FFT', color='b')
plt_arr[6].plot(output_magnitude, label='Vdem Input FFT', color='b')

f.legend(loc='outside upper right')
plt.autoscale()
plt.legend()
plt.show()