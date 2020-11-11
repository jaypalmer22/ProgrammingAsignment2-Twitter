""" 
Jason Palmer
CS3251 Computer Netowrking I
September 22, 2020
PA1
ttweetcli.py
"""

from socket import *
import sys

# Perform client functionality
def clientTalk(serverName, port):

	# Throw exception if server not started 
	try:

		# Intitate socked using TCP protocol (second argument)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.settimeout(5)

		# Connect to server and send the flag and the tweet if upload
		clientSocket.connect((serverName, port))
		clientSocket.send(username.encode())

		# Response from server
		received = clientSocket.recv(1024)

		# Print server response based on flag
		if (sys.argv[1] == "-u"):
			print (received.decode())
		else:
			print ("\nTweet: {0}".format(received.decode()))

		clientSocket.close()

	# If server not connected
	except ConnectionRefusedError:
		print ("\nError: Server not found")

	# If server times out
	except timeout:
		print ("\nError: Timeout occured")	
	

# Initiate and error checking
if __name__ == '__main__':

	# Help menu to show script usage
	if (sys.argv[1] == "-h"):
		print ("Usage: python3 ttweetscli.py -u <serverIP> <serverPort> <username>\n")
		exit()

	# If not requesting help, check to see if there are either 4 or 5 parameters
	if len(sys.argv) != 4:
		print ("error: args should contain <ServerIP> <ServerPort> <Username>")
		exit()

	# Make sure the server ip is valid
	try:
		serverIp = inet_aton(sys.argv[1])
		serverName = str(sys.argv[1])
	except:
		print ("error: server ip invalid, connection refused.")
		exit()

	# Make sure the port number is valid
	try:
		port = int(sys.argv[3])
		if (port < 1024 or port > 65536):
			print ("error: server port invalid connection refused")
			exit()
	except ValueError:
		print ("error: server port invalid, connection refused")
		exit()

	username = sys.argv[4]

	if not username.isalnum():
		print ("error: username has wrong format, connection refused.")
		exit()

	# Main client performance
	clientTalk(serverName, port);
