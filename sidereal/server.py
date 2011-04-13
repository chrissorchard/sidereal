import json
import hashlib
import sys

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall

from sidereal.network import DigestDict
from sidereal.game import Gameloop

DEFAULT_PORT = 25005

class Server(object):
    def __init__(self,gamestate=None):
        # if not passed a gamestate, it'll make one of its own
        if gamestate is None:
            self.gamestate = Gamestate()

        #TODO Make it possible to change from default
        self.port = DEFAULT_PORT

        self.protocol = ServerProcotol()

    def setup(self):
        # set up our UDP listener
        from twisted.internet import reactor
        reactor.listenUDP(self.port,self.protocol)

        # set the gamestate to tick every 0.01 seconds
        self.gamestate_loop = LoopingCall(self.gamestate.kaujul_tick)
        self.gamestate_loop.start(0.01,now=True)

    def run(self):
        self.reactor.run()


class ServerProtocol(DatagramProtocol):
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
        try:
            d = json.loads(data,object_pairs_hook=DigestDict)
        except ValueError as e:
            # BAD JSON

            # TODO Complain on the log
            sys.stderr.write("Bad data: {0}".format(data))
            return

        # then verify the hash

        if not d.verify() and "verifydigest" in self.options:
            # BAD HASH

            # TODO also complain on the log
            sys.stderr.write("Bad digest: {0}".format(data))
            return

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


# we want to listen on port 25005
#reactor.listenUDP(9999, Echo())
#reactor.run()
