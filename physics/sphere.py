import time

import bullet
from bullet import Vector3

class Ball(bullet.RigidBody,object):
    def __init__(self,origin=bullet.Vector3(0,100,0)):
        self.shape = bullet.SphereShape(1.0)
        self.transform = bullet.Transform()
        self.transform.setIdentity()
        self.transform.setOrigin(origin)
        self.motion = bullet.DefaultMotionState()
        self.motion.setWorldTransform(self.transform)
        bullet.RigidBody.__init__(self,self.motion, self.shape, 1.0)

class Ground(bullet.RigidBody,object):
    def __init__(self):
        self.shape = bullet.BoxShape(bullet.Vector3(50,50,50))
        self.transform = bullet.Transform()
        self.transform.setIdentity()
        self.transform.setOrigin(bullet.Vector3(0,-50,0))
        self.motion = bullet.DefaultMotionState()
        self.motion.setWorldTransform(self.transform)
        bullet.RigidBody.__init__(self,self.motion, self.shape)

class PhysicsHelper(object):
    def __init__(self,body):
        self.body = body

    def _yaw(self,yaw):
        pass
    def _pitch(self,pitch):
        pass
    def _roll(self,roll):
        pass

def _tick(world,items):
    world.stepSimulation(1.0/60.0,100)
    for obj in items:
        vector = obj.getWorldTransform().getOrigin()
        print vector

if __name__=='__main__':
    b = Ball()
    b.setRestitution(0.9)
    g = Ground()
    world = bullet.DiscreteDynamicsWorld()

    world.addRigidBody(g)
    world.addRigidBody(b)
