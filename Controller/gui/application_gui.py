import tkinter as tk
import tkinter.messagebox
from Controller.backend_control import ConnectionManager, VehicleController, StreamController, VideoStreamer
import pygame
import math

class ApplicationGUI(tk.Tk):
    def __init__(self, args, title="Remote Robot Control Application", **kwargs):
        super().__init__(screenName=title, **kwargs)
        # # Initialize the pygame library
        pygame.init()
        pygame.joystick.init()

        self.title(title)
        self.version = "0.1.0"

        self.connectionManager = ConnectionManager(args.vehicle_address, args.vehicle_port, args.stream_port)
        self.vehicleController = VehicleController(self.connectionManager)
        self.videoStreamer     = VideoStreamer    (self.connectionManager, self)
        self.streamController  = StreamController (self.connectionManager, self.videoStreamer)

        self.menu_deviceControl = None
        self.displayMenu()

        # Schedule the joystick update task

        # self.sendJoystickCommand()

    def update_joystick(self):
        if not pygame.joystick.get_count():
            return []

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        # Get the number of axes
        num_axes = joystick.get_numaxes()

        # Handle joystick events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Get joystick axes values
        axes = [joystick.get_axis(i) for i in range(num_axes)]

        # Schedule the next update
        # self.after(50, self.update_joystick)

        return axes

    def sendJoystickCommand(self, stop=False):
        # Get joystick axes values
        axes = self.update_joystick()

        

        # Round the values to 2 decimal places, otherwise 0 will be sometimes 0.0023 or something
        axes = [round(axis, 2) for axis in axes]
        # Print the axes values
        print("Axes: ", axes)

        right, left = self.joystickToDiff(axes[0], -axes[1], -1, 1, -100, 100) 
        print("Left: ", left, "Right: ", right)

        self.vehicleController.setInput([left, right])

        # Schedule the next print
        if not stop:
            self.after(500, self.sendJoystickCommand)  # NOTE change this to 50ms in the final version


    def joystickToDiff(self, x, y, minJoystick, maxJoystick, minSpeed, maxSpeed):
        # If x and y are 0, then there is not much to calculate...
        if x == 0 and y == 0:
            return (0, 0)

        # First Compute the angle in deg
        # First hypotenuse
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(math.fabs(x) / z)

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the coeff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
        turn = round(turn * 100, 0) / 100

        # And max of y or x is the movement
        mov = max(math.fabs(y), math.fabs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = mov
            rawRight = turn
        else:
            rawRight = mov
            rawLeft = turn

        # Reverse polarity
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0 - rawRight

        # minJoystick, maxJoystick, minSpeed, maxSpeed
        # Map the values onto the defined rang
        rightOut = self.map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
        leftOut = self.map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

        return (rightOut, leftOut)



    def map(self, v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


    def displayMenu(self):
        menubar = tk.Menu(self)

        self.menu_deviceControl = tk.Menu(menubar, tearoff=0)
        self.menu_deviceControl.add_command(label="Connect to Device", command=lambda: menu_onConnect(self))
        self.menu_deviceControl.add_command(label="Disconnect Device", command=lambda: menu_onDisconnect(self))
        self.menu_deviceControl.add_command(label="Start Streaming",   command=lambda: menu_onSteamStart(self))
        self.menu_deviceControl.add_command(label="Stop Steaming",     command=lambda: menu_onSteamStop(self))
        menubar.add_cascade(label="Device", menu=self.menu_deviceControl, underline=0)
        
        # Add an "About" menu with an "Instructions" option
        self.menu_about = tk.Menu(menubar, tearoff=0)
        self.menu_about.add_command(label="Instructions", command=lambda: menu_onInstructions(self))
        menubar.add_cascade(label="About", menu=self.menu_about, underline=0)

        # Disable certain menu options at start
        self.menu_deviceControl.entryconfig("Disconnect Device", state="disabled")
        self.menu_deviceControl.entryconfig("Start Streaming", state="disabled")
        self.menu_deviceControl.entryconfig("Stop Steaming", state="disabled")

        # Add a "Controller Input" menu with a "Start Controller Input" option
        self.menu_controllerInput = tk.Menu(menubar, tearoff=0)
        self.menu_controllerInput.add_command(label="Start Controller Input", command=lambda: menu_onInputStart(self))
        self.menu_controllerInput.add_command(label="Stop Controller Input", command=lambda: menu_onInputStop(self))
        menubar.add_cascade(label="Controller Input", menu=self.menu_controllerInput, underline=0)

        self.config(menu=menubar)


#-----------------------------------------------------------------------------------------------------------------------
""" The Section Below are Functions for the GUI Menu
"""

def menu_onInstructions(gui: ApplicationGUI):                     #Show Instructions
    instructions = "Instructions:\n\n" \
                   "1. Connect to the device by clicking 'Connect to Device' in the 'Device' menu.\n\n" \
                   "2. Once connected, start streaming by clicking 'Start Streaming'. The video feed will appear in a new window.\n\n" \
                   "3. To pause the streaming, click 'Stop Streaming'.\n\n" \
                   "4. To disconnect from the device, click 'Disconnect Device' in the 'Device' menu."
    tk.messagebox.showinfo(title="About", message=instructions)


def menu_onConnect(gui: ApplicationGUI):                            #Connect to Device
    if (gui.connectionManager.isConnected): return
    if (gui.connectionManager.connect()):
        menu_onSteamStart(gui)
        gui.menu_deviceControl.entryconfig("Connect to Device", state="disabled")
        gui.menu_deviceControl.entryconfig("Disconnect Device", state="normal")
    else:
        tk.messagebox.showerror(title="Network Error", message="Cannot connect to device at:\n" +
                                gui.connectionManager.address + "\nport " + str(gui.connectionManager.port))

def menu_onDisconnect(gui: ApplicationGUI):                         #Disconnect From Device
    if (not gui.connectionManager.isConnected): return
    if (gui.connectionManager.isServerActive):
        gui.streamController.stop_stream()
        gui.connectionManager.closeServer()
    gui.connectionManager.disconnect()
    gui.menu_deviceControl.entryconfig("Start Streaming", state="disabled")
    gui.menu_deviceControl.entryconfig("Stop Steaming", state="disabled")
    gui.menu_deviceControl.entryconfig("Disconnect Device", state="disabled")
    gui.menu_deviceControl.entryconfig("Connect to Device", state="normal")

def menu_onSteamStart(gui: ApplicationGUI):                         #Start Video Streaming
    if (not gui.connectionManager.isConnected): return
    if (not gui.streamController.start_stream()): return
    gui.menu_deviceControl.entryconfig("Start Streaming", state="disabled")
    gui.menu_deviceControl.entryconfig("Stop Steaming", state="normal")

def menu_onSteamStop(gui: ApplicationGUI):                          #Pause Video Streaming
    if (not gui.connectionManager.isConnected): return
    if (not gui.streamController.pause_stream()): return
    gui.menu_deviceControl.entryconfig("Stop Steaming", state="disabled")
    gui.menu_deviceControl.entryconfig("Start Streaming", state="normal")



def menu_onInputStart(gui: ApplicationGUI):
    gui.sendJoystickCommand()
    gui.menu_controllerInput.entryconfig("Start Controller Input", state="disabled")
    gui.menu_controllerInput.entryconfig("Stop Controller Input", state="normal")

def menu_onInputStop(gui: ApplicationGUI):
    gui.after_cancel(gui.sendJoystickCommand(stop=True))
    gui.vehicleController.setInput([0, 0])
    gui.menu_controllerInput.entryconfig("Start Controller Input", state="normal")
    gui.menu_controllerInput.entryconfig("Stop Controller Input", state="disabled")

