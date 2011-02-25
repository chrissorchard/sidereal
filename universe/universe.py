"""The universe in sidereal is the game space, it is the space
in which all ingame object occupy. It should keep track of all in-game
related objects, such as ships, explosions, projectiles, and so on, or be
able to keep track of them on demand."""

__all__ = ["Universe","foo","bar","get_unique_id"]

class Universe(object):
    def __init__(self):
        self._id = 0
    def foo(self):
        pass
    def bar(self):
        pass
    def get_unique_id(self):
        id = self._id
        self.id += 1
        return id

# inspired by python's random module, create one instance, and export its
# functions as module-level functions. The user can create their own
# Universe() instance if they like
_inst = Universe()
foo = _inst.foo
bar = _inst.bar
get_unique_id = _inst.get_unique_id
