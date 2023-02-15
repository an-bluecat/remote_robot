import argparse
from cam import CamStreamer
from communication import functionWrapper
from server import Server, DictCommandHandler
from micro_controller import VehicleController


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", dest="port", default=8080, type=int)

    cam_streamer = CamStreamer()

    vehicle_controller = VehicleController()

    commands = functionWrapper(cam_streamer)

    handler = DictCommandHandler(commands)
    args = parser.parse_args()

    server = Server(port=args.port, command_handler=handler)
    server.server_loop()