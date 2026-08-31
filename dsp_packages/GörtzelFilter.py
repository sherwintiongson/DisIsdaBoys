import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Sampling parameters
fs = 8000
t = np.arange(0, 1.0, 1 / fs)

# -----------------------------
# Input signal
base_frequencies = [300, 1000]  # original
cluster_frequencies = np.arange(350, 451, 10)  # 350, 360, ..., 450 Hz

# Add 20 more frequencies (spread out)
additional_frequencies = np.linspace(200, 1100, 20)

# Combine all frequencies
all_frequencies = base_frequencies + list(cluster_frequencies) + list(additional_frequencies)

# Create the input signal
signal = np.zeros_like(t)

for f in all_frequencies:
    if f == 400:  # target frequency: set phase to 45°
        signal += np.sin(2 * np.pi * f * t + np.pi / 4)
    else:
        signal += np.sin(2 * np.pi * f * t)


# -----------------------------
# Goertzel algorithm returning complex value
def goertzel_complex(samples, sample_rate, target_freq):
    N = len(samples)
    k = int(0.5 + ((N * target_freq) / sample_rate))
    omega = (2 * np.pi * k) / N
    coeff = 2 * np.cos(omega)

    s_prev = 0
    s_prev2 = 0
    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s

    Xk = s_prev - np.exp(-1j * omega) * s_prev2
    return Xk


# -----------------------------
# Compute X-Y vectors for all frequencies in the input
Xk_vectors = [goertzel_complex(signal, fs, f) for f in all_frequencies]

# -----------------------------
# Pick one target frequency for Goertzel output
target_freq = 400
Xk_output = goertzel_complex(signal, fs, target_freq)
amplitude = np.abs(Xk_output) / (len(signal) / 2)
phase = np.angle(Xk_output)
filtered_signal = amplitude * np.sin(2 * np.pi * target_freq * t + phase)


# -----------------------------
# Compute FFT
def compute_fft(x, fs):
    N = len(x)
    X = np.fft.fft(x)
    X_mag = np.abs(X) / N
    f = np.fft.fftfreq(N, 1 / fs)
    return f[:N // 2], X_mag[:N // 2]


f_in, X_in = compute_fft(signal, fs)
f_out, X_out = compute_fft(filtered_signal, fs)

# -----------------------------
# Plotting
plt.figure(figsize=(14, 16))

# 1. Input signal (time domain)
plt.subplot(6, 1, 1)
plt.plot(t, signal)
plt.title("Input Signal (Time Domain) - 400Hz phase shifted to 45°")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# 2. Goertzel output (time domain)
plt.subplot(6, 1, 2)
plt.plot(t, filtered_signal, color='orange')
plt.title(f"Goertzel Output at {target_freq} Hz (Time Domain)")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# 3. Input signal spectrum
plt.subplot(6, 1, 3)
plt.stem(f_in, X_in, basefmt=" ", markerfmt='C0o')
plt.title("Input Signal Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.xlim(0, 1200)

# 4. Goertzel output spectrum
plt.subplot(6, 1, 4)
plt.stem(f_out, X_out, linefmt='C1-', markerfmt='C1o', basefmt=" ")
plt.title(f"Goertzel Output Spectrum at {target_freq} Hz")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.xlim(0, 1200)

# 5. Input vectors (X-Y plane)
plt.subplot(6, 1, 5)
for Xk in Xk_vectors:
    plt.quiver(0, 0, Xk.real, Xk.imag, angles='xy', scale_units='xy', scale=1,
               color='blue', alpha=0.7, width=0.003)
plt.xlim(-1.5 * max(abs(x) for x in Xk_vectors), 1.5 * max(abs(x) for x in Xk_vectors))
plt.ylim(-1.5 * max(abs(x) for x in Xk_vectors), 1.5 * max(abs(x) for x in Xk_vectors))
plt.grid(True)
plt.xlabel("Real")
plt.ylabel("Imag")
plt.title("Input Signal Vectors (All Frequencies)")

# 6. Output X-Y vector (target frequency)
plt.subplot(6, 1, 6)
plt.quiver(0, 0, Xk_output.real, Xk_output.imag, angles='xy', scale_units='xy', scale=1,
           color='red', width=0.003)
plt.xlim(-1.5 * abs(Xk_output), 1.5 * abs(Xk_output))
plt.ylim(-1.5 * abs(Xk_output), 1.5 * abs(Xk_output))
plt.grid(True)
plt.xlabel("Real")
plt.ylabel("Imag")
plt.title(f"Goertzel Output Vector at {target_freq} Hz (X-Y Plane)")

plt.tight_layout()
plt.show()
