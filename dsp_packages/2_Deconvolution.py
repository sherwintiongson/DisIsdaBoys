from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style


sig = np.array([0,0,0,0,1,1,1,1])
filter = np.array([1,1,0,1])

conv_result = signal.convolve(sig,filter)
deconv_result = signal.deconvolve(conv_result,filter)

print("Convolution result :")
print(conv_result)
print("Deconvolution result : ")
print(deconv_result)

