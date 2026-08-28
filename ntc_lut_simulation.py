import numpy as np
import matplotlib.pyplot as plt

# Design Decision:
# - LUT will be stored in FW in HAL config file (header), not in Storage Manager
# - For RAW return type, it will do filter and then return the adc value
# - For Celsius return type, it will do filter and then do linear interpolation using the Symmetric LUT and then return celsius
# - no opamp needed
# - Self-heating is ignored(current along the voltage divider is so small to self-heat)
# - Beta Value is used to calculate the resistance-temperature (R-T) relationship
# - Voltage divider is used instead of Wheatstone bridge


# Configuration
LUT_TEMP_INTERVAL = 8  # °C steps for LUT, reducing memory to ~44 bytes (11 points)

# NTC Parameters
R_25 = 47000  # 47 kOhm at 25°C - Reference resistance of NTC thermistor at 25°C
BETA = 4050   # Beta value - NTC parameter for resistance-temperature relationship
R_S = 47000   # 47 kOhm series resistor - Matches NTC at 25°C for balanced voltage divider output
V_S = 3.3     # Supply voltage - Standard for MCU, ensures compatibility with 12-bit ADC
ADC_BITS = 12 # 12-bit ADC resolution - Provides 4096 levels for good precision
ADC_MAX = 2**ADC_BITS - 1  # 4095 for 12-bit ADC - Maximum ADC count for calculations

# Function to create LUT
# Generates ADC counts and temperatures (tenths of °C) for given temperature range
def create_lut(start_temp, end_temp, temp_interval, r_25, beta, r_s, v_s, adc_max):
    # Temperature range for LUT (e.g., -40°C to 120°C, step 16°C)
    temp_c = np.arange(start_temp, end_temp + 1, temp_interval)  # Coarse steps save memory
    temp_k = temp_c + 273.15  # Convert to Kelvin for beta formula
    # Calculate NTC resistance using beta formula: R_NTC = R_25 * exp(β * (1/T - 1/298.15))
    R_NTC = r_25 * np.exp(beta * (1/temp_k - 1/298.15))
    # Calculate voltage divider output: V_OUT = V_S * R_NTC / (R_S + R_NTC)
    #V_OUT = v_s - (v_s * R_NTC / (r_s + R_NTC))
    V_OUT = v_s * R_NTC / (r_s + R_NTC)
    # Calculate ADC counts (12-bit): floor((V_OUT / V_S) * 4095)
    ADC_counts = np.floor((V_OUT / v_s) * adc_max).astype(int)
    # Create LUT: [ADC counts, Temperature in tenths of °C]
    # Stores ADC counts and temperatures (e.g., 250 for 25.0°C) for fixed-point arithmetic
    LUT = np.column_stack((ADC_counts, (temp_c * 10).astype(int)))
    return LUT, temp_c, R_NTC, V_OUT, ADC_counts

# Generate LUT and related data
LUT, temp_c, R_NTC, V_OUT, ADC_counts = create_lut(-40, 120, LUT_TEMP_INTERVAL, R_25, BETA, R_S, V_S, ADC_MAX)

# Simulate ADC readings (clean, no noise)
# Fine grid (0.1°C steps) simulates continuous temperature data for testing accuracy
test_temps = np.arange(-40, 125.1, 0.1)  # Fine grid for testing
test_R_NTC = R_25 * np.exp(BETA * (1/(test_temps + 273.15) - 1/298.15))  # NTC resistance for test points
test_V_OUT = V_S * test_R_NTC / (R_S + test_R_NTC)  # Voltage for test points
test_ADC = np.floor((test_V_OUT / V_S) * ADC_MAX).astype(int)  # Clean ADC counts

# Function to interpolate temperature from ADC using LUT
# Mimics MCU fixed-point arithmetic for efficient temperature calculation
def interpolate_temperature(adc, lut):
    # Handle out-of-range ADC values
    if adc > lut[0][0]:  # ADC above max (e.g., >3988), return lowest temperature (-40°C)
        return lut[0][1] / 10.0
    if adc < lut[-1][0]:  # ADC below min (e.g., <127), return highest temperature (120°C)
        return lut[-1][1] / 10.0
    for i in range(len(lut) - 1):
        # Check if ADC value falls between LUT points (note: ADC decreases with temperature)
        if adc >= lut[i+1][0] and adc <= lut[i][0]:
            adc_high, temp_high = lut[i]  # Higher ADC count, lower temperature
            adc_low, temp_low = lut[i+1]  # Lower ADC count, higher temperature
            # Linear interpolation: temp = temp_low + (temp_high - temp_low) * (adc - adc_low) / (adc_high - adc_low)
            # Integer division (//) ensures fixed-point math, compatible with MCU without FPU
            temp = temp_low + ((temp_high - temp_low) * (adc - adc_low)) // (adc_high - adc_low)
            return temp / 10.0  # Convert tenths of °C to °C for plotting
    return lut[-1][1] / 10.0  # Fallback: return highest temperature if no match

