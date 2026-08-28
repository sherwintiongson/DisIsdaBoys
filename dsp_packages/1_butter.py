from scipy import signal
from matplotlib import pyplot as plt
import numpy as np

# Design a filter
filter_order = 4
critical_frequency = 3600       # In Hz, by default IIR filters assume passband
filter_type = 'lowpass'             # 'lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’
analog_filter = True                # True, for analog filter, otherwise a digital filter is returned.
b,a= signal.butter(filter_order, critical_frequency ,filter_type, analog=analog_filter)
print('\n b =',b)
print('\n a =',a)

# Plot filter's frequency response
w,h = signal.freqs(b,a)
plt.plot(w,20*np.log10(abs(h)))
plt.xscale('linear')
plt.title('Butterworth filter frequencry response')
plt.xlabel('Frequency (rads/second)')
plt.ylabel('Amplitude (db)')
plt.margins(0,0.2)
plt.grid(True)
plt.axvline(2500,color='green', label='2.5KHz')
plt.axvline(critical_frequency,color='red', label='Fc')
plt.axhline(-30,color='green')
plt.show()