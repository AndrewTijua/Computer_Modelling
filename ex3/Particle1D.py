"""
 CMod Ex3: Particle1D, a class to describe 1D particles
"""

class Particle1D(object):

    # Initialise a Particle1D instance
    def __init__(self, pos, vel, mass):
        self.position = pos
        self.velocity = vel
        self.mass = mass
    
    # Formatted output as String
    def __str__(self):
        return "x = " + str(self.position) + ", v = " + str(self.velocity) + ", m = " + str(self.mass)
    
    # Kinetic energy
    def kineticEnergy(self):
        return 0.5*self.mass*self.velocity**2

    # Time integration methods
    # First-order velocity update
    def leapVelocity(self, dt, force):
        self.velocity = self.velocity + dt*force/self.mass

    # First-order position update
    def leapPos1st(self, dt):
        self.position = self.position + dt*self.velocity

    # Second-order position update
    def leapPos2nd(self, dt, force):
        self.position = self.position + dt*self.velocity + 0.5*dt**2*force/self.mass
