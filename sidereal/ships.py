import json
import logging
import code
import io

import sidereal.universe

# Basically, we may have loggers in the ship.* hierachy, but by default
# we're not going to listen to them. If you change your mind, you'll
# need to add additional handlers
_nullhandler = logging.NullHandler()
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
            myuniverse = universe

        self.id = myuniverse.get_unique_id()
        self.logger = logging.getLogger("ship.{}".format(self.id))

    @classmethod
    def create_from_json(cls, jsonstr):
        """Given a json string, builds a new Ship object, and returns it."""
        d = json.loads(jsonstr)
        code.interact("ZOMG",raw_input,locals())
        newship = cls()
        newship.__dict__.update(d)
        return newship


if __name__=='__main__':
    ship = Ship.create_from_json(_examplejson)
