import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ADC parameters
# -----------------------------
n_bits = 12  # ADC resolution
max_code = 2 ** n_bits - 1  # Maximum ADC value

# Input voltages to evaluate
Vin_selected = np.array([0.1, 0.2, 0.5, 1.0])

# Reference voltages to compare
Vrefs = [1.4, 3.3]
colors = ['blue', 'green']

# -----------------------------
# Calculate ADC readings and print
# -----------------------------
print("ADC readings for selected input voltages:\n")
for Vref in Vrefs:
    print(f"Vref = {Vref} V")
    ADC_codes = np.round((Vin_selected / Vref) * max_code)
    for vin, code in zip(Vin_selected, ADC_codes):
        if vin <= Vref:  # only show voltages within Vref
            print(f"  Vin = {vin} V -> ADC code = {int(code)}")
    print()

# -----------------------------
# Plot ADC staircases
# -----------------------------
plt.figure(figsize=(8, 5))

for Vref, color in zip(Vrefs, colors):
    # Full staircase
    Vin_full = np.linspace(0, Vref, max_code + 1)
    ADC_full = np.floor((Vin_full / Vref) * max_code)
    plt.step(Vin_full, ADC_full, where='post', label=f'ADC Staircase Vref={Vref}V', color=color)

    # Highlight selected input voltages
    ADC_selected = np.round((Vin_selected / Vref) * max_code)
    valid = Vin_selected <= Vref
    plt.scatter(Vin_selected[valid], ADC_selected[valid], color=color, zorder=5)
    for v, code in zip(Vin_selected[valid], ADC_selected[valid]):
        plt.text(v, code + 20, str(int(code)), ha='center', color=color)

plt.title('12-bit ADC Staircase for Vref = 1.4V and 3.3V')
plt.xlabel('Input Voltage (V)')
plt.ylabel('ADC Code')
plt.grid(True)
plt.legend()
plt.show()
