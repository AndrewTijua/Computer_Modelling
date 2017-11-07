import sys
from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np

def morse_force(r1, r2, D_e, r_e, alpha):
    """
    Calculates the force due to the morse potential on particle 1 due to particle 2
    """
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    sep = Particle3D.separation(r1, r2)
    #Split expression for force into smaller parts for easier digestion
    force_part_one = -2 * alpha * D_e * (1 - math.exp(-1 * alpha * (norm(sep) - r_e)))
    force_part_two = math.exp(-1 * alpha * (norm(sep) - r_e))
    return force_part_one * force_part_two * sep

def morse_energy(r1, r2, D_e, r_e, alpha):
    """
    Expression for energy of two particle due to morse potential
    """
    D_e, r_e, alpha = float(D_e), float(r_e), float(alpha)
    sep = Particle3D.separation(r1, r2)
    energy = D_e * ((1 - math.exp(-1 * alpha*(norm(sep) - r_e))) ** 2 - 1)
    return energy

def total_energy(D_e, r_e, alpha, particle_list):
    """
    Computes the total system of the system
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
        if i.startswith('#') == False and i != '':
            non_comments.append(i)
    part_params_list = non_comments[3:6]
    sim_params_list = non_comments[0:3]
    particles_list = []
    for i in range((len(non_comments) - 3) // 4):
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

def step_time(particles_list, part_params_list, dt):
    """
    We step time using the verlet
    Inputs:
    list particles_list: list of particles (class Particle3D) to step
    list part_params_list: list of parameters specific to the particles simulated
    float dt: timestep to step over
    """
    D_e = part_params_list[0]
    r_e = part_params_list[1]
    alpha = part_params_list[2]
    for i in particles_list:
        new_force = np.array([0,0,0])
        for j in particles_list:
            if i != j:
                new_force = new_force + morse_force(i, j, D_e, r_e, alpha)
        i.current_force = new_force
        i.step_velocity(0.5*(new_force + i.prev_force), dt)
        i.prev_force = new_force
    for i in particles_list:
        i.second_order_posint(i.current_force, dt)

def energy_error_step(current_energy, init_energy):
    return (current_energy-init_energy)/init_energy

def main():
    in_args = get_input_vars(str(sys.argv[1]))
    
    out_file_name = str(sys.argv[2])
    out_file = open(out_file_name, 'w')

    particles_list = in_args[2]
    sim_params_list = in_args[0]
    part_params_list = in_args[1]
    
    numstep = int(sim_params_list[0])
    time = float(sim_params_list[1])
    dt = float(sim_params_list[2])

    D_e = part_params_list[0]
    r_e = part_params_list[1]
    alpha = part_params_list[2]

    tVals = [float(time)]
    sepVals = [norm(Particle3D.separation(particles_list[0], particles_list[1]))]
    energVals = [total_energy(D_e, r_e, alpha, particles_list)]
    initEnergy = total_energy(D_e, r_e, alpha, particles_list)
    relEnergyError = [0]

    out_file.write("{0:f} {1:f}\n".format(time, norm(Particle3D.separation(particles_list[0], particles_list[1]))))

    
    #create initial forces
    for i in particles_list:
        i.prev_force = np.array([0,0,0])
        for j in particles_list:
            if i != j:
                i.prev_force = i.prev_force + morse_force(i, j, D_e, r_e, alpha)

    for i in range(numstep):
        
        step_time(particles_list, part_params_list, dt)
        time = time + dt
        
        tVals.append(time)
        out_file.write("{0:f} {1:f}\n".format(time, norm(Particle3D.separation(particles_list[0], particles_list[1]))))
        sepVals.append(norm(Particle3D.separation(particles_list[0], particles_list[1])))
        energVals.append(total_energy(D_e, r_e, alpha, particles_list)) 
        relEnergyError.append(energy_error_step(total_energy(D_e, r_e, alpha, particles_list), initEnergy))
    out_file.close()


    #1 in time is 10.18 fs or 1.018x10^-14s
    timescale = 1.018e-14
    tVals = [timescale*t for t in tVals]

    f, axarr = plot.subplots(3)
    axarr[0].plot(tVals, sepVals)
    axarr[0].set_title("Particle Separation")
    #axarr[1].plot(tVals, energVals)
    #axarr[1].set_title("System Energy")
    axarr[1].plot(tVals, relEnergyError)
    axarr[1].set_title("Relative Energy Error")
    plot.show()

main()
