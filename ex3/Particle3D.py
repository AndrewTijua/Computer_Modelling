import numpy as np
from numpy import array as array
from numpy import linalg as linalg

class Particle3D:
    def __init__(self, label, mass, position, velocity):
        try:
            self.label = str(label)
            self.mass = float(mass)
            self.position = array(position)
            self.velocity = array(velocity)
        except:
             raise ValueError('Something went wrong initialising a Particle3D')
    
    def __str__(self):
        return str("{0} {1} {2} {3}".format(self.label, self.position[0], self.position[1], self.position[2]))

    def kinetic_energy(self):
        return 0.5 * mass * (linalg.norm(velocity) ** 2)

    def step_velocity(self, force, timestep):
        self.velocity = self.velocity + (force * timestep)

    def first_order_posint(self, timestep):
        self.position = self.position + (self.velocity * timestep)

    def second_order_posint(self, force, timestep):
        self.position = self.position + (self.velocity * timestep) + ((force / (2 * self.mass)) * (timestep ** 2))

    @staticmethod
    def make_from_file(filename):
        file = open(filename)
        particle = Particle3D()
        lines = file.readlines()
        label = str(lines[0].rstrip('\n'))
        mass = float(lines[1].rstrip('\n'))
