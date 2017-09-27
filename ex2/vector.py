import math

def sq_mag(a):
    retval = 0
    for i in range(len(a)):
        retval = retval + i**2
    return retval

def mag(a):
    return math.sqrt(sq_mag(a))

def vec_sum(a, b):
    retvec = []
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retvec.append(a[i] + b[i])
    return retvec

def vec_diff(a, b):
    retvec = []
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retvec.append(a[i] - b[i])
    return retvec

def vec_mult(a, b):
    retvec = []
    for i in range(len(a)):
        retvec.append(a[i] * b)
    return retvec

def vec_cross(a, b):
    retvec = [0,0,0]
    retvec[0] = a[1]*b[2] - a[2]*b[1]
    retvec[1] = a[2]*b[0] - a[0]*b[2]
    retvec[2] = a[0]*b[1] - a[1]*b[0]
    return retvec

def vec_dot(a, b):
    retval = 0
    if len(a) != len(b):
        raise ValueError("Vectors a and b not of same length!")
    for i in range(len(a)):
        retval = retval + (a[i] * b[i])
    return retval

