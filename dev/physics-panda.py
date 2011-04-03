import random
import math
import readline
import code
random.seed(0)

import panda3d.core
import ode

import sidereal.panda as panda
import sidereal.universe
import sidereal.ships as ships
import sidereal.physics as odeobjects
import sidereal.navigation as navigation

engine = panda.PandaEngine()
engine.disableMouse()
engine.setBackgroundColor(0,0,0,1)

ambient = panda3d.core.AmbientLight('ambient')
ambient.setColor((0.1,0.1,0.1,0.1))
ambientnp = engine.render.attachNewNode(ambient)
engine.render.setLight(ambientnp)

physicsworld = odeobjects.World()
collisionspace = ode.HashSpace()
shipnodes = []
geoms = []

for i in range(10):
    if i == 0:
        pos = (0,0,0)
    else:
        pos = [random.randint(-100,100) for x in range(3)]
    physics = odeobjects.PhysicsObject(physicsworld,100)
    physics.body.setPosition(tuple(pos))
    geom = ode.GeomSphere(collisionspace,radius=10.0)
    geoms.append(geom)
    ship = ships.PhysicsShip(physics)
    shipnode = panda.ShipNode(ship,engine)
    shipnode.debuglight = True
    shipnodes.append(shipnode)

mainview = sidereal.panda.MainView(base)
for region in engine.win.getDisplayRegions():
    region.setCamera(mainview.camera_np)

def anglexyz(q):
    q1,q2,q3,q4 = q
    halftheta = math.acos(q4)
    x = q1 / math.sin(halftheta)
    y = q2 / math.sin(halftheta)
    z = q3 / math.sin(halftheta)
    print "%.2f %.2f %.2f %.2f" % (x,y,z,math.degrees(halftheta*2))

def update_physics(task):
    for shipnode in shipnodes:
        if shipnode is shipnodes[0]:
            #w,x,y,z = shipnode.ship.quaternion
            #W,X,Y,Z = math.asin(w),math.asin(x),math.asin(y),math.asin(z)
            #print math.degrees(W),math.degrees(X),math.degrees(Y),math.degrees(Z)
            anglexyz(shipnode.ship.quaternion)

        shipnode.physics_update()
    physicsworld.step(0.01)
    return task.again

class ThrusterEngineControl(object):
    def __init__(self,engine,physicsobject):
        self.physicsobject = physicsobject
        self.engine = engine
        self.engine.accept("arrow_up",self.task_modify,['up',True])
        self.engine.accept("arrow_up-up",self.task_modify,['up',False])
        self.engine.accept("arrow_left",self.task_modify,['left',True])
        self.engine.accept("arrow_left-up",self.task_modify,['left',False])
        self.engine.accept("arrow_right",self.task_modify,['right',True])
        self.engine.accept("arrow_right-up",self.task_modify,['right',False])

    def task_modify(self,task,state):
        if task == "up":
            if state:
                self.engine.taskMgr.doMethodLater(0.01,self.forward,
                                                  'forwardtask')
            else:
                self.engine.taskMgr.remove('forwardtask')
        elif task == "left":
            if state:
                self.engine.taskMgr.doMethodLater(0.01,self.left,
                                                  'lefttask')
            else:
                self.engine.taskMgr.remove('lefttask')
        elif task == "right":
            if state:
                self.engine.taskMgr.doMethodLater(0.01,self.right,
                                                  'righttask')
            else:
                self.engine.taskMgr.remove('righttask')

    def forward(self,task):
        self.physicsobject.body.addRelForce((100,0,0))
        #print "Forward."
        return task.again

    def left(self,task):
        self.physicsobject.body.addRelTorque((0,0,0.5))
        print "Left."
        #print self.physicsobject.quaternion
        return task.again

    def right(self,task):
        self.physicsobject.body.addRelTorque((-0,-0,-0.5))
        print "Right."
        #print self.physicsobject.quaternion
        return task.again


class SelectionRay(object):
    def __init__(self,engine,mainview):
        self.engine = engine
        self.mainview = mainview
        self.engine.accept("mouse1",self.ray)
    def ray(self):
        # get camera location
        location = self.mainview.camera_location

        # and facing

        #USE PANDA?

        
        # make our geom

        # collide

        # determine what we've hit, if any

        # recentre the camera

    def collision_callback(self,args,geom1,geom2):
        contacts = ode.collide(geom1,geom2)
        world,contactgroup = args
        for c in contacts:
            pass


# code interject
engine.accept("c",code.interact,['Interpreter: ',raw_input,locals()])

thrustercontrol = ThrusterEngineControl(engine,shipnodes[0].ship.physics)
engine.taskMgr.doMethodLater(0.01,update_physics,"physics")

# select first objects
mainview.focusmanager.add(shipnodes[0].ship)

# making it easier to call when running interactively, for testing
step = engine.taskMgr.step
while True:
    # same as engine.run()
    step()
