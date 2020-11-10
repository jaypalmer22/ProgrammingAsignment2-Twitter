import socket
import sys


def clientTalk(username, host, port):
    ClientSocket = socket.socket()

    try:
        ClientSocket.settimeout(5)
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    nameString = "username " + username
    ClientSocket.send(nameString.encode())

    # initial loop for validating username before entering command input loop
    while True:
        # Response from server, decode() removes "b'" from beginning of string
        received = ClientSocket.recv(1024).decode()

        # Case: Username was invalid, will close the connection
        if received[0:2] == "-f":
            print(received[3:len(received)])
            ClientSocket.send("exit".encode())
            ClientSocket.close()
            return

        # Case: Username validated, will proceed to command loop
        elif received[0:2] == "-s":
            print()
            break

        # Case: Server sent back message which didn't start with result flag
        else:
            print("Server sent unknown result flag? Check username validation loop")

    # Command input loop
    while True:
        Input = input()
        ClientSocket.send(str.encode(Input))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

    ClientSocket.close()    # this was included in template?


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
