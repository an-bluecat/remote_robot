import socket

from .vehicle_controller_interface import VehicleControllerI
from Controller.communication import server_utilities as server, Configurator


class VehicleController(VehicleControllerI):
    """
    Controller implementation communicating with the RC vehicle
    """

    def __init__(self, address: str, port: int, streamport: int = 8000):
        
        print("initializing vehicle controller, ", "address: ", address, " port: ", port)
        self.streamport=streamport
        self.connection: socket = server.connect(address, port)

    def set_drive(self, val: int) -> None:
        server.send(self.connection, "DRIVE;" + str(val))

    def set_gear(self, val: int) -> None:
        server.send(self.connection, "GEAR;" + str(val))

    def set_throttle(self, val: int) -> None:
        server.send(self.connection, "THROTTLE;" + str(val))

    def set_direction(self, val: int) -> None:
        server.send(self.connection, "DIRECTION;" + str(val))

    def set_lights(self, val: int) -> None:
        server.send(self.connection, "LIGHT;" + str(val))