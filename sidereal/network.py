import json
import hashlib
import struct
import warnings
import logging

from twisted.internet import protocol

from twisted.python.log import PythonLoggingObserver
_observer = PythonLoggingObserver()
_observer.start()

DEFAULT_PORT = 25005

# random network utlity classes and functions

class DigestDict(dict):
    """This is a docstring.

    This whole class is unused."""
    def digest(self):
        """This is also a docstring.

        """
        # Given a dictionary, inserts a json digest, assuming that
        # the element 'digest' contains N zeros, and it's printed
        # with indent 4, sorted
        # where N is the hash length
        warnings.warn("DigestDict is deprecated",DeprecationWarning,stacklevel=2)
        dcopy = self.copy()
        hasher = hashlib.new('md5')
        N = len(hasher.hexdigest())
        dcopy['digest'] = "0"*N

        representation = str(dcopy)
        hasher.update(representation)
        digest = hasher.hexdigest()

        self['digest'] = digest

    def verify(self):
        warnings.warn("DigestDict is deprecated",DeprecationWarning,stacklevel=2)
        our_digest = self.get('digest',None)

        dcopy = self.copy()

        hasher = hashlib.new('md5')
        N = len(hasher.hexdigest())
        dcopy['digest'] = "0"*N

        representation = str(dcopy)
        hasher.update(representation)
        their_digest = hasher.hexdigest()

        return our_digest == their_digest
    def __str__(self):
        return json.dumps(self,sort_keys=True,indent=4)
    def __repr__(self):
        return json.dumps(self,sort_keys=True)

class BadDigest(Exception):
    pass

class BadLength(Exception):
    pass

class PseudoHeader(object):
    """
    our header consists of:

    unsigned short - sequence number
    16 byte string - md5 hash
    unsigned short - flags
    unsigned short - length of packet, header + payload
    """
    format = ">H16sBH"
    length = struct.calcsize(format)

    @classmethod
    def calculate(cls,data,sequence=0,flagnum=0):
        # data should be a string, otherwise, convert it
        data = str(data)

        length = cls.length + len(data)

        packet = struct.pack(cls.format,sequence,"0"*16,flagnum,length)
        hasher = hashlib.md5()
        hasher.update(packet)
        hash = hasher.digest()

        return struct.pack(cls.format,sequence,hash,flagnum,length) + data

    @classmethod
    def unpack(cls,data,check_hash=True):
        # given a packet, check that its length, and hash are true
        sequence,hash,flags,length = struct.unpack(cls.format,data[:cls.length])

        if len(data) != length:
            raise BadLength("Packet specifies a size of {0}, we got {1}.".format(length,len(data)))

        if check_hash:
            verify_packet = struct.pack(cls.format,sequence,"0"*16,flags,length)
            hasher = hashlib.md5()
            hasher.update(verify_packet)
            our_hash = hasher.digest()

            if hash != our_hash:
                raise BadDigest

        return sequence,hash,flags,length,data[cls.length:]
    @classmethod
    def pretty(cls,data):
        sequence,hash,flags,length,data = cls.unpack(data,True)
        return "Sequence:{0},Flags:{1},Length:{2},Data:{3}".format(sequence,flags,length,data.strip("\n"))

calculate_packet = PseudoHeader.calculate
unpack_packet = PseudoHeader.unpack
pretty_packet = PseudoHeader.pretty

# packet handler
class PacketReciever(protocol.DatagramProtocol):
    def __init__(self,handler):
        """handler - has to have a .handle method"""
        self.handler = handler

    def datagramReceived(self, datagram, (host,port)):
        try:
            sequence,hash,flags,length,data = unpack_packet(datagram)
            logging.debug(pretty_packet(datagram))
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
        if "ACK" not in flag_unpack(flags):
            ack_packet = self.create_ack(sequence)
            self.transport.write(ack_packet,(host,port))

        self.handler.handle(message,(host,port),sequence,flags)
    def create_ack(self,sequence):
        ackflag = flag_pack(['ACK'])
        return calculate_packet("{}",sequence,ackflag)

class PacketManager(object):
    def __init__(self,protocol):
        self.protocol = protocol
        # Mapping sequence to sent packets
        # Keeps tracks of packets that have been sent, but not ACK'd
        self.sent_packets = {}
        self._sequence = 0
    def next_sequence(self):
        seq = self._sequence
        self._sequence += 1
        self._sequence %= 2**16
        return seq
    def send_packet(self,data,(host,port)):
        j = json.dumps(data)
        seq = self.next_sequence()
        packet = calculate_packet(j+"\n",seq)
        size = len(packet)
        if size > 512:
            logging.warning("Packet sent of size {0}".format(size))
        self.sent_packets[seq] = [packet,0]
        self.protocol.transport.write(packet,(host,port))
    def ack_packet(self,sequence):
        if sequence in self.sent_packets:
            del self.sent_packets[sequence]
        else:
            logging.warning("WTF, {0} isn't a packet we've sent".format(sequence))
    def check(self):
        """Check that we've been replied to."""
        # FIXME Temporary fix for unacked. we will retrnsmit them
        # eventually.
        remove = set()
        for sequence,packetcount in self.sent_packets.items():
            packetcount[1] += 1
            if packetcount[1] > TOO_LONG:
                pretty = pretty_packet(packetcount[0])
                logging.warning("unacknowledged packet: {0}".format(pretty))
                remove.add(sequence)
        while remove:
            item = remove.pop()
            del self.sent_packets[item]

TOO_LONG = 1000

class Handler(object):
    def __init__(self):
        self.type_action = {}
        self.flag_handler = {}

    def handle(self,data,(host,port),sequence=0,flags=0):
        flagset = flag_unpack(flags)
        for flag in flagset:
            if flag in self.flag_handler:
                self.flag_handler[flag](data,(host,port),sequence,flags)

        # Assuming data is a dictionary type object.
        type = data.get('type',None)
        if type in self.type_action:
            # call our type with data, (host,port) as arguments
            self.type_action[type](data,(host,port))
        elif type is not None:
            logging.warning("No action found for packet type: {0}".format(type))
            #TODO replace with Twisted failure?
            #return False
    def do_debug(self,data,(host,port)):
        # An optional debug handler. Can be added like any other handler
        action = data.get('action',None)
        if action is None:
            return
        elif action == "gc":
            # We'll burn this city down; manual garbarge collection GO
            from gc import collect
            collect()



# flag variables
# We have a byte's worth, so that's 8 flags, so 128 is our highest.
flags = {}
flags['ACK'] = 1
# 2
# 4
# 8
flags['RAINBOW'] = 16
# 32
# 64
flags['AWESOME'] = 128

def flag_unpack(i):
    """given an integer, return a set of keys"""
    keys = set()
    for flag,value in flags.items():
        if i & value == value:
            keys.add(flag)
    return keys

def flag_pack(s):
    """given a set, or something that supports .pop()
    returns an integer"""
    value = 0
    while s:
        flag = s.pop()
        if flag in flags:
            value = value | flags[flag]
    return value
