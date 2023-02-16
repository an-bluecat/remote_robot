# Python program to implement server of controller software
import socket
from typing import Optional
from .protocol import NetworkCommands


""" A Server Class on Raspberry PI to Receive Commands for Vehicle
"""
class PI_ServerManager():
    def __init__(self, port: int, command: NetworkCommands, message=True):
        self.port = port
        self.connection: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server    : socket = None
        self.clientAddr = None
        self.connected  = False
        self.localIP    = self.__getLocalIP()
        self.commands   = command.functionWrapper
        self.__message  = message

        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((self.localIP, self.port))
        self.connection.listen(1)                                       #Listens for only One connection
        if (self.__message): print("[PI_Server] listening on local IP:", self.localIP, "port", self.port)

    def connect(self) -> bool:                                          #Establish a Server Connection
        self.server, self.clientAddr = self.connection.accept()
        self.connected = (self.server and self.clientAddr)
        if (self.__message): print("[PI_Server] client connected at:", self.clientAddr,
                                   " [SUCCESS]" if self.connected else " [FAILED]")
        return self.connected

    def receive(self) -> Optional[str]:                                 #Receive Valid Commands
        if (not self.connected): return None
        data = self.server.recv(32).decode()
        if (not data): return None
        valid = data.split(";")[0] in self.commands
        self.server.send(("ACK" if valid else "NACK").encode("UTF-8"))
        if (self.__message): print("[PI_Server] data received:", data, " [VALID]" if valid else " [INVALID]")
        return data

    @staticmethod
    def __getLocalIP():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]