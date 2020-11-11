import socket
import sys
import _thread


def on_new_client(clientsocket,addr):
    while True:

        #todo implement server side
        try:
            #data = clientsocket.recv(1024)






        except Exception as e:
            print(str(e))
            break

    clientsocket.close()


###################
#start of program
###################

#checks appropriate parameters
if sys.argv < 2 or sys.argv > 2:
    exit(error="error: args should contain <serverPort>")


#setup socket
port = int(sys.argv[1])
s = socket.socket()
host = ''
s.bind((host, port))
s.listen(5)


print("Server Started")


while True:
    #searches for connections
    conn, address = s.accept()

    #creates a new thread for each new connection
    print('Got connection from: ', address)
    _thread.start_new_thread(on_new_client, (conn, address))

