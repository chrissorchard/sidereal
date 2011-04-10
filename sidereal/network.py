import json
import hashlib

# random network utlity classes and functions

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
