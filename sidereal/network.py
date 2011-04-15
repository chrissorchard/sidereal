import json
import hashlib
import struct
import warnings

from twisted.internet import protocol

DEFAULT_PORT = 25005

# random network utlity classes and functions

class DigestDict(dict):
    def digest(self):
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
    format = ">H16sBH"
    length = struct.calcsize(format)
    """
    our header consists of:

    unsigned short - sequence number
    16 byte string - md5 hash
    unsigned short - flags
    unsigned short - length of packet, header + payload
    """

    @classmethod
    def calculate(cls,data,sequence=0,**kwargs):
        # data should be a string, otherwise, convert it
        data = str(data)

        # do flags
        flags = 0 | 1 | 4

        length = cls.length + len(data)

        packet = struct.pack(cls.format,sequence,"0"*16,flags,length)
        hasher = hashlib.md5()
        hasher.update(packet)
        hash = hasher.digest()

        return struct.pack(cls.format,sequence,hash,flags,length) + data

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

calculate_packet = PseudoHeader.calculate
unpack_packet = PseudoHeader.unpack

# packet handler
class PacketReciever(protocol.DatagramProtocol):
    def __init__(self,handler):
        # has to have a .handle method
        self.handler = handler

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
        self.handler.handle(message,(host,port))


# flag variables
# We have a byte's worth, so that's 8 flags, so 128 is our highest.
flags = {}
flags['ACK'] = 1
# 2
# 4
# 8
# 16
# 32
# 64
flags['AWESOME'] = 128

def flag_unpack(i):
    # given an integer, return a set of keys
    keys = set()
    for flag,value in flags.items():
        if i & value == value:
            keys.add(flag)
    return keys

def flag_pack(s):
    # given a set, or something that support "in"
    # returns an integer
    value = 0
    while s:
        flag = s.pop()
        if flag in flags:
            value = value | flags[flag]
    return value
