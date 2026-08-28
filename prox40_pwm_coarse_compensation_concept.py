import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
fs = 50e6
t_end = 50e-6  # 50µs window
f_pwm = 412e3
duty = 0.5
v_high = 3.3
v_low = 0.0

# Phase in degrees (40° steps = 10 windows total)
phase_degrees = np.arange(0, 361, 40)


def generate_pwm(t, freq, duty, phase_deg=0.0):
    period = 1.0 / freq
    phase = phase_deg / 360.0
    t_shifted = (t + phase * period) % period
    return np.where(t_shifted < duty * period, v_high, v_low)


# -----------------------------
# Time vector
# -----------------------------
t = np.arange(0, t_end, 1 / fs)
t_plot = t * 1e6  # Convert to µs

# -----------------------------
# Multi-Window Generation
# -----------------------------
pwm1 = generate_pwm(t, f_pwm, duty, phase_deg=0)

for deg in phase_degrees:
    # Create a new, separate window for each phase
    fig, axs = plt.subplots(4, 1, figsize=(8, 8), sharex=False)
    fig.canvas.manager.set_window_title(f"Phase Test: {deg} Degrees")

    pwm2 = generate_pwm(t, f_pwm, duty, phase_deg=deg)

    # Hardware Logic: Node P115 is the average (Resistor Summer)
    v_p115 = (pwm1 + pwm2) / 2.0

    # -----------------------------
    # FFT of P115 (ADDED)
    # -----------------------------
    n = len(v_p115)
    v_fft = np.fft.rfft(v_p115)
    freqs = np.fft.rfftfreq(n, d=1/fs)
    v_mag = np.abs(v_fft) / n

    # Plot 1: PA2 (Reference)
    axs[0].plot(t_plot, pwm1, color='black')
    axs[0].set_title(f"Phase Shift: {deg}°")
    axs[0].set_ylabel("PA2 (PWM1)")
    axs[0].set_ylim(-0.5, 3.8)
    axs[0].grid(True, alpha=0.3)

    # Plot 2: PA3 (Shifted)
    axs[1].plot(t_plot, pwm2, color='tab:green')
    axs[1].set_ylabel("PA3 (PWM2)")
    axs[1].set_ylim(-0.5, 3.8)
    axs[1].grid(True, alpha=0.3)

    # Plot 3: Resulting Node P115
    axs[2].plot(t_plot, v_p115, color='tab:purple', linewidth=2)
    axs[2].set_ylabel("Node P115\n(Average)")
    axs[2].set_xlabel("Time (µs)")
    axs[2].set_ylim(-0.5, 3.8)
    axs[2].grid(True, alpha=0.3)

    # Plot 4: FFT of P115 (ADDED)
    axs[3].plot(freqs / 1e3, v_mag, color='tab:red')
    axs[3].set_ylabel("|FFT(P115)|")
    axs[3].set_xlabel("Frequency (KHz)")
    axs[3].set_xlim(0, fs / 2 / 1e3)
    axs[3].grid(True, alpha=0.3)

    plt.tight_layout()

# Standard call to show all windows at once
print(f"Opening {len(phase_degrees)} windows...")
plt.show()