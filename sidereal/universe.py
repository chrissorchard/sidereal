"""The universe in sidereal is the game space, it is the space
in which all ingame object occupy. It should keep track of all in-game
related objects, such as ships, explosions, projectiles, and so on, or be
able to keep track of them on demand."""

import weakref

__all__ = ["Universe","get_unique_id"]

class Universe(object):
    def __init__(self):
        self._id = 0
        self.idmap = weakref.WeakValueDictionary()
    def get_unique_id(self,obj):
        """An object calls this method, passing a reference to itself,
        and is returned a unique integer, which will uniquely identify
        it.
        """
        id = self._id
        self._id += 1
        self.idmap[id] = obj
        return id

# inspired by python's random module, create one instance, and export its
# functions as module-level functions. The user can create their own
# Universe() instance if they like
_inst = Universe()
get_unique_id = _inst.get_unique_id
