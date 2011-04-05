"""
Navigation internal AI.

Need to get to a specific location? This is the thang.

"""

import math
import collections

# utility functions
def rotate_diff(one,two):
    coord = one.coord
    q = one.quaternion
    dest = two.coord
    return perfect_rotation(one.coord,two.coord)

def perfect_rotation(onecoord,twocoord):
    # this is a GOD AWFUL method of doing it
    from panda3d.core import NodePath
    foo = NodePath("foo")
    bar = NodePath("bar")
    foo.setPos(onecoord)
    bar.setPos(twocoord)
    foo.lookAt(bar)

    return foo.getQuat()

def distance(one,two):
    # for (x1,y1,z1) and (x2,y2,z2)
    total = [(j - i)**2 for i,j in zip(one,two)]
    # [ (x2 - x1)^2 etc. ]
    return math.sqrt(sum(total))

class FakeNav(collections.deque):
    """Instead of a magical natural physics basic system, this is our
    cheap hack. Given a target, look in that direction, and suddenly
    start moving at some defined max speed."""
    def navigate(self,physics):
        # check to see if we have no waypoints
        if self.target is None:
            return
        # not actually working
        rotation = perfect_rotation(self.target,physics.coord)
        physics.quaternion = rotation

        # ugh, velocity

        # check to see if we're "here"
        #print physics.coord
        #print self.target
        d = distance(physics.coord,self.target)
        if d < 5:
            self.popleft()

    @property
    def target(self):
        if len(self) == 0:
            return None
        else:
            return self[0]


class CrudeNav(object):
    """A fairly poor form of navigation that does the following:
        #. Rotate until we're facing target direction.
        #. Apply force until at desired speed.
        #. When within X metres, rotate and slow down.
    """

if __name__=='__main__':
    class O:
        pass
    one = O()
    one.coord = (0,0,0)
    one.quaternion = (1,0,0,0)
    two = O()
    two.coord = (20,-40,60)
    print rotate_diff(one,two)

