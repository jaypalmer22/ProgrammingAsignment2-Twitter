import socket
import sys
from _thread import *


# Username mapped to connection
user_connections = {}
# Username mapped to hashtag subscriptions (a set)
user_subs = {}
# Hashtag mapped to subscribed usernames (a set)
hashtag_subs = {}
# Current hashtags in use
curr_hashtags = set()
# User mapped to their history of received tweets
recv_history = {}
# User mapped to their history of sent tweets
send_history = {}
# Usernames of users who subscribe to #ALL
all_subs = set()


class TweetEvent:
    def __init__(self, sender, message, hashline):
        self.sender = sender
        self.message = message
        self.hashline = hashline

    def to_str(self):
        return self.sender + ": \"" + self.message + "\" " + self.hashline


def process_hashline(hashline):
    res = list()
    if len(hashline) > 15 or ' ' in hashline or '##' in hashline:
        return -1

    hash_units = hashline[1:len(hashline)].split("#")
    for i in range(0, len(hash_units)):
        curr = hash_units[i]
        if len(curr) == 0:
            return -1
        res.append(curr)
    return res if len(res) <= 5 else -1


def drop_user(username):
    # remove user from hashtag:subscriber mapping
    for h in user_subs[username]:
        hashtag_subs[h].remove(username)
        if len(hashtag_subs[h]) == 0:
            del hashtag_subs[h]
    # remove user from user:subscriptions mapping
    del user_subs[username]

    # remove user connection from current set
    del user_connections[username]

    # clear user received history
    del recv_history[username]

    # clear user sent history
    del send_history[username]

    # remove user from list of subscribers to #ALL
    if username in all_subs:
        all_subs.remove(username)


def broadcast(message, hashtags, tweet_event):
    # want to avoid sending tweet to some particular subscriber multiple times
    # in the case that they are subscribed to multiple hashtags in this tweet
    already_received = set()
    message = "-r " + message

    # Send to those who subscribe to #ALL
    for s in all_subs:
        if s not in already_received:
            send_tweet(s, message, tweet_event)
            already_received.add(s)

    # Send to everyone else who subscribes to relevant hashtag
    for i in range(0, len(hashtags)):
        subscribers = hashtag_subs.get(hashtags[i])

        # no current subscribers to the hashtag, nothing to do
        if subscribers is None or len(subscribers) == 0:
            continue

        # loop through subscribers, broadcasting tweet to them if they haven't already
        # received it
        for x in subscribers:
            if x not in already_received:
                send_tweet(x, message, tweet_event)
                already_received.add(x)


# just changed this to the tweet event str output...
def send_tweet(recipient, message, tweet_event):
    target_connection = user_connections.get(recipient)
    str = "-r " + tweet_event.to_str()
    target_connection.send(str.encode())
    recv_history[recipient].append(tweet_event)


