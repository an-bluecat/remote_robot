import io
import socket
import struct
import time
from threading import Thread
try:
    import picamera
except ModuleNotFoundError as e:
    print("No camera module", e)


class StreamingCAM():
    """
    Utilizes the RPI cam to serve a stream
    """
    def __init__(self):
        self.rpi_socket: socket = None
        self.connection = None
        self.terminate = False
        self.thread = None
        self.time_limit: int = -1

    def initialize_connection(self, address: str, port: int):
        """
        Initializes connection to the server
        """
        print("Initializing connection to client at ", address, ":", port, " ...")
        try:
            self.rpi_socket = socket.socket()
            self.rpi_socket.connect((address, port))
            self.connection = self.rpi_socket.makefile('wb')
            print("Connection initialized")
        except Exception as e:
            print(f"Error: {e}")

    def terminate_connection(self):
        """
        Terminates connection, and closes socket
        """
        self.connection.close()
        self.rpi_socket.close()
        self.connection = None
        self.rpi_socket = None
        print("Camera Connection terminated")

    def serve_footage(self, time_limit: int = -1) -> None:
        """
        Starts serving video footage in separate thread
        :param time_limit: how many seconds the stream should be served. If <0, stream continues forever
        """
        self.time_limit = time_limit
        if (self.thread): self.stop_camera_streaming()
        self.terminate = False
        self.thread = Thread(target=self.serve_footage_loop)
        self.thread.start()

    def serve_footage_loop(self):
        """
        Serves camera footage live

        If no limit is given, streaming can be stopped by calling 'stop_camera_streaming'
        """
        print("Serving footage!")
        # Make a file-like object out of the connection
        with picamera.PiCamera(framerate=30) as camera:
            camera.resolution = (1024, 576)
            camera.rotation = 270
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(2)
            camera.stop_preview()

            # the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol.py simple)
            start = time.time()
            stream = io.BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True, thumbnail=None, quality=10):
                elapsed = time.time()
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                self.connection.write(struct.pack('<L', stream.tell()))
                self.connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                self.connection.write(stream.read())
                # If we've been capturing for more than time_limit seconds, quit
                if 0 < self.time_limit < time.time() - start or self.terminate:
                    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
                #print("Picture took: " + str(1/(elapsed - time.time())))
        # Write a length of zero to the stream to signal we're done
        self.connection.write(struct.pack('<L', 0))
        print("No longer serving footage")

    def stop_camera_streaming(self) -> None:
        """
        Requests that the streamer stops streaming the camera feed
        """
        if (not self.thread): return
        self.terminate = True
        self.thread.join()
        self.thread = None