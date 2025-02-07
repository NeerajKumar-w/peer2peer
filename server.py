import peerPackage.peer as Peer
from threading import Thread
from time import sleep

server = Peer.Peer()

thread = Thread(target= server.listener, args=(6001, ), daemon=True)
thread.start()

server.sender(6000, 7001)
