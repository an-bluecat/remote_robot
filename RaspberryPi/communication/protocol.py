from typing import List, Dict, Callable
try:
    from cam import Streamer
except ModuleNotFoundError:
    from RaspberryPi.cam import Streamer


""" An abstract class for All Vehicle to Client Network Communication Commands
    IMPORTANT: only using this class to add handshake functions
"""
class NetworkCommands():
    NO_OP = "NO_OP"

    STREAM_INIT      = "STRM_INIT"
    STREAM_START     = "STRM_STRT"
    STREAM_STOP      = "STRM_STOP"
    STREAM_TERMINATE = "STRM_TERM"

    CONTROL_THROTTLE = "CTRL_THROT"
    CONTROL_INPUT    = "CTRL_DRIVE"


#-----------------------------------------------------------------------------------------------------------------------
""" Handles Command to Function Handshake 
"""
def functionWrapper(streamer: Streamer) -> Dict[str, Callable[[List[str]], None]]:

    return {
        NetworkCommands.NO_OP: lambda args: True,

        NetworkCommands.STREAM_INIT: lambda args: streamer.initialize_connection(args[0], int(args[1])),
        NetworkCommands.STREAM_START: lambda args: streamer.serve_footage(),
        NetworkCommands.STREAM_STOP: lambda args: streamer.stop_camera_streaming(),
        NetworkCommands.STREAM_TERMINATE: lambda args: streamer.terminate_connection()
    }