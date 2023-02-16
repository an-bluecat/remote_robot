from ..backend_control import ConnectionManager
from RaspberryPi.communication import NetworkCommands as Command


""" A Class for Controls and Communication with the Vehicle
"""
class VehicleController():
    def __init__(self, connect: ConnectionManager):
        self.connect = connect
        # self.throttle = [0] * 4

    def setMaxThrottle(self, val) -> None:  # Note: THESE ARE PLACEHOLDERS, to be implemented
        self.connect.send(Command.CONTROL_THROTTLE, val[0], val[1], val[2], val[3])

    def setInput(self, val) -> None:
        self.connect.send(Command.CONTROL_INPUT, val[0], val[1])