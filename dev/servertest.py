import sidereal.server

s = sidereal.server.Server()
s.setup()

import sidereal.universe as universe
import sidereal.physics as physics

gasau = universe.id()
s.gamestate._physics[gasau] = body = physics.Body(s.gamestate._world)
body.velocity = 0,1,0

from twisted.internet import reactor
reactor.run()
