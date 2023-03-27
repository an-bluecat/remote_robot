import sys
sys.path.append("/Users/jerryyu/Documents/project/capstone/remote_robot")
import argparse
from gui.application_gui import ApplicationGUI

""" Use this command in the capstone folder:
 >> python application.py -vehicleAddress=192.168.2.31 -streamPort 8080
"""

if __name__ == "__main__":
    import socket
    print("socket host name", socket.gethostbyname(socket.gethostname()))

    parser = argparse.ArgumentParser()
    parser.add_argument("-vehicleAddress", dest="vehicle_address", default="192.168.2.31", type=str)
    parser.add_argument("-vehiclePort", dest="vehicle_port", default=8080, type=int)
    parser.add_argument("-streamPort", dest="stream_port", default=8080, type=int)
    args = parser.parse_args()

    gui = ApplicationGUI(args)
    gui.mainloop()