""" 
Jason Palmer
CS3251 Computer Netowrking I
September 22, 2020
PA1
ttweetsrv.py
"""

from socket import *
import sys

Users = dict()

class User:
	def __init__(self, username):
		self.username = username
		self.hashtags = set()



def subscribe(username, message):
	# Split command into 
	msg = message.split(' ')

	hashtag = msg[1]
	words = hashtag[1:]
	if len(msg) != 2:
		print ("message format illegal.")
		exit()

	if hashtag[0] != "#" or len(hastag) < 2 or not words.isalnum():
		print ("hashtag illegal format, connection refused.")
		exit()

	if words in Users[username].hashtags or len(Users[username].hashtags) >= 3:
		print ("operation failed: sub " + hashtag + " failed, already exists or exceeds 3 limitation")
		exit()

	Users[username].hashtag.add(words)
	print ("operation success")
	return

def unsubscribe(username, message):
	msg = message.split(' ')

	hashtag = msg[1]
	words = hashtag[1:]
	if len(msg) != 2:
		print ("message format illegal")
		exit()

	if hashtag[0] != "#" or len(hashtag) < 2 or not words.isalnum():
		print ("hashtag illegal format, connection refused")
		exit()

	if words == "ALL":
		Users[username].hashtags.clear()
		print ("operation success")
		return

	if words not in Users[username].hashtags:
		return

	Users[username].hashtags.remove(words)
	print ("operation success")
	return

def getUsers(username, message):
	for i in Users.keys():
		print ("\n" + i)
	return


def ServerTalk (port):

	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Bind to the port number
	serverSocket.bind(("", port))
	serverSocket.listen(1)
	print ("The server is ready to receive at port: ", port)

	# Begin infinite loop
	while True:
		# Wait for client request
		connectionSocket, addr = serverSocket.accept()

		# Message from client 
		username = connectionSocket.recv(1024).decode()
		
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
		print ("error: args should contain <ServerPort>")
		exit()

	# Help menu
	if (sys.argv[1] == "-h"):
		print ("Usage: python3 ttweetsrv.py <ServerPort>\n")
		exit()

	# Check for valid port number
	try:
		port = int(sys.argv[1])
		if (port < 13000 or port > 14000):
			print ("error: server port invalid, connection refused.")
			exit()
	except ValueError:
		print ("error: server port invalid, connection refused.")
		exit()

	serverTalk(port);

