import ode
import collections
import math

class PhysicsObject(object):
    def __init__(self,world,mass=1.0):
        self.body = ode.Body(world)
        self.mass = ode.Mass()
        self.mass.setSphere(2500.0, 0.05)
        self.mass.mass = mass
        self.body.setMass(self.mass)
    @property
    def coord(self):
        return self.body.getPosition()

    @property
    def quaternion(self):
        return self.body.getQuaternion()
        

class PhysicsWorld(ode.World):
    def __init__(self):
        ode.World.__init__(self)
        self.setGravity((0,0,0))
