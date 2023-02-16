import argparse
from communication import NetworkCommands, PI_ServerManager, StreamingCAM
from modules import DriveController


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", dest="port", default=8080, type=int)
    args = parser.parse_args()

    command = NetworkCommands(DriveController(), StreamingCAM())

#-----------------------------------------------------------------------------------------------------------------------
    while (True):                                                   #Server Main Loop
        serverManager = PI_ServerManager(args.port, command)
        if (not serverManager.connect()):                           #Keep Listening to Client Connections
            continue
        while (True):
            data = serverManager.receive()                          #Handle Commands from Client
            if (not data or command.handleCommand(data)): break
        serverManager.server.close()
        serverManager.connection.close()