import sys
from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np

def grav_force(p1, p2, G):
    """
    Calculates the force due to gravity on particle 1 due to particle 2
    Inputs:
    Particle3D p1: particle 1
    Particle3d p2: particle 2
    float G: simulation specific parameters
    return numpy array: force
    """
    if p1 == p2:
        return np.array([0,0,0])
    G = float(G)
    sep = Particle3D.separation(p1, p2)
    #Split expression for force into smaller parts for easier digestion
    force_part_one = G * p1.mass * p2.mass
    force_part_two = norm(sep) ** 3
    return -1*(force_part_one / force_part_two) * (sep)

def grav_pot(p1, p2, G):
    """
    Expression for energy potential of two particles due to gravity
    Inputs:
    Particle3D p1: particle 1
    Particle3d p2: particle 2
    float G: simulation specific parameters
    return float: energy potentialx
    """
    G = float(G)
    if p1 == p2:
        return 0
    sep = Particle3D.separation(p1, p2)
    energy = -1 * G * p1.mass * p2.mass / norm(sep)
    return energy

def total_energy(G, particle_list):
    """
    Computes the total energy of the system
    Inputs:
    float G: simulation specific parameters
    list particle_list: list containing all particles in system
    return float: energy of system
    """
    t_energy = 0
    for i in particle_list:
        t_energy = t_energy + i.kinetic_energy('au')
    for i in range(len(particle_list)):
        for j in range(i, len(particle_list)):
            t_energy = t_energy + grav_pot(particle_list[i], particle_list[j], G)
    return t_energy

def drift_correct(particle_list):
    """
    Corrects the drift of the system
    """
    system_momentum = np.array([0, 0, 0])
    mass_sum = 0
    for i in particle_list:
        system_momentum = system_momentum + (i.mass * i.velocity)
        mass_sum = mass_sum + i.mass
    CoM_vel = system_momentum / mass_sum
    for i in particle_list:
        i.velocity = i.velocity - CoM_vel
    return None

def get_particles(particle_file):
    """
    Reads in an arbitrary number of particles from a file
    input: str param_file: file containing appropriately formatted particles
    return: list of particles
    """
    in_file = str(particle_file)
    read_file = open(in_file, 'r')
    in_file_contents = read_file.read()
    file_list = in_file_contents.split('\n')
    non_comments = []
    particles_list = []
    wrt_arr = []
    tol_arr = []
    for i in file_list:
        if i.startswith('#') == False and i != '': #filters out comment lines in file
            non_comments.append(i)
    for i in range((len(non_comments)) // 5): #5 because each particle is specified by 5 lines
        start = 5*(i) 
        end = 5*(i+1)
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
        wrt_arr.append(int(temp_l[4]))
    read_file.close()
    return (particles_list, wrt_arr)


def get_params(param_file):
    """
    Reads in simulation parameters
    input: str param_file: file containing formatted parameters
    return: 4-tuple containing the parameters
    """
    in_file = str(param_file)
    read_file = open(in_file, 'r')
    in_file_contents = read_file.read()
    file_list = in_file_contents.split('\n')
    non_comments = []
    for i in file_list:
        if i.startswith('#') == False and i != '': #filters out comment lines in file
            non_comments.append(i)
    G = float(non_comments[0])
    dt = float(non_comments[1])
    numsteps = int(non_comments[2])
    init_time = float(non_comments[3])
    every_n = int(non_comments[4])
    return (G, dt, numsteps, init_time, every_n)

def energy_error_step(current_energy, init_energy):
    """
    Calculates delta E / E for the current step (delta from initial state)
    Inputs:
    float current_energy: current energy of system
    float init_energy: initial energy of system
    """
    return (current_energy-init_energy)/init_energy

def step_time(particle_list, G, dt, out_file_handle, current_step, every_n = 1, energy_file_handle = None, INIT_ENERGY = 1):
    """
    We step time using the verlet
    Inputs:
    list particles_list: list of particles (class Particle3D) to step
    list params_list: list of parameters specific to the particles simulated
    float dt: timestep to step over
    """
    G = float(G)
    for i in particle_list:
        i.second_order_posint(i.current_force, dt)
    for i in particle_list:
        new_force = np.array([0,0,0])
        for j in particle_list:
            if i != j:
                new_force = new_force + grav_force(i, j, G)
        i.current_force = new_force
        i.step_velocity(0.5*(new_force + i.prev_force), dt)
        i.prev_force = new_force

    if energy_file_handle != None:
        energy_file_handle.write("{0:.4g}, {1:.4g}\n".format(total_energy(G, particle_list), (total_energy(G, particle_list) - INIT_ENERGY)/INIT_ENERGY))

    if current_step % every_n == 0:
        current_step = (current_step // every_n) + 1
        out_file_handle.write("{0}\nPoint = {1}".format(len(particle_list), current_step))
        for i in particle_list:
            out_file_handle.write("\n{0}".format(i))
        out_file_handle.write("\n")

def check_observables(particle_list, max_arr, min_arr, wrt_arr, time, orbit_complete_flags, period_arr):
    """
    Computes the observables for the planets
    Inputs:
    list particle_list: list of particles
    array max_arr: array of current maximum orbit disances (float)
    array min_arr: array of current maximum orbit disances (float)
    wrt_arr: array of integers corresponding to the index of the particle that the particle of the index of the element is orbiting
    time: current time in simulation (float)
    orbit_complete_flags: boolean array that is true when the particle with that index has traversed 2pi radians
    period_arr: array containing the period of the particle with that index
    Return: 4 tuple containing adjusted max_arr, min_arr, orbit_complete_flags, period_arr
    """

    #apoapsis/periapsis
    for i in range(len(particle_list)):
        sep = Particle3D.separation(particle_list[i], particle_list[wrt_arr[i]])
        if norm(sep) > max_arr[i]:
            max_arr[i] = norm(sep)
        elif norm(sep) < min_arr[i]:
            min_arr[i] = norm(sep)
            
    #period
    for i in range(len(particle_list)):
        if not orbit_complete_flags[i]:
            if orbit_complete(particle_list[i], particle_list[wrt_arr[i]]):
                orbit_complete_flags[i] = True
                period_arr[i] = time

    return (max_arr, min_arr, orbit_complete_flags, period_arr)

def angle_between(v1, v2):
    """
    returns the smallest angle between two vectors (<= pi)
    Inputs: v1, v2 3d numpy vectors
    Returns: float angle 0<=angle<=pi
    """
    angle = np.arccos(np.dot(v1,v2)/(norm(v1)*norm(v2)))
    if angle > np.pi:
        angle = 2*np.pi - angle
    return angle
    

def orbit_complete(particle, wrt_particle):
    """
    This functions steps the angle of the particle forwards and checks if it has complete an orbit
    Input: 
    particle: a particle 3d object
    wrt_particle: a particle 3d object that the orbit of particle is taken with respect to
    """
    if norm(particle.position - wrt_particle.position) != 0:
        particle.angle_traversed = particle.angle_traversed + angle_between(particle.position-wrt_particle.position, particle.prev_pos-wrt_particle.prev_pos)
    else: 
        particle.angle_traversed = particle.angle_traversed + angle_between(particle.position, particle.prev_pos)

    if particle.angle_traversed >= 2*np.pi:
        return True
    else:
        return False
