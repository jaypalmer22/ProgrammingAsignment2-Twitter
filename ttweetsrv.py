import socket
import os
import sys
from _thread import *


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()


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