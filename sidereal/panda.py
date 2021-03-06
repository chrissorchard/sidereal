"""The main view should be considered the default view, the one with all
of the spaceships and stuff around.

TODO this doc is clearly incomplete."""

# stdlib
import collections
import random
import math
import threading

# third party
import panda3d.core
import direct.showbase.ShowBase
import direct.task

# internal

from sidereal.turtles import triple_float


# One thing I'm wondering about, is whether we implement the gui overlay
# in a seperate space. How does it intercept the clicks, and know which one
# is which? I guess we hope for panda magic.

# Right, in core homeworld, the camera is always focused on something, unless
# it's been destroyed. But my point that the camera always rotates and pivots
# around a central point. I'm sure we could implement "look around" later
# but first things need to rotate.

# things only rotate when the right mouse button is held down.

# Imagine we're on the surface of a sphere, which is centered around the point
# that we're looking at. Moving the mouse left rotates left from your
# perspective, and so on.
class MainView(object):
    def __init__(self,showbase):
        self.base = showbase

        # The mainview has its own camera.
        self.camera = panda3d.core.Camera('MainView camera')
        self.camera_np = panda3d.core.NodePath(self.camera)
        # A camera is its own node. Although we need to attach it to the
        # tree to see anything.
        self.camera_np.reparentTo(self.base.render)
        self.focusmanager = FocusManager()
        self.focuspoint = (0,0,0)
        self.camera_position = (0,0,0)
        self.zoom = 100

        # where max, is maximum zoom out
        # where min, is minimum zoon in
        self.maxzoom = 300
        self.minzoom = 10

        # setting sensitivity to negative inverts the axis
        self.horizontal_sensitivity = -0.5 # Higher is more precise
        # As in, slower
        self.vertical_sensitivity = 1
        self.spherepoint = SpherePoint(self.zoom,0,0.5)

        self.set_up_event_handlers()

        # always follow camera
        self.base.taskMgr.add(self._pandatask_update_camera,'cameraupdate')

    def set_up_event_handlers(self):
        self.mouse_lock = threading.Lock()
        self.mouse_rotate = False
        self.base.accept('mouse1',self.watch_mouse)
        self.base.accept('mouse1-up',self.stop_watching_mouse)
        self.base.accept('mouse3',self.watch_mouse)
        self.base.accept('mouse3-up',self.stop_watching_mouse)
        self.base.accept('wheel_up',self.adjust_zoom,[-10])
        self.base.accept('wheel_down',self.adjust_zoom,[10])


        #self.base.taskMgr.doMethodLater(0.5,self._randomise_spherepoint,'randomise')
    def adjust_zoom(self,adjustment):
        self.zoom += adjustment
        self.zoom = max(self.zoom,self.minzoom)
        self.zoom = min(self.zoom,self.maxzoom)

        self.spherepoint.radius = self.zoom

    def watch_mouse(self):
        with self.mouse_lock:
            if self.mouse_rotate == False:
                self.mouse_coords = ()
                self.base.taskMgr.doMethodLater(0.01,self.mouse_monitor_task, 'main-view mouse watch')
                self.mouse_rotate = True
    def stop_watching_mouse(self):
        with self.mouse_lock:
            if self.mouse_rotate == True:
                self.base.taskMgr.remove('main-view mouse watch')
                self.mouse_rotate = False

    def mouse_monitor_task(self,task):
        x = self.base.mouseWatcherNode.getMouseX()
        y = self.base.mouseWatcherNode.getMouseY()

        #print x,y

        # If the coords are empty, then skip this whole block
        if self.mouse_coords == ():
            self.mouse_coords = (x,y)
            return task.cont # do the same next frame

        if self.mouse_coords == (x,y):
            return task.again


        dx = self.mouse_coords[0] - x
        dy = self.mouse_coords[1] - y

        self.mouse_coords = (x,y)

        #print dx,dy

        # then based on the dx,dy move the mainview's camera around its
        # focused point. Preferable moving the mouse left, also rotates
        # the camera to the left.

        angle = self.spherepoint.angle
        angle += dx / self.horizontal_sensitivity
        angle %= math.pi * 2
        self.spherepoint.angle = angle

        vertical = self.spherepoint.vertical
        vertical += dy / self.vertical_sensitivity
        vertical = min(vertical,0.999999)
        vertical = max(vertical,0.000001)
        self.spherepoint.vertical = vertical

        return task.again

    def _update_camera(self):
        offset = self.spherepoint.calculate()
        self.camera_position = [x+y for x,y in zip(offset,self.focusmanager.coord)]
        self.camera_np.setPos(*self.camera_position)
        self.camera_np.lookAt(self.focusmanager.coord)
    def _pandatask_update_camera(self,task):
        self._update_camera()
        return task.cont

    def _randomise_spherepoint(self,task):
        self.spherepoint.vertical = random.random()
        self.spherepoint.angle = random.random() * math.pi * 2
        self.camera_np.setPos(*self.spherepoint.calculate())
        self.camera_np.lookAt((0,0,0))
        return task.again

