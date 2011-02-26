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
    @property
    def orientation(self):
        return self.body.getOrientation()

class FlightHelper(list):
    """Given a sequence of waypoints, the FlightHelper will call
    the methods of the PhysicsCompenent in the appropriate strength
    and direction, to move the object towards the waypoint
    (possibly, preparing for the waypoint after that.
    
    """
    def __init__(self):
        list.__init__(self)
    def tick(self,ship):
        # This method should be called on each Physics tick

        # Do we have any waypoints? If not, then return
        if len(self) == 0:
            return
        
        # Given the waypoint at the beginning of the list
        waypoint = self[0] 
        
        # Determine what we have to do to orient ourselves towards
        # this waypoint.

        # Are we spinning enough?

        # Are we spinning too much?

        # Are we spinning just right?

        # Use any methods of rotation that we have. Some may be more
        # extreme than others, which we only use in life or death situations

        # If we're pointing towards it enough, then fire the relevent
        # or whatever mechanism we use for movement

        # But don't go too fast, because we have to slow down. We could
        # go fast in case of an emergency.

        # It's likely that different set of methods will have to be used
        # for a ship that doesn't use rear engines + gimal or rotation
        # thrusters
    def fire_all_engines(self,ship):
        # Try our best to determine where the placement of
        # the engines on the ship are.

        # For a placeholder, apply the maximum given thrust, (divded by 60) in the
        # direction of our orientation.
        # pchooooo >[ ]
        totalthrust = 0
        for engine in ship.engines:
            totalthrust += engine['thrust']


