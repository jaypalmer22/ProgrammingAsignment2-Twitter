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
		msg = sys.argv[1]

		# Add the tweet if the flag is upload
		if (sys.argv[1] == "-u" and len(sys.argv[4]) < 150 and len(sys.argv[4]) > 0):
			msg += sys.argv[4]

		# Check if tweet is less than 150 characters
		if (sys.argv[1] == "-u" and len(sys.argv[4]) > 150):
			print("\nError: Tweet is greater than 150 characters")
			exit()

		# Intitate socked using TCP protocol (second argument)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.settimeout(5)

		# Connect to server and send the flag and the tweet if upload
		clientSocket.connect((serverName, port))
		clientSocket.send(msg.encode())

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
		print ("Usage: python3 ttweetscli.py -u <serverIP> <serverPort> \"Message\" \npython3 ttweet.py -d <serverIP> <serverPort>\n")
		exit()

	# If not requesting help, check to see if there are either 4 or 5 parameters
	if (len(sys.argv) < 4 or len(sys.argv) > 5):
		print ("\nInvalid parameters, use -h tag for usage")
		exit()

	# Make sure the flags are either -u or -d
	if (sys.argv[1] != "-u" and sys.argv[1] != "-d"):
		print ("\nIncorrect flags, use -u or -d")
		exit()

	# If the flag is -u, make sure there are 5 parameters
	if (sys.argv[1] == "-u" and len(sys.argv) != 5):
		print ("\nIncorrect number of parameters for upload")
		exit()

	# If the flag is -d, make sure there are 4 parameters
	if (sys.argv[1] == "-d" and len(sys.argv) != 4):
		print("\nIncorrect number of parameters for download")
		exit()

	# Make sure the server ip is valid
	try:
		serverIp = inet_aton(sys.argv[2])
		serverName = str(sys.argv[2])
	except:
		print ("\nInvalid server ip address")
		exit()

	# Make sure the port number is valid
	try:
		port = int(sys.argv[3])
		if (port < 13000 or port > 14000):
			print ("\nPlease specify a port between 13000 and 14000")
			exit()
	except ValueError:
		print ("\nSpecified port is not a number")
		exit()

	# Main client performance
	clientTalk(serverName, port);
