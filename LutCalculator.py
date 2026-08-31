import numpy
from numpy.polynomial import polynomial
from numpy import mean as numpy_mean, sum as numpy_sum, min as numpy_min, max as numpy_max
import os
import matplotlib.pyplot as plt

# Input log file from temperature measurement
inputFile = r"C:\PythonRoot\Logfile Tempgang - M18TLUT.txt"

# Parameters
sn = 8  # distance [mm]
roomTemp = 25  # 'Set Temp' value
fieldSeparator = '\t'  # TAB (field separator in input file)
polyRegrDeg = 6  # degree of polynomial regression
CSV_SEP = ';'  # separator in .csv file
postfix = "_corr"

# Input File Column Mapping/Index
readTempIdx = 0  # 'Read Temp'
setTempIdx = 1  # 'Set Temp'
sensorIdx = 3  # 'Sensor#'
snIdx = 4  # 'Sn'
voffsIdx = 5  # 'Voffset,mean'
vntcIdx = 7  # 'VNTC,mean'
vdemIdx = 6  # 'Vdem,mean'

# Data Containers - these lists store measurement data grouped by sensor sample.
samples = []
tempValues = []
voffsValues = []
vntcValues = []
vlcValues = []
vlcRTValues = []

# Log file parsing
with open(inputFile) as file:
    # Reads the logfile line by line
    for line in file:

        # Converts commas to decimal points
        line = line.strip().replace(',', '.')

        if line:

            # Process only numeric lines
            if line[0:1].isnumeric() or (line[0:1] in ['-', '+']):

                fields = line.split(fieldSeparator)

                try:
                    tempVal = float(fields[readTempIdx])
                    setTempVal = float(fields[setTempIdx])
                    sampleVal = int(float(fields[sensorIdx]))
                    snVal = float(fields[snIdx])
                    voffsVal = float(fields[voffsIdx])
                    vntcVal = float(fields[vntcIdx])

                    # VLC calculation
                    # VLC = Vdem - Voffset
                    # This calculation works even if temperature compensation is enabled
                    vlcVal = float(fields[vdemIdx]) - voffsVal

                except:
                    snVal = -1

                # Only measurements matching the selected sensor distance are processed
                if snVal == sn:

                    if sampleVal in samples:
                        listIdx = samples.index(sampleVal)

                    else:
                        listIdx = len(samples)

                        samples.append(sampleVal)
                        tempValues.append([])
                        voffsValues.append([])
                        vntcValues.append([])
                        vlcValues.append([])
                        vlcRTValues.append(0)

                    # Store measurement values
                    tempValues[listIdx].append(tempVal)
                    voffsValues[listIdx].append(voffsVal)
                    vntcValues[listIdx].append(vntcVal)
                    vlcValues[listIdx].append(vlcVal)

                    """
                    Room Temperature Reference

                    The VLC value at room temperature is stored as a reference baseline.

                    This reference is later used to:
                    - Normalize measurements
                    - Calculate correction values
                    - Calculate residual compensation error
                    """

                    if setTempVal == roomTemp:
                        vlcRTValues[listIdx] = vlcVal

    print("temp:", tempValues)
    print("voffset:", voffsValues)
    print("vntc:", vntcValues)
    print("vlc", vlcValues)

    sIdx = 0
    measCsvStr = ""

    calcVNTCSamples = []
    calcCorrValueSamples = []
    vlcRTValueSamples = []

    """
    ============================================================================
    CLASS 3 LUT PROCESSING
    ============================================================================

    A dedicated LUT is generated for each individual sample.
    """

    for sampleVal in samples[:4]:

        outputFile = os.path.join(
            os.path.dirname(inputFile),
            "TLUT_BES_{}_CL3_{}mm.csv".format(sampleVal, sn)
        )

        # Plot raw VLC measurement over temperature
        plt.figure()
        plt.plot(tempValues[sIdx], vlcValues[sIdx], marker='o')
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC measured")
        plt.xlabel("Temperature [°C]")
        plt.ylabel("[digits]")

        """
        VLC Difference Calculation

        Difference between room-temperature VLC and measured VLC.

        This represents temperature-induced drift:

            VLC_diff = VLC_room_temp - VLC_measured
        """

        vlcDiffValues = []

        for vlcVal in vlcValues[sIdx][::2]:
            vlcDiffValues.append(vlcRTValues[sIdx] - vlcVal)

        """
        Polynomial Regression

        Regression mapping:

            VNTC -> VLC correction value

        Polynomial coefficients are later used for LUT generation.
        """

        pfResults = polynomial.polyfit(
            vntcValues[sIdx][::2],   # X-axis: VNTC values
            vlcDiffValues,           # Y-axis: correction values
            polyRegrDeg,             # Polynomial degree
            rcond=None,
            full=True
        )

        # Regression coefficients
        pfCoeffs = pfResults[0]

        # Mean value of measured drift
        diffMean = numpy_mean(vlcDiffValues)

        print("sample{} coeffs: {}".format(sampleVal, pfCoeffs))

        """
        LUT Resolution Calculation

        Dynamic step-size calculation to keep LUT size below ~80 entries.
        """

        vntcMin = numpy_min(vntcValues[sIdx])
        vntcMax = numpy_max(vntcValues[sIdx])

        pow = 1

        while ((vntcMax - vntcMin) / (2 ** pow)) > 80:
            pow += 1

        step = (2 ** pow)

        # Number of LUT points
        nop = 1 + round(((vntcMax - vntcMin) / step) + 0.5)

        print(f"Number of points LUT: {nop}")
        print(f"VNTC stepsize LUT: {step}")

        """
        LUT Generation

        Generates:
        - calcVntc  -> LUT X-axis
        - corrValue -> LUT correction values
        """

        corrValue = []
        calcVntc = []

        vntcVal = int(vntcMin)

        for i in range(nop):

            calcVals = polynomial.polyval([vntcVal], pfCoeffs)

            calcVntc.append(vntcVal)
            corrValue.append(round(calcVals[0]))

            vntcVal += step

        # Store LUT values for later Class 1 averaging
        calcVNTCSamples.append(calcVntc)
        calcCorrValueSamples.append(corrValue)

        print(f"Calculated VNTC LUT Class3 Sample{sIdx + 1}", calcVntc)
        print(f"Calculated correction LUT Class3 Sample{sIdx + 1}", corrValue)

        newCorrValue = []

        """
        ============================================================================
        CLASS 3 LUT INTERPOLATION
        ============================================================================
        """

        for i in range(0, len(vntcValues[sIdx])):

            # Find LUT interval index
            index = (vntcValues[sIdx][i] - vntcMin) // step

            # Prevent overflow at last interval
            if index >= len(calcVntc) - 1:
                index = len(calcVntc) - 2

            # LUT interval points
            x0 = calcVntc[int(index)]
            x1 = calcVntc[int(index) + 1]

            y0 = corrValue[int(index)]
            y1 = corrValue[int(index) + 1]

            """
            Linear interpolation

            Interpolates correction value between LUT points.
            """

            num = (y1 - y0) * (vntcValues[sIdx][i] - x0)
            den = (x1 - x0)

            # Integer rounding behavior for embedded compatibility
            if num >= 0:
                y = y0 + (num + den // 2) // den
            else:
                y = y0 + (num - den // 2) // den

            newCorrValue.append(int(y))

        print(f"New Correction Values Class3: {newCorrValue}")
        print(f"Measured VLC diff values: {vlcDiffValues}")

        # Store room-temperature VLC values for Class 1 averaging
        vlcRTValueSamples.append(vlcRTValues[sIdx])

        """
        Apply correction

        Corrected VLC = measured VLC + interpolated correction
        """

        corrVLCvalue = [
            int(x) + int(y)
            for x, y in zip(vlcValues[sIdx], newCorrValue)
        ]

        print(f"Corrected VLC values Class3: {corrVLCvalue}")

        """
        Residual error calculation

        Error relative to room-temperature baseline.
        """

        errorVLC = [x - vlcRTValues[sIdx] for x in corrVLCvalue]

        print(f"Error of VLC Class3: {errorVLC}")

        # Plot compensation error
        plt.figure(figsize=(8, 6))
        plt.plot(vntcValues[sIdx], errorVLC, marker='o')
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC error Class3")
        plt.xlabel("VNTC [digits]")
        plt.ylabel("[digits]")

        # Plot LUT and interpolation behavior
        plt.figure(figsize=(8, 6))

        plt.plot(calcVntc, corrValue, marker='o', label='Corr Value LUT')
        plt.grid(True)

        plt.plot(
            vntcValues[sIdx],
            newCorrValue,
            marker='*',
            label='Corr Value interpolated'
        )

        plt.plot(
            vntcValues[sIdx][::2],
            vlcDiffValues,
            marker='o',
            label='Measured VLC diff values'
        )

        plt.title(f"Sample {sIdx + 1} Correction over VNTC Class3")
        plt.legend()
        plt.xlabel("VNTC value [digits]")
        plt.ylabel("Correction value [digits]")

        sIdx += 1

    """
    ============================================================================
    CLASS 1 LUT EVALUATION
    ============================================================================

    Generates a global LUT by averaging all Class 3 LUTs.
    """

    meanCalcVNTCvalues = [
        round(sum(values) / len(values))
        for values in zip(*calcVNTCSamples)
    ]

    meanCalcCorrValues = [
        round(sum(values) / len(values))
        for values in zip(*calcCorrValueSamples)
    ]

    meanVLCRTvalues = (
            sum([x for x in vlcRTValueSamples])
            // len(vlcRTValueSamples)
    )

    vntcMinClass1 = min(meanCalcVNTCvalues)

    print(f"Calculated VNTC mean value: {meanCalcVNTCvalues}")
    print(f"Calculated correction mean value: {meanCalcCorrValues}")
    print(f"VLC RT mean value: {meanVLCRTvalues}")
    print(f"VNTC min mean value: {vntcMinClass1}")

    plt.figure(figsize=(10, 8))

    for sample in samples[:4]:

        newCorrValueClass1 = []

        for i in range(0, len(vntcValues[sample - 1])):

            # Find LUT interval
            index = (
                    (vntcValues[sample - 1][i] - vntcMinClass1)
                    // step
            )

            # Prevent overflow
            if index >= len(meanCalcVNTCvalues) - 1:
                index = len(meanCalcVNTCvalues) - 2

            # LUT interval points
            x0 = meanCalcVNTCvalues[int(index)]
            x1 = meanCalcVNTCvalues[int(index) + 1]

            y0 = meanCalcCorrValues[int(index)]
            y1 = meanCalcCorrValues[int(index) + 1]

            # Linear interpolation
            num = (y1 - y0) * (vntcValues[sample - 1][i] - x0)
            den = (x1 - x0)

            if num >= 0:
                y = y0 + (num + den // 2) // den
            else:
                y = y0 + (num - den // 2) // den

            newCorrValueClass1.append(int(y))

        print(f"Calculated correction value Class1 Sample {sample}: ",
              newCorrValueClass1)

        # Apply Class 1 correction
        corrVLCClass1 = [
            int(x) + int(y)
            for x, y in zip(vlcValues[sample - 1], newCorrValueClass1)
        ]

        print(f"Corrected VLC values Class 1 Sample {sample}: {corrVLCClass1}")

        # Residual error
        errorVLCClass1 = [
            x - meanVLCRTvalues
            for x in corrVLCClass1
        ]

        print(f"Error of VLC Class 1 Sample {sample}: {errorVLCClass1}")

        # Plot Class 1 error
        plt.title(f"VLC error Class1 all samples")

        plt.plot(
            vntcValues[sample - 1],
            errorVLCClass1,
            marker='o',
            label=f"VLC Error Sample {sample}"
        )

        plt.grid(True)
        plt.legend()

        plt.xlabel("VNTC value [digits]")
        plt.ylabel("VLC value [digits]")

    plt.show()

    # writes input (measurement) data
    # with open(os.path.join(os.path.dirname(inputFile),
    # "measurement_{}mm{}.csv".format(sn, postfix)), 'w') as fl:
    #     fl.write(measCsvStr)