#!/usr/bin/env python3
import sys
import socket
import select
import library
import json
import signal
#       Filename: client.py
#       Author:  Josh Cacayan
#       Creation Date:11/21/2023
#    	Deadline: 12/14/2023
#   	Date of Submission: 12/13/2023
#    	Course: 	CSC 328 Fall 2023
#    	Professor:   	Dr. Schwesinger
#    	Assignment:     Final Project (Network Chat)
#       Purpose: 
#       This project creates a network chat between multiple clients connected to a server.
#       This part of the project is the client, which recieves and sends messages to other clients.

#       Function name: shutDownProcess
#       Description: This function is for the client to shut down the server.
#       Parameters: sock_server
#       sock_server- This is used to reference the current socket.
#       decodedPacket - Packet from the server side
#       Returns: none

#       Function name: shutDownProcess
#       Description: This function is for the client to shut down.
#       Parameters: sock_server, decodedPacket, username
#       sock_server- This is used to reference the current socket.
#       username - This is the current username.
#       decodedPacket - this is the decoded packet.
#       Returns: none


def shutDownProcess(sock_Server, decodedPacket,username):
    print("Server will be shutting down in " + str(decodedPacket.split(" ")[1] + " seconds."))
    message = "BYE " + username
    sock_Server.sendall(len(message).to_bytes(2, 'big') + message.encode("ascii"))
    print("Connection Closed")
    exit()
    
#       Function name: readMessages
#       Description: This function is for the client to read messages from the server.
#       Parameters: sock_server
#       sock_server- This is used to reference the current socket.
#       Returns: none

def readMessages(sock_Server):
     byteObject= library.reallyread(sock_Server,2)
     x= int.from_bytes(byteObject,'big',signed = False)
     message = library.reallyread(sock_Server,x)
     decodedPacket = message.decode('utf-8')
     return decodedPacket
#       Function name: readHello
#       Description: This function is for the client to accept the hello message from the server.
#       Parameters: sock_server
#       sock_server- This is used to reference the current socket.
#       Returns: none

def readHello(sock_Server):
    while(True):  
        decodedPacket = readMessages(sock_Server)
        if (decodedPacket != "HELLO"):
            print("Incorrect message")
        else:
            print(decodedPacket)
            break
            
#       Function name: write_username
#       Description: This function is for the client to pick out a username, and loops until the username is unique.
#       Parameters: sock_server
#       sock_server: Used to access the current socket that is connected to the server
#       Returns: username decodedPacket.split("")[0]
#       username: the accepted username

def write_username(sock_Server):
     while(True):
        username = "NICK " +  input("What is your username? ")
        sock_Server.sendall(len(username).to_bytes(2, 'big') + username.encode('ascii'))
        username = username.split("NICK ", 1)[1]
        decodedPacket = readMessages(sock_Server)
        if (decodedPacket.split(" ")[0] == "SHUTDOWN"):
            shutDownProcess(sock_Server, decodedPacket,username)
        elif (decodedPacket == "RETRY"):
            print("Not a unique username, please choose another one")
        elif (decodedPacket == "READY"):
            print("***************************************")
            print("Welcome to the Network Chat server.")
            print("Type /BYE in order to leave the chat!")
            print("Feel Free to send any messages!")
            print("*************************************** \n")
            return username
                
#       Function name: send_messages
#       Description: This function is for the clients to send messages to the other client using the server.
#       sock_server: Used to access the current socket that is connected to the server
#       username: the client's picked username
#       Returns: none
#       none- used to end the function


def send_messages(sock_Server,username):
   while (True):
        sockets = [sys.stdin,sock_Server]
        sockets_list, _, _ = select.select(sockets, [], []) 
        for sock in sockets_list:
            if (sock == sock_Server):  
                decodedPacket = readMessages(sock_Server)
                if (decodedPacket.split(" ")[0] == "SHUTDOWN"):
                    shutDownProcess(sock_Server, decodedPacket,username)
                else:
                    decodedPacket = json.loads(decodedPacket)
                    print("***********************************************************")
                    print(f"{decodedPacket['nickname']} > {decodedPacket['message']}")
                    print("***********************************************************")
            else:
                message = input()
                if (message== "/BYE"):
                    message = "BYE " + username
                    sock_Server.sendall(len(message).to_bytes(2, 'big') + message.encode("ascii"))
                    print("Connection Closed")
                    return None
                messageData = json.dumps({ 
                "nickname": username, 
                "message": message
                })
                sock_Server.sendall(len(messageData).to_bytes(2, 'big') + messageData.encode("ascii"))

#       Function name: main
#       Description: This function is used to execute the whole client program.
#       1. accepts the command line arguements for the  program
#       2. opens the socket
#       3. checks for a unique username
#       4. sends messages
def main():
    server,port = library.acceptArgs(sys.argv)
    username = ""

    library.checkPort(port)
    try:
        with socket.socket() as sock_Server:
            sock_Server.connect((server, port))

            # shut down client
            def handler(signum, frame):
                message = "BYE " + username
                sock_Server.sendall(len(message).to_bytes(2, 'big') + message.encode("ascii"))
                print(" Connection Closed")
                exit()

            signal.signal(signal.SIGINT, handler)
            signal.signal(signal.SIGTERM, handler)

            readHello(sock_Server)
            username = write_username(sock_Server)
            send_messages(sock_Server, username)
    except socket.error as err:
        print("Socket Failed, Please try again.")
        exit(-1)
    except OSError as e:
        exit(f'{e}')
        
    
if __name__ == "__main__":
    main()        
