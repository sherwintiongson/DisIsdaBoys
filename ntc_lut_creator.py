import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Original data
adc_original = [
    4004, 3990, 3974, 3956, 3936, 3913, 3888, 3860, 3830, 3796, 3758, 3718, 3673, 3625,
    3573, 3517, 3457, 3393, 3325, 3253, 3178, 3099, 3017, 2931, 2844, 2753, 2661, 2568,
    2474, 2378, 2283, 2188, 2094, 2001, 1909, 1819, 1731, 1645, 1562, 1481, 1403, 1329,
    1257, 1188, 1123, 1060, 1001, 944, 891, 840, 792, 747, 704, 664, 626, 590, 556, 524,
    494, 466, 440, 415, 392, 370, 350, 330, 312, 295, 279, 264, 250, 237, 224, 213, 202,
    191, 181, 172, 164, 155, 148
]
temp_original = [
    -40.0, -38.0, -36.0, -34.0, -32.0, -30.0, -28.0, -26.0, -24.0, -22.0, -20.0, -18.0,
    -16.0, -14.0, -12.0, -10.0, -8.0, -6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0,
    12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0,
    40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0, 62.0, 64.0, 66.0,
    68.0, 70.0, 72.0, 74.0, 76.0, 78.0, 80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 92.0, 94.0,
    96.0, 98.0, 100.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0, 116.0, 118.0, 120.0
]
adc_original = np.array(adc_original)
temp_original = np.array(temp_original)

# Provided Excel 6th-degree polynomial
def excel_poly6(x):
    return (
        0.00000000000000000051 * x**6 -
        0.00000000000000839074 * x**5 +
        0.00000000005230705293 * x**4 -
        0.00000016102752086779 * x**3 +
        0.000261975960983815 * x**2 -
        0.241247598747928 * x +
        147.551632648802
    )

# Fit a new 6th-degree polynomial
coeffs_poly6 = np.polyfit(adc_original, temp_original, 6)
poly6_new = np.poly1d(coeffs_poly6)

# Generate ADC values starting at 148 with step 128
adc_start = 148
adc_end = 3968  # Largest multiple of 128 ≤ 4004
adc_step = 128
adc_lut = np.arange(adc_start, adc_end + adc_step, adc_step)

# Compute temperatures using the new polynomial (since provided one is incorrect)
temp_lut = poly6_new(adc_lut)

# Create LUT as a DataFrame
lut = pd.DataFrame({'ADC': adc_lut, 'Temperature (°C)': temp_lut})

# Save LUT to CSV
lut.to_csv('adc_temp_lut_corrected.csv', index=False)
print("LUT saved to 'adc_temp_lut_corrected.csv'")
print("\nLookup Table (using new 6th-degree polynomial):")
print(lut)

# Calculate RMSE for both polynomials
temp_excel = excel_poly6(adc_original)
rmse_excel = np.sqrt(np.mean((temp_original - temp_excel)**2))
print(f"\nProvided Excel 6th-degree polynomial RMSE: {rmse_excel:.4f} °C")

temp_new = poly6_new(adc_original)
rmse_new = np.sqrt(np.mean((temp_original - temp_new)**2))
print(f"New 6th-degree polynomial RMSE: {rmse_new:.4f} °C")
print("\nNew 6th-degree polynomial coefficients (highest degree first):")
print(coeffs_poly6)

# Plotting
adc_fit = np.linspace(min(adc_original), max(adc_original), 1000)
temp_new_fit = poly6_new(adc_fit)
temp_excel_fit = excel_poly6(adc_fit)
plt.figure(figsize=(10, 6))
plt.scatter(adc_original, temp_original, color='blue', label='Original Data', s=20)
plt.scatter(adc_lut, temp_lut, color='red', marker='x', label='LUT Points (New Poly)', s=50)
plt.plot(adc_fit, temp_new_fit, color='green', label='New 6th Degree Polynomial')
plt.plot(adc_fit, temp_excel_fit, color='purple', label='Provided Excel Polynomial')
plt.xlabel('ADC Value')
plt.ylabel('Temperature (°C)')
plt.title('ADC to Temperature: LUT and Polynomial Comparison')
plt.legend()
plt.grid(True)
plt.show()