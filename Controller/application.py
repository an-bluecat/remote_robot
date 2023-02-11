import argparse
from typing import Dict, List, Tuple, Callable
# Get the current directory of the script
import sys, os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # Navigate to the parent directory
# parent_dir = os.path.dirname(current_dir)
# # Append the parent directory to the sys.path list
# sys.path.append(parent_dir)
# sys.path.append(current_dir)
# parent_dir = os.path.dirname(parent_dir)
# sys.path.append(parent_dir)
# try:
#     from Controller.gui.application_gui import GUI
#     from Controller.gui.model import MiscControlSpec
#     from Controller.vehicle_control import VehicleController, StreamControllerI, SimpleStreamController
#     from Controller.video import VideoStreamReceiver
# except ModuleNotFoundError:
#     from gui.application_gui import GUI
#     from gui.model import MiscControlSpec
#     from vehicle_control import VehicleController, StreamControllerI, SimpleStreamController
#     from video import VideoStreamReceiver

from gui.application_gui import GUI
from gui.model import MiscControlSpec
from vehicle_control import VehicleController, StreamControllerI, SimpleStreamController
# from video import VideoStreamReceiver


# from video.video_stream_receiver import VideoStreamReceiver

# from video import video_stream_receiver
from video.video_stream_receiver import VideoStreamReceiver
# from video_stream_receiver import VideoStreamReceiver


def build_stream_configuration(controller: VehicleController) -> StreamControllerI:
    """
    :param controller: controller for the vehicle
    :return: streamController for interfacing with the video-stream
    """
    return SimpleStreamController(
        controller.stream_initialize,
        controller.stream_terminate,
        controller.stream_start,
        controller.stream_stop
    )


def default_vehicle_config(controller: VehicleController) -> Tuple[Dict[str, bool], List[MiscControlSpec]]:
    """
    Fallback configuration. Everything is disabled

    :param controller: the controller used in communicating with the vehicle
    :return: configuration for std vehicle, empty misc map
    """
    return {}, []


def mini_car_config(controller: VehicleController) -> Tuple[Dict[str, bool], List[MiscControlSpec]]:
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

    # mini_misc = [
    #     MiscControlSpec("lights", lambda v: controller.set_lights((1 if v else 0)), param_type=bool, row=0, column=0,
    #                     description="Toggles lights on vehicle")
    # ]

    mini_misc = [
        MiscControlSpec("video", lambda v: controller.stream_start() if v else controller.stream_stop(), param_type=bool, row=0, column=0,
                        description="Toggles video on vehicle")
    ]
    return mini_enabled, mini_misc


if __name__ == "__main__":
    configuration_builders: Dict[str, Callable[[VehicleController], Tuple[Dict[str, bool], List[MiscControlSpec]]]] = {
        "Fallback": default_vehicle_config,
        "MiniCar": mini_car_config
    }

    import socket
    print("socket host name", socket.gethostbyname(socket.gethostname()))

    parser = argparse.ArgumentParser()
    parser.add_argument("-config", dest="config", default="Fallback", type=str)
    parser.add_argument("-vehicleAddress", dest="vehicle_address", default="127.0.0.1", type=str)
    parser.add_argument("-vehiclePort", dest="vehicle_port", default=8080, type=int)
    parser.add_argument("-streamPort", dest="stream_port", default=8000, type=int)

    args = parser.parse_args()

    if args.config in configuration_builders:
        vehicle_controller: VehicleController = VehicleController(args.vehicle_address, args.vehicle_port, args.stream_port)

        enabled, misc = configuration_builders[args.config](vehicle_controller)
        print("args.stream_port",args.stream_port)
        streamer = VideoStreamReceiver(args.stream_port, placeholder_image_name=r"../unnamed.png")
        stream_controller: StreamControllerI = build_stream_configuration(vehicle_controller)
        gui = GUI(viewer=streamer, controller=vehicle_controller, stream_controller=stream_controller, enabled=enabled,
                  misc_controls=misc)

        gui.mainloop()
    else:
        print("Configuration '" + args.config + "' not found. Options are: " + ", ".join(
            list(configuration_builders.keys())))


# use this command in the capstone folder: /usr/local/bin/python3 application.py -vehicleAddress=192.168.0.31 -config MiniCar