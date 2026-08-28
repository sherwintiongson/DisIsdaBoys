import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import cmsisdsp as dsp
import cmsisdsp.fixedpoint as cmsis_dsp_fpoint
import sounddevice as sd

# Very Good Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html

# sampling rate 340KHz, nyquist is 340KHz / 2 = 170KHz
SamplingRate = 357000             # Must matched the ADC Scan Rate
NyquistRate = 357000 * 2             # Minimum NyquistRate = SamplingRate/2
SampleSize = 540000 + 1             # SampleSize = NyquistRate + 1
t = np.linspace(0, 1, SampleSize)

# generate 5Hz sine wave sine(2*pi*f*t)
#offset = 0
voffset = 2062

VdemFreq = 2500
VdemScaleFactor = 1500
Vdem = (np.sin(2*np.pi*VdemFreq*t) * VdemScaleFactor) + voffset
Vdem1 = (np.sin(2*np.pi*VdemFreq*t) * VdemScaleFactor)

Noise1Freq = 32000
Noise1ScaleFactor = 700
Noise1 = np.sin(2 * np.pi * Noise1Freq * t) * Noise1ScaleFactor

Noise2Freq = 82000
Noise2ScaleFactor = 500
Noise2 = np.sin(2 * np.pi * Noise2Freq * t) * Noise2ScaleFactor

np.random.seed(0)
Noise3ScaleFactor = 1000
Noise3 = np.random.randn(SampleSize) * Noise3ScaleFactor

sig_combined = Vdem + Noise2 + Noise1 + Noise3

##################################################
# Stage 1 Filter
# Design a lowpass Butterworth Digital filter
filter_order = 2  # Only filter order = 2, will work. Refer to https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html.
cutoff_freq = 9000  # Hz
b1, a1 = signal.butter(filter_order, cutoff_freq, fs=SamplingRate, btype='low', analog=False, output='ba')
print('\n b =',b1)
print('\n a =',a1)

# Plot the FIR's frequency response
plt.figure(1)
plt.clf()
w, h = signal.freqz(b1, a1)
plt.plot(0.5 * SamplingRate * w / np.pi, np.abs(h), "blue")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Gain")
plt.grid(True)
plt.axvline(2500,color='green', label='Vdem = %dHz' % VdemFreq)
plt.axvline(cutoff_freq, color='green', label='Cutoff = %dHz' % cutoff_freq,linestyle =":")
plt.axhline(0.7071, color='red', label ='-3dB Gain', linestyle =":")
plt.xlim(0,30000)
plt.ylim(0.6,1.1)
plt.title('Stage 1 IIR Filter Frequency Response')
plt.legend()
plt.grid(True)

# For use in CMSIS, denominator coefs 'a' must be negated and first coef A0 which is always 1 must be removed
# Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html
last_index = len(a1)
filter_coeff_stage1 = np.hstack((b1,-a1[1:last_index]))
print('\n filter_coeff_stage1 =',filter_coeff_stage1)

##################################################
# Stage 2 Filter
# Design a lowpass Butterworth Digital filter
filter_order = 2  # Only filter order = 2, will work. Refer to https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html.
cutoff_freq = 11000  # Hz
b2, a2 = signal.butter(filter_order, cutoff_freq, fs=SamplingRate, btype='low', analog=False, output='ba')
print('\n b =',b2)
print('\n a =',a2)

# Plot the FIR's frequency response
plt.figure(2)
plt.clf()
w, h = signal.freqz(b2, a2)
plt.plot(0.5 * SamplingRate * w / np.pi, np.abs(h), "blue")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Gain")
plt.grid(True)
plt.axvline(2500,color='green', label='Vdem = %dHz' % VdemFreq)
plt.axvline(cutoff_freq, color='green', label='Cutoff = %dHz' % cutoff_freq,linestyle =":")
plt.axhline(0.7071, color='red', label ='-3dB Gain', linestyle =":")
plt.xlim(0,40000)
plt.ylim(0.6,1.1)
plt.title('Stage 2 IIR Filter Frequency Response')
plt.legend()
plt.grid(True)

# For use in CMSIS, denominator coefs 'a' must be negated and first coef A0 which is always 1 must be removed
# Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html
last_index = len(a2)
filter_coeff_stage2 = np.hstack((b2,-a2[1:last_index]))
print('\n filter_coeff_stage2 =',filter_coeff_stage2)


# Combine filter coefficients {b10, b11, b12, a11, a12, b20, b21, b22, a21, a22, ...}
# where b1x and a1x are the coefficients for the first stage
# where b2x and a2x are the coefficients for the second stage, and so on.
# https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html
filter_coeff = np.hstack(( filter_coeff_stage1, filter_coeff_stage2))
print('\n filter_coeff =',filter_coeff)

#########################################
# Scaling of coefficients
# Filter coefficients are represented as fractional values and
# coefficients are restricted to lie in the range [-1 +1). The fixed-point functions have an additional
# scaling parameter postShift which allow the filter coefficients to exceed the range [+1 -1).
# To avoid saturations in the Q31 implementation we need to scale down the coefficients by postShift
postShift = 1
filter_coeff = filter_coeff / (2**postShift)
print('\n Scaled down filter_coeff =',filter_coeff)

# Convert values to fixed-point
fp_lpf_coef = cmsis_dsp_fpoint.toQ31(filter_coeff)
print('\n Two Stage Q31 IIR filter_coeff =',fp_lpf_coef)

# IIR Digital Filter
numStages = 2   # this is not the same with filter order. Higher order filters are realized as a cascade of second order sections. numStages refers to the number of second order stages used
state=np.zeros(numStages*4)
IirQ31 = dsp.arm_biquad_casd_df1_inst_q31()
dsp.arm_biquad_cascade_df1_init_q31(IirQ31, numStages, fp_lpf_coef, state, postShift)
filtered_output = dsp.arm_biquad_cascade_df1_q31(IirQ31, sig_combined)

# Plot
freq_domain_in = fft(sig_combined)
in_magnitude = np.abs(freq_domain_in)

freq_domain_out = fft(filtered_output)
output_magnitude = np.abs(freq_domain_out)

f, plt_arr = plt.subplots(8, figsize=(15, 9), sharex=True)
f.suptitle('CMSIS DSP IIR Low Pass Filter Simulation using fixed-point number')
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
