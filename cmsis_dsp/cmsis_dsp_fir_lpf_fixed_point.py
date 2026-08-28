import numpy as np
import cmsisdsp as dsp
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
import cmsisdsp.fixedpoint as cmsis_dsp_fpoint

# sampling rate 340KHz, nyquist is 340KHz / 2 = 170KHz
SamplingRate = 355871                   # From syscfg ADC_TIMER = 2.81uS - must matched the ADC Scan Rate
NyquistRate = SamplingRate * 2          # Minimum NyquistRate = SamplingRate/2
SampleSize = NyquistRate + 1                 # SampleSize = NyquistRate + 1
ripple_db = 60.0                     # The desired attenuation in the stop band, in dB.

# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.  We'll design the filter
# with a 3000 Hz transition width.
width = 500/NyquistRate
N, beta = signal.kaiserord(ripple_db, width)
t = np.linspace(0, 1, SampleSize)

# generate 5Hz sine wave sine(2*pi*f*t)
voffset = 2000
VdemFreq = 2500
VdemScaleFactor = 1400
Vdem = (np.sin(2*np.pi*VdemFreq*t) * VdemScaleFactor) + voffset

Noise1Freq = 64000
Noise1ScaleFactor = 300
Noise1 = np.sin(2 * np.pi * Noise1Freq * t) * Noise1ScaleFactor

Noise2Freq = 90000
Noise2ScaleFactor = 1200
Noise2 = np.sin(2 * np.pi * Noise2Freq * t) * Noise2ScaleFactor

# white noise
np.random.seed(0)
Noise3ScaleFactor = 400
Noise3 = np.random.randn(SampleSize) * Noise3ScaleFactor

# Combine Vdem signal with Noise
sig_combined = Vdem + Noise2 + Noise1 + Noise3

# More exact size in C, for now we make it as big as possible
firState = [0] * SampleSize

# filter specifications
number_of_taps = 16    # number of filter coefficients in the filter. Must be even and greater than or equal to 4.
cutoff_lpf = 12000          # in hz

# Create filter coefficient using Scipy
lpf_coef = signal.firwin(number_of_taps, cutoff_lpf, fs=NyquistRate)
print(lpf_coef)

# Plot filter coefficient
plt.figure(1)
plt.plot(lpf_coef, 'bo-', linewidth=2)
plt.title('Fiter Coefficients (%d taps)' % number_of_taps)

# Plot the FIR's frequency response
plt.figure(2)
plt.clf()
w,h = signal.freqz(lpf_coef, worN=8000)
plt.plot((w/np.pi)*NyquistRate, np.abs(h), linewidth=2)
plt.ylabel('Gain')
plt.xlabel('Frequency (Hz)')
plt.axvline(2500,color='green', label='2.5KHz')
#plt.axvline(cutoff_lpf,color='red', label='Cutoff Freq', linestyle =":")
plt.axhline(0.7071,color='red', linestyle =":", label ='-3dB Bandwidth')
plt.xlim(0,300000)
plt.ylim(0.6,1.1)
plt.title('Filter Frequency Response')
plt.legend()
plt.grid(True)

# Convert decimal values to fixed-point, if needed down-scale to make sure it is within the range of (−1,1).
# FIR coefficient are float numbers, so we convert it to fixed-point
FixedPointScale = np.max(sig_combined)
fp_lpf_coef = cmsis_dsp_fpoint.toQ15(lpf_coef)
print(fp_lpf_coef)

# FIR Digital Filter
# Vdem signal is not converted to fixed-point
# Only filter coefficient is converted to fixed-point
fir_filter = dsp.arm_fir_instance_q15()
dsp.arm_fir_init_q15(fir_filter, number_of_taps, fp_lpf_coef, firState)
filtered_output = dsp.arm_fir_fast_q15(fir_filter, sig_combined)

# FFT to check the frequency reponse
freq_domain_in = fft(sig_combined)
in_magnitude = np.abs(freq_domain_in)
freq_domain_out = fft(filtered_output)
output_magnitude = np.abs(freq_domain_out)

# Time and Frequency domain plot
f, plt_arr = plt.subplots(7, figsize=(15, 9), sharex=True)
f.suptitle('CMSIS DSP FIR Low Pass Filter Simulation using Q15 Fixed Point number')
plt_arr[0].plot(Vdem, label='Vdem(Green) vs. Filtered Signal(Green)', color='b')
plt_arr[0].plot(filtered_output, label='Filtered Signal', color='g')
plt_arr[1].plot(Noise1, label='Noise1', color='b')
plt_arr[2].plot(Noise2, label='Noise2', color='b')
plt_arr[3].plot(sig_combined, label='Vdem with noise', color='b')
plt_arr[4].plot(filtered_output, label='Filtered Signal', color='g')
plt_arr[5].plot(in_magnitude, label='FFT of Vdem Input ', color='b')
plt_arr[6].plot(output_magnitude, label='FFT of Vdem Output', color='g')
f.legend(loc='outside upper right')
plt.autoscale()
plt.legend()
plt.show()