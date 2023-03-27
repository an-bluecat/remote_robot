
# RC-car

Repository for code used in creating a remote-controlled car. The car is controlled through a python interface, on a
laptop on the same network as the car

# Devices

The project consists of multiple devices, working together. This section will describe the devices and the connection.
The devices are

- [Raspberry Pi Zero](https://thepihut.com/collections/raspberry-pi-kits-and-bundles/products/raspberry-pi-zero-essential-kit)
  with [camera](https://www.raspberrypi.org/products/camera-module-v2/). This will host the interface to the car, and
  supply a video feed from its front.

# Commands
- scp -r -P80 RaspberryPi/ pi@192.168.0.38:/home/pi/Desktop/
- windows: scp -r -P80 .\RaspberryPi pi@192.168.2.31:/home/pi/Desktop/
- Controller jerryyu$ python3 application.py -vehicleAddress=192.168.0.64 -streamPort 8080

- python3 application.py -vehicleAddress=192.168.0.38 -config MiniCar
