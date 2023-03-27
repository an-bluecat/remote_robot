from .cam_streamer import StreamingCAM
try:
    from modules import DriveController
except ModuleNotFoundError:
    from ..modules import DriveController

""" An abstract class for All Vehicle to Client Network Communication Commands
    IMPORTANT: only using this class to add handshake functions
               MAX INSTRUCTION LENGTH IS 32 BYTES
"""
class NetworkCommands():
    NO_OP = "NO_OP"
    DISCONNECT = "DISCONNECT"

    STREAM_INIT      = "STRM_INIT"                                  #"STRM_INIT;192.168.255.255;65535"
    STREAM_START     = "STRM_STRT"
    STREAM_STOP      = "STRM_STOP"
    STREAM_TERMINATE = "STRM_TERM"

    CONTROL_THROTTLE = "CTRL_THROT"                                 #"CTRL_THROT;255;255;255;255"
    CONTROL_INPUT    = "CTRL_DRIVE"

#-----------------------------------------------------------------------------------------------------------------------
    """ Handles Command to Function Handshake
    """
    def __init__(self, driver: DriveController, streamer: StreamingCAM):
        self.functionWrapper = {
            self.NO_OP: lambda args: True,
            self.DISCONNECT: lambda args: True,

            self.STREAM_INIT:      lambda args: streamer.initialize_connection(args[0], int(args[1])),
            self.STREAM_START:     lambda args: streamer.serve_footage(),
            self.STREAM_STOP:      lambda args: streamer.stop_camera_streaming(),
            self.STREAM_TERMINATE: lambda args: streamer.terminate_connection(),

            self.CONTROL_THROTTLE: lambda args: driver.setMaxThrottle(args),
            self.CONTROL_INPUT:    lambda args: driver.setInput(args)
        }

#-----------------------------------------------------------------------------------------------------------------------
    """ CommandHandler doing lookups in dictionary
        @return: if command DISCONNECT
    """
    def handleCommand(self, data: str) -> bool:
        split = data.split(";")
        self.functionWrapper[split[0]](split[1:])
        return split[0] == self.DISCONNECT