class SpherePoint(object):
    """Manipulating a camera on a sphere's surface seems complicated.
    As such, this class SHOULD be helpful in that.

    Imagine the camera as a point on the sphere, which if you take a
    2d flat horizontal slice is a circle. The camera is somewhere on
    that circle, at a certain angle. Where you take the 2d slice
    could be called the vertical.

    The radius of the sphere should be obvious.

    This sphere is centered on 0,0,0"""
    def __init__(self,radius,angle,vertical):
        """
        Radius is a positive number.
        Angle is 0 < a < 2pi
        Vertical ranges from 0 < v < 1
        """
        self.radius = radius
        self.angle = angle
        self.vertical = vertical
    def __repr__(self):
        return "SpherePoint({0},{1},{2})".format(self.radius,self.angle,self.vertical)
    def calculate(self):
        slice_r = self.radius * math.sin(self.vertical * math.pi)
        x = slice_r * math.sin(self.angle)
        y = slice_r * math.cos(self.angle)
        z = (2 * self.radius * self.vertical) - self.radius
        return (x,y,z) # Remember, the center of this sphere is 0,0,0

class FocusManager(collections.MutableSet):
    """The FocusManager the utility for maintaining focus on one to many
    game objects, with none being a special case.

    It is treated as a Set of objects, which should (TODO change to MUST)
    be ingame objects with coordinates. It can then determine the average
    point to focus on from all of its component objects.

    If objects leave the FocusManager (such as by being destroyed, or
    de-focused, the FocusManager then recalculates its "average".
    If all objects leave, then it will continue to stare at the last point
    a la CalHomeworld behaviour."""
    def __init__(self):
        self._internal_set = set()
        self._coord = (0,0,0)
    def add(self,item):
        self._internal_set.add(item)
        #self.update()
    def discard(self,item):
        self._internal_set.discard(item)
        # If len is 0, then it'll keep its last average_coord
        #if len(self) > 0:
            #    self.update()
    def __len__(self):
        return len(self._internal_set)
    def __iter__(self):
        return iter(self._internal_set)
    def __contains__(self,item):
        return item in self._internal_set
    @property
    def coord(self):
        if len(self) > 0:
            self._coord = self._calculate_average()
        return self._coord
    def _calculate_average(self):
        """Assumes that all objects in the set have a .coord attribute"""
        # AVerageX and so on.
        if len(self) <= 0:
            return

        avx = avy = avz = 0
        for item in self:
            avx += item.coord[0]
            avy += item.coord[1]
            avz += item.coord[2]

        avx /= len(self)
        avy /= len(self)
        avz /= len(self)
        #print avx,avy,avz
        return (avx,avy,avz)


class PandaEngine(direct.showbase.ShowBase.ShowBase):
    def __init__(self):
        direct.showbase.ShowBase.ShowBase.__init__(self)

class ShipNode(object):
    """
    Assuming that a created ship has a .coord and .quaternion attributes
    (which may talk to its own .physics instance, or be set for "artifical"
    ships that a client has, it associates it with a model, places it in the
    scene, and has a method for updating its place in the scene.
    """
    def __init__(self,ship,engine,model="models/teapot"):
        self.ship = ship
        self.nodepath = engine.loader.loadModel(model)
        self.nodepath.reparentTo(engine.render)
        self.id = hash(self.ship)

        self.engine = engine
        self._debuglight = False

    def _get_debuglight(self):
        return self._debuglight

    def _set_debuglight(self,value):
        if value == True and self._debuglight == False:
            # turn on the light
            light = panda3d.core.PointLight("my light")
            color = triple_float(hash(self.id),alpha=True)
            light.setColor(color)
            light.setAttenuation((0,0,0.01))
            self.lightnodepath = self.nodepath.attachNewNode(light)
            self.lightnodepath.setPos(0, 0, 10)
            self.engine.render.setLight(self.lightnodepath)

            # and set it so we're flagged as on
            self._debuglight = True
        elif value == False and self._debuglight == True:
            # if the lights on, turn it off, otherwise
            self._debuglight = False

            self.lightnodepath.detachNode()
            self.engine.render.clearLight(self.lightnodepath)
            self.lightnodepath.removeNode()

            # set if so we're flagged as off

    debuglight = property(_get_debuglight, _set_debuglight)

    def physics_update(self):
        coord = self.ship.coord
        quaternion = self.ship.quaternion
        # setPos takes (x,y,z), and our coord is a tuple, so we need to
        # unpack the coordinates
        self.nodepath.setPos(*coord)
        self.nodepath.setQuat(panda3d.core.Quat(*quaternion))

class Visualrepr(ShipNode):
    def __init__(self,engine,model="models/teapot",id=0):
        self.nodepath = engine.loader.loadModel(model)
        self.nodepath.reparentTo(engine.render)
        self.engine = engine
        self._debuglight = False
        self.id = id

    def get_coord(self):
        return tuple(self.nodepath.getPos())
    def set_coord(self,coord):
        self.nodepath.setPos(*coord)
    coord = property(get_coord,set_coord)
    def get_quat(self):
        return tuple(self.nodepath.getQuat())
    def set_quat(self,quat):
        self.nodepath.setQuat(panda3d.core.Quat(*quat))
    quaternion = property(get_quat,set_quat)

