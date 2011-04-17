"""
Since netcat isn't sufficent for our purposes, since we want to verify all
of our packets recieved, this is writing our own. It uses UDP.

"""

import os
import argparse
import time
import json

from twisted.internet import stdio, protocol
from twisted.protocols import basic
import sidereal.network
from sidereal.network import (calculate_packet, unpack_packet,
                              BadLength, BadDigest)

class StdinInput(basic.LineReceiver):
    delimiter = os.linesep

    def connectionMade(self):
        pass
    def lineReceived(self, line):
        # The dude typed a line. Send it.
        conn.transport.write(calculate_packet(line),(HOST,PORT))

class Handler(sidereal.network.Handler):
    def __init__(self):
        sidereal.network.Handler.__init__(self)

        self.type_action['heartbeat'] = self.check_beat
    def check_beat(self,data,(host,port)):
        timediff = time.time() - data.get("time",0)
        print "Difference of {} seconds.".format(timediff)


class Connection(protocol.DatagramProtocol):

    def datagramReceived(self, payload, (host,port)):
        try:
            sequence,hash,flags,length,data = unpack_packet(payload)
        except BadDigest as e:
            print e
            return
        except BadLength as e:
            print e
            return

        print "Sequence:{},Flags:{},Length:{},Data:{}".format(sequence,flags,length,data.strip("\n"))
        ackflag = sidereal.network.flag_pack(["ACK"])
        self.transport.write(calculate_packet("{}",sequence,ackflag),(host,port))
        handler.handle(json.loads(data),(host,port),sequence,flags)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('HOST',default='127.0.0.1',nargs='?')
    parser.add_argument('PORT',type=int,default=25005,nargs='?')
    args = parser.parse_args()

    global HOST
    global PORT
    HOST = args.HOST
    PORT = args.PORT

    textinput = StdinInput()
    conn = Connection()
    handler = Handler()

    stdio.StandardIO(textinput)

    from twisted.internet import reactor
    reactor.listenUDP(0,conn)
    reactor.run()
