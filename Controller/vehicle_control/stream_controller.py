from time import sleep
from Controller.communication import server_utilities as server, Configurator
from Controller.vehicle_control import ConnectionManager


class StreamController():
    """
    Stream Controller class, a wrapper for stream operation functions.
    """
    def __init__(self, connect: ConnectionManager, message=True):
        if (message): print("[StreamController] initializing")
        self.__initialize = lambda : connect.send("STREAM-INITIALIZE", connect.localIP, connect.streamPort)
        self.__terminate  = lambda : connect.send("STREAM-TERMINATE")
        self.__serve      = lambda : connect.send("STREAM-SERVE-FOOTAGE")
        self.__stop_serve = lambda : connect.send("STREAM-STOP-STREAMING")
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