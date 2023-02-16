import tkinter as tk
import tkinter.messagebox
from Controller.backend_control import ConnectionManager, VehicleController, StreamController, VideoStreamer


class ApplicationGUI(tk.Tk):
    def __init__(self, args, title="Remote Robot Control Application", **kwargs):
        super().__init__(screenName=title, **kwargs)

        self.title(title)
        self.version = "0.1.0"

        self.connectionManager = ConnectionManager(args.vehicle_address, args.vehicle_port, args.stream_port)
        self.vehicleController = VehicleController(self.connectionManager)
        self.videoStreamer     = VideoStreamer    (self.connectionManager, self)
        self.streamController  = StreamController (self.connectionManager, self.videoStreamer)

        self.menu_deviceControl = None
        self.displayMenu()


    def displayMenu(self):
        menubar = tk.Menu(self)

        self.menu_deviceControl = tk.Menu(menubar, tearoff=0)
        self.menu_deviceControl.add_command(label="Connect to Device", command=lambda: menu_onConnect(self))
        self.menu_deviceControl.add_command(label="Disconnect Device", command=lambda: menu_onDisconnect(self))
        self.menu_deviceControl.add_command(label="Start Streaming",   command=lambda: menu_onSteamStart(self))
        self.menu_deviceControl.add_command(label="Stop Steaming",     command=lambda: menu_onSteamStop(self))
        menubar.add_cascade(label="Device", menu=self.menu_deviceControl, underline=0)

        self.menu_deviceControl.entryconfig("Disconnect Device", state="disabled")
        self.menu_deviceControl.entryconfig("Start Streaming", state="disabled")
        self.menu_deviceControl.entryconfig("Stop Steaming", state="disabled")

        self.config(menu=menubar)


#-----------------------------------------------------------------------------------------------------------------------
""" The Section Below are Functions for the GUI Menu
"""
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