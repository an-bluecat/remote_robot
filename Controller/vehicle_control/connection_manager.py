import socket
from Controller.communication import server_utilities as server, Configurator


""" A Class to Manage Robot to Client Connections
"""
class ConnectionManager():
    def __init__(self, address: str, port: int = 8080, streamPort: int = 8000, message=True):
        self.__address = address
        self.__port = port
        self.streamPort = streamPort
        self.localIP = Configurator.get_local_ip()

        self.connection: socket = None
        self.isConnected        = False
        self.server: socket = None
        self.__serverSocket = None
        self.isServerActive = False
        self.__message = message

    def connect(self):
        self.connection = server.connect(self.__address, self.__port)
        self.isConnected = self.connection is not None
        if (self.__message): print("[ConnectionManager] establishing connection:", self.__address, "port", self.__port,
                                   " [SUCCESS]" if self.isConnected else " [FAILED]")

    def disconnect(self):
        self.connection.close()
        self.connection = None
        self.isConnected = False
        if (self.__message): print("[ConnectionManager] closing connection")

    def send(self, command: str, *params) -> bool:
        for param in params: command += ";" + str(param)
        ack = server.send(self.connection, command, len(command))
        if (self.__message): print("[ConnectionManager] sending message:", command, "[SUCCESS]" if ack else None)
        return ack

    def createSever(self):
        self.__serverSocket = server.create_server(self.streamPort)
        self.server = self.__serverSocket.accept()[0].makefile('rb') if (self.__serverSocket) else None
        self.isServerActive = self.server is not None
        if (self.__message): print("[ConnectionManager] establishing streaming sever:", self.__address,
                                   "port", self.streamPort, " [SUCCESS]" if self.isConnected else " [FAILED]")

    def closeServer(self):
        self.server.close()
        self.__serverSocket.close()
        self.server: socket = None
        self.__serverSocket = None
        self.isServerActive = False
        if (self.__message): print("[ConnectionManager] streaming sever terminated")