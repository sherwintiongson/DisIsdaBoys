import mysignals as sigs
import matplotlib.pyplot as plt
import math


def calc_dft(sig_src_arr):
    sig_dest_imx_arr = [None] * int((len(sig_src_arr) / 2))
    sig_dest_rex_arr = [None] * int((len(sig_src_arr) / 2))

    for j in range(int(len(sig_src_arr) / 2)):
        sig_dest_rex_arr[j] = 0
        sig_dest_imx_arr[j] = 0

    for k in range(int(len(sig_src_arr) / 2)):
        for i in range(len(sig_src_arr)):
            sig_dest_rex_arr[k] = sig_dest_rex_arr[k] + sig_src_arr[i] * math.cos(
                2 * math.pi * k * i / len(sig_src_arr))
            sig_dest_imx_arr[k] = sig_dest_imx_arr[k] - sig_src_arr[i] * math.sin(
                2 * math.pi * k * i / len(sig_src_arr))

    style.use('ggplot')
    f, plt_arr = plt.subplots(3, sharex=True)
    f.suptitle("Discrete Fourier Transform (DFT)")

    plt_arr[0].plot(sig_src_arr, color='red')
    plt_arr[0].set_title("Input Signal", color='red')

    plt_arr[1].plot(sig_dest_rex_arr, color='green')
    plt_arr[1].set_title("Frequency Domain(Real part)", color='green')

    plt_arr[2].plot(sig_dest_imx_arr, color='green')
    plt_arr[2].set_title("Frequency Domain(Imaginary part)", color='green')

    plt.show()


calc_dft(sigs.InputSignal_1kHz_15kHz)
