import cmsisdsp as dsp
import numpy as np
from scipy import signal
from scipy.fftpack import dct
import cmsisdsp.fixedpoint as f

def test_float_to_Q():
    # create floats
    fn1 = np.array([52.0, -3.12])
    fn2 = np.array([22.3, -14.12])
    fn3 = fn1 + fn2
    print('\nfn3 =',fn3)

    # add floats using fixed-point
    qn1 = f.toQ15(fn1)
    qn2 = f.toQ15(fn2)
    qn3 = dsp.arm_add_q15(qn1, qn2)
    print('qn3 = ', qn3)

    # convert floats to fixed point to compare later
    qn4 = f.toQ15(fn3)
    print('qn4 = ', qn4)

    fn4 = f.Q31toF32(qn3)

    # expect both Q numbers are equal
    assert np.allclose(qn3, qn4)
