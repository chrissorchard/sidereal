import logging
import argparse
logging.basicConfig(level=logging.DEBUG)

# Ignore packet debugs
logging.getLogger('sidereal.network.packets').setLevel("INFO")

import sidereal.client
import sidereal.network
import sidereal.panda as panda

c = sidereal.client.Client()
c.setup()

parser = argparse.ArgumentParser()
parser.add_argument('HOST',default='127.0.0.1',nargs='?')
parser.add_argument('PORT',type=int,default=25005,nargs='?')
parser.add_argument('--autoconnect','-a',action='store_true',default=False)

args = parser.parse_args()
HOST,PORT = args.HOST, args.PORT

from twisted.internet import task, reactor, stdio

class PandaUpdater(object):
    def __init__(self,engine,gamestate):
        self.engine = engine
        self.gamestate = gamestate
        self.visualrepr = {}
    def step(self):
        self.update_physics()
        self.engine.taskMgr.step()
    def update_physics(self):
        snapshots = self.gamestate.physics_snapshot()
        for id,snapshot in snapshots.items():
            if not id in self.visualrepr:
                node = self.visualrepr[id] = panda.Visualrepr(self.engine,id=id)
                node.debuglight = True

            self.visualrepr[id].coord = snapshot.coord
            self.visualrepr[id].quaternion = snapshot.quaternion

engine = panda.PandaEngine()
engine.disableMouse()
engine.setBackgroundColor(0,0,0,1)

from panda3d.core import AmbientLight

ambient = AmbientLight('ambient')
ambient.setColor((0.1,0.1,0.1,0.1))
ambientnp = engine.render.attachNewNode(ambient)
engine.render.setLight(ambientnp)

mainview = sidereal.panda.MainView(engine)
for region in engine.win.getDisplayRegions():
    region.setCamera(mainview.camera_np)

# engine set up
task.LoopingCall(PandaUpdater(engine,c.gamestate).step).start(0.1)

# and set up IO
input = sidereal.network.StdinInput(c,(HOST,PORT))
stdio.StandardIO(input)

if args.autoconnect:
    c.manager.send_packet({"type":"knock"},(HOST,PORT))

reactor.run()
