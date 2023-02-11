import socket


class Configurator(object):
    """"
    Utility class for configuration helper methods.
    """

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # This is done to establish a temporary connection to a remote host. The connect method for UDP sockets does not actually send any packets, but it's used here to associate the socket with a remote address, which is needed to determine the local IP address.
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        # returns the address and port number of the local end of the socket as a tuple. The first element of this tuple is the local IP address, which is what the function returns.
        ip=s.getsockname()[0]
        print("get_local_ip returns: " + ip)
        return ip
