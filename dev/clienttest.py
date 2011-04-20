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
    def __init__(self,client,(host,port)):
        self.client = client
        self.host,self.port = (host,port)
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
            self.client.manager.send_packet(j,(self.host,self.port))


stdio.StandardIO(StdinInput(c,(HOST,PORT)))

from twisted.internet import reactor
reactor.run()
