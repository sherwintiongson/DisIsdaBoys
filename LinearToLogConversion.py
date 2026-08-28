import numpy as np
import math
import matplotlib.pyplot as plt

# 12-bit ADC limits
ADC_MIN = 0
ADC_MAX = 4095

# Log mapping function (maps ADC → 1..1000 range)
def adc_to_log(x, log_min=1, log_max=1000):
    # Normalize ADC to 0–1
    t = (x - ADC_MIN) / (ADC_MAX - ADC_MIN)

    # Log-domain endpoints
    log_min_exp = math.log10(log_min)
    log_max_exp = math.log10(log_max)

    # Interpolate in log domain
    return 10 ** (log_min_exp + t * (log_max_exp - log_min_exp))

# Generate ADC values
x_vals = np.linspace(ADC_MIN, ADC_MAX, 500)
y_vals = [adc_to_log(x) for x in x_vals]

# Plot
plt.figure()
plt.plot(x_vals, y_vals)
plt.xlabel("ADC Value (0–4095)")
plt.ylabel("Log-Scaled Output")
plt.title("12-bit ADC → Logarithmic Scaling")
plt.grid(True)

plt.show()
2