import random

import panda3d.core

import sidereal.panda as panda
import sidereal.universe
import sidereal.ships as ships
import sidereal.physics.odeobjects as odeobjects

engine = panda.PandaEngine()
engine.disableMouse()
engine.setBackgroundColor(0,0,0,1)

ambient = panda3d.core.AmbientLight('ambient')
ambient.setColor((0.1,0.1,0.1,0.1))
ambientnp = engine.render.attachNewNode(ambient)
engine.render.setLight(ambientnp)

physicsworld = odeobjects.PhysicsWorld()
shipnodes = []

for i in range(10):
    if i == 0:
        pos = (0,0,0)
    else:
        pos = [random.randint(-100,100) for x in range(3)]
    physics = odeobjects.PhysicsObject(physicsworld,100)
    physics.body.setPosition(tuple(pos))
    ship = ships.PhysicsShip(physics)
    shipnode = panda.ShipNode(ship,engine)
    shipnode.debuglight = True
    shipnodes.append(shipnode)

mainview = sidereal.panda.MainView(base)
for region in engine.win.getDisplayRegions():
    region.setCamera(mainview.camera_np)

def update_physics(task):
    for shipnode in shipnodes:
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
        print "Forward."
        return task.again

    def left(self,task):
        self.physicsobject.body.addRelTorque((0,0,0.5))
        print "Left."
        return task.again

    def right(self,task):
        self.physicsobject.body.addRelTorque((-0,-0,-0.5))
        print "Right."
        return task.again

thrustercontrol = ThrusterEngineControl(engine,shipnodes[0].ship.physics)
engine.taskMgr.doMethodLater(0.01,update_physics,"physics")

# making it easier to call when running interactively, for testing
step = engine.taskMgr.step
while True:
    # same as engine.run()
    step()
