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
        self.protocol = sidereal.network.PacketReciever(self.handler)
        self.manager = sidereal.network.PacketManager(self.protocol)
    def gamestate_wrapper(self):
        self.manager.check()
        self.gamestate.tick()

class Handler(sidereal.server.Handler):
    def __init__(self,client):
        self.client = client

        # the server.Handler method will check this variable
        self.type_action = {"snap":self.keyframe_handler}
        self.type_action = {"diff":self.diff_handler}
    def keyframe_handler(self,data,(host,port)):
        client_time = self.client.gamestate.time
        server_time = data['time']
        gamestate = self.client.gamestate


    def diff_handler(self,data,(host,port)):
        time = self.client.gamestate.time
        gamestate = self.client.gamestate

