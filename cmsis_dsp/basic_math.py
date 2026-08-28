import cmsisdsp as dsp
import numpy as np
import cmsisdsp.fixedpoint as f

# Test the cmsis-dsp Basic Math functions, we only test Add, Subtract, Multiply
def test_arm_add_f32():
    SrcA = np.array([66000.12, 55000.46, 64000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([66003.24, 55001.92, 64031.297])
    Dst = dsp.arm_add_f32(SrcA,SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)


def test_arm_add_f64():
    SrcA = np.array([665000.12, 555000.46, 645000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([665003.2423, 555001.92, 645031.3])
    blockSize = len(SrcA)
    Dst = dsp.arm_add_f64(SrcA, SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)

def test_arm_sub_f32():
    SrcA = np.array([66000.12, 55000.46, 64000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([65996.99, 54999.00, 63970.00])
    blockSize = len(SrcA)
    Dst = dsp.arm_sub_f32(SrcA,SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)

def test_arm_sub_f64():
    SrcA = np.array([66000.12, 55000.46, 64000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([65996.99, 54999.00, 63970.00])
    blockSize = len(SrcA)
    Dst = dsp.arm_sub_f64(SrcA,SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)
def test_arm_mult_f32():
    SrcA = np.array([66000.12, 55000.46, 64000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([ 206072.16, 80300.67, 1961619.9])
    Dst = dsp.arm_mult_f32(SrcA,SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)

def test_arm_mult_f64():
    SrcA = np.array([66000.12, 55000.46, 64000.65])
    SrcB = np.array([3.1223, 1.46, 30.65])
    resp = np.array([ 206072.16, 80300.67, 1961619.9])
    Dst = dsp.arm_mult_f32(SrcA,SrcB)
    print('\nSrcA = ', SrcA)
    print('SrcB = ', SrcB)
    print('Dst = ', Dst)
    assert np.allclose(resp, Dst)

def test_arm_add_q31():
    ''' Fixed point arithment using
    values in range of (−1,1) '''
    f1 = np.array([0.12])
    f2 = np.array([0.23])
    f3 = f1 + f2
    print('\nf1 = ', f1)
    print('f2 = ', f2)
    print('f3 = ', f3)

    #  Make sure it is within the range of (−1,1).
    #  Otherwise, you will get the wrong results.
    #  For values, greater than the limit, you have to scale
    #  down the range of input.
    # Convert float values to
    q1 = f.toQ15(f1)
    q2 = f.toQ15(f2)
    q3 = dsp.arm_add_q15(q1, q2)

    q4 = f.toQ15(f3)
    f4 = f.Q15toF32(q4)

    print('q1 = ', q1)
    print('q2 = ', q2)
    print('q3 = ', q3)
    print('q4 = ', q4)
    print('f4 = ', f4)
    assert np.allclose(q3, q4)

def test_arm_add_q31_beyond_range():
    ''' Fixed point arithment using
    values in range of (−1,1) '''
    f1 = np.array([0.12])
    f2 = np.array([0.23])
    f3 = f1 + f2
    print('\nf1 = ', f1)
    print('f2 = ', f2)
    print('f3 = ', f3)

    #  Make sure it is within the range of (−1,1).
    #  Otherwise, you will get the wrong results.
    #  For values, greater than the limit, you have to scale
    #  down the range of input.
    # Convert float values to

    # Scale the number first so its within (−1,1)
    scale = 64

    f1 = np.array([10.12]) / scale
    f2 = np.array([50.23]) / scale
    print('f1 = ', f1)
    print('f2 = ', f2)
    q1 = f.toQ15(f1)
    q2 = f.toQ15(f2)
    q3 = dsp.arm_add_q15(q1, q2)
    f4 = f.Q15toF32(q3)

    print('q3 = ', q3)
    # Scale back to get the right number
    print('f4 = ', f4 * scale)
    assert np.allclose(f4*scale, 60.34960938)


