===================
The Basic Game Loop
===================

For a moment, let us put aside the initalisation, and all the storyline, and
other things. Let's go through the process on each game "tick", from the
perspective of everything. The process of rendering the frames, and calculating
the position of ingame objects may be split between the client and server, and
may indeed happen at different rates.

------------------
Things to Consider
------------------
It seems likely that the game "ticks" at the same rate as the framerate, or
there'll be some sort of organic process that adjusts these things.

Bullet, has an "internal rate" of 60Hz, any faster than that, and it just starts
returning interpolated results.

On the client side:
 - The screen is redrawn, using magical graphics foo.
 - Orders are sent to the server.
 - The UI may change, the camera may move. Camera stuff is probably done client
   side?

On the server side:
 - For each game object, it's new position and orientation is calcuated with the
   underlying physics library.
 - We check for collisions, which generally involves exploding death in most
   cases for at least one, if not both partipants. Things are damaged or
   destroyed. This includes stuff in radioactive clouds, in theory, since
   objects within them are "colliding" with their space.
 - Clientside orders are assigned to relevant game objects.
 - The AI components run their checks, to see if they can issue any new
   autonomous orders, or issue any emergency orders (ie .avoiding collisions).
 - The waypoint calculating systems calculate waypoints for the orders, and pass
   them to the FlightHelpers.
 - The FlightHelpers, on their tick, then calculate how to spin their
   respective game objects, and make calls to their PhysicsComponents, which
   then bothers the physics library.
