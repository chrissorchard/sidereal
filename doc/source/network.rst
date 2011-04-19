Networking
==========

It's amazing, I know.

Packet Specification
--------------------

With an attached psuedo header, packets currently consist of a JSON object.

Except for special packets, the JSON has a field called "type".
Various types are sent by the client and server.

Clients currently send:
 * knock - Packets for saying "HAI CAN I COME TO THE PARTY?"
 * stop - A leave request, which means the server stops sending the
   client stuff.

Servers currently send:
 * snap - A snapshot of a specific object, generally sent all at once to
   constitute a "keyframe" a snapshot of the whole world state at any
   one time.
 * diff - A "diff" of a particular object, which contains a subset of
   the object's traits which should be updated.

The server packets have the following attributes:
 * id - The id of the object that the packet describes; every in game
   world object has a unique id within a particular session/universe.
 * time - The universal time. When the world "ticks" and all the physics
   is updated, and the AI reevalutes, and turrets decide whether to
   shoot or not, this time is incremented. Since the client and server
   will almost (except for perfect conditions, and even then) never be
   in perfect step, it is important to timestamp any changes to an
   object.

An ACK packet has an empty JSON object, the sequence number set to the
packet it is replying to, and (unsurpringly) the ACK flag set.

Current Flags
-------------

 * ACK (1) - This packet is an acknowledge packet.

Unused Flags
------------
 * RAINBOW (16) - This packet has a rainbow flag, and is thus proud.
 * AWESOME (128) - This packet is awesome.

.. automodule:: sidereal.network
    :members:
    :undoc-members:
