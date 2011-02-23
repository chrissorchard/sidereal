import bullet

class Ball(object):
    def __init__(self,origin=bullet.Vector3(0,10,0)):
        self.shape = bullet.SphereShape(1.0)
        self.transform = bullet.Transform()
        self.transform.setIdentity()
        self.transform.setOrigin(origin)
        self.motion = bullet.DefaultMotionState()
        self.motion.setWorldTransform(self.transform)
        self.body = bullet.RigidBody(self.motion, self.shape, 1.0)

class Ground(object):
    def __init__(self):
        self.shape = bullet.BoxShape(bullet.Vector3(50,50,50))
        self.transform = bullet.Transform()
        self.transform.setIdentity()
        self.transform.setOrigin(bullet.Vector3(0,-50,0))
        self.motion = bullet.DefaultMotionState()
        self.motion.setWorldTransform(self.transform)
        self.body = bullet.RigidBody(self.motion, self.shape)

if __name__=='__main__':
    b = Ball()
    g = Ground()
