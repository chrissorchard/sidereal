import json
import hashlib
import sys

from twisted.internet.protocol import DatagramProtocol

class DigestDict(dict):
    def digest(self):
        # Given a dictionary, inserts a json digest, assuming that
        # the element 'digest' contains N zeros, and it's printed
        # with indent 4, sorted
        # where N is the hash length
        dcopy = self.copy()
        hasher = hashlib.new('md5')
        N = len(hasher.hexdigest())
        dcopy['digest'] = "0"*N
        
        representation = json.dumps(dcopy,sort_keys=True,indent=4)
        hasher.update(representation)
        digest = hasher.hexdigest()

        self['digest'] = digest

    def verify(self):
        our_digest = self.get('digest',None)

        dcopy = self.copy()

        hasher = hashlib.new('md5')
        N = len(hasher.hexdigest())
        dcopy['digest'] = "0"*N
        
        representation = json.dumps(dcopy,sort_keys=True,indent=4)
        hasher.update(representation)
        their_digest = hasher.hexdigest()

        return our_digest == their_digest


class Server(object):
    port = 25005

    def setup(self):
        from twisted.internet import reactor
        self.reactor = reactor
        reactor.listenUDP(self.port,Protocol())

    def run(self):
        self.reactor.run()

class Protocol(DatagramProtocol):
    def __init__(self):
        self.clients = {}

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

        if not d.verify():
            # BAD HASH

            # TODO also complain on the log
            sys.stderr.write("Bad digest: {0}".format(data))
            return

        print "DO STUFF"

        print "received %r from %s:%d" % (data, host, port)
        #self.transport.write(data, (host, port))

# we want to listen on port 25005
#reactor.listenUDP(9999, Echo())
#reactor.run()
