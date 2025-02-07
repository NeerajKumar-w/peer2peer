import socket
import asyncio

class Peer:
    def __init__(self, lport, sport, dport) -> None:
        self.lport = lport
        self.sport = sport
        self.dport = dport
        self.queue = asyncio.Queue()
        self.recieved = []
        
    def broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_ip = "255.255.255.255"
        port = 5000
        message = "Sender"
        sock.sendto(message.encode(), (broadcast_ip, port))
        print(f"Message {message} send to {broadcast_ip}:{port}")
        sock.close()
 
    def listener(self):
        server_ip = "127.0.0.1"
        server_port = self.lport
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((server_ip, server_port))
        try:
            while True:
                print("waiting for data")
                data, _ = sock.recvfrom(1024)
                yield data.decode()
        except KeyboardInterrupt:
            print("\nListener Stopped")
        finally:
            sock.close()

    def send(self, message):
        server_ip = "127.0.0.1"
        server_port = self.sport
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((server_ip, server_port))
        try:
            sock.sendto(message.encode("utf-8"), ("127.0.0.1", self.dport))
        except KeyboardInterrupt:
            print("\nSenderStopped")
        finally:
            sock.close()