def threaded_client(connection):
    validUser = False
    username = ""

    while True:
        msg = connection.recv(2048).decode()
        if not msg:
            break
        split_msg = msg.split(' ')
        command = split_msg[0]

        # Remove print debugs later
        print("Received: " + msg)

        # Processing commands
        ######################################################################################################
        #       Validating Username
        ######################################################################################################
        if command == "username":
            username_req = split_msg[1]

            # check that username is valid (only alphanumeric characters)
            if not username_req.isalnum():
                connection.send("iu error: username has wrong format, connection refused.".encode())

            # check that username is not already in use
            elif username_req in user_subs.keys():
                connection.send("iu username illegal, connection refused.".encode())

            # username request was valid
            else:
                validUser = True
                username = username_req
                connection.send("-s username legal, connection established.".encode())
                user_subs[username] = set()
                user_connections[username] = connection
                recv_history[username] = list()
                send_history[username] = list()

        ######################################################################################################
        #       Tweet Command
        ######################################################################################################
        elif validUser and command == "tweet":
            # Parsing by quotations, should only have 3 segments: <command> <message> <hashline>
            parsed = msg.split("\"")
            if len(parsed) != 3 or len(parsed[1]) == 0:
                connection.send("-f message format illegal.".encode())

            elif len(parsed[1]) > 150:
                connection.send("-f message length illegal, connection refused.".encode())

            else:
                hashtags = process_hashline(parsed[2].strip())
                if hashtags == -1:
                    connection.send("-f hashtag illegal format, connection refused.".encode())

                # Add any hashtags in the tweet which are not in curr_hashtags to curr_hashtags

                # Create new TweetEvent for user history
                tweet_event = TweetEvent(username, parsed[1], parsed[2].strip())

                # broadcast tweet to subscribers
                broadcast(parsed[1], hashtags, tweet_event)
                send_history[username].append(tweet_event)

        ######################################################################################################
        #       Subscribe Command
        ######################################################################################################
        elif validUser and command == "subscribe":
            # need to add check for split_msg length

            target_hashtag = split_msg[1].strip()
            target_hashtag = target_hashtag[1:len(target_hashtag)]

            # If user is already subscribed to 3 hashtags, they cannot subscribe to more
            count_subscribed = len(user_subs[username])
            if count_subscribed == 3:
                failure_message = "-f operation failed: sub #" + target_hashtag + " failed, already exists, " \
                                                                                 "or exceeds 3 limitation"
                connection.send(failure_message.encode())

            #  #ALL only counts as 1 hashtag according to pdf, so don't need to handle special case?
            else:
                user_subs[username].add(target_hashtag)

                if hashtag_subs.get(target_hashtag) is None:
                    hashtag_subs[target_hashtag] = set()
                hashtag_subs[target_hashtag].add(username)

                if target_hashtag == "ALL":
                    all_subs.add(username)

                # indicate success to client
                connection.send("-s operation success".encode())


            # Remove print debug later
            print(username + " current subscriptions:\n")
            for s in user_subs[username]:
                print(s)

        ######################################################################################################
        #       Unsubscribe Command
        ######################################################################################################
        elif validUser and command == "unsubscribe":
            target_hashtag = split_msg[1].strip()
            target_hashtag = target_hashtag[1:len(target_hashtag)]

            if target_hashtag == "ALL":
                if username in all_subs:
                    all_subs.remove(username)
                for h in user_subs.get(username):
                    hashtag_subs[h].remove(username)
                user_subs[username] = set()
                connection.send("-s operation success".encode())
            elif target_hashtag in hashtag_subs:
                hashtag_subs[target_hashtag].remove(username)
                user_subs[username].remove(target_hashtag)
                connection.send("-s operation success".encode())

        ######################################################################################################
        #       Timeline Command
        ######################################################################################################
        elif validUser and command == "timeline":
            tl_string = "-s "
            if recv_history.get(username) is not None:
                for e in recv_history[username]:
                    tl_string += e.to_str() + "\n"
            connection.send(tl_string.encode())

        ######################################################################################################
        #       Get Users Command
        ######################################################################################################
        elif validUser and command == "getusers":
            user_str = "-s "
            for u in user_connections.keys():
                user_str += u + "\n"
            connection.send(user_str.encode())

        ######################################################################################################
        #       Get Tweets Command
        ######################################################################################################
        elif validUser and command == "gettweets":
            query_user = split_msg[1]
            if query_user not in user_connections:
                connection.send("-f no user " + query_user + " in the system")
            else:
                twt_str = "-s "
                for t in send_history[query_user]:
                    twt_str += t.to_str() + "\n"
                connection.send(twt_str.encode())

        ######################################################################################################
        #       Exit Command
        ######################################################################################################
        elif command == "exit":
            # Only remove a registered username if connection is valid
            if validUser:
                drop_user(username)
            connection.send("-b bye bye".encode())
            exit_thread()

        # unrecognized command
        else:
            print("Server received unrecognized command")


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
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid number of parameters, use format python3 ttweetser.py <ServerPort>")
        exit()

    # Check for valid port number
    try:
        port = int(sys.argv[1])
        if port < 0 or port > pow(2, 16) - 1:
            print("error: server port invalid, connection refused.")
            exit()
    except ValueError:
        print("error: server port invalid, connection refused.")
        exit()

    run_server(port)
