import os
import logging
import json
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

        # of course, we're loading this data, when we're about to
        # dump it in a second.
        try:
            j = json.loads(line)
        except ValueError as e:
            logging.warning(e)
        else:
            c.manager.send_packet(j,(HOST,PORT))


stdio.StandardIO(StdinInput())

from twisted.internet import reactor
reactor.run()
