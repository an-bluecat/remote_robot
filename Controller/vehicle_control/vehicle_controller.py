from Controller.vehicle_control import ConnectionManager


""" A Class for Controls and Communication with the Vehicle
"""
class VehicleController():
    def __init__(self, connect: ConnectionManager):
        self.connect = connect

    def set_drive(self, val: int) -> None:
        self.connect.send("DRIVE", val)

    def set_gear(self, val: int) -> None:
        self.connect.send("GEAR", val)

    def set_throttle(self, val: int) -> None:
        self.connect.send("THROTTLE", val)

    def set_direction(self, val: int) -> None:
        self.connect.send("DIRECTION", val)

    def set_lights(self, val: int) -> None:
        self.connect.send("LIGHT", val)