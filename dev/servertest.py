import sidereal.server

s = sidereal.server.Server(debug=True)
s.setup()

import sidereal.universe as universe
import sidereal.physics as physics

def new(velocity=(0,1,0)):
    gasau = universe.id()
    body = s.gamestate.new_body(gasau)
    body.velocity = velocity

new()

from twisted.internet import reactor
reactor.callLater(4,new,(3,-4,7))
reactor.callLater(8,new,(9,-1.5,3))
reactor.run()
