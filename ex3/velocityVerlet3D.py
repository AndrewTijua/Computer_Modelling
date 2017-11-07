import sys
from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np
from P3DMorseUtils import * #very little in it, all named explicitly

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

    f, axarr = plot.subplots(2)
    axarr[0].plot(tVals, sepVals)
    axarr[0].set_title("Particle Separation")
    #axarr[1].plot(tVals, energVals)
    #axarr[1].set_title("System Energy")
    axarr[1].plot(tVals, relEnergyError)
    axarr[1].set_title("Relative Energy Error")
    plot.show()

main()
