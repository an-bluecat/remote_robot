import hid  #>> pip install hidapi
import math
import time
import threading
from ..backend_control import ConnectionManager
from RaspberryPi.communication import NetworkCommands as Command


""" A Class for Controls and Communication with the Vehicle
"""
class VehicleController():
    def __init__(self, connect: ConnectionManager, controller: bool = False, message: bool = True):
        self.connect = connect
        self.__prevInput = [0,0]
        self.gamepad = hid.device()
        self.isFlyStick = False

        if (controller):
            deviceList = []
            for device in hid.enumerate():
                if (not(device['product_string'] != "" and device['product_string'] != "HIDI2C Device")): continue
                if (message):
                    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
                deviceList.append(device)
            self.gamepad.open(deviceList[0]['vendor_id'], deviceList[0]['product_id'])
            if (deviceList[0]['product_string'] == "T.A320 Pilot"): self.isFlyStick = True

        self.createEventListener = lambda : threading.Thread(target=self.controlStickListener)
        self.eventListener: threading.Thread = self.createEventListener()


    def setInput(self, val) -> None:
        if (val[0] == self.__prevInput[0] and val[1] == self.__prevInput[1]): return
        self.__prevInput[0], self.__prevInput[1] = val[0], val[1]
        self.connect.send(Command.CONTROL_INPUT, val[0], val[1])  # NOTE enable this line to send input to vehicle


    def controlStickListener(self):
        while(True):
            axes = self.gamepad.read(64)

            if (self.isFlyStick):
                throttle = (255 - axes[6]) / 255
                axes = ((axes[2]*256+axes[1])/64 - 128, (axes[4]*256+axes[3])/64 - 128) if axes else [0, 0]
            else:
                axes = (axes[3] - 128, axes[4] - 128) if axes else [0, 0]
                throttle = 0.75

            if (abs(axes[0]) <= 1 and abs(axes[1]) <= 1):
                self.setInput([0, 0])
                continue

            power = math.sqrt(axes[0] ** 2 + axes[1] ** 2)
            angle = math.atan2(axes[0], axes[1])
            turnSpeedReduction = 1 - math.sin(math.fmod(angle+math.pi, math.pi)) * 0.25

            if (angle >= 0):
                if (angle >= math.pi / 2):  # Front-Right
                    left = 1
                    right = math.cos(angle * 2)
                else:  # Back-Right
                    left = -math.cos(angle * 2)
                    right = -1
            else:
                if (angle >= -math.pi / 2):  # Back-Left
                    left = -1
                    right = -math.cos(angle * 2)
                else:  # Front-Left
                    left = math.cos(angle * 2)
                    right = 1

            if (-math.pi / 4 * 3 <= angle < -math.pi / 4):  # Normalize Power Factor
                power /= -1 / math.sin(angle)
            elif (-math.pi / 4 <= angle < math.pi / 4):
                power /= 1 / math.cos(angle)
            elif (math.pi / 4 <= angle < math.pi / 4 * 3):
                power /= 1 / math.sin(angle)
            else:
                power /= -1 / math.cos(angle)

            left *= power * 512 * throttle * turnSpeedReduction  # 0 ~ +-65535
            right *= power * 512 * throttle * turnSpeedReduction
            self.setInput([int(left), int(right)])