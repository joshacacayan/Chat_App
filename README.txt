------------
ID BLOCK
------------
Names: Nathanael Garner, Josh Cacayan, Zachary Kociban
Major: Computer Science
Professor: Dr. Schwesinger
Class: CSC328
Semester: Fall 2023
Due: 12/14/2023
Assignment: Client-server chat project
Description: A chat server that allows multiple clients to connect and chat using 
distinct usernames.

------------
BUILD INSTRUCTIONS
------------
To build the client and server executables you must type "make all" into your command line.

Once the executables have been built, to run the server you must type....

./server <port>

With the port being the desired port to connect at.

To run the client you must type....

./client <host> <port>

To specify the correct host for the server, and the port to connect on.

------------
FILE/FOLDER MANIFEST
------------

-NetworkProgrammingProject : The repository holding all of the code

   - client.py : Allows creation of a client to connect to the chat server and chat

   - server.py : Chat server that waits for clients to connect, creating multiple threads to handle 
   several clients concurrently, allowing unique nicknames and simple UI.
       - logs.txt : Created by the server, a text file containing the logs of the chat room.

   - library.py : Library containing functions to be used in both the client and the server.
   Main purpose was for reading, but also used to accept arguments and handle errors.

   - Makefile : File that builds the executables and links to the library

------------
RESPONSIBILITY MATRIX
------------

-------------------------------------------------------------------------------|
         |                                                                     |
 Name    |                            Worked on                                |                                         
-------------------------------------------------------------------------------|                                                                               
Zach     | library.py, README.txt, Makefile, project design                    |                                                    
---------|---------------------------------------------------------------------|
Nathanael| server.py, README.txt, Makefile , project design                    |                                              
---------|---------------------------------------------------------------------|
Josh     | client.py, README.txt, Makefile, project design                     |
---------|---------------------------------------------------------------------|

------------
TASK + TIME
------------

Zach : Library functions -> 2 days

Nathanael : Accepting command line arguments -> 1 day
            Open respective sockets for client and server -> 1 day
            Authenticate nickname -> 2 days
            Check which clients are connected to the server -> 1 day
            Send message data back to corresponding client -> 3 days
            Inform clients when the server shuts down early -> 1 day


Josh : readHello function: This is first function executed for the client to read hello from the exsisting server -> 1 day
       ************************************************************************************************************************
       write_username: This is the function that tells the user what a person's username will be for the project. It will keep 
       looping until the user chooses a unique nickname -> 2 days
       *************************************************************************************************************************
       send_messages: This function allows the client to recieve and send messages to the server, in which the server will pass         down the messages to other clients. -> 3 days
       *************************************************************************************************************************
       Sending a goodbye message once the client sends \bye -> 1 day
      
------------
PROTOCOL
------------

The chat server used the pull-based method to accept clients. The server is set to run at a 
certain port at which clients can connect. 

Clients will enter the same port as the desired server, receiving a hello message on success.

Clients will then enter their Nickname for the server. The server contains a dictionary to ensure
that each client has a unique nickname associated with their socket descriptor, if the name is not unique the user will be prompted to enter another.

If the Nickname is succesfully entered, the client program will enter an infinite loop where it will 
determine if messages are coming from the server, or if there is user input. Messages from the server include
the messages from other clients and a server shutdown message. 

On the server-side, the server is created and waits in an infinite loop waiting for clients to connect. A 
log file and dictionary entry are created for each new client.

A new thread is then created in the server, which will allow multiple clients to run concurrently. Following this
the server will send a hello message to the client. 

The server will then look for actions recieved from the client to determine what to do next. If it is "NICK", then the nickname registration 
process occurs. If it is BYE, then the client is disconnecting. Otherwise it is a message from the client to be posted in the 
chat server.

If the server is closed early using a SIGINT or SIGTERM signal, the server informs the client by sending a "SHUTDOWN 5" signal, telling the
client that the server will be shutdown in 5 seconds.

The client can disconnect from the server by using the signal handler and pressing ctrl-c, as well as an input message of /BYE.

------------
ASSUMPTIONS
------------

Zach -> I had originally assumed that more functions would be shared 
between the client and server. I was correct with the assumption of how 
the clients would use the server to communicate with each other via the 
chat room. 

Nathanael -> For running the server, it is assumed that the server will be shut down only after connected clients have choosen a nickname. Additonally, the only way to exit the client program would be a /BYE command or a SIGINT/SIGTERM signal.

Josh -> I would assume that in order the client to send and recieve messages at the same time, I thought that I would need to run processes and another socket on the client and server for those to work. I was wrong in believing that i needed another socket for the client to read and print at the same time, as I only needed if else statements in order for the client to know when it is time to print and time to read. 

------------
DISCUSSION
------------

Zach -> Overall I was a bit withdrawn from the core of the project. The main challenge I faced 
was when developing the acceptArgs function, how I would get it to properly differentiate between
the client and the server. The solution was to parse the argv list to obtain the 
first argument which would tell me which file was currently being used.

Nathanael -> Generally, I had a clear idea on what to do at each step, but I had run into unexpected problems that halted progress. Sending and
recieving data worked fine each time, however difficulty occured when discerning when to properly close certain client sockets. At one point, I had
clientsocket closing with a with statement, but this would close the socket at an inappropriate time. Eventually, I ended up closing the socket in the
closeClient function, which in retrospect, should have been the obvious thing to do from the start. Additionally, when making the server,
I initially opted for using processes, but I had trouble keeping track of the socket object attached to a given nickname. To solve this, I opted to use
threads instead and kept track of the client socket object and its nickname using a dictionary of connected clients.

Josh -> I was happy on much I contributed to the project, as I was able to finish a whole client program. The hardest part of the program was sending and recieving messages, as it involves using code that I have not used before in a CSC328 project. 
I was correct with this assumption that I needed to use code that I haven't used before with the previous projects to do the final project, 
as I was searching up a lot of resources on the internet in order to make the client recieve and send messages at the same time. 
However, I owe a lot of thanks to our team leader Nathanael, who created meetings for us to help each other run the project.

------------
STATUS
------------
All of the files compile, as well as run doing its accomplished task. 
Client can send messages to the server, as the client sends a \BYE whenever it wants to turn off or any other message for another user to read.
The client program successfully obtains messages from the server, knowing when the server shuts down as well as getting messages from the server from other clients.
The clients shut down effectively after 5 seconds of the server shutting down, however, if the client has not inputted a username yet, the client and the server fail to shut down.
