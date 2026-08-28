import numpy as np
import matplotlib.pyplot as plt

# ---- CONFIG ----
filename = "COM3D_SET_COARSE.txt"
use_time_axis = True  # set False if you just want sample index

# Known from file header
frequency = 2.567e3          # Hz
period = 389.560e-6          # seconds

# ---- PARSE FILE ----
ch1 = []
ch2 = []

with open(filename, "r") as f:
    for line in f:
        parts = line.strip().split()

        # Skip non-data lines
        if len(parts) != 3:
            continue

        try:
            idx = int(parts[0])
            v1 = float(parts[1])
            v2 = float(parts[2])

            ch1.append(v1)
            ch2.append(v2)
        except ValueError:
            continue  # skip header lines

ch1 = np.array(ch1)
ch2 = np.array(ch2)

# ---- TIME AXIS ----
n = len(ch1)

if use_time_axis:
    # Assume one period spans the dataset (adjust if needed)
    t = np.linspace(0, period, n)
    x = t * 1e6  # convert to µs
    xlabel = "Time (µs)"
else:
    x = np.arange(n)
    xlabel = "Sample index"

# ---- PLOT ----
plt.figure(figsize=(10, 5))

plt.plot(x, ch1, label="CH1 (mV)")
plt.plot(x, ch2, label="CH2 (mV)")

plt.xlabel(xlabel)
plt.ylabel("Voltage (mV)")
plt.title("Voltage Waveforms")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()