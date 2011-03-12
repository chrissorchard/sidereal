import turtle
import collections
import random

def triple_float(seed):
    r = random.Random()
    r.seed(seed)
    return r.random(), r.random(), r.random()

class Display(collections.MutableSet):
    def __init__(self):
        self._tracked = set()
        self._turtlemap = {}
        self._freeturtles = collections.deque()

        self.screen = turtle.Screen()
        self.screen.tracer(False)

        self.autocoord = False

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
            if self.autocoord == True:
                if aturtle.just_printed_coord == True:
                    aturtle.undo()
                    aturtle.just_printed_coord = False

            x,y,z = tracked.coord
            aturtle.settiltangle(aturtle.towards(x,y))
            aturtle.setposition(x,y)

            if self.autocoord == True:
                self.print_tracked_coord(tracked,aturtle)
                aturtle.just_printed_coord = True

        # after going through all the turtles, update the screen
        self.screen.update()
    def print_coord(self):
        for tracked,aturtle in self._turtlemap.items():
            self.print_tracked_coord(tracked,aturtle)

    def print_tracked_coord(self,tracked,aturtle):
        x,y,z = tracked.coord
        aturtle.write("({},{},{})".format(int(x),int(y),int(z)))

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
