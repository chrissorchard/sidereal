import json
import hashlib
import sys

from twisted.internet import protocol
from twisted.internet.task import LoopingCall

from sidereal.network import (BadDigest, BadLength,
                              calculate_packet, unpack_packet)

import sidereal.network
import sidereal.server
import sidereal.game

class Client(object):
    def __init__(self):
        self.gamestate = sidereal.game.Gamestate()
        # empty gamestate

        self.port = sidereal.network.DEFAULT_PORT
        self.handler = Handler()

class Handler(sidereal.server.Handler):
    def __init__(self,client):
        self.client = client

        # the server.Handler method will check this variable
        self.type_action = {}

