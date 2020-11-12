""" 
Jason Palmer
CS3251 Computer Netowrking I
November 11, 2020
PA2
ttweetsrv.py
"""

from socketserver import ThreadingMixIn
from socket import *
import sys
import threading

Users = {}
num_users = 0

class User:
	def __init__(self, username, thread, socket):
		self.username = username
		self.hashtags = set()
		self.thread = thread
		self.timeline = []
		self.tweets = []
		self.socket = socket

def Tweet(username, message):
	try:
		split = message.split(' ')
		msg = split[1]
		hashtag = split[2]
	except ValueError:
		resp = "error: invalid tweet command"
		return resp

	if len(msg) <= 2:
		resp = "message format illegal."
		return resp

	if msg[0] != "\"" or msg[-1] != "\"":
		resp = "message format illegal."
		return resp

	msg = msg[1:-1]

	if len(msg) > 150:
		resp = "message length illegal, connection refused."
		return resp

	hashtags = hashtag[1:].split('#')

	for tag in hashtags:
		if len(tag) <= 0 or tag == "ALL" or not tag.isalnum():
			resp = "hashtag illegal format, connection refused."
			return resp

	print (hashtags)
	twit = username + ': "' + msg + '" ' + hashtag

	for user in Users.values():
		for tag in hashtags:
			if tag in user.hashtags or "ALL" in user.hashtags:
				user.socket.send((' ' + username + ' "' + msg + hashtag).encode())
				print (twit)
				user.timeline += twit

	Users[username].tweets += twit

	return ''

def subscribe(username, message):
	# Split command into 
	msg = message.split(' ')

	hashtag = msg[1]
	words = hashtag[1:]
	if len(msg) != 2:
		resp = "message format illegal."
		return resp

	if hashtag[0] != "#" or len(hastag) < 2 or not words.isalnum():
		resp = "hashtag illegal format, connection refused."
		return resp

	if words in Users[username].hashtags or len(Users[username].hashtags) >= 3:
		resp = "operation failed: sub " + hashtag + " failed, already exists or exceeds 3 limitation"
		return resp

	Users[username].hashtag.add(words)
	resp = "operation success"
	return resp

def unsubscribe(username, message):
	msg = message.split(' ')

	hashtag = msg[1]
	words = hashtag[1:]
	if len(msg) != 2:
		resp = "message format illegal"
		return resp

	if hashtag[0] != "#" or len(hashtag) < 2 or not words.isalnum():
		resp = "hashtag illegal format, connection refused"
		return resp

	if words == "ALL":
		Users[username].hashtags.clear()
		resp = "operation success"
		return resp

	if words not in Users[username].hashtags:
		resp = "hashtag doesn't exit, connection refused"
		return resp

	Users[username].hashtags.remove(words)
	resp = "operation success"
	return resp

def newUser(socket, addr, username):
	while True:
		message = socket.recv(1024)[1:]
		message = message.decode()
		cmd = message.split(' ')[0]

		if cmd == "tweet":
			resp = tweet(username, message)
		elif cmd == "subscribe":
			resp = subscribe(username, message)
		elif cmd == "unsubscribe":
			resp = unsubscribe(username, message)
		elif cmd == "getUsers":
			resp = getUsers()
		else:
			resp = "Unrecognized command"

		for start in range(0, len(resp), 1023):
			end = start + 1023
			# If there's more to send, prepend +
			if len(resp) >= end:
				prefix = '+'
				# If this is the last message, prepend space
			else:
				prefix = ' '
			socket.send((prefix + resp[start:end]).encode())

	socket.close()

def getUsers():
	for i in Users.keys():
		print ("\n" + i)
	return


def serverTalk (port):

	global num_users

	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Bind to the port number
	serverSocket.bind(("", port))
	serverSocket.listen(1)
	print ("The server is ready to receive at port: ", port)

	# Begin infinite loop
	while True:
		# Wait for client request
		connectionSocket, addr = serverSocket.accept()
		if (num_users < 5):

			# Message from client 
			username = connectionSocket.recv(1024).decode()
			if username not in Users.keys():
				num_users += 1
				print ("User number ", num_users, " has connected.")
				thread = threading.Thread(target=newUser, args=(connectionSocket, addr, username)).start()
				connectionSocket.send(" username legal, connection established.".encode())
				Users[username] = User(username, thread, connectionSocket)
			else:
				connectionSocket.send(" username ilagal, connection refused.".encode())
				connectionSocket.close()
		else:
			print ("Too many clients")
			connectionSocket.send(" Too many clients".encode())
			connectionSocket.close()
			
	serverSocket.close()

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