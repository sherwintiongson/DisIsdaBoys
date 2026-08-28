import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style

def test_ADC_Resolution():
    lsb_mV = ((3.3-0) / pow(2, 12)) * 1000
    print('\n Resolution in mV = ', lsb_mV)

    print(8e-3 * 1e3)
def test_calculate_adc_tau():
    Cpar = np.array([1e-9, 2e-9, 3e-9, 4e-9, 5e-9, 6e-9, 7e-9, 8e-9])
    #Rpar = 0.5e3           # 0.5Kohm   - Cpar and Rpar represent the parasitic capacitance and resistance of the external ADC input circuitry
    Rpar = 1e-9             # 1nF       - Cpar and Rpar represent the parasitic capacitance and resistance of the external ADC input circuitry
    Rin = 0.5e3             # 0.5Kohm   - ADC sampling switch resistance
    Csh = 3.3e-12           # 3.3pF     - ADC sample-and-hold capacitance
    C1 = 5e-12              # 5pF - Pin Input capacitance from datasheet
    tau = ((Rpar + Rin) * Csh) + (Rpar * (Cpar + C1))
    print('\n tau = ', tau)
    plt.plot(tau,label ='tau')
    plt.show()


