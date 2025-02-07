import peerPackage.peer as peer
from threading import Thread
from time import sleep


server = peer.Peer()

thread = Thread(target=server.listener, args=(7001,), daemon=True)
thread.start()

server.sender(7000, 6001)
