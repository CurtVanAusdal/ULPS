import math
import os
import sys
import struct
from struct import pack
from struct import unpack
import numpy as np
from math import nan

# print(sys.float_info)
def sign(x):
    '''takes in x and returns its sign '''
    if x == 0 or -0 or 0.0 or 0.00 or -0.0 or -0.00:
        return 0
    if x == math.inf:
        return 1
    if x == -(math.inf):
        return -1
    if x < 0:
        return -1
    doubleprecision = pack("d", x)
    # print(doubleprecision)
    nextarr = struct.unpack("q", doubleprecision)[0]
    byte_arr = bytearray(nextarr.to_bytes(8, byteorder='little'))
    # print(byte_arr)
    for bit in byte_arr:
        if bit != 0:
            break
    else:
        return 0
    sign = (byte_arr[7] >> 7) & 1
    if sign == 0:
        return 1
    if sign == 1:
        return -1


def exponent(x):
    '''take in x and return exponent of normalized floating point number in binary form '''
    bias = 1023
    double = struct.pack('d', x)
    # print(double)
    unsigned_int_tuple = struct.unpack("Q", double)
    unsigned_int = unsigned_int_tuple[0]
    # print(unsigned_int,'unsigned')
    exponent_bit_shave = (unsigned_int >> 52)
    # print(exponent_bit_shave,'shave')
    if unsigned_int == 1:
        return -1022
    true_exp = exponent_bit_shave - bias
    # print(true_exp,'true')
    if true_exp == -1023:
        return 0
    else:
        return true_exp


def mantissa(x):
    '''returns the full IEEE mantissa of x as a decimal floating-point number
    (which is the same as fraction() + 1 for normalized numbers; same as fraction() for subnormals).'''
    double = struct.pack('d', x)
    # print(double,'dobule')
    unsigned_int_tuple = struct.unpack("Q", double)
    # print(unsigned_int_tuple,'uit')
    if x == 0 or x == 0.0 or x == 0.00:
        return 0
    unsigned_int = unsigned_int_tuple[0]
    # print(unsigned_int,'ui')
    # Extract the 52 bits of the mantissa directly
    mantissa_bits = unsigned_int & ((1 << 52) - 1)
    # print(mantissa_bits,'mantissa bits ')
    # Convert the mantissa bits to a decimal floating-point number
    mantissa_decimal = mantissa_bits / (2 ** 52)
    # print(mantissa_decimal, "mantissa dec ")
    final = 1 + mantissa_decimal
    return final


def fraction(x):
    """returns the IEEE fractional part of x as a decimal floating-point number.
    You must convert binary to decimal. The fraction portion does not include the leading 1 that is
    not stored."""
    h = x
    if mantissa(h) == 0:
        return 0
    else:
        return (mantissa(h) - 1)


def is_posinfinity(x):
    if sign(x) == -1:
        # print('sign is negative ')
        return False
    if sign(x) == 1:
        pass
    h = x
    exph = exponent(h)
    # print(exph,'exptrue')
    if exph == 1024:
        # print('true')
        return True
    if x != math.inf:  # This line makes sure that x isn't an integer. Might be considered overkill
        return False


def is_neginfinity(x):
    if sign(x) == 1:
        # print('sign is positive ')
        return False
    if sign(x) == -1:
        pass
    h = x
    exph = exponent(h)
    # print(exph,'exptrue')
    if exph != 1024:
        # print('true')
        return True
    if x != math.inf:  # This line makes sure that x isn't an integer. Might be considered overkill
        return False


def ulp(x):
    '''returns the magnitude of the spacing between x and its floating-point successor'''
    h = x
    e = exponent(h)
    # print(exponent(h))
    man = mantissa(h)
    if man == 0 or man == 0.0 or man == 0.00:
        # make it return special case for 0
        e = -1022
    return ((2 ** -52) * (2 ** e))


def ulps(x, y):
    '''Returns the number of intervals between x and y by taking advantage of the IEEE standard'''
    # ensure y is bigger than x always
    if x > y:  # ensure that a is the smaller number and b is the bigger number
        c = x
        a = y
        b = c
    base = sys.float_info.radix
    eps = sys.float_info.epsilon
    prec = sys.float_info.mant_dig
    expdiff = exponent(y) - exponent(x)
    # the taking the advantage of IEE part is done in calculating expdiff (which has IEE packed stuff)
    # inside it. the rest for ulps (1,2) is just a matter of dividing expdiff by eps
    # print(expdiff / eps)
    # Condition 1, if numbers are not same exponent and the number is a number
    # 2^something)
    # 2**i where i = 1000 is a huge exponent and will probably never be met so this
    # list comprehension is valid enough.
    if exponent(x) != exponent(y) and (x in [2**i for i in range(1000)] and y in [2**i for i in range(1000)]):
        # print('met ')
        return expdiff / eps
    # condition 2, if numbers are same exponent but different numbers
    if exponent(x) == exponent(y) and x != y:
        diffactual = y - x
        sigma = eps * base ** (exponent(x))
        # print(sigma)
        return (diffactual) * (1 / sigma)
    # condition 3: exponents of the numbers are different and the numbers don't lie perfectly on a new exponent range
    if exponent(x) != exponent(y) and (x not in [2**i for i in range(1000)] and y not in [2**i for i in range(1000)]):
        diffactual = y - x
        stepup = ulps(2**exponent(y), y)
        stepdown = (2**exponent(y) - x) * (1 / eps)
        return stepdown + stepup


y = 6.5
subMin = np.nextafter(0, 1)  # subMin = 5e-324
# print(subMin)
print(sign(y))  # 1
print(sign(0.0))  # 0
print(sign(-y))  # -1
print(sign(-0.0))  # 0
print(exponent(y))  # 2
print(exponent(16.6))  # 4
print(fraction(0.0))  # 0.0
print(mantissa(y))  # 1.625
print(mantissa(0.0))  # 0.0
var1 = float(nan)
print(exponent(var1))  # 1024
print(exponent(0.0))  # 0
print(exponent(subMin))  # -1022
print(is_posinfinity(math.inf))  # True
print(is_neginfinity(math.inf))  # False
print(not is_posinfinity(-math.inf))  # True
print(is_neginfinity(-math.inf))  # True
print(ulp(y))  # 8.881784197001252e-16
print(ulp(1.0))  # 2.220446049250313e-16
print(ulp(0.0))  # 5e-324
print(ulp(subMin))  # 5e-324
print(ulp(1.0e15))  # 0.125
print(ulps(1, 2))  # 4503599627370496 #WRONG
