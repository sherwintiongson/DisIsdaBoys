import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Sensor calibration data
dist = np.array([0.2, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8])
adc = np.array([260, 310, 390, 500, 620, 770, 836, 935, 1020, 1070, 1120, 1150, 1180, 1200, 1270, 1300, 1320])

# Parameters for linearization
min_dist, max_dist = 0.2, 8.0
min_adc, max_adc = 260, 1320
dist_range = max_dist - min_dist
adc_range = max_adc - min_adc

# Step 1: Compute linearized values for calibration points (LUT base)
linearized_calib = min_adc + adc_range * (dist - min_dist) / dist_range

# Step 2: Create LUT - Precompute for all integer ADC values from min_adc to max_adc
# LUT shape: array of size (max_adc - min_adc + 1), index = raw_adc - min_adc
lut_size = max_adc - min_adc + 1
adc_lut = np.arange(min_adc, max_adc + 1)  # All possible integer ADCs
dist_lut = np.interp(adc_lut, adc, dist)   # Interp distance from raw ADC
linearized_lut = min_adc + adc_range * (dist_lut - min_dist) / dist_range  # Linearized from dist

# LUT as numpy array: lut[raw_adc - min_adc] = linearized_value
lut = linearized_lut

# Function to get linearized digits from raw ADC using LUT (with bounds check)
def get_linearized_lut(raw_adc):
    if raw_adc < min_adc:
        return min_adc  # Clamp to min
    if raw_adc > max_adc:
        return max_adc  # Clamp to max
    idx = raw_adc - min_adc
    return lut[idx]

# Alternative: If you want a dict-based LUT for sparse lookup (only calibration points)
lut_dict = dict(zip(adc, linearized_calib))
def get_linearized_dict(raw_adc):
    # For non-exact, fall back to interp
    if raw_adc in lut_dict:
        return lut_dict[raw_adc]
    else:
        f_adc_to_linear = interp1d(adc, linearized_calib, kind='linear', bounds_error=False, fill_value='extrapolate')
        return f_adc_to_linear(raw_adc)

# Compute linearized for original data points (using array LUT for demo)
d_actual = dist
raw_adc_actual = adc
linearized_actual = np.array([get_linearized_lut(adc_val) for adc_val in raw_adc_actual])

# Print LUT info
print("LUT Overview:")
print(f"LUT covers ADC {min_adc} to {max_adc} (size: {lut_size})")
print(f"Example LUT entries (first 5 and last 5):")
for i in [0, 1, 2, 3, 4, -5, -4, -3, -2, -1]:
    adc_val = adc_lut[i]
    lin_val = lut[i]
    print(f"ADC {adc_val:4.0f} → Linearized {lin_val:.0f}")

# Verification table (should be exact at calibration points due to interp)
print("\nVerification: Actual vs. LUT Linearized (at calibration points)")
print("Distance (mm) | Raw ADC | Linearized (LUT) | Target Linearized | Error")
print("-" * 65)
for i in range(len(dist)):
    target_lin = linearized_calib[i]
    lut_lin = get_linearized_lut(adc[i])
    print(f"{dist[i]:10.1f}     | {adc[i]:6.0f}   | {lut_lin:14.0f}     | {target_lin:16.0f} | {lut_lin - target_lin:5.0f}")

# Plot: Overlay raw ADC and LUT-linearized digits vs. distance
plt.figure(figsize=(10, 6))
x_plot = np.linspace(min_dist, max_dist, 200)
adc_interp = np.interp(x_plot, dist, adc)  # Raw curve

# LUT-based linearized curve (sample from LUT for smooth plot)
adc_plot = np.linspace(min_adc, max_adc, 200)
dist_plot = np.interp(adc_plot, adc, dist)
linearized_plot = min_adc + adc_range * (dist_plot - min_dist) / dist_range
plt.scatter(dist, adc, label='Raw ADC Data', color='blue', s=50, alpha=0.7)
plt.plot(x_plot, adc_interp, label='Raw ADC Curve', color='blue', linewidth=2)

plt.scatter(dist, linearized_actual, label='LUT Linearized Data', color='green', s=50, alpha=0.7)
plt.plot(x_plot, linearized_plot, label='LUT Linearized (Target Line)', color='green', linewidth=2, linestyle='--')

plt.xlabel('Distance (mm)')
plt.ylabel('Digits')
plt.title('Raw ADC vs. LUT-Linearized Digits (Overlaid)\n(LUT precomputes for fast integer ADC lookups)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Example usage
print("\nExample: Linearize a raw ADC reading using LUT")
raw_example = 1000
lin_ex_lut = get_linearized_lut(raw_example)
print(f"Raw ADC = {raw_example} → Linearized Digits (LUT) = {lin_ex_lut:.0f}")

# Performance note: LUT lookup is O(1) for integer ADCs in range