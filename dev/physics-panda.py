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
    if i == 1:
        pos = (0,0,0)
    else:
        pos = [random.randint(-100,100) for x in range(3)]
    physics = odeobjects.PhysicsObject(physicsworld,1000)
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
    physicsworld.step(0.04)
    return task.again

engine.taskMgr.doMethodLater(0.04,update_physics,"physics")
engine.run()
