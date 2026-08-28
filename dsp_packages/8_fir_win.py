import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
from matplotlib import style

# sampling rate 2KHz, nyquist is 2KHz / 2 = 1KHz
t = np.linspace(0, 1, 2001)

# generate 5Hz sine wave sine(2*pi*f*t)
sig_5Hz = np.sin(2*np.pi*5*t)
sig_50Hz = np.sin(2*np.pi*50*t)
sig_250Hz = np.sin(2*np.pi*250*t)
sig_combined = sig_5Hz + sig_250Hz + sig_50Hz

# filter specifications
number_of_taps = 101    # number of filter coef
cutoff_lpf = 7          # in hz
cutoff_hpf = 100        # in hz
cutoff_low_bpf = 15     # in hz
cutoff_high_bpf = 90   # in hz
nyquist = 1000          #  sampling rate 2KHz, nyquist is 2KHz / 2 = 1KHz
def plot_5Hz():
    plt.plot(sig_5Hz,label ='sig_5Hz')
    #plt.plot(sig_50Hz,label ='sig_50Hz')
    #plt.plot(sig_250Hz,label ='sig_250Hz')
    #plt.plot(sig_combined,label ='sig_combined')
    plt.xlabel('time')
    plt.title('Simple Chart')
    plt.legend()
    plt.show()
def plot_50Hz():
    plt.plot(sig_50Hz,label ='sig_50Hz')
    plt.xlabel('time')
    plt.title('Simple Chart')
    plt.legend()
    plt.show()
def plot_250Hz():
    plt.plot(sig_250Hz,label ='sig_250Hz')
    plt.xlabel('time')
    plt.title('Simple Chart')
    plt.legend()
    plt.show()
def plot_all():
    plt.plot(sig_5Hz,label ='sig_5Hz')
    plt.plot(sig_50Hz, label='sig_50Hz')
    plt.plot(sig_250Hz, label='sig_250Hz')
    plt.xlabel('time')
    plt.title('Simple Chart')
    plt.legend()
    plt.show()
def plot_sig_combined():
    plt.plot(sig_combined,label ='sig_combined')
    plt.xlabel('time')
    plt.title('Simple Chart')
    plt.legend()
    plt.show()


def LowPass_FIR():
    # we first create the filter coefficients, also called the impulse response
    filter_coef = signal.firwin(number_of_taps, cutoff_lpf, fs =nyquist)
    lpf_output = signal.convolve(sig_combined,filter_coef, mode='same')

    plt.plot(lpf_output,label ='lpf_output')
    plt.xlabel('time')
    plt.title('FIr Filter Output')
    plt.legend()
    plt.show()


def HighPass_FIR():
    # we first create the filter coefficients, also called the impulse response
    filter_coef = signal.firwin(number_of_taps, 100, pass_zero=False,fs =nyquist)
    hpf_output = signal.convolve(sig_combined,filter_coef, mode='same')

    plt.plot(hpf_output,label ='hpf_output')
    plt.xlabel('time')
    plt.title('FIr Filter Output')
    plt.legend()
    plt.show()

def BandPass_FIR():
    # we first create the filter coefficients, also called the impulse response
    filter_coef = signal.firwin(number_of_taps, [cutoff_low_bpf, cutoff_high_bpf], pass_zero=False,fs =nyquist)
    bpf_output = signal.convolve(sig_combined,filter_coef, mode='same')

    plt.plot(bpf_output,label ='bpf_output')
    plt.xlabel('time')
    plt.title('FIr Filter Output')
    plt.legend()
    plt.show()


def app():
    lpf_coef = signal.firwin(number_of_taps, cutoff_lpf, fs =nyquist)
    lpf_output = signal.convolve(sig_combined,lpf_coef, mode='same')

    hpf_coef = signal.firwin(number_of_taps, 100, pass_zero=False,fs =nyquist)
    hpf_output = signal.convolve(sig_combined,hpf_coef, mode='same')

    filter_coef = signal.firwin(number_of_taps, [cutoff_low_bpf, cutoff_high_bpf], pass_zero=False,fs =nyquist)
    bpf_output = signal.convolve(sig_combined,filter_coef, mode='same')


    f,plt_arr = plt.subplots(7, figsize=(15,9),sharex=True)
    f.suptitle('FIR Filter Waves')

    plt_arr[0].plot(sig_5Hz,label ='sig_5Hz')
    plt_arr[0].set_title('5Hz Signal')

    plt_arr[1].plot(sig_50Hz, label='sig_50Hz')
    plt_arr[1].set_title('50Hz Signal')

    plt_arr[2].plot(sig_250Hz, label='sig_250Hz')
    plt_arr[2].set_title('250Hz Signal')

    plt_arr[3].plot(sig_combined, label='sig_combined')
    plt_arr[3].set_title('Combined 5Hz, 50Hz and 250Hz')


    plt_arr[4].plot(lpf_output, label='lpf_output')
    plt_arr[4].set_title('Low pass filter output cutoff Freq = 7Hz')


    plt_arr[5].plot(hpf_output, label='hpf_output')
    plt_arr[5].set_title('High pass filter output cutoff Freq = 100Hz')

    plt_arr[6].plot(bpf_output, label='bpf_output')
    plt_arr[6].set_title('High pass filter output cutoff Freq = 15Hz & 90Hz')

    plt.show()


def FrequencySpectrum():
    freq_domain_signal = fft(sig_combined)
    magnitude = np.abs(freq_domain_signal)

    f, plt_arr = plt.subplots(2, figsize=(15,9), sharex=True)
    f.suptitle("Fast Fourier Transform (FFT)")

    plt_arr[0].plot(freq_domain_signal, color='red')
    plt_arr[0].set_title("Frequency Domain (FFT) with Imaginary Number", color='red')

    plt_arr[1].plot(magnitude, color='blue')
    plt_arr[1].set_title("Frequency Domain (FFT) Absolute Values", color='blue')
    plt.show()


app()
#FrequencySpectrum()