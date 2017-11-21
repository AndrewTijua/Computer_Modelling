import sys
from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np

def morse_force(r1, r2, D_e, r_e, alpha):
    """
    Calculates the force due to the morse potential on particle 1 due to particle 2
    Inputs:
    Particle3D r1: particle 1
    Particle3d r2: particle 2
    float D_e, r_e, alpha: simulation specific parameters
    return numpy array: force
    """
    if r1 == r2:
        return np.array([0,0,0])
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    sep = Particle3D.separation(r1, r2)
    #Split expression for force into smaller parts for easier digestion
    force_part_one = -2 * alpha * D_e * (1 - math.exp(-1 * alpha * (norm(sep) - r_e)))
    force_part_two = math.exp(-1 * alpha * (norm(sep) - r_e))
    return force_part_one * force_part_two * (sep/norm(sep))

def morse_energy(r1, r2, D_e, r_e, alpha):
    """
    Expression for energy potential of two particles due to morse potential
    Inputs:
    Particle3D r1: particle 1
    Particle3d r2: particle 2
    float D_e, r_e, alpha: simulation specific parameters
    return float: energy potential
    """
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    if r1 == r2:
        return 0
    sep = Particle3D.separation(r1, r2)
    energy = D_e * ((1 - math.exp(-1 * alpha*(norm(sep) - r_e))) ** 2 - 1)
    return energy

def total_energy(D_e, r_e, alpha, particle_list):
    """
    Computes the total energy of the system
    Inputs:
    float D_e, r_e, alpha: simulation specific parameters
    return float: energy of system
    """
    t_energy = 0
    for i in particle_list:
        t_energy = t_energy + i.kinetic_energy()
    for i in range(len(particle_list)):
        for j in range(i, len(particle_list)):
            t_energy = t_energy + morse_energy(particle_list[i], particle_list[j], D_e, r_e, alpha)
    return t_energy

def get_input_vars(param_file):
    """
    Reads in an arbitrary number of particles and the simulation parameters from a file
    input: str param_file: file containing appropriately formatted parameters and particles
    return: 3-tuple containing a list of sim params, particle params and the particles themselves
    """
    in_file = str(param_file)
    read_file = open(in_file, 'r')
    in_file_contents = read_file.read()
    file_list = in_file_contents.split('\n')
    non_comments = []
    for i in file_list:
        if i.startswith('#') == False and i != '': #filters out comment lines in file
            non_comments.append(i)
    sim_params_list = non_comments[0:3] #first 3 non comments are sim params (numstep, dt, init_time)
    part_params_list = non_comments[3:6] #second 3 non comments are particle params (D_e, r_e, alpha)
    particles_list = []
    for i in range((len(non_comments) - 3) // 4): #4 because each particle is specified by four lines
        start = 6 + 4*(i) 
        end = 6 + 4*(i+1)
        temp_l = non_comments[start:end]
        p_lab = str(temp_l[0])
        p_mass = float(temp_l[1])
        p_pos = temp_l[2].split(', ')
        for i in range(len(p_pos)):
            p_pos[i] = float(p_pos[i])
        p_pos = np.array(p_pos)
        p_vel = temp_l[3].split(', ')
        for i in range(len(p_vel)):
            p_vel[i] = float(p_vel[i])
        p_vel = np.array(p_vel)
        particle = Particle3D(p_lab, p_mass, p_pos, p_vel)
        particles_list.append(particle)
    read_file.close()
    return (sim_params_list, part_params_list, particles_list)

def energy_error_step(current_energy, init_energy):
    """
    Calculates delta E / E for the current step (delta from initial state)
    Inputs:
    float current_energy: current energy of system
    float init_energy: initial energy of system
    """
    return (current_energy-init_energy)/init_energy
