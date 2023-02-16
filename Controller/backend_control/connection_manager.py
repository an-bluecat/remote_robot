import socket
from ..communication import server_utilities as server
from RaspberryPi.communication import NetworkCommands as Command


""" A Class to Manage Robot to Client Connections
"""
class ConnectionManager():
    def __init__(self, address: str = "192.168.1.1", port: int = 8080, streamPort: int = 8000, message=True):
        self.address = address
        self.port = port
        self.streamPort = streamPort

        self.connection: socket = None
        self.isConnected        = False
        self.server: socket = None
        self.__serverSocket = None
        self.isServerActive = False
        self.__message = message
        self.localIP = self.__getLocalIP()

    def connect(self) -> bool:
        self.connection = server.connect(self.address, self.port)
        self.isConnected = self.send(Command.NO_OP) if (self.connection) else False
        if (self.__message): print("[ConnectionManager] establishing connection:", self.address, "port", self.port,
                                   " [SUCCESS]" if self.isConnected else " [FAILED]")
        return self.isConnected

    def disconnect(self) -> bool:
        if (not self.isConnected): return True
        self.send(Command.DISCONNECT)
        self.connection.close()
        self.connection = None
        self.isConnected = False
        self.isServerActive = False
        if (self.__message): print("[ConnectionManager] closing connection")
        return self.isConnected

    def send(self, command: str, *params) -> bool:
        for param in params: command += ";" + str(param)
        ack = server.send(self.connection, command, 5)
        if (self.__message): print("[ConnectionManager] sending message:", command," [SUCCESS]" if ack else " [FAILED]")
        return ack

    def createSever(self):
        self.__serverSocket = server.create_server(self.streamPort)
        self.server = self.__serverSocket.accept()[0].makefile('rb') if (self.__serverSocket) else None
        self.isServerActive = self.server is not None
        if (self.__message): print("[ConnectionManager] establishing streaming sever:", self.address,
                                   "port", self.streamPort, " [SUCCESS]" if self.isConnected else " [FAILED]")

    def closeServer(self):
        if (not self.server): return
        self.server.close()
        self.__serverSocket.close()
        self.server: socket = None
        self.__serverSocket = None
        self.isServerActive = False
        if (self.__message): print("[ConnectionManager] streaming sever terminated")

    def __getLocalIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # This is done to establish a temporary connection to a remote host. The connect method for UDP sockets does
        #     not actually send any packets, but it's used here to associate the socket with a remote address, which
        #     is needed to determine the local IP address.
        s.connect(('8.8.8.8', 1))  #connect() for UDP doesn't send packets
        # returns the address and port number of the local end of the socket as a tuple. The first element of this
        #     tuple is the local IP address, which is what the function returns.
        ip = s.getsockname()[0]
        if (self.__message): print("Local IP Address: " + ip)
        return ip