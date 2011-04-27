import os
import logging
import json
logging.basicConfig(level=logging.DEBUG)
import sidereal.client
import sidereal.network

c = sidereal.client.Client()
c.setup()

from twisted.internet import stdio, protocol
from twisted.protocols import basic

HOST,PORT = "127.0.0.1",25005

input = sidereal.network.StdinInput(c,(HOST,PORT))
stdio.StandardIO(sidereal.network.StdinInput(c,(HOST,PORT)))

from twisted.internet import reactor
reactor.run()
