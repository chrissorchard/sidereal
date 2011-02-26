# Copyright (c) 2010 Jean-Paul Calderone
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
#    3. This notice may not be removed or altered from any source
#    distribution.

from bullet.bullet import (
    Vector3, Transform,
    BoxShape,
    DefaultMotionState,
    RigidBody,
    DiscreteDynamicsWorld)

def main():
    dynamicsWorld = DiscreteDynamicsWorld()

    groundShape = BoxShape(Vector3(50, 50, 50))
    groundTransform = Transform()
    groundTransform.setIdentity()
    groundTransform.setOrigin(Vector3(0, -56, 0))
    groundMotion = DefaultMotionState()
    groundMotion.setWorldTransform(groundTransform)
    ground = RigidBody(groundMotion, groundShape)
    dynamicsWorld.addRigidBody(ground)

    ballShape = BoxShape(Vector3(1, 1, 1))
    ballTransform = Transform()
    ballTransform.setIdentity()
    ballTransform.setOrigin(Vector3(2, 10, 0))
    ballMotion = DefaultMotionState()
    ballMotion.setWorldTransform(ballTransform)
    ball = RigidBody(ballMotion, ballShape, 1.0)
    dynamicsWorld.addRigidBody(ball)

    for i in range(100):
        dynamicsWorld.stepSimulation(1.0 / 60.0, 10)

        for obj in ballMotion, groundMotion:
            o = obj.getWorldTransform().getOrigin()
            print 'world pos = %0.6f,%0.6f,%0.6f' % (o.x, o.y, o.z)


main()
