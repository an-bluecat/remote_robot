import threading
from ..backend_control import ConnectionManager
from RaspberryPi.communication import NetworkCommands as Command


class StreamController():
    """
    Stream Controller class, a wrapper for stream operation functions.
    """
    def __init__(self, connect: ConnectionManager, streamer, message=True):
        self.__initialize = lambda : connect.send(Command.STREAM_INIT, connect.localIP, connect.streamPort)
        self.__terminate  = lambda : connect.send(Command.STREAM_TERMINATE)
        self.__serve      = lambda : connect.send(Command.STREAM_START)
        self.__stop_serve = lambda : connect.send(Command.STREAM_STOP)

        self.streamInitialized = False
        self.__videoStreamer = streamer
        self.__streamThread  = threading.Thread(target=self.__videoStreamer.video_stream_loop)
        self.__message = message

    def start_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Start")

        if (self.__streamThread.is_alive()): self.__streamThread.join(timeout=1)
        self.__streamThread = threading.Thread(target=self.__videoStreamer.video_stream_loop)
        self.__streamThread.start()

        if (not self.streamInitialized): self.streamInitialized = self.__initialize()
        if (not self.streamInitialized or not self.__serve()): return False
        return True

    def stop_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Terminate")
        if (self.__stop_serve()):
            if (self.__streamThread.is_alive()): self.__streamThread.join(timeout=1)
            self.__videoStreamer.set_coverImage()
            self.streamInitialized = not self.__terminate()
            return not self.streamInitialized
        return False

    def pause_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Pause")
        return self.__stop_serve()

    def resume_stream(self) -> bool:
        if (self.__message): print("[StreamController] client requesting stream Resume")
        return self.__serve()