import json
import hashlib
import sys
import collections
import time

from twisted.internet import protocol
from twisted.internet.task import LoopingCall

import sidereal.network
from sidereal.network import (DigestDict, BadDigest, BadLength,
                              calculate_packet, unpack_packet)
import sidereal.game

TOO_LONG = 1000

class Handler(sidereal.network.Handler):
    def __init__(self,server):
        sidereal.network.Handler.__init__(self)
        self.server = server

        self.type_action['knock'] = self.do_knock
        self.type_action['stop'] = self.do_stop

        self.flag_handler['ACK'] = self.handle_ack

    def handle_ack(self,data,(host,port),sequence,flags):
        # This isn't a normal packet, it's an ACK.
        # The sequence number is the packet it is a reply to.
        self.server.manager.ack_packet(sequence)

    def do_knock(self,data,(host,port)):
        self.server.add_client((host,port))

    def do_stop(self,data,(host,port)):
        self.server.clients.discard((host,port))

class Server(object):
    def __init__(self,gamestate=None):
        # if not passed a gamestate, it'll make one of its own
        if gamestate is None:
            self.gamestate = sidereal.game.Gamestate()

        #TODO Make it possible to change from default
        self.port = sidereal.network.DEFAULT_PORT

        self.handler = Handler(self)
        self.protocol = sidereal.network.PacketReciever(self.handler)
        self.manager = sidereal.network.PacketManager(self.protocol)

        self.clients = set()
        self.unsynced = set()

    def add_client(self,(host,port)):
        self.clients.add((host,port))
        self.unsynced.add((host,port))

    def setup(self):
        # set up our UDP listener
        from twisted.internet import reactor
        reactor.listenUDP(self.port,self.protocol)

        # set the gamestate to tick every 0.01 seconds
        self.gamestate_loop = LoopingCall(self.gamestate_wrapper)
        self.gamestate_loop.start(0.01,now=False)

        self.heartbeat_loop = LoopingCall(self.heartbeat)
        self.heartbeat_loop.start(2,now=False)

    def gamestate_wrapper(self):
        # First of all, increment the sent packets.
        self.manager.check()

        # Either, everyone gets a snapshot/keyframe,
        # or only the unsynced ones get them, and everyone else
        # gets a diff
        diff = self.gamestate.tick()

        diff_empty = len(diff) == 0

        # Is it time for a keyframe?
        keyframe_time = self.gamestate.time % 1000 == 0

        snapshot = self.gamestate.physics_snapshot()

        prepare_snapshot = keyframe_time or (len(self.unsynced) != 0)

        if prepare_snapshot:
            snapshot = self.gamestate.physics_snapshot()
            snapmessages = []
            for id,physics in snapshot.items():
                snapmessage = DigestDict()
                snapmessage['type'] = 'snap'
                snapmessage['id'] = id
                snapmessage['time'] = self.gamestate.time
                snapmessage['snapshot'] = physics
                snapmessages.append(snapmessage)

        if not keyframe_time and not diff_empty:
            diffmessage = {}
            diffmessage['diff'] = diff
            diffmessage['time'] = self.gamestate.time

        for host,port in self.clients:
            unsynced = (host,port) in self.unsynced

            if keyframe_time or unsynced:
                if unsynced:
                    self.unsynced.remove((host,port))
                # transmit the snapshot
                for snapmessage in snapmessages:
                    self.manager.send_packet(snapmessage,(host,port))
            elif not diff_empty:
                # send a diff
                self.manager.send_packet(diffmessage,(host,port))
    def heartbeat(self):
        for host,port in self.clients:
            packet = {'type':'heartbeat','time':time.time()}
            self.manager.send_packet(packet,(host,port))
