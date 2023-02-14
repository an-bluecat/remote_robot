# Reads stream from cam_streamer.py and displays it in window.
# This is technically the server should be renamed when re-written
import io
import struct
import time
from tkinter import *
from typing import Callable
from PIL import ImageTk, Image

from Controller.vehicle_control import ConnectionManager

""" A Class for handling the video-stream from the Raspberry Pi
"""
class VideoReceiver():
    def __init__(self, connect: ConnectionManager, coverImage=r"../cover.png"):
        self.connect = connect
        self.image = coverImage
        self.display_label = None

    def set_label(self, display_label: Label):
        self.display_label = display_label
        self.set_coverImage()

    def set_coverImage(self):
        """
        Displays placeholder image
        """
        import os
        curDir=os.getcwd()
        if not curDir.endswith("Controller"):
            os.chdir(curDir+"/remote_robot/Controller/")
        if self.image:
            image: PhotoImage = PhotoImage(file=r"../cover.png")
            self.display_label.imgtk = image
            self.display_label.configure(image=image)
        os.chdir(curDir)

    def loop_repeater(self, func: Callable[[], bool]) -> None:
        """
        Repeats loop, and prints result of each iteration
        """
        while True:
            res: bool = func()
            self.set_coverImage()
            if res:
                print("Loop terminated successfully  [ server connection:",self.connect.isServerActive,"]")
            else:
                print("Loop terminated with error  [ server connection:",self.connect.isServerActive,"]")

    def video_stream_loop(self) -> None:
        self.loop_repeater(self.video_stream_loop_inner)

    def video_stream_loop_inner(self) -> bool:
        """
        The stream loop, which reads the loop and updates the label with the new images
        Does not terminate until an error occurs
        :return: False if an error occurs, True otherwise
        """
        # Accept a single connection and make a file-like object out of it
        if (not self.connect.isServerActive): self.connect.createSever()
        print("video_stream_loop_inner started, waiting for image...")
        try:
            frameTime = [0]*30
            frameRate = 0
            frameCounter = 0

            while True:
                elapsed = time.time()
                # Read the length of the image as a 32-bit unsigned int. If the length is zero, quit the loop
                image_len = struct.unpack('<L', self.connect.server.read(4))[0]
                if (not image_len): return True
                # Construct a stream to hold the image data and read the image data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connect.server.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some processing on it
                image_stream.seek(0)
                image = Image.open(image_stream)
                img_tk = ImageTk.PhotoImage(image=image)
                self.display_label.imgtk = img_tk
                self.display_label.configure(image=img_tk)

                frameCounter = (frameCounter+1) % 30
                frameRate -= frameTime[frameCounter]
                frameTime[frameCounter] = time.time() - elapsed
                frameRate += frameTime[frameCounter]
                if (frameCounter == 0): print("Frame Rate: {:0.2f}fps".format(30/frameRate))

        except Exception as e:
            print(f"Something unexpected happened, causing the stream to crash: {e}")
            self.connect.closeServer()
            return False