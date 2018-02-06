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
    every_n = sim_params_list[4]

    t_vals = np.zeros(numsteps)
    energy_vals = np.zeros(numsteps)
    rel_energy_error = np.zeros(numsteps)
    init_pos_arr = np.zeros((len(particle_list), 3))
    max_arr = np.zeros(len(particle_list))
    min_arr = np.zeros(len(particle_list))
    wrt_arr = np.zeros(len(particle_list), dtype=np.int_)
    period_arr = np.zeros(len(particle_list))
    orbit_complete_flags = np.full(len(particle_list), False, dtype=bool)

    t_vals[0] = float(time)
    INIT_ENERGY= GU.total_energy(G, particle_list)
    energy_vals[0] = INIT_ENERGY

    for i in range(len(init_pos_arr)):
        init_pos_arr[i] = particle_list[i].position
        max_arr[i] = norm(particle_list[i].position - particle_list[wrt_arr[i]].position)
        min_arr[i] = norm(particle_list[i].position - particle_list[wrt_arr[i]].position)
    

    #apply CoM correction
    GU.drift_correct(particle_list)

    #create initial forces
    for i in particle_list:
        i.prev_force = np.array([0,0,0])
        for j in particle_list:
            if i != j:
                i.prev_force = i.prev_force + GU.grav_force(i, j, G)

    for i in range(numsteps):
        
        GU.step_time(particle_list, G, dt, out_file, i, every_n)
        time = time + dt
        if i > 0:
            t_vals[i] = time
            energy_vals[i] = GU.total_energy(G, particle_list)
            rel_energy_error[i] = (energy_vals[i] - INIT_ENERGY) / INIT_ENERGY

    out_file.close()


if __name__ == "__main__": main()
