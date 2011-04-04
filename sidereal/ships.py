import json
import logging
import code
import io

import sidereal.universe

# Basically, we may have loggers in the ship.* hierachy, but by default
# we're not going to listen to them. If you change your mind, you'll
# need to add additional handlers
try:
    _nullhandler = logging.NullHandler()
except AttributeError:
    class _NullHandler(logging.Handler):
        def emit(self, record):
            pass
    _nullhandler = _NullHandler()

logging.getLogger("ship").addHandler(_nullhandler)

# This is the example configuration for an example ship
# Most of these stats may or may not make any sense as we work
# on the physics system. But it should indicate the vague feel of it
_exampleconfiguration = {
    "classname":"Striker",
    "race":["foobeings","barbeings"],
    "mass":5000,
    "engines":[
        {"placement":(10,-50,0),
         "thrust":2000,
         "warmuptime":10,
        },
        {"placement":(-10,-50,0),
         "thrust":2000,
         "warmuptime":10,
        }
    ],
    "guns":[
        {"type":"massdriver",
         "mass":5,
         "damage":50
        }
    ],
    "navlights":[(25,0,25),(-25,0,25)],
}
_examplejson = json.dumps(_exampleconfiguration)


class Ship(object):
    """The basic core ship class in Sidereal."""
    def __init__(self,myuniverse=None):
        if myuniverse is None:
            # If we haven't been passed an instance of the universe
            # use the module's already instantiated instance
            myuniverse = sidereal.universe

        self.id = myuniverse.get_unique_id(self)
        self.logger = logging.getLogger("ship.{0}".format(self.id))

    @classmethod
    def create_from_json(cls, jsonstr):
        """Given a json string, builds a new Ship object, and returns it."""
        d = json.loads(jsonstr)
        newship = cls()
        newship.__dict__.update(d)
        return newship

    def __hash__(self):
        return hash(self.id)
    def __repr__(self):
        return "<Ship (id={})>".format(self.id)

class PhysicsShip(Ship):
    def __init__(self,physics,myuniverse=None):
        Ship.__init__(self,myuniverse)
        self.physics = physics
    @classmethod
    def create_from_json(cls, jsonstr, physics):
        ship = super(Ship,cls).create_from_json(jsonstr)
        ship.physics = physics

        return ship

    @property
    def coord(self):
        return self.physics.coord
    @property
    def quaternion(self):
        return self.physics.quaternion

    

if __name__=='__main__':
    ship = Ship.create_from_json(_examplejson)
