"""The universe in sidereal is the game space, it is the space
in which all ingame object occupy. It should keep track of all in-game
related objects, such as ships, explosions, projectiles, and so on, or be
able to keep track of them on demand."""

import logging

# A gasau is an ingame object or agent.

# Basically, we may have loggers in the gasau.* hierachy, but by default
# we're not going to listen to them. If you change your mind, you'll
# need to add additional handlers

# Make us compatible with python2.6
try:
    _nullhandler = logging.NullHandler()
except AttributeError:
    class _NullHandler(logging.Handler):
        def emit(self, record):
            pass
    _nullhandler = _NullHandler()

logging.getLogger("gasau").addHandler(_nullhandler)


__all__ = ["Universe","id","logger"]

class Universe(object):
    def __init__(self):
        self._id = 0
    def id(self):
        """Returns a unique id.
        """
        id = self._id
        self._id += 1
        return id
    def logger(self,id):
        """Returns a logger for the specified id"""
        return logging.getLogger("gasau.{0}".format(id))

# inspired by python's random module, create one instance, and export its
# functions as module-level functions. The user can create their own
# Universe() instance if they like
_inst = Universe()
id = _inst.id
logger = _inst.logger
