"""
Navigation internal AI.

Need to get to a specific location? This is the thang.

"""

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
    
class FakeNav(list):
    """Instead of a magical natural physics basic system, this is our
    cheap hack. Given a target, look in that direction, and suddenly
    start moving at some defined max speed."""
    def navigate(self,physics):
        if len(self) == 0:
            return
        target = self[0]
        rotation = perfect_rotation(physics.coord,target)
        physics.quaternion = rotation
        physics.velocity = (0,0,50)


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

