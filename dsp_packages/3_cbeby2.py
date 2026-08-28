from scipy import signal
from matplotlib import pyplot as plt
from matplotlib import style

import numpy as np

# Design a filter
filter_order = 4
attenuation  = 60
critical_frequency = 100       # In Hz, by default IIR filters assume passband
filter_type = 'lowpass'                     # ‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’
b,a = signal.cheby2(filter_order, attenuation, critical_frequency,filter_type,analog=True)

print('\n b =',b)
print('\n a =',a)

#Get frequency response
w,h = signal.freqs(b,a)

#plot
plt.plot(w,20*np.log10(abs(h)))
plt.xscale('log')
plt.title("Chebyshev Type 2 frequency response (rp=5)")
plt.xlabel("Frequency (rad/second)")
plt.ylabel("Amplitude (dB)")
plt.margins(0,0.1)
plt.grid(which='both', axis='both')
plt.axvline(100,color='green')
plt.axhline(-5,color='green')
plt.show()