# Interpolate temperatures for clean ADC readings
# Apply LUT interpolation to simulate MCU temperature calculation
sim_temps = np.array([interpolate_temperature(adc, LUT) for adc in test_ADC])

# Error analysis
# Calculate absolute error: |interpolated temperature - actual temperature|
errors = np.abs(sim_temps - test_temps)

# Compute statistics: mean, max, and standard deviation of absolute errors
mean_error = np.mean(errors)
max_error = np.max(errors)
std_error = np.std(errors)

# Print error statistics
print("Error Analysis (LUT with 16°C steps):")
print(f"Mean Absolute Error: {mean_error:.3f} °C")
print(f"Maximum Absolute Error: {max_error:.3f} °C")
print(f"Standard Deviation of Error: {std_error:.3f} °C")

# Print lookup table for reference
# Useful for copying into C++ header file for firmware
print("\nLookup Table (ADC Counts, Temperature in tenths of °C):")
for adc, temp in LUT:
    print(f"ADC: {adc}, Temp: {temp/10:.1f}°C")

# Plotting for analysis and understanding
plt.figure(figsize=(15, 12))  # Large figure for six plots

# Plot 1: Resistance vs. Temperature
# Shows NTC’s exponential resistance curve, critical for understanding sensitivity
plt.subplot(3, 2, 1)
plt.plot(temp_c, R_NTC / 1000, 'b-', label='NTC Resistance')  # Continuous curve
plt.scatter(temp_c, R_NTC / 1000, color='red', s=50, label='LUT Points', zorder=5)  # Mark LUT points
plt.xlabel('Temperature (°C)')
plt.ylabel('Resistance (kΩ)')
plt.title('NTC Resistance vs. Temperature')
plt.grid(True)
plt.legend()

# Plot 2: Voltage vs. Temperature
# Shows voltage divider output, key for ADC input range
plt.subplot(3, 2, 2)
plt.plot(temp_c, V_OUT, 'r-', label='V_OUT')  # Continuous voltage curve
plt.scatter(temp_c, V_OUT, color='red', s=50, label='LUT Points', zorder=5)  # Mark LUT points
plt.xlabel('Temperature (°C)')
plt.ylabel('Voltage (V)')
plt.title('Output Voltage vs. Temperature')
plt.grid(True)
plt.legend()

# Plot 3: ADC Counts vs. Temperature
# Shows ADC output, critical for assessing resolution
plt.subplot(3, 2, 3)
plt.plot(temp_c, ADC_counts, 'g-', label='ADC Counts')  # Continuous ADC curve
plt.scatter(temp_c, ADC_counts, color='red', s=50, label='LUT Points', zorder=5)  # Mark LUT points
plt.xlabel('Temperature (°C)')
plt.ylabel('ADC Counts (12-bit)')
plt.title('ADC Counts vs. Temperature')
plt.grid(True)
plt.legend()

# Plot 4: Interpolated vs. Actual Temperature
# Validates LUT accuracy for clean ADC readings
plt.subplot(3, 2, 4)
plt.plot(test_temps, test_temps, 'k--', label='Actual Temperature', alpha=0.5)  # Ideal line
plt.plot(test_temps, sim_temps, 'b-', label='Interpolated (Clean ADC)')  # Interpolated results
plt.scatter(temp_c, temp_c, color='red', s=50, label='LUT Points', zorder=5)  # Mark LUT points
plt.xlabel('Actual Temperature (°C)')
plt.ylabel('Calculated Temperature (°C)')
plt.title('Interpolated vs. Actual Temperature')
plt.grid(True)
plt.legend()

# Plot 5: LUT Plot
# Shows temperature as a function of ADC counts, visualizing LUT relationship
plt.subplot(3, 2, 5)
plt.plot(ADC_counts, temp_c, 'c-', label='Temperature')  # Continuous curve
plt.scatter(ADC_counts, temp_c, color='red', s=50, label='LUT Points', zorder=5)  # Mark LUT points
plt.xlabel('ADC Counts (12-bit)')
plt.ylabel('Temperature (°C)')
plt.title('LUT Plot - each point is stored in HAL_Cfg.hpp')
plt.grid(True)
plt.legend()

# Plot 6: Interpolation Error vs. Actual Temperature
# Shows absolute error to assess LUT accuracy
plt.subplot(3, 2, 6)
plt.plot(test_temps, errors, 'm-', label='Absolute Error')  # Error curve
plt.scatter(temp_c, np.zeros_like(temp_c), color='red', s=50, label='LUT Points', zorder=5)  # Zero error at LUT points
plt.xlabel('Temperature (°C)')
plt.ylabel('Absolute Error (°C)')
plt.title('Interpolation Error vs. Actual Temperature')
plt.grid(True)
plt.legend()

plt.tight_layout()  # Ensures clean plot layout
plt.show()