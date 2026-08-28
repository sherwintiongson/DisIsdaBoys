import cmsisdsp as dsp
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import dct
from matplotlib import style

def test_arm_fir_f32_template():
    input_array = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    numTaps = 3
    coef_scipy = [3, 2, 1.]
    coef_cmsis = [1., 2, 3]

    # instantiate cmsis dsp filter
    firf32 = dsp.arm_fir_instance_f32()
    dsp.arm_fir_init_f32(firf32, numTaps, coef_cmsis, [0, 0, 0, 0, 0, 0, 0])

    # test filter using functionality using a known working filter library
    filter_out_scipy = signal.lfilter(coef_scipy, 1.0, input_array)

    # Run CMSIS DSP filter
    filter_out_cmsis = dsp.a

    # Plot
    style.use('ggplot')
    f, plt_arr = plt.subplots(3, sharex=True)
    f.suptitle("CMSIS DSP F32 FIR Filter")
    plt_arr[0].plot(input_array)
    plt_arr[0].set_title("Filter Input ")

    plt_arr[1].plot(filter_out_scipy)
    plt_arr[1].set_title("Scipy Filter Output")

    plt_arr[2].plot(filter_out_cmsis)
    plt_arr[2].set_title("CMSIS DSP Filter Output")

    plt.show()




