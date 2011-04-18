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
import sidereal.physics

class Client(object):
    def __init__(self):
        self.gamestate = sidereal.game.Gamestate()
        # empty gamestate

        self.port = sidereal.network.DEFAULT_PORT
        self.handler = Handler(self)
        self.protocol = sidereal.network.PacketReciever(self.handler)
        self.manager = sidereal.network.PacketManager(self.protocol)
    def setup(self):
        from twisted.internet import reactor
        reactor.listenUDP(0,self.protocol)

        self.gamestate_loop = LoopingCall(self.gamestate_wrapper)
        self.gamestate_loop.start(0.01,now=False)
    def gamestate_wrapper(self):
        self.manager.check()
        self.gamestate.tick()

class Handler(sidereal.network.Handler):
    def __init__(self,client):
        sidereal.network.Handler.__init__(self)
        self.client = client

        # the server.Handler method will check this variable
        self.type_action = {"snap":self.keyframe_handler}
        self.type_action = {"diff":self.diff_handler}

        self.flag_handler['ACK'] = self.handle_ack
    def keyframe_handler(self,data,(host,port)):
        # FIXME Currently unused  #
        client_time = self.client.gamestate.time
        server_time = data['time']
        #-------------------------#

        gamestate = self.client.gamestate

        id = data['id']
        snapshot = BodySnapshot(data['snapshot'])

        body = gamestate.get_body(id)
        logger.debug(body.snapshot)
        body.unsnapshot(snapshot)

    # UGGGH repeated code
    def handle_ack(self,data,(host,port),sequence,flags):
        self.client.manager.ack_packet(sequence)

    def diff_handler(self,data,(host,port)):
        time = self.client.gamestate.time
        gamestate = self.client.gamestate

