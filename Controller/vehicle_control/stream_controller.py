from time import sleep
from Controller.communication import server_utilities as server, Configurator


class StreamController(object):
    """
    Stream Controller class, a wrapper for stream operation functions.
    """
    def __init__(self, vehicleController, message=True):
        if (message): print("[StreamController] initializing")
        self.connection = vehicleController.connection
        self.streamPort = vehicleController.streamport
        self.__initialize = lambda : server.send(self.connection, "STREAM-INITIALIZE;" + Configurator.get_local_ip() +
                                                 ";"+ str(self.streamPort))
        self.__terminate  = lambda : server.send(self.connection, "STREAM-TERMINATE;")
        self.__serve      = lambda : server.send(self.connection, "STREAM-SERVE-FOOTAGE;")
        self.__stop_serve = lambda : server.send(self.connection, "STREAM-STOP-STREAMING;")
        self.streamInitialized = False
        self.__message = message

    def start_stream(self) -> None:
        if (self.__message): print("[StreamController] client requesting stream Start")
        if (not self.streamInitialized): self.__initialize()
        self.streamInitialized = True
        self.__serve()

    def stop_stream(self) -> None:
        if (self.__message): print("[StreamController] client requesting stream Terminate")
        self.__stop_serve()
        sleep(1)
        self.streamInitialized = False
        self.__terminate()

    def pause_stream(self) -> None:
        if (self.__message): print("[StreamController] client requesting stream Pause")
        self.__stop_serve()

    def resume_stream(self) -> None:
        if (self.__message): print("[StreamController] client requesting stream Resume")
        self.__serve()