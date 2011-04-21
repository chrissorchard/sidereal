import ode
import collections
import math

from sidereal.vector import Vector

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

class Body(object):
    """A wrapper for the ode.Body() object that has a bunch of properties."""
    def __init__(self,world,mass=1.0):
        self.body = ode.Body(world)
        self._mass = ode.Mass()
        self._mass.setSphere(2500.0, 0.05)
        self._mass.mass = mass
        self.body.setMass(self._mass)
    def _get_mass(self):
        return self._mass.mass
    def _set_mass(self,mass_value):
        self._mass.mass = mass_value
        self.body.setMass(self._mass)
    mass = property(_get_mass,_set_mass)

    def _get_coord(self):
        return self.body.getPosition()
    def _set_coord(self,coord):
        self.body.setPosition(coord)
    coord = property(_get_coord,_set_coord)

    def _get_quaternion(self):
        return self.body.getQuaternion()
    def _set_quaternion(self,quaternion):
        self.body.setQuaternion(quaternion)
    quaternion = property(_get_quaternion,_set_quaternion)

    def _get_velocity(self):
        return self.body.getLinearVel()
    def _set_velocity(self,velocity):
        self.body.setLinearVel(velocity)

    velocity = property(_get_velocity,_set_velocity)

    def _get_avelocity(self):
        return self.body.getAngularVel()
    def _set_avelocity(self,avelocity):
        self.body.setAngularVel(avelocity)
    avelocity = property(_get_avelocity,_set_avelocity)

    def snapshot(self):
        # Returns a named tuple containing all important variables
        return BodySnapshot(self.velocity,
                            self.avelocity,
                            self.quaternion,
                            self.coord,
                            self.mass)
    def unsnapshot(self,snapshot):
        # Given a snapshot, set everything that needs to be set
        velocity,avelocity,quaternion,coord,mass = snapshot
        self.velocity = velocity
        self.avelocity = avelocity
        self.quaternion = quaternion
        self.coord = coord
        self.mass = mass

_fields = ['velocity','avelocity','quaternion','coord','mass']
BodySnapshot = collections.namedtuple("BodySnapshot",_fields)

def vector_orientation(physics):
    tempworld = World()
    tempbody = Body(tempworld)
    # mass of 1
    tempbody.coord = (0,0,0)
    tempbody.quaternion = physics.quaternion
    tempbody.body.addRelForce((1,0,0))
    tempworld.step(1)
    return Vector(tempbody.coord)

class World(ode.World):
    def __init__(self):
        ode.World.__init__(self)
        self.setGravity((0,0,0))

# constants
STEPSIZE = 0.01
