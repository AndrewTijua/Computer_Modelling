import numpy as np
from numpy import array as array
from numpy import linalg as linalg

class Particle3D:
    """
    This class is set up to allow easy manipulation of a point particle in three dimensions
    """

    def __init__(self, label, mass, position, velocity, prev_force=[0,0,0], current_force=[0,0,0]):
        """
        This method creates the particle from input
        :string label: The label wanted for the particle
        :float mass: The mass wanted for the particle
        :numpy array position: The initial position wanted for the particle
        :numpy array velocity: The initial velocity wanted for the particle
        :numpy array prev_force: previous force applied to particle (useful for verlet)
        :numpy array current_force: current force (for synchronicity)
        """
        try:
            self.label = str(label)
            self.mass = float(mass)
            self.position = array(position, dtype=np.float64)
            self.velocity = array(velocity, dtype=np.float64)
            self.prev_force = array(prev_force, dtype=np.float64)
            self.current_force = array(current_force, dtype=np.float64)
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
        return 0.5 * self.mass * (linalg.norm(self.velocity) ** 2)

    def step_velocity(self, force, timestep):
        """
        This method updates the velocity of the particle given a force and timestep
        :numpy array force: The force applied to the particle
        :float time: The time interval to step over
        """
        self.velocity = self.velocity + (force * timestep)/self.mass

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
    def make_from_file(filehandle):
        """
        This method takes a properly formatted file and creates a Particle3D class with the given parameters
        :filehandle filehandle: The handle of the file we are reading from
        :return particle: A particle from the file
        """
        lines = filehandle.readlines()
        label = str(lines[0].rstrip('\n'))
        mass = float(lines[1].rstrip('\n'))
        position = list(lines[2].rstrip('\n').split(','))
        velocity = list(lines[3].rstrip('\n').split(','))
        particle = Particle3D(label=label, mass=mass, position=position, velocity=velocity)
        filehandle.close()
        return particle

    @staticmethod
    def separation(p1, p2):
        """
        This method computes the vector separation of two particles represented by Particle3D classes
        :p1 Particle3D: A particle
        :p2 Particle3D: A particle
        :return numpy array: The vector separation of the particles
        """
        return(p1.position - p2.position)

