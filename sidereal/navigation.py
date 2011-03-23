"""
Navigation internal AI.

Need to get to a specific location? This is the thang.

"""

# utility functions
def rotate_diff(one,two):
    coord = one.coord
    q = one.quaternion
    dest = two.coord

    # this is a GOD AWFUL method of doing it
    from panda3d.core import NodePath
    foo = NodePath("foo")
    bar = NodePath("bar")

    foo.setPos(one.coord)
    bar.setPos(two.coord)
    foo.lookAt(bar)
    return tuple(foo.getQuat())
    


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

