import socket
import os
import sys
from _thread import *

# Username: Subscribed hashtags
user_subs = {"Joseph": set()}


def threaded_client(connection):
    validUser = False
    username = ""

    while True:
        msg = connection.recv(2048).decode()
        if not msg:
            break
        split_msg = msg.split(' ')
        command = split_msg[0]

        # Process command
        # Case: User has not yet validated username
        if command == "username":
            username_req = split_msg[1]

            # check that username is valid (only alphanumeric characters)
            if not username_req.isalnum():
                connection.send("-f error: username has wrong format, connection refused".encode())

            # check that username is not already in use
            if user_subs.get(username_req) is not None:
                connection.send("-f username illegal, connection refused".encode())

            # username request was valid
            else:
                validUser = True
                username = username_req
                connection.send("-s username legal, connection established".encode())
                # create new set to hold the user's hashtag subscriptions
                user_subs[username_req] = set()

        if command == "tweet":
            x = 1
        elif command == "subscribe":
            x = 2
        elif command == "unsubscribe":
            x = 3
        elif command == "timeline":
            x = 4
        elif command == "getusers":
            x = 5
        elif command == "gettweets":
            x = 6
        elif command == "exit":
            # Check that this is subtracting from the thread count
            # Only remove a registered username if connection is valid
            if validUser:
                del user_subs[username]
            connection.close()
            return
        else:
            # command given was invalid
            x = 8


def run_server(port):
    ServerSocket = socket.socket()
    host = '127.0.0.1'
    ThreadCount = 0
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Waitiing for a Connection..')
    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("Invalid number of parameters, use format python3 ttweetsrv.py <ServerPort>")
        exit()

    # Check for valid port number
    try:
        port = int(sys.argv[1])
        if port < 0 or port > pow(2, 16)-1:
            print("\nerror: server port invalid, connection refused.")
            exit()
    except ValueError:
        print("\nerror: server port invalid, connection refused.")
        exit()

    run_server(port)