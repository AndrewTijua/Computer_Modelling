import sys
#from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np
import GravUtils as GU #very little in it, all named explicitly



def main():
    if len(sys.argv) != 3:
        raise ValueError("Incorrect number of parameters!\n usage: {0} <particle_file> <param_file> <output_file>".format(sys.argv[0]))
    particles_list = GU.get_particles(sys.argv[1])
    sim_params_list = GU.get_params(sys.argv[2])
    
    out_file_name = str(sys.argv[3])
    out_file = open(out_file_name, 'w')

    G = sim_params_list[0]
    dt = sim_params_list[1]
    numsteps = sim_params_list[2]
    time = sim_params_list[3]

    tVals = [float(time)]
    energVals = [total_energy(G, particle_list)]
    initEnergy = total_energy(G, particle_list)
    relEnergyError = [0]
    
    #create initial forces
    for i in particles_list:
        i.prev_force = np.array([0,0,0])
        for j in particles_list:
            if i != j:
                i.prev_force = i.prev_force + GU.grav_force(i, j, D_e, r_e, alpha)

    for i in range(numstep):
        
        step_time(particles_list, G, dt, out_file, numstep + 1)
        time = time + dt
        
        tVals.append(time)
    out_file.close()


    #1 in time is 10.18 fs or 1.018x10^-14s
    tVals = [timescale*t for t in tVals]

if __name__ == "__main__": main()
