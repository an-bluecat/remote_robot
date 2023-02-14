import argparse
from typing import Dict, List, Tuple

""" Use this command in the capstone folder:
 >> python application.py -vehicleAddress=192.168.0.31 -streamPort 8080
"""

from gui.application_gui import ApplicationGUI
from gui.model import MiscControlSpec
from vehicle_control import VehicleController
from vehicle_control import ConnectionManager


def remote_robot_config(controller: VehicleController) -> Tuple[Dict[str, bool], List[MiscControlSpec]]:
    """
    Generates and outputs configuration map
    :param controller: the controller used in communicating with the vehicle
    :return: configuration for MiniCar, Misc map
    """
    mini_enabled = {
        "misc": True,
        "throttle": True,
        "direction": True
    }
    mini_misc = [
        MiscControlSpec("video", lambda v: None, param_type=bool, row=0, column=0,
                        description="Toggles video on vehicle")
    ]
    return mini_enabled, mini_misc


if __name__ == "__main__":
    import socket
    print("socket host name", socket.gethostbyname(socket.gethostname()))

    parser = argparse.ArgumentParser()
    parser.add_argument("-vehicleAddress", dest="vehicle_address", default="127.0.0.1", type=str)
    parser.add_argument("-vehiclePort", dest="vehicle_port", default=8080, type=int)
    parser.add_argument("-streamPort", dest="stream_port", default=8000, type=int)
    args = parser.parse_args()

    connectionManager = ConnectionManager(args.vehicle_address, args.vehicle_port, args.stream_port)

    connectionManager.connect()
    gui = ApplicationGUI(connectionManager)
    gui.mainloop()

    #gui = GUI(viewer=streamer, controller=vehicle_controller, enabled=enabled, misc_controls=misc)
    #gui.mainloop()