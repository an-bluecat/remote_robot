import io
import struct
import time
from tkinter import *
from PIL import ImageTk, Image  #>> pip install pillow
from ..backend_control import ConnectionManager


""" A Class for handling the video-stream from the Raspberry Pi
    Which also function as a video player widget on screen
"""
class VideoStreamer(Frame):
    def __init__(self, connect: ConnectionManager, parent, coverImage=r"../cover.png"):
        Frame.__init__(self, parent)
        self.misc_controls_frame: LabelFrame = LabelFrame(parent, text="Video Stream")
        self.display_label = [Label(self.misc_controls_frame), Label(self.misc_controls_frame)] #double buffering
        self.display_label[0].grid(row=0, column=0, columnspan=2, rowspan=2, padx=5, pady=5)
        self.display_label[1].grid(row=0, column=0, columnspan=2, rowspan=2, padx=5, pady=5)
        self.misc_controls_frame.grid(row=0, column=0, sticky=N + S + E + W)

        self.connect = connect
        self.image = coverImage
        self.set_coverImage()

    def set_coverImage(self):
        """ Displays cover image
        """
        if self.image:
            image: PhotoImage = PhotoImage(file=r"../cover.png")
            self.display_label[0].imgtk = image
            self.display_label[0].configure(image=image)
            self.display_label[1].imgtk = image
            self.display_label[1].configure(image=image)

    def video_stream_loop(self) -> None:
        """
        The stream loop, which reads the loop and updates the label with the new images
        Does not terminate until an error occurs
        :return: False if an error occurs, True otherwise
        """
        # Accept a single connection and make a file-like object out of it
        if (not self.connect.isServerActive): self.connect.createSever()
        print("waiting for image...")
        try:
            frameTime = [0]*30
            frameRate = 0
            frameCounter = 0

            while True:
                elapsed = time.time()
                # Read the length of the image as a 32-bit unsigned int. If the length is zero, quit the loop
                image_len = struct.unpack('<L', self.connect.server.read(4))[0]
                if (not image_len):
                    self.set_coverImage()
                    return
                # Construct a stream to hold the image data and read the image data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connect.server.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some processing on it
                image_stream.seek(0)
                image = Image.open(image_stream)
                img_tk = ImageTk.PhotoImage(image=image)
                self.display_label[(frameCounter+1)%2].lift()
                self.display_label[frameCounter%2].imgtk = img_tk
                self.display_label[frameCounter%2].configure(image=img_tk)

                frameCounter = (frameCounter+1) % 30
                frameRate -= frameTime[frameCounter]
                frameTime[frameCounter] = time.time() - elapsed
                frameRate += frameTime[frameCounter]
                if (frameCounter == 0): print("Frame Rate: {:0.2f}fps".format(30/frameRate))

        except Exception as e:
            self.connect.closeServer()
            self.set_coverImage()