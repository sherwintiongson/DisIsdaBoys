from scipy.signal import freqs, iirfilter
from matplotlib import pyplot as plt
import numpy as np

# Design a filter
filter_order = 8
critical_frequencies = [2300,2700]       # In Hz, by default IIR filters assume passband
iir_type = 'cheby2'                     # ‘butter’ ‘cheby1’ ‘cheby2’ ‘ellip’ ‘bessel’
maximum_ripple = 1
minimum_attenuation = 60
b,a = iirfilter(filter_order,critical_frequencies,maximum_ripple,minimum_attenuation, analog =True,ftype=iir_type)

# Plot filter coefficient
plt.title('Fiter Kernel')
plt.plot(b)
plt.show()

# Plot filter's frequency response
w,h= freqs(b,a)
plt.semilogx(w,abs(h))
plt.xlabel('Frequency')
plt.ylabel('Amplitude Response')
plt.grid()
plt.show()
