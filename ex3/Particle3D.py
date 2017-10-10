import numpy as np
from numpy import array as array
from numpy import linalg as linalg

class Particle3D:
    """
    This class is set up to allow easy manipulation of a point particle in three dimensions
    """

    def __init__(self, label, mass, position, velocity):
        """
        This method creates the particle from input
        :string label: The label wanted for the particle
        :float mass: The mass wanted for the particle
        :numpy array position: The initial position wanted for the particle
        :numpy array velocity: The initial velocity wanted for the particle
        """
        try:
            self.label = str(label)
            self.mass = float(mass)
            self.position = array(position)
            self.velocity = array(velocity)
        except:
             raise ValueError('Something went wrong initialising a Particle3D')
    
    def __str__(self):
        """
        This method returns the label and 3d coordinates of a particle in an easy to parse format
        :return string: Machine readable string containing the particle label and position
        """
        return str("{0} {1} {2} {3}".format(self.label, self.position[0], self.position[1], self.position[2]))

    def kinetic_energy(self):
        """
        This method calculates the kinetic energy of the particle
        :return float: The kinetic energy of the particle
        """
        return 0.5 * mass * (linalg.norm(velocity) ** 2)

    def step_velocity(self, force, timestep):
        """
        This method updates the velocity of the particle given a force and timestep
        :numpy array force: The force applied to the particle
        :float time: The time interval to step over
        """
        self.velocity = self.velocity + (force * timestep)

    def first_order_posint(self, timestep):
        """
        This method performs first order time integration on the particles position
        :float timestep: The time interval to step over
        """
        self.position = self.position + (self.velocity * timestep)

    def second_order_posint(self, force, timestep):
        """
        This method performs second order time integration on the particles position
        :numpy array force: The force applied to the particle
        :float timestep: The time interval to step over
        """
        self.position = self.position + (self.velocity * timestep) + ((force / (2 * self.mass)) * (timestep ** 2))

    @staticmethod
    def make_from_file(filename):
        """
        This method takes a properly formatted file and creates a Particle3D class with the given parameters
        """
        file = open(filename)
        particle = Particle3D()
        lines = file.readlines()
        label = str(lines[0].rstrip('\n'))
        mass = float(lines[1].rstrip('\n'))
        position = array(list(lines[2].rstrip('\n').split(',')), dtype='float64')
        velocity = array(list(lines[3].rstrip('\n').split(',')), dtype='float64')
        particle.__init__(label, mass, position, velocity)

    @staticmethod
    def separation(p1, p2):
        """
        This method computes the vector separation of two particles represented by Particle3D classes
        :p1 Particle3D: A particle
        :p2 Particle3D: A particle
        :return numpy array: The vector separation of the particles
        """
        return(p1.position - p2.position)