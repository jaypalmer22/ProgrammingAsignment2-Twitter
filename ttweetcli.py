import socket
import sys


def clientTalk(username, host, port):
    ClientSocket = socket.socket()

    try:
        #ClientSocket.settimeout(5)
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

    # Command input loop
    while True:
        Input = input()
        ClientSocket.send(str.encode(Input))
        received = ClientSocket.recv(1024).decode()

        # Case: Command failed
        if received[0:2] == "-f":
            print(received[3:len(received)])
            continue

        # Case: Tweet success, don't print anything?
        if received[0:2] == "-t":
            continue

        # Case: Safe exit
        if received[0:2] == "-q":
            print(received[3:len(received)])
            return()

    ClientSocket.close()


if __name__ == '__main__':
    # Make sure parameter count is correct (error message #5)
    if len(sys.argv) != 4:
        print("\nInvalid number of parameters, use <ServerIP> <ServerPort> <Username>")
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
