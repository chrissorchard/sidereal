"""The main view should be considered the default view, the one with all
of the spaceships and stuff around.

TODO this doc is clearly incomplete."""

# stdlib
import collections

# third party
import panda3d.core
import direct.task

# internal


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

        self.set_up_event_handlers()Q

    def set_up_event_handlers(self):
        self.base.accept('mouse2',self.watch_mouse)
        self.base.accept('mouse2-up',self.stop_watching_mouse)

    def watch_mouse(self):
        self.mouse_coords = []
        self.base.taskMgr.add(self.mouse_monitor_task, 'main-view mouse watch')
    def stop_watching_mouse(self):
        self.base.taskMgr.remove('main-view mouse watch')

    def mouse_monitor_task(self,task)
        x = self.base.mouseWatcherNode.getMouseX()
        y = self.base.mouseWatcherNode.getMouseY()

        if self.mouse_coords == []:
            self.mouse_coords = [x,y]
        else:
            dx = self.mouse_coords[0] - x
            dy = self.mouse_coords[1] - y

            # then based on the dx,dy move the mainview's camera around its
            # focused point. Preferable moving the mouse left, also rotates
            # the camera to the left. TODO

        return direct.task.Task.cont # do the same next frame
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
        self.coord = (0,0,0)
    def add(self,item):
        self._internal_set.add(item)
        self.coord = self._calculate_average()
    def discard(self,item):
        self._internal_set.discard(item)
        # If len is 0, then it'll keep its last average_coord
        if len(self) > 0:
            self.coord = self._calculate_average()
    def __len__(self):
        return len(self._internal_set)
    def __iter__(self):
        return iter(self._internal_set)
    def __contains__(self,item):
        return item in self._internal_set
    def _calculate_average(self):
        """Assumes that all objects in the set have a .coord attribute"""
        # AVerageX and so on.
        avx,avy,avz = 0
        for item in self:
            avx += item.coord[0]
            avy += item.coord[1]
            avz += item.coord[2]

        avx /= len(self)
        avy /= len(self)
        avz /= len(self)
        return (avx,avy,avz)


