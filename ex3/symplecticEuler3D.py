import sys
from matplotlib import pyplot as pyplot
from Particle3D import Particle3D
import math
from numpy.linalg import norm

def morse_force(r1, r2, D_e, r_e, alpha):
    """
    Calculates the force due to the morse potential on particle 1 due to particle 2
    """
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    sep = Particle3D.separation(r1, r2)
    #Split expression for force into smaller parts for easier digestion
    force_part_one = -2 * alpha * D_e * (1 - math.exp(-1 * alpha * (norm(Particle3D.separation(r1, r2)) * r_e)))
    force_part_two = math.exp(-1 * alpha * (norm(Particle3D.separation(r1, r2)) - r_2))
    return force_part_one * force_part_two * Particle3D.separation(r1, r2)

def morse_energy(r1, r2, D_e, r_e, alpha):
    """
    Expression for energy of two particle due to morse potential
    """
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    sep = Particle3D.separation(r1, r2)
    energy = D_e * ((1 - math.exp(-1 * alpha*(norm(Particle3D.separation(r1, r2)) - r_e))) ** 2 - 1)
    return energy

def total_energy(D_e, r_e, alpha, *args):
    """
    Computes the total system of the system
    """
    t_energy = 0
    for i in args:
        t_energy = t_energy + i.kinetic_energy()
    for i in range(len(args)):
        for j in range(i, len(args)):
            t_energy = t_energy + morse_energy(args[i], args[j], D_e, r_e, alpha)
    return t_energy

def get_input_vars(sysargs):
    in_file = str(sysargs[1])
    read_file = open(in_file, 'r')
    in_file_contents = read_file.read().
    file_list = in_file_contents.split('\n')
    non_comments_list = []
    for i in file_list:
        if i.startswith('#') == False:
            non_comments_list.append(i)
    sim_params_list = non_comments[0:3]
