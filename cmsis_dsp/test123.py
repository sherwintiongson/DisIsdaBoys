import scipy.signal as signal
import cmsisdsp.fixedpoint as fp
import matplotlib.pyplot as plt
import numpy as np

# Design a lowpass Butterworth Digital filter
SamplingRate = 355871
filter_order = 2  # Only filter order = 2, will work. Refer to https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html.
cutoff_freq = 9000  # Hz
b1, a1 = signal.butter(filter_order, cutoff_freq, fs=SamplingRate, btype='low', analog=False, output='ba')
print('\nb =',b1)
print('a =',a1)

# For use in CMSIS, denominator coefs 'a' must be negated and first coef A0 which is always 1 must be removed
# Reference https://www.keil.com/pack/doc/CMSIS/DSP/html/group__BiquadCascadeDF1.html
last_index = len(a1)
filter_coeff = np.hstack((b1,-a1[1:last_index]))
print('filter_coeff =',filter_coeff)

#########################################
# Scaling of coefficients
# Filter coefficients are represented as fractional values and
# coefficients are restricted to lie in the range [-1 +1). The fixed-point functions have an additional
# scaling parameter postShift which allow the filter coefficients to exceed the range [+1 -1).
# To avoid saturations in the Q31 implementation we need to scale down the coefficients by 4
postShift = 1
filter_coeff = filter_coeff / (2**postShift)
print('Scaled down filter_coeff =',filter_coeff)

# Convert values to fixed-point
fp_lpf_coef = fp.toQ31(filter_coeff)
print('Single Stage Q31 IIR Filter Coeff =',fp_lpf_coef)

# Plot the frequency response
VdemFreq = 2500
plt.figure(2)
plt.clf()
w, h = signal.freqz(b1, a1)
plt.plot(0.5 * SamplingRate * w / np.pi, np.abs(h), "blue")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Gain")
plt.grid(True)
plt.axvline(2500,color='green', label='Vdem = %dHz' % VdemFreq)
plt.axvline(cutoff_freq, color='green', label='Cutoff = %dHz' % cutoff_freq,linestyle =":")
plt.axhline(0.7071, color='red', label ='-3dB Gain', linestyle =":")
plt.xlim(0,10000)
plt.ylim(0.6,1.1)
plt.title('IIR Filter Frequency Response')
plt.legend()
plt.grid(True)
plt.show()