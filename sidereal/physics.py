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

class Body(ode.Body):
    """A wrapper for the ode.Body() object that has a bunch of properties."""
    def __init__(self,world,mass=1.0):
        ode.Body.__init__(self,world)
        self.mass = ode.Mass()
        self.mass.setSphere(2500.0, 0.05)
        self.mass.mass = mass
        self.setMass(self.mass)

    def _get_coord(self):
        return self.getPosition()
    def _set_coord(self,coord):
        self.setPosition(coord)
    coord = property(_get_coord,_set_coord)

    def _get_quaternion(self):
        return self.getQuaternion()
    def _set_quaternion(self,quaternion):
        self.setQuaternion(quaternion)
    quaternion = property(_get_quaternion,_set_quaternion)

    def _get_velocity(self):
        return self.getLinearVel()
    def _set_velocity(self,velocity):
        self.setLinearVel(velocity)
    velocity = property(_get_velocity,_set_velocity)

    def _get_avelocity(self):
        return self.getAngularVel()
    def _set_avelocity(self,avelocity):
        self.setAngularVel(avelocity)
    avelocity = property(_get_avelocity,_set_avelocity)


class PhysicsWorld(ode.World):
    def __init__(self):
        ode.World.__init__(self)
        self.setGravity((0,0,0))
