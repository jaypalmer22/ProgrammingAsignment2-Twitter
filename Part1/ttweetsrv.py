""" 
Jason Palmer
CS3251 Computer Netowrking I
September 22, 2020
PA1
ttweetsrv.py
"""

from socket import *
import sys

def serverTalk(port):

	# Start socket on server end
	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Bind to the port number
	serverSocket.bind(("", port))
	serverSocket.listen(1)
	print ("The server is ready to receive at port: ", port)
	tweet = ""

	# Begin infinite loop
	while True:
		# Wait for client request
		connectionSocket, addr = serverSocket.accept()

		# Message from client 
		msg = connectionSocket.recv(1024).decode()
		
		# If client sent -u flag, send a confirmation that tweet is uploaded
		if msg[0:2] == "-u":
			connectionSocket.send("\nTweet uploaded".encode())
			tweet = msg[2:]

		# If client sent -d flag, respond with the tweet
		else:
			connectionSocket.send(tweet.encode())
			
		connectionSocket.close()

if __name__ == '__main__':

	# Check for valid number of parameters
	if (len(sys.argv) != 2):
		print ("Invalid number of parameters, use format python3 ttweetsrv.py <ServerPort>")
		exit()

	# Help menu
	if (sys.argv[1] == "-h"):
		print ("Usage: python3 ttweetsrv.py <ServerPort>\n")
		exit()

	# Check for valid port number
	try:
		port = int(sys.argv[1])
		if (port < 13000 or port > 14000):
			print ("Please specify a port between 13000 and 14000")
			exit()
	except ValueError:
		print ("Specified port is not a number")
		exit()

	serverTalk(port);

