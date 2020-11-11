# CS 3251 Programming Assignment I

Name: Jason Palmer  
Email Address: jpalmer48@gatech.edu  

Class Name: CS 3251 Computer Networking I  
Date: September 22, 2020  
Assignment Title: Programming Assignment I  

NOTE: I used python 3 in the design of my protocol and python 3 did indeed work on shuttle1. I sftp the files onto the shuttle machine and ran them there with python3 (using the methods documented in this file). It worked fine. 

**ttweetsrv.py**
This file executes the server for our Twitter application. When this file is executed with a given port, it performs error checking to make sure the correct number and format of parameters are given. This includes a correct port. Assuming the command is correct, it responds to the user, letting them know that the server is running and ready to be used. When the user uploads a tweet from the client end, the tweet is kept in the server and when downloaded, returns it back to the user. See below for how to call from the command line.

**ttweetcli.py**
This file executes the client end of our Twitter application. When this file is executed, it performs error checking to make sure the correct number and format of parameters are given. This includes the correct flag, a proper ip address, the matching port and a correctly formated message (if uploading). Assuming the command is correct, it determines whether the user is uploading or downloading a tweet based on the given flag. If uploading, it sends the tweet to the server in which the server responds with a confirmation message. If downloading, it sends a download request to the server in which the server responds by sending over the message.

**References**  
Used the textbook examples of TCPServer.py and TCPClient.py and python library references for function usage

**Compilation and Script Execution**
1. Make sure you are in the correct directory with the two files
2. Initilize the server by running python3 ttweetsrv.py <"serverPort"> (serverPort must be between 13000 and 14000 inclusive)
3. You should receive a confirmation message; the server is ready to tweet
4. Open a new terminal to begin uploading and downloading tweets
5. To upload, run the command python3 ttweetsrv.py -u <"serverIP"> <"serverPort"> "*your tweet here*"
6. To download, run the command python3 ttweetcli.py -d <"serverIP"> <"serverPort">
7. Close the server when you have finished tweeting by using escape sequence Ctrl-C in the server terminal
8. If you run into trouble, follow the instructions in error messages or run the command python3 ttweetsrv.py -h or ttweetcli.py -h

NOTE: You can only store one message on the server at a time (also only one client at a time)

NOTE: Server Port must be in between 13000 and 14000 inclusive

**Test Output**

root@LAPTOP-########:/mnt/c/Users/jason/Documents# python3 ttweetcli.py -u 127.0.0.1 13000 "If there ever comes a day when we can't be together, keep me in your heart, I'll stay there forever."

Tweet uploaded  
root@LAPTOP-########:/mnt/c/Users/jason/Documents# python3 ttweetcli.py -d 127.0.0.1 13000

Tweet: If there ever comes a day when we can't be together, keep me in your heart, I'll stay there forever.

*See Sample.txt for more detailed outputs*

**Protocol Description**

When the server establishes with a specified port number, it begins to wait for a response. It should never shut down unless forced closed. A TCP socket is used to transfer tweets to and from the server. When the server recieves a request, it decodes it to determine whether it is an upload or download request. If it is an upload request, it takes the tweet and stores it locally. It then responds, letting the client know that the tweet was successfully received. If it is an download request, it returns the tweet being stored. If there is no tweet, then it returns an empty response. 

Error checking includes making sure we have the correct number of parameters (2 for the server and 4/5 for the client). On the server side, we make sure that the port number is between 13000 and 14000, based on the assignment instructions. We also make sure the server port is indeed an actual number. On the client side, we make sure the flag is either -d or -u, we make sure the ip address is the correct format (ipV4) and that the server port is an actually number. If the server port specified on the client side doesn't match the port used to initialize the server, an error is thrown. Finally, we make sure the message is not over 150 characters long.

When we send a message to the server, it is sent in UTF-8 encoding. The server decodes it back into string format, parses it to determine the desired instruction and then sends the proper decoded response. When we print the message, it is decoded back into string format. 

**Errors**

- "Invalid number of parameters": Invalid number of parameters
- "Plese specify a port": Port not in between 13000 and 14000
- "Specified port is not a number": Port not a number
- "Incorrect flags": Didn't have flags "-u or -d"
- "Incorrect number of parameters for upload or download": upload (5), download (4)
- "Invalid server IP address": Invalid IP address format specified
- "Error: Server Not found": Tried to upload or download when server was off or port's don't match