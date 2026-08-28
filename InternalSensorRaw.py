import matplotlib.pyplot as plt
import numpy as np

# Temperature Coefficient from datasheet Volts/Celcius
TEMP_COEFF = -0.00175   # MSMP0L13xxx

# ADC Configuration during factory trimming
TRIM_VREF = 1.4
TRIM_RESOLUTION = 4096      # 12-bit
TRIM_TEMP = 30              # Factory trimming temperature from datasheet
TRIM_ADC_VALUE = 1857       # Factory trimming value(ADC) from datasheet

# Calculate Temperature Coefficient in Digits/Celcius
TRIM_DIGITS_PER_VOLTAGE = TRIM_VREF / TRIM_RESOLUTION
TRIM_TEMP_COEFF_RAW = TEMP_COEFF / TRIM_DIGITS_PER_VOLTAGE   # Digits change per celcius

# ADC Configuration during runtime
RUNTIME_VREF = 3.3
RUNTIME_RESOLUTION = 4096      # 12-bit
RUNTIME_DIGITS_PER_VOLTAGE = RUNTIME_VREF / RUNTIME_RESOLUTION
RUNTIME_TEMP_COEFF_RAW = TEMP_COEFF / RUNTIME_DIGITS_PER_VOLTAGE   # Digits change per celcius

# Read TEMP_SENSE0.DATA
def readTrimValue():
    return TRIM_ADC_VALUE

# ADC conversion
def getAdcValues(min_val, max_val):
    return np.arange(min_val, max_val)

# Calculate sensor output voltage during trimming
def calculateSensorTrimVoltage():
    """
    ADC has a linear response, so we used ratio and proportion;
    (Vtrim / TRIM_VREF) =  (TrimADC / TRIM_RESOLUTION)
    """
    TrimADC = readTrimValue()
    VTrim = (TRIM_VREF * TrimADC) / TRIM_RESOLUTION
    print("Vtrim = ", VTrim)
    return  VTrim

# Trimming ADC Vref is 1.4V, but runtime Vref is 3.3V
def normalizeTrimPoint(Vtrim):
    """
    ADC has a linear response, so we use ratio and proportion;
    (Vtrim / RUNTIME_VREF) =  (runTimeTrimAdc / TRIM_RESOLUTION)
    """
    runTimeTrimAdc = (Vtrim * TRIM_RESOLUTION) / RUNTIME_VREF
    print("runTimeTrimAdc = ", runTimeTrimAdc)
    return  runTimeTrimAdc

def convertRawToCelcius(rawValue, trimValue, temp_coeff):
    """
    From slope equation:
    x2 = x1 + ((y2-y1)/m)
    where m is TRIM_TEMP_COEFF_RAW = temp_coeff / TRIM_DIGITS_PER_VOLTAGE
    """
    x1 = TRIM_TEMP
    y1 = trimValue
    y2 = rawValue
    return x1 + ((y2 - y1) / temp_coeff)

# If both Trimming and runtime is using Vref = 1.4V, then this is valid
def simulateProcessRaw_Vref14V():
    # Simulate ADC sampling across temperature range
    adc_values = getAdcValues(TRIM_ADC_VALUE - 300, TRIM_ADC_VALUE + 380)

    # Convert ADC readings to temperatures
    temperatures = [convertRawToCelcius(val, TRIM_ADC_VALUE, TRIM_TEMP_COEFF_RAW) for val in adc_values]

    # Plot 1: Original ADC Raw Value vs Temperature
    plt.figure(figsize=(10, 6))
    plt.plot(temperatures, adc_values, color='green', label='Using TRIM_TEMP_COEFF_RAW.', marker='o', markersize=3)
    plt.scatter([TRIM_TEMP], [TRIM_ADC_VALUE], color='red', label='Factory Trim Point (30°C)', zorder=5)
    plt.title('ADC Raw Value vs Temperature (Vref = 1.4V)')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('ADC Raw Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print info
    print("TEMP_COEFF = ", TEMP_COEFF)
    print("TRIM_DIGITS_PER_VOLTAGE = ", TRIM_DIGITS_PER_VOLTAGE)
    print("TRIM_TEMP_COEFF_RAW = ", TRIM_TEMP_COEFF_RAW)

# If Trimming Vref = 1.4V and runtime is Vref = 3.3V, then this is valid
def simulateProcessRaw_Vref33V():
    Vtrim = calculateSensorTrimVoltage()
    runTimeTrimAdc = normalizeTrimPoint(Vtrim)

    # Simulate ADC sampling across temperature range
    adc_values = getAdcValues(runTimeTrimAdc - 300, runTimeTrimAdc + 380)

    # Convert ADC readings to temperatures
    temperatures = [convertRawToCelcius(val, runTimeTrimAdc, RUNTIME_TEMP_COEFF_RAW) for val in adc_values]

    # Plot 1: Original ADC Raw Value vs Temperature
    plt.figure(figsize=(10, 6))
    plt.plot(temperatures, adc_values, color='green', label='Using RUNTIME_TEMP_COEFF_RAW.', marker='o', markersize=3)
    plt.scatter([TRIM_TEMP], [runTimeTrimAdc], color='red', label='Factory Trim Point (30°C)', zorder=5)
    plt.title('ADC Raw Value vs Temperature (Vref = 3.3V)')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('ADC Raw Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print info
    print("TEMP_COEFF = ", TEMP_COEFF)
    print("RUNTIME_DIGITS_PER_VOLTAGE = ", RUNTIME_DIGITS_PER_VOLTAGE)
    print("RUNTIME_TEMP_COEFF_RAW = ", RUNTIME_TEMP_COEFF_RAW)

simulateProcessRaw_Vref33V()

