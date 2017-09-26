import vector
from random import random as random

vec_1 = [random(),random(),random()]
vec_2 = [random(),random(),random()]
vec_3 = [random(),random(),random()]

print("v_1 = {0}, |v_1| = {1}".format(vec_1, vector.mag(vec_1)))
print("v_2 = {0}, |v_2| = {1}".format(vec_2, vector.mag(vec_2)))
print("v_3 = {0}, |v_3| = {1}".format(vec_3, vector.mag(vec_3)))

print("\nv_1 + v_2 = {0}".format(vector.vec_sum(vec_1, vec_2)))

print("\nv_1 . v_2 = {0}".format(vector.vec_dot(vec_1, vec_2)))

print("\nv_1 x v_2 = {0}".format(vector.vec_cross(vec_1, vec_2)))

print("\n\n---Testing Identities---\n\n")
