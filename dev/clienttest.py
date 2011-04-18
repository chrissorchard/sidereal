import os
import logging
logging.basicConfig(level=logging.DEBUG)
import sidereal.client

c = sidereal.client.Client()
c.setup()

from twisted.internet import stdio, protocol
from twisted.protocols import basic

HOST,PORT = "127.0.0.1",25005

class StdinInput(basic.LineReceiver):
    delimiter = os.linesep

    def connectionMade(self):
        pass
    def lineReceived(self, line):
        # The dude typed a line. Send it.
        c.manager.send_packet(line,(HOST,PORT))

stdio.StandardIO(StdinInput())

from twisted.internet import reactor
reactor.run()
