import turtle
import collections
import random

def triple_float(seed,alpha=False):
    r = random.Random()
    r.seed(seed)
    if alpha:
        return r.random(), r.random(), r.random(), r.random()
    else:
        return r.random(), r.random(), r.random()


class Display(collections.MutableSet):
    def __init__(self):
        self._tracked = set()
        self._turtlemap = {}
        self._freeturtles = collections.deque()

        self.screen = turtle.Screen()
        self.screen.tracer(False)

        self.selectedaxis = (0,1)

        # The types of coordinates to display. Possible are:
        # 'coord' is x,y,z coordinates
        # 'quaternion' is the w,x,y,z rotation, and relies on the
        # objects added to the display having a .quaternion attr
        #
        # If empty, no coords of any type are printed.
        self.autocoord_display = {}

        # Method of determining turtle tilt
        # Our turtles are not actually rotated that a call to say,
        # t.fd(100) would be altered, but the angle in which they
        # appear to be pointing. Valid:
        # 'lastmovement' - The tilt is pointing in the direction in which
        # the turtle is moving
        # 'rotation' - The tilt is pointing how the tracked object is
        # pointing. Requires tracked to have a .quaternion attr
        self.tilt_type = 'lastmovement'

    def add(self,o):
        self._tracked.add(o)
        aturtle = self._new_turtle()
        x,y,z = o.coord
        aturtle.color(*triple_float(o))
        aturtle.setposition(x,y)
        aturtle.pendown()
        aturtle.just_printed_coord = False

        self._turtlemap[o] = aturtle

    def discard(self,o):
        self._tracked.discard(o)
        aturtle = self._turtlemap.pop(o)
        aturtle.clear()
        aturtle.hideturtle()
        aturtle.penup()
        # I can't work out how to get the turtle screen to cease having
        # a reference to the turtles, so instead, we'll just hide it, and
        # reuse it, if needs be.
        self._freeturtles.append(aturtle)

    def draw(self):
        for tracked,aturtle in self._turtlemap.items():
            if self.autocoord_display != {}:
                if aturtle.just_printed_coord == True:
                    aturtle.undo()
                    aturtle.just_printed_coord = False

            X,Y = self.selected_axis_components(tracked.coord)

            self.set_turtle_tilt(tracked,aturtle)
            aturtle.setposition(X,Y)

            if self.autocoord_display != {}:
                if 'coord' in self.autocoord_display:
                    self.print_tracked_coord(tracked,aturtle)
                if 'quaternion' in self.autocoord_display:
                    self.print_tracked_quaternion(tracked,aturtle)
                aturtle.just_printed_coord = True

        # after going through all the turtles, update the screen
        self.screen.update()

    def set_turtle_tilt(self,tracked,aturtle):
        X,Y = self.selected_axis_components(tracked.coord)
        if self.tilt_type == 'lastmovement':
            aturtle.settiltangle(aturtle.towards(X,Y))
        elif self.tilt_type == 'rotation':
            pass

    def print_coord(self):
        for tracked,aturtle in self._turtlemap.items():
            self.print_tracked_coord(tracked,aturtle)

    def print_tracked_coord(self,tracked,aturtle):
        x,y,z = tracked.coord
        #aturtle.write("({},{},{})".format(int(x),int(y),int(z)))
        aturtle.write("({},{},{})".format(x,y,z))

    def print_tracked_quaternion(self,tracked,aturtle):
        w,x,y,z = tracked.quaternion
        aturtle.write("({},{},{},{})".format(w,x,y,z),
                     align='left')

    def _new_turtle(self):
        # if it's empty
        if not self._freeturtles:
            aturtle = turtle.RawTurtle(self.screen)
        # else
        else:
            aturtle = self._freeturtles.pop()
        aturtle.penup()
        return aturtle
    def _jitter_all(self):
        for i in self:
            i.jitter()

    def selected_axis_components(self,coord):
        # selects the axis for x, which we'll call X, and
        # the axis for Y
        X = coord[self.selectedaxis[0]]
        Y = coord[self.selectedaxis[1]]
        return X,Y


    #boring required methods
    def __len__(self):
        return len(self._tracked)
    def __iter__(self):
        return iter(self._tracked)
    def __contains__(self,o):
        return o in self._tracked

class _Dummy(object):
    """A test object, which has a .coord attribute."""
    def __init__(self,id):
        self.id = id
    @classmethod
    def random_coord(cls,max=150):
        """ID should be set globally, since the hash (which is independent
        of the coords) is based/is that id.
        This is a test object anyway."""
        global ID
        self = cls(ID)
        ID += 1
        self.x = random.randint(0-max,max)
        self.y = random.randint(0-max,max)
        self.z = random.randint(0-max,max)
        return self
    def get_coord(self):
        return (self.x,self.y,self.z)
    def set_coord(self,coord):
        self.x, self.y, self.z = coord
    coord = property(get_coord,set_coord)
    def __hash__(self):
        return hash(self.id)
    def jitter(self,amount=25):
        self.x += random.randint(0-amount,amount)
        self.y += random.randint(0-amount,amount)
        self.z += random.randint(0-amount,amount)

if __name__=='__main__':
    ID=0
    d = Display()
    for i in range(3):
        d.add(_Dummy.random_coord())
    d.draw()
