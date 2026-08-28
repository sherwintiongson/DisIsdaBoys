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
polyRegrDeg = 6  # degree of polinomial regression
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
            # if it contains values
            if line[0:1].isnumeric() or (line[0:1] in ['-', '+']):
                fields = line.split(fieldSeparator)

                try:
                    tempVal = float(fields[readTempIdx])
                    setTempVal = float(fields[setTempIdx])
                    sampleVal = int(float(fields[sensorIdx]))
                    snVal = float(fields[snIdx])
                    voffsVal = float(fields[voffsIdx])
                    vntcVal = float(fields[vntcIdx])

                    # Vlc is calculated to work even if someone forgets to disable temp comp
                    # VLC = Vdem - Voffset
                    vlcVal = float(fields[vdemIdx]) - voffsVal
                except:
                    snVal = -1

                # Only measurements matching the configured sensor distance are processed.
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

                    tempValues[listIdx].append(tempVal)
                    voffsValues[listIdx].append(voffsVal)
                    vntcValues[listIdx].append(vntcVal)
                    vlcValues[listIdx].append(vlcVal)

                    """ 
                    Room Temperature Reference, saves vlc at room temp
                    The VLC value at room temperature is stored as a reference baseline.
                    This value is later used to:
                        - Normalize measurements
                        - Compute correction values
                        - Calculate residual errors
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
    Class 3 LUT Processing
    """
    for sampleVal in samples[:4]:
        outputFile = os.path.join(os.path.dirname(inputFile), "TLUT_BES_{}_CL3_{}mm.csv".format(sampleVal, sn))

        plt.figure()
        plt.plot(tempValues[sIdx], vlcValues[sIdx], marker='o')
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC measured")
        plt.xlabel("Temperature [°C]")
        plt.ylabel("[digits]")


        """
        VLC Difference Calculation
        The difference between the room-temperature VLC and measured VLC is computed.
        This represents the temperature-induced drift.
        
        
        """
        # creates list from differences (vlc-vlc(room temp))
        # print(f"Reduced temp values: {vlcValues[sIdx][::2]}")
        vlcDiffValues = []
        for vlcVal in vlcValues[sIdx][::2]:
            vlcDiffValues.append(vlcRTValues[sIdx] - vlcVal)

        """
        Polynomial Regression
        The regression maps: VNTC -> VLC correction value
        The resulting polynomial coefficients are later used to generate LUT correction values.
        """
        pfResults = polynomial.polyfit(vntcValues[sIdx][::2],   # VNTC
                                       vlcDiffValues,           # VLC
                                       polyRegrDeg,             # Configuration setting
                                       rcond=None,
                                       full=True)

        # Regression of VLC
        # pfVLC = polynomial.polyfit(tempValues[sIdx], vlcValues[sIdx], 10)
        # temp_new = numpy.linspace(-35, 85, 121)
        # VLC_new = polynomial.polyval(temp_new, pfVLC)
        '''
        plt.plot(temp_new, VLC_new)
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC valued")
        plt.xlabel("Temperature [°C]")
        plt.ylabel("[digits]")
        
        plt.figure()
        plt.plot(vntcValues[sIdx], vlcDiffValues, marker='o')
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC diff to RT over VNTC")
        plt.xlabel("VNTC [digits]")
        plt.ylabel("[digits]")
        '''

        # calculates r^2
        pfCoeffs = pfResults[0]
        # ssRes = pfResults[1][0][0]
        diffMean = numpy_mean(vlcDiffValues)
        # ssTot = numpy_sum((vlcDiffValues - diffMean) ** 2)
        # rSquared = 1 - (ssRes / ssTot)

        print("sample{} coeffs: {}".format(sampleVal, pfCoeffs))
        # print("sample{} r^2: {}".format(sampleVal, rSquared))

        """
        LUT Resolution Calculation:
        Purpose: The algorithm dynamically determines a LUT step size that keeps the number of LUT entries 
        below approximately 80.
        """
        # searching for step which results less than 80 points
        vntcMin = numpy_min(vntcValues[sIdx])
        vntcMax = numpy_max(vntcValues[sIdx])
        pow = 1
        while ((vntcMax - vntcMin) / (2 ** pow)) > 80:
            pow += 1
        step = (2 ** pow)

        # number of points
        nop = 1 + round(((vntcMax - vntcMin) / step) + 0.5)
        print(f"Number of points LUT: {nop}")
        print(f"VNTC stepsize LUT: {step}")

        # Calculate the parameters for the LUT (VNTC & correction value)
        corrValue = []
        calcVntc = []
        vntcVal = int(vntcMin)
        for i in range(nop):
            row = []
            calcVals = polynomial.polyval([vntcVal], pfCoeffs)
            calcVntc.append(vntcVal)
            corrValue.append(round(calcVals[0]))
            vntcVal += step

        # Calculated values (VNTC and correction value) for LUT of each sample
        calcVNTCSamples.append(calcVntc)
        calcCorrValueSamples.append(corrValue)

        print(f"Calculated VNTC LUT Class3 Sample{sIdx + 1}", calcVntc)
        print(f"Calculated correction LUT Class3 Sample{sIdx + 1}", corrValue)

        newCorrValue = []

        # Class 3 LUT evaluation
        for i in range(0, len(vntcValues[sIdx])):
            # print(vntcValues[sIdx][i])
            # Find the left index of desired interval based on the measured VNTC value from a sample
            index = (vntcValues[sIdx][i] - vntcMin) // step
            # Avoid to run over the last interval
            if index >= len(calcVntc) - 1:
                index = len(calcVntc) - 2

            # Get the values (P0(x0, y0); P1(x1, y1)) of the interval from the class 3 LUT
            x0 = calcVntc[int(index)]
            x1 = calcVntc[int(index) + 1]
            y0 = corrValue[int(index)]
            y1 = corrValue[int(index) + 1]

            # Calculate interpolated data between the interval
            num = (y1 - y0) * (vntcValues[sIdx][i] - x0)
            den = (x1 - x0)

            if num >= 0:
                y = y0 + (num + den // 2) // den
            else:
                y = y0 + (num - den // 2) // den

            newCorrValue.append(int(y))

        print(f"New Correction Values Class3: {newCorrValue}")
        print(f"Measured VLC diff values: {vlcDiffValues}")

        # Gather VLC room temperature values from all samples
        vlcRTValueSamples.append(vlcRTValues[sIdx])

        # Calculate the compensated VLC value
        corrVLCvalue = [int(x) + int(y) for x, y in zip(vlcValues[sIdx], newCorrValue)]
        print(f"Corrected VLC values Class3: {corrVLCvalue}")

        # Caclulate the error to the room temperature value
        errorVLC = [x - vlcRTValues[sIdx] for x in corrVLCvalue]
        print(f"Error of VLC Class3: {errorVLC}")

        plt.figure(figsize=(8, 6))
        plt.plot(vntcValues[sIdx], errorVLC, marker='o')
        plt.grid(True)
        plt.title(f"Sample{sIdx + 1} VLC error Class3")
        plt.xlabel("VNTC [digits]")
        plt.ylabel("[digits]")

        plt.figure(figsize=(8, 6))
        plt.plot(calcVntc, corrValue, marker='o', label='Corr Value LUT')
        plt.grid(True)
        plt.plot(vntcValues[sIdx], newCorrValue, marker='*', label='Corr Value interpolated')
        plt.plot(vntcValues[sIdx][::2], vlcDiffValues, marker='o', label='Measured VLC diff values')
        plt.title(f"Sample {sIdx + 1} Correction over VNTC Class3")
        plt.legend()
        plt.xlabel("VNTC value [digits]")
        plt.ylabel("Correction value [digits]")

        sIdx += 1

    # Class 1 LUT evaluation
    # Calculate the mean LUT (calculated VNTC and correction value)
    meanCalcVNTCvalues = [round(sum(values) / len(values)) for values in zip(*calcVNTCSamples)]
    meanCalcCorrValues = [round(sum(values) / len(values)) for values in zip(*calcCorrValueSamples)]
    meanVLCRTvalues = sum([x for x in vlcRTValueSamples]) // len(vlcRTValueSamples)
    vntcMinClass1 = min(meanCalcVNTCvalues)
    print(f"Calculated VNTC mean value: {meanCalcVNTCvalues}")
    print(f"Calculated correction mean value: {meanCalcCorrValues}")
    print(f"VLC RT mean value: {meanVLCRTvalues}")
    print(f"VNTC min mean value: {vntcMinClass1}")

    plt.figure(figsize=(10, 8))

    for sample in samples[:4]:

        newCorrValueClass1 = []

        for i in range(0, len(vntcValues[sample-1])):
            # print(vntcValues[sample][i])

            # Find the left index of desired interval based on the measured VNTC value from a sample in the Class 1 LUT
            index = (vntcValues[sample-1][i] - vntcMinClass1) // step
            # Avoid to run over the last interval
            if index >= len(meanCalcVNTCvalues) - 1:
                index = len(meanCalcVNTCvalues) - 2

            # Get the values (P0(x0, y0); P1(x1, y1)) from the class 1 LUT
            # x --> VNTC value from LUT; y --> correction value from LUT
            x0 = meanCalcVNTCvalues[int(index)]
            x1 = meanCalcVNTCvalues[int(index) + 1]
            y0 = meanCalcCorrValues[int(index)]
            y1 = meanCalcCorrValues[int(index) + 1]

            # Calculate interpolated data between the interval
            num = (y1 - y0) * (vntcValues[sample-1][i] - x0)
            den = (x1 - x0)

            if num >= 0:
                y = y0 + (num + den // 2) // den
            else:
                y = y0 + (num - den // 2) // den

            newCorrValueClass1.append(int(y))

        print(f"Calculated correction value Class1 Sample {sample}: ", newCorrValueClass1)

        corrVLCClass1 = [int(x) + int(y) for x, y in zip(vlcValues[sample - 1], newCorrValueClass1)]
        print(f"Corrected VLC values Class 1 Sample {sample}: {corrVLCClass1}")

        errorVLCClass1 = [x - meanVLCRTvalues for x in corrVLCClass1]
        print(f"Error of VLC Class 1 Sample {sample}: {errorVLCClass1}")

        plt.title(f"VLC error Class1 all samples")
        plt.plot(vntcValues[sample - 1], errorVLCClass1, marker='o', label=f"VLC Error Sample {sample}")
        plt.grid(True)
        plt.legend()
        plt.xlabel("VNTC value [digits]")
        plt.ylabel("VLC value [digits]")

    plt.show()

    # writes input (measurement) data
    # with open(os.path.join(os.path.dirname(inputFile), "measurement_{}mm{}.csv".format(sn, postfix)), 'w') as fl:
    # fl.write(measCsvStr)
