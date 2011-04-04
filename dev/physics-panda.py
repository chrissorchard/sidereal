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
import sidereal.game

engine = panda.PandaEngine()
engine.disableMouse()
engine.setBackgroundColor(0,0,0,1)

ambient = panda3d.core.AmbientLight('ambient')
ambient.setColor((0.1,0.1,0.1,0.1))
ambientnp = engine.render.attachNewNode(ambient)
engine.render.setLight(ambientnp)


gameloop = sidereal.game.Gameloop(do_graphics=False)
first = None

# little wrapper for panda
def gameloop_tick_task(task):
    global gameloop
    gameloop.tick()
    return task.again

for i in range(10):
    gasau = gameloop.new_gasau()
    r = random.Random()
    r.seed(hash(gasau))

    if i == 0:
        first = gasau
        pos = (0,0,0)
    else:
        pos = [r.randint(-100,100) for x in range(3)]
    
    gameloop.gasau_physics[gasau].mass = 1000
    gameloop.gasau_physics[gasau].coord = pos
    shipnode = panda.Visualrepr(engine,id=hash(gasau))

    shipnode.debuglight = True
    gameloop.gasau_visualrepr[gasau] = shipnode

mainview = sidereal.panda.MainView(base)
for region in engine.win.getDisplayRegions():
    region.setCamera(mainview.camera_np)

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
        self.physicsobject.addRelForce((100,0,0))
        #print "Forward."
        return task.again

    def left(self,task):
        self.physicsobject.addRelTorque((0,0,0.5))
        print "Left."
        #print self.physicsobject.quaternion
        return task.again

    def right(self,task):
        self.physicsobject.addRelTorque((-0,-0,-0.5))
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

thrustercontrol = ThrusterEngineControl(engine,gameloop.gasau_physics[first])

engine.taskMgr.doMethodLater(0.01,gameloop_tick_task,"gameloop")

# select first objects
mainview.focusmanager.add(gameloop.gasau_physics[first])

# making it easier to call when running interactively, for testing
step = engine.taskMgr.step
while True:
    # same as engine.run()
    step()
