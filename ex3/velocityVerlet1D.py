"""
CMod Ex3: velocity Verlet time integration of
particle in anharmonic potential.

Produce both a plot of the amplitude and an
output file.
"""

import sys
import matplotlib.pyplot as pyplot
from Particle1D import Particle1D

# Read name of output file from command line
if len(sys.argv)!=2:
    print("Wrong number of arguments.")
    print("Usage: " + sys.argv[0] + " <output file>")
    quit()
else:
    outfileName = sys.argv[1]

# Open output file for writing
outfile = open(outfileName, "w")

# Set up particle
mass = 1.0
pos  = 0.0
vel  = 1.0
p = Particle1D(pos, vel, mass)

# Set up simulation parameters
numstep = 100
time = 0.0
dt = 0.1

# Set up anharmonic potential constants
fc2 = 1.0
fc4 = 1.0
force = -fc2*p.position -fc4*p.position**3

# Set up data lists
tValue = [time]
posValue = [p.position]

outfile.write("{0:f} {1:f}\n".format(time, p.position))

# Start the time integration loop

for i in range(numstep):
    # Update particle position
    p.leapPos2nd(dt, force)
    # Update force
    force_new = -fc2*p.position -fc4*p.position**3
    # Update particle velocity, based on average
    # of current and new forces
    p.leapVelocity(dt, 0.5*(force+force_new))

    # Reset force variable
    force = force_new

    # Increase time
    time = time + dt
    
    # Output particle information
    tValue.append(time)
    posValue.append(p.position)
    outfile.write("{0:f} {1:f}\n".format(time, p.position))

# Close output file
outfile.close()

# Plot graph of amplitude vs time
pyplot.plot(tValue,posValue)
pyplot.show()
