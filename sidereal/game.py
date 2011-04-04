import collections

import ode

import sidereal.ships as ships
import sidereal.navigation as navigation
import sidereal.universe
import sidereal.physics as physics
import sidereal.panda

class Gameloop(object):
    def __init__(self,do_graphics = True):
        self.do_graphics = do_graphics

        self.orders = []
        # maps gasau to physics,navigation,ingame,and visualrepr
        self.gasau_physics = {}
        self.gasau_navigation = {}
        self.gasau_ingame = {}
        self.gasau_visualrepr = {}

        self.world = physics.World()
        self.space = ode.HashSpace()

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


