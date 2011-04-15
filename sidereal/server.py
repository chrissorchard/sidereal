import json
import hashlib
import sys

from twisted.internet import protocol
from twisted.internet.task import LoopingCall

from sidereal.network import (DigestDict, BadDigest, BadLength,
                              calculate_packet, unpack_packet)
import sidereal.game

DEFAULT_PORT = 25005

class Server(object):
    def __init__(self,gamestate=None):
        # if not passed a gamestate, it'll make one of its own
        if gamestate is None:
            self.gamestate = sidereal.game.Gamestate()

        #TODO Make it possible to change from default
        self.port = DEFAULT_PORT

        self.protocol = JoinNotifier(self)

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
    def gamestate_wrapper(self):
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
                    m = calculate_packet(json.dumps(snapmessage) + "\n")
                    self.protocol.transport.write(m,(host,port))
            elif not diff_empty:
                # send a diff
                m = calculate_packet(json.dumps(diffmessage) + "\n")
                self.protocol.transport.write(m,(host,port))

class JoinNotifier(protocol.DatagramProtocol):
    def __init__(self,server):
        self.server = server

    def datagramReceived(self, datagram, (host,port)):
        try:
            sequence,hash,flags,length,data = unpack_packet(datagram)
            message = json.loads(data)
        except BadLength as e:
            print e
            return
        except BadDigest as e:
            print e
            return
        except ValueError as e:
            print e
            return

        if message.get('type',None) == 'knock':
            self.server.add_client((host,port))

        elif message.get('type',None) == 'stop':
            # discard means, remove if present
            self.server.clients.discard((host,port))
        else:
            print "Unrecognised message: " + repr(message)


class ServerProtocol(protocol.DatagramProtocol):
    def __init__(self,server):
        self.clients = {}
        self.server = server

        # normal options
        #self.options = set(["verifydigest","stoprepeatjoins"])

        # debug options
        self.options = set(["stoprepeatjoins"])

        # FIXME THIS IS A DEBUG VALUE
        self.player_slots = set([1,2,3,4])

    def datagramReceived(self, data, (host, port)):
        # all of our data is in JSON.

        self.process_message(d,(host,port))

    def process_message(self,d,(host,port)):
        type = d['type']
        message = DigestDict()

        if type == "knock":
            # start crafting response
            message['type'] = 'knock-response'


            # check for game full
            if len(self.player_slots) == 0:
                # GAME IS FULL.
                # Rejected.

                message['answer'] = False
                message['message'] = "Game is full."

            elif (host,port) in self.clients and "stoprepeatjoins" in self.options:
                message['answer'] = False
                message['message'] = "You're already in the game."

            else:
                request = d.get('player_request',None)
                if request in self.player_slots:
                    self.player_slots.remove(request)
                    assigned = request
                else:
                    assigned = self.player_slots.pop()

                self.clients[(host,port)] = assigned

                message['answer'] = True
                message['slot'] = assigned

                # Maybe later we can give them "tokens"
                # so if they rejoin under a different ip, or just again
                # it goes: OH WAIT, UR PLAYER 6, LET ME FIX THAT
                from twisted.internet import reactor
                reactor.callWhenRunning(self.check_for_full)

        if message:
            message.digest()
            jmessage = json.dumps(message)
            self.transport.write(jmessage, (host,port))

    def check_for_full(self):
        if len(self.player_slots) == 0:
            # craft our global message
            message = DigestDict()
            message['type'] = 'start game'
            message.digest()
            for (host,port),playerid in self.clients.items():
                personalised = message.copy()
                personalised['slot'] = playerid
                self.transport.write(json.dumps(personalised),(host,port))

def process_message(m):
    data = json.loads(m,object_pairs_hook=DigestDict)
    # could throw a ValueError for bad JSON

    # then verify the hash

    # Set to False, to disable digest verify
    DEBUG_verify = False #FIXME
    # The fixme is so we'll remember to change this back.
    if DEBUG_verify and not data.verify():
        raise BadDigest("Bad digest for message: {0}".format(repr(data)))

    return data

def create_digests(snap_or_diff):
    digests = []
    for id,physics in snap_or_diff:
        snapmessage['id'] = id
        snapmessage['physics'] = physics



# we want to listen on port 25005
#reactor.listenUDP(9999, Echo())
#reactor.run()
