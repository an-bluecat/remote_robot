# Python program to implement client side of the control-flow
import socket
import time

def create_server(port: int) -> socket:
    """
    Establishes a connection to a server

    :param port: port to be used
    :return: socket with an active connection to the specified server
    """
    server = socket.socket()
    try:
        server.bind((socket.gethostname(), port))
        server.listen(5)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        time.sleep(1)
        print("Listening on address: ", server.getsockname()[0])
        print("Listening on port: ", server.getsockname()[1])

        return server
    except Exception as e:
        print(f"Error creating server: {e}")
        return None

def is_server_listening(host: str, port: int) -> bool:
    """
    Check if a server is listening on a specified host and port

    :param host: host address
    :param port: port number
    :return: True if the server is listening, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

def connect(address: str, port: int) -> socket:
    """
    Establishes a connection to a server

    :param address: server address to connect to
    :param port: port to be used
    :return: socket with an active connection to the specified server
    """
    conn: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((address, port))
    except ConnectionRefusedError as e:
        # Handle the exception here
        print("Error: Connection refused, please check the server is running and IP address and port are correct.")
        print("tried to connect to: " + str(address) + ":" + str(port))
    return conn


def send(conn: socket, msg: str, msg_length: int = 4096) -> bool:
    """
    Sends a message through the supplied connection, and returns whether a response is received
    If a response is received it's printed

    :param conn: connection to send the message through
    :param msg: message to be sent
    :param msg_length: length of the message to be sent. Default is 4096
    :return: whether a response has been received and logged to terminal
    """
    try:
        conn.send(msg.encode())
        from_server = conn.recv(msg_length).decode()
    except OSError as e:
        print(e)
        return False
    if not from_server:
        return False
    if not "ack" == str(from_server):
        print("Received message different from 'ack' as response. Terminating connection. Response was: "
              + str(from_server))
        terminate(conn)
        return False
    return True


def terminate(conn: socket) -> None:
    """
    terminates the connection of a socket

    :param conn: connection to be terminated
    """
    conn.close()