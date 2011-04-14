import collections

import ode

import sidereal.navigation as navigation
import sidereal.universe
import sidereal.physics as physics

class Gameloop(object):
    def __init__(self,do_graphics = False):
        self.do_graphics = do_graphics

        self.orders = []
        # maps gasau to physics,navigation,ingame,and visualrepr
        self.gasau_physics = {}
        self.gasau_navigation = {}
        self.gasau_ingame = {}
        self.gasau_visualrepr = {}

        self.world = physics.World()
        self.space = ode.HashSpace()
        
        # UNIVERSAL TIMER
        self.timer = 0
        # mapping from kaujul time to world snapshot
        self.kaujul_worldsnapshot = collections.OrderedDict()
        self.maxsize = 300

        # mapping (OLD,NEW) to diff
        self.kaujul_diff = {}

    def new_gasau(self,navclass=None,ingameclass=None,visualreprclass=None):
        if navclass is None:
            navclass = navigation.FakeNav
        if ingameclass is None:
            # TODO not implemented ingame class yet
            ingameclass = lambda: None

        if visualreprclass is None and self.do_graphics:
            visualreprclass = sidereal.panda.Visualrepr

        gasau = ships.Ship()
        body = physics.Body(self.world)

        nav = navclass()
        ingame = ingameclass()
        if self.do_graphics:
            visualrepr = visualreprclass()

        self.gasau_physics[gasau] = body
        self.gasau_navigation[gasau] = nav
        self.gasau_ingame[gasau] = ingame
        if self.do_graphics:
            self.gasau_visualrepr[gasau] = visualrepr
        return gasau

    def tick(self):
        for order in self.orders:
            pass
            # DO MAGIC
        self.update_navigation()
        self.world.step(0.01)
        # if no visualreprs have been added, then nothing will happen
        self.update_visualrepr()

    def update_visualrepr(self):
        for gasau,visualrepr in self.gasau_visualrepr.items():
            physics = self.gasau_physics[gasau]
            visualrepr.coord = physics.coord
            visualrepr.quaternion = physics.quaternion
    def update_navigation(self):
        for gasau,navigation in self.gasau_navigation.items():
            physics = self.gasau_physics[gasau]
            navigation.navigate(physics)

    def kaujul_tick(self):
        self.world.step(0.01)

        # a worldsnapshot is a mapping of ingame ids to body snapshots
        worldsnapshot = {}
        for gasau,body in self.gasau_physics.items():
            worldsnapshot[hash(gasau)] = body.snapshot()

        self.kaujul_worldsnapshot[self.kaujul] = worldsnapshot

        while len(self.kaujul_worldsnapshot) > self.maxsize:
            # fifo order
            self.kaujul_worldsnapshot.popitem(False)


        # our diff isn't what is DIFFERENT, because in a physics
        # simulation, practically everything's going to change
        # each tick. What we want, is stuff that has differed in
        # behaviour from what is expected

        # this means change in avelocity, or velocity

        # don't compare snapshots if kaujul is 0
        if self.kaujul != 0:
            prevsnapshot = self.kaujul_worldsnapshot[self.kaujul]
            diff = worldsnapshot.copy()
            for id,body in worldsnapshot.items():
                if id in prevsnapshot:
                    prevbody = prevsnapshot[id]
                    if (body.velocity == prevbody.velocity and
                        body.avelocity == prevbody.avelocity and
                        body.mass == prevbody.mass):
                        del diff[id]
            self.kaujul_diff[self.kaujul] = diff

        self.kaujul += 1

class Gamestate(object):
    def __init__(self):
        # An ingame object, or agent, or gasau isn't a single entity
        # It is a collection of different sets of data.
        #
        # Physics - It's physical location within space, speed, etc.
        # Ingame - Ingame information, fuel, damage, affilation, orders etc.
        # Navigation - Given waypoints, ingame, and physics, NAVIGATE
        self._physics = {}
        self._ingame = {}
        self._nav = {}
        
        self._dirty = set()

        self._world = physics.World()
        
        # UNIVERSE TIME, incremented on every tick.
        self.time = 0

        self.step_size = 0.01

    def gasau_data(self,id):
        physics = self._physics.get(id,None)
        ingame = self._ingame.get(id,None)
        nav = self._nav.get(id,None)
        return physics,ingame,nav

    def tick(self):
        # Returns physics diff
        self._world.step(self.step_size)

    def physics_snapshot(self):
        snapshot = {}
        for id,physics in self._physics.items():
            snapshot[id] = physics.snapshot()
        return snapshot
