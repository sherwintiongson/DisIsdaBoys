from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style

#Siganl sampling rate 20000Hz

t = np.linspace(0,1.0,2001)

sig_5Hz = np.sin(2*np.pi*5*t)
sig_250Hz = np.sin(2*np.pi*250*t)
sig_5Hz_250Hz = sig_5Hz + sig_250Hz

style.use('dark_background')
f,plt_arr = plt.subplots(3, sharex=True)
f.suptitle('Signal Generation')

plt_arr[0].plot(sig_5Hz,color ='yellow')
plt_arr[0].set_title('5Hz signal', color ='yellow')

plt_arr[1].plot(sig_250Hz,color ='yellow')
plt_arr[1].set_title('250Hz signal', color ='yellow')

plt_arr[2].plot(sig_5Hz_250Hz,color ='cyan')
plt_arr[2].set_title('Combined 5Hz and 250Hz signal', color ='cyan')

plt.show()
