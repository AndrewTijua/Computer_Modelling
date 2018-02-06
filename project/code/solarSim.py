import sys
#from matplotlib import pyplot as plot
from Particle3D import Particle3D
import math
from numpy.linalg import norm
import numpy as np
import GravUtils as GU #very little in it, all named explicitly



def main():
    if len(sys.argv) != 4:
        raise ValueError("Incorrect number of parameters!\n usage: {0} <particle_file> <param_file> <output_file>".format(sys.argv[0]))
    particle_list = GU.get_particles(sys.argv[1])
    sim_params_list = GU.get_params(sys.argv[2])
    
    out_file_name = str(sys.argv[3])
    out_file = open(out_file_name, 'w')

    G = sim_params_list[0]
    dt = sim_params_list[1]
    numsteps = sim_params_list[2]
    time = sim_params_list[3]

    tVals = [float(time)]
    energVals = [GU.total_energy(G, particle_list)]
    initEnergy = GU.total_energy(G, particle_list)
    relEnergyError = [0]
    
    #create initial forces
    for i in particle_list:
        i.prev_force = np.array([0,0,0])
        for j in particle_list:
            if i != j:
                i.prev_force = i.prev_force + GU.grav_force(i, j, G)

    for i in range(numsteps):
        
        GU.step_time(particle_list, G, dt, out_file, i+1)
        time = time + dt
        
        tVals.append(time)
    out_file.close()


if __name__ == "__main__": main()
