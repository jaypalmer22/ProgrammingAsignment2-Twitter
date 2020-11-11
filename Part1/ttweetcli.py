import sys
import socket


#sets system arguments as variable arg
arg = sys.argv

#checks for correct number of arguments
if(len(arg) == 4):

    host = arg[1] #ip-address
    serverPort = int(arg[2]) #port number
    username = arg[3] #username


    #checks that username consists of alphabet and number characters only
    if (not username.isalnum()):
        exit(code='error: username has wrong format, connection refused.')


    #attempts to connect to server using ip-address and port number
    try:
        s = socket.socket()
        s.connect((host, serverPort))
    except ConnectionRefusedError as ce:
        exit('error: server port invalid, connection refused.')  # invalid port number
    except TimeoutError as te:
        exit('error: server ip invalid, connection refused.')  # invalid sever ip
    except Exception as e:
        exit(code='Connection Error') #any misc errors not caught (something went wrong if you see this error)


    #now that a server connection is made, checks that the username is valid (not already in use)
    try:
        #todo implement client side here





    except Exception as e:
        exit(code=e)

else:
    exit(code='error: args should contain <ServerIP> <ServerPort> <Username>')

