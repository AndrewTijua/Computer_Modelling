"""
This module implements basic vector operations on 3 element numerical lists in python

Designed for python3
"""

import math

def sq_mag(a):
    """
    This function gives the squared magnitude of a vector
    :param a: A 3D vector in list form
    :return: Squared magnitude of a
    """
    retval = 0
    for i in range(len(a)):
        retval = retval + i**2
    return retval

def mag(a):
    """
    This function gives the magnitude of a vector
    :param a: A 3D vector in list form
    :return: The magnitude of a
    """
    return math.sqrt(sq_mag(a))

def vec_sum(a, b):
    """
    This function sums 2 vectors
    :param a: A 3D vector in list form
    :param b: A 3D vector in list form
    :return: a + b as a 3D vector in list form
    """
    retvec = []
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retvec.append(a[i] + b[i])
    return retvec

def vec_diff(a, b):
    """
    This function takes the difference of 2 vectors
    :param a: A 3D vector in list form
    :param b: A 3D vector in list form
    :return: a - b as a 3D vector in list form
    """
    retvec = []
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retvec.append(a[i] - b[i])
    return retvec

def vec_mult(a, c):
    """
    This function multiplies a vector by a scalar
    :param a: A 3D vector in list form
    :param c: A scalar number
    :return: c * a as a 3D vector in list form
    """
    retvec = []
    for i in range(len(a)):
        retvec.append(a[i] * c)
    return retvec

def vec_cross(a, b):
    """
    This function takes the cross product of 2 vectors
    :param a: A 3D vector in list form
    :param b: A 3D vector in list form
    :return: a x b as a 3D vector in list form
    """
    retvec = [0,0,0]
    retvec[0] = a[1]*b[2] - a[2]*b[1]
    retvec[1] = a[2]*b[0] - a[0]*b[2]
    retvec[2] = a[0]*b[1] - a[1]*b[0]
    return retvec

def vec_dot(a, b):
    """
    This function takes the dot product of 2 vectors
    :param a: A 3D vector in list form
    :param b: A 3D vector in list form
    :return: a . b as a scalar number
    """
    retval = 0
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retval = retval + (a[i] * b[i])
    return retval

