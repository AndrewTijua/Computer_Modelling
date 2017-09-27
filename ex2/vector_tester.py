import vector as v
from random import random as random

vec_1 = [random(),random(),random()]
vec_2 = [random(),random(),random()]
vec_3 = [random(),random(),random()]

print("v_1 = {0}, |v_1| = {1}".format(vec_1, v.mag(vec_1)))
print("v_2 = {0}, |v_2| = {1}".format(vec_2, v.mag(vec_2)))
print("v_3 = {0}, |v_3| = {1}".format(vec_3, v.mag(vec_3)))

print("\nv_1 + v_2 = {0}".format(v.vec_sum(vec_1, vec_2)))

print("\nv_1 . v_2 = {0}".format(v.vec_dot(vec_1, vec_2)))

print("\nv_1 x v_2 = {0}".format(v.vec_cross(vec_1, vec_2)))

print("\n\n---Testing Identities---\n\n")

print("\nv_1 x v_2 = {0}".format(v.vec_cross(vec_1, vec_2)))
print("\n-v_2 x v_1 = {0}".format(v.vec_diff([0,0,0], v.vec_cross(vec_2, vec_1))))

print("\n\nv_1 x (v_2 + v_3) = {0}".format(v.vec_cross(vec_1, v.vec_sum(vec_2, vec_3))))
print("\n(v_1 x v_2) + (v_1 x v_3) = {0}".format(v.vec_sum(v.vec_cross(vec_1, vec_2), v.vec_cross(vec_1, vec_3))))

print("\n\nv_1 x (v_2 x v_3) = {0}".format(v.vec_cross(vec_1, v.vec_cross(vec_2, vec_3))))
print("\n(v_1 . v_3)v_2 - (v_1 . v_2)v_3 = {0}".format(v.vec_diff(v.vec_mult(vec_2, v.vec_dot(vec_1, vec_3)), v.vec_mult(vec_3, v.vec_dot(vec_1, vec_2)))))


