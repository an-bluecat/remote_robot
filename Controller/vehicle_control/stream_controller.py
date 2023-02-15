from time import sleep
from RaspberryPi.communication import NetworkCommands as Command
from Controller.vehicle_control import ConnectionManager


class StreamController():
    """
    Stream Controller class, a wrapper for stream operation functions.
    """
    def __init__(self, connect: ConnectionManager, message=True):
        if (message): print("[StreamController] initializing")
        self.__initialize = lambda : connect.send(Command.STREAM_INIT, connect.localIP, connect.streamPort)
        self.__terminate  = lambda : connect.send(Command.STREAM_TERMINATE)
        self.__serve      = lambda : connect.send(Command.STREAM_START)
        self.__stop_serve = lambda : connect.send(Command.STREAM_STOP)
        self.streamInitialized = False
        self.__message = message

    def start_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Start")
        if (not self.streamInitialized): self.streamInitialized = self.__initialize()
        return self.__serve() if (self.streamInitialized) else False

    def stop_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Terminate")
        if (self.__stop_serve()):
            sleep(1)
            self.streamInitialized = not self.__terminate()
            return not self.streamInitialized
        return False

    def pause_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Pause")
        return self.__stop_serve()

    def resume_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Resume")
        return self.__serve()