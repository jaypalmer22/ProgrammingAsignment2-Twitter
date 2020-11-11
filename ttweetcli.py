import socket
import sys
from _thread import *

listener_open = True


def listener_thread(connection):
    while True:
        received = connection.recv(1024).decode()

        # Case: Server sent a tweet to which we are subscribed
        if received[0:2] == "-r":
            print(received[3:len(received)])

        # Case: Command failed, full stop not required
        elif received[0:2] == "-f":
            print(received[3:len(received)])

        # Case: General success with print statement
        elif received[0:2] == "-s":
            print(received[3:len(received)])

        # Case: Safe exit
        elif received[0:2] == "-b":
            print(received[3:len(received)])
            connection.close()
            exit()


def clientTalk(username, host, port):
    ClientSocket = socket.socket()

    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    nameString = "username " + username
    ClientSocket.send(nameString.encode())

    # validating username before entering command input loop
    received = ClientSocket.recv(1024).decode()

    # Case: username was invalid --> full stop
    if received[0:2] == "-f":
        print(received[3:len(received)])
        exit()

    # Case: username successfully validated
    elif received[0:2] == "-s":
        print(received[3:len(received)])

    # Start new thread to listen for server responses while this thread blocks for input
    start_new_thread(listener_thread, (ClientSocket,))

    # Command input loop
    while True:
        Input = input()

        # According to professor Konte on Piazza, we can update after input if another thread closes the connection
        try:
            ClientSocket.send(str.encode(Input))
        except:
            exit()
    #ClientSocket.close()


if __name__ == '__main__':
    # Make sure parameter count is correct (error message #5)
    if len(sys.argv) != 4:
        print("\nerror: args should contain <ServerIP> <ServerPort> <Username>")
        exit()

    # Make sure the server ip is valid (error message #1)
    try:
        serverIp = socket.inet_aton(sys.argv[1])
        serverName = str(sys.argv[1])
    except:
        print("\nerror: server ip invalid, connection refused.")
        exit()

    # Make sure the port number is valid (error message #2)
    try:
        port = int(sys.argv[2])
        if port < 0 or port > pow(2, 16) - 1:
            print("\nerror: server port invalid, connection refused.")
            exit()
    except ValueError:
        print("\nSpecified port is not a number")
        exit()

    username = sys.argv[3]
    # add username chacks here

    # Main client performance
    clientTalk(username, serverName, port)
