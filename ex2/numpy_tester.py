import numpy
from random import random
from numpy import linalg as linalg
from numpy import array as array

vec_1 = array([random(), random(), random()])
vec_2 = array([random(), random(), random()])
vec_3 = array([random(), random(), random()])

print("v_1 = {0}, |v_1| = {1}".format(vec_1, linalg.norm(vec_1)))
print("v_2 = {0}, |v_2| = {1}".format(vec_2, linalg.norm(vec_2)))
print("v_3 = {0}, |v_3| = {1}".format(vec_3, linalg.norm(vec_3)))

print("\nv_1 + v_2 = {0}".format(vec_1 + vec_2))

print("\nv_1 . v_2 = {0}".format(numpy.inner(vec_1, vec_2)))

print("\nv_1 x v_2 = {0}".format(numpy.cross(vec_1, vec_2)))

print("\n\n---Testing Identities---\n\n")

print("\nv_1 x v_2 = {0}".format(numpy.cross(vec_1, vec_2)))
print("\n-v_2 x v_1 = {0}".format(-1 * numpy.cross(vec_2, vec_1)))

print("\n\nv_1 x (v_2 + v_3) = {0}".format(numpy.cross(vec_1, vec_2 + vec_3)))
print("\n(v_1 x v_2) + (v_1 x v_3) = {0}".format(numpy.cross(vec_1, vec_2) + numpy.cross(vec_1, vec_3)))

print("\n\nv_1 x (v_2 x v_3) = {0}".format(numpy.cross(vec_1, numpy.cross(vec_2, vec_3))))
print("\n(v_1 . v_3)v_2 - (v_1 . v_2)v_3 = {0}".format((vec_2 * numpy.inner(vec_1, vec_3)) - (vec_3 * numpy.inner(vec_1, vec_2))))
