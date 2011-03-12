import ode
import collections
import math

class PhysicsObject(object):
    def __init__(self,world):
        self.body = ode.Body(world)
        self.mass = ode.Mass()
        self.mass.setSphere(2500.0, 0.05)
        self.mass.mass = 1.0
        self.body.setMass(self.mass)
    @property
    def coord(self):
        return self.body.getPosition()
        

class PhysicsWorld(ode.World):
    def __init__(self):
        ode.World.__init__(self)
        self.setGravity((0,0,0))
