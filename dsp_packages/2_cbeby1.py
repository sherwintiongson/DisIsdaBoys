from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style

import numpy as np

# Design a filter
filter_order = 4
maximum_ripple = 1
critical_frequency = 2800       # In Hz, by default IIR filters assume passband
filter_type = 'lowpass'                     # ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’
minimum_attenuation = 100
b,a = signal.cheby1(filter_order, maximum_ripple, critical_frequency,filter_type,analog=True)

print('\n b =',b)
print('\n a =',a)


#Get frequency response
w,h = signal.freqs(b,a)

#plot
plt.plot(w,20*np.log10(abs(h)))
plt.xscale('linear')
plt.title("Chebyshev Type I frequency response (rp=5)")
plt.xlabel("Frequency (rad/second)")
plt.ylabel("Amplitude (dB)")
plt.margins(0,0.1)
plt.grid(which='both', axis='both')
plt.axvline(2500,color='green')
plt.axhline(-30,color='green')
plt.show()
