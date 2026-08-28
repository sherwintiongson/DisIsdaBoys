import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
ADC_MAX = 4095
ADC_MID = ADC_MAX // 2          # 2047
N = 64
GOERTZEL_LENGTH = 128

# -----------------------------
# Time base
# -----------------------------
t = np.arange(N)

# -----------------------------
# Generate a VALID ADC signal
# centered at mid-scale (standard DSP practice)
# -----------------------------
amplitude = 60   # matches your observed ±60 behavior
freq_bin = 4     # 16-sample period (N/16)

adc_analog = ADC_MID + amplitude * np.sin(2 * np.pi * t / 16)

# Quantize to ADC (no clipping distortion now)
adc_signal = np.clip(adc_analog, 0, ADC_MAX).astype(int)

# -----------------------------
# Extract segment (your original window)
# -----------------------------
segment = adc_signal[32:48]

# -----------------------------
# Proper DC removal
# (THIS is what you actually want)
# -----------------------------
dc = np.mean(segment)
ac = segment - dc

# -----------------------------
# Repeat for Goertzel input
# -----------------------------
repeated = np.tile(ac, GOERTZEL_LENGTH // len(ac))

# -----------------------------
# Diagnostics (critical)
# -----------------------------
print("Segment min:", np.min(segment))
print("Segment max:", np.max(segment))
print("Segment DC:", dc)
print("AC p2p:", np.max(ac) - np.min(ac))

# -----------------------------
# Plotting
# -----------------------------
plt.figure()
plt.title("ADC Signal (Correct Mid-Scale Model)")
plt.plot(adc_signal)
plt.xlabel("Sample")
plt.ylabel("ADC Counts")

plt.figure()
plt.title("Extracted Segment")
plt.plot(segment)
plt.xlabel("Sample")
plt.ylabel("ADC Counts")

plt.figure()
plt.title("DC-Removed Signal (AC Component)")
plt.plot(ac)
plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.figure()
plt.title("Repeated Signal (Goertzel Input)")
plt.plot(repeated)
plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.show()