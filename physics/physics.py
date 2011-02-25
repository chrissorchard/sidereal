import sys
import os
import collections

import bullet.bullet as bullet

class PhysicsComponent(object):
    """Contains physical data for an ingame object, and actually modifies
    torque and position."""
    def __init__(self,body):
        #given a ridgid body, store a reference to it
        self.body = body
    def apply_force(self,force,relpos=None):
    """Apply force to the object. For a ship, this should only be in the
    appropriate direction that makes sense for the engines, and NOT
    arbitrary."""
        if relpos is None:
            self.body.applyCentralForce(force)
        else:
            self.body.applyForce(force,relpos)

class FlightHelper(list):
    """Given a sequence of waypoints, the FlightHelper will call
    the methods of the PhysicsCompenent in the appropriate strength
    and direction, to move the object towards the waypoint
    (possibly, preparing for the waypoint after that.
    
    """
    def __init__(self):
        super().__init__(self)
        
