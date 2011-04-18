import sidereal.client

c = sidereal.client.Client()
c.setup()

from twisted.internet import reactor
reactor.run()
