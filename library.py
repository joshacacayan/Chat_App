#!/usr/bin/env python3
import logging
import sys
import socket
import struct

#Name: Zachary Kociban
#Major: Computer Science
#Professor: Dr. Schwesinger
#Class: CSC328
#Semester: Fall 2023
#Due: 12/14/23
#Assignment: Final
#Description: Library containing functions useful for 
# the client and the server.


#   Name: reallyread - from Dr. Schwesinger project 5 solution
#   Description: Takes in the socket and the number of bytes to be 
#   read, continues reading until all bytes have been read
#   Parameters: s - the socket used for communication, n - the number of bytes to be read
#   Returns: bytes - The message in bytes
def reallyread(s, n):
    bytes = b''    
    while len(bytes) != n:
        curr_read = s.recv(n - len(bytes))
        bytes += curr_read
        if len(curr_read) == 0: break
    return bytes




#   Name: handleError
#   Description: Used to log error messages
#   Parameters: e - the error, message - optional error message
#   Returns: N/A
def handleError(e,message=""):
    e_message = f"Error: {e}"
    if message:
        e_message += f"\nReport: {message}"

    logging.error(e_message)
    exit()


#   Name: checkPort
#   Description: helper function for acceptArgs to check that the port is in the correct range
#   Parameters: port - the port to be checked
#   Returns: N/A
def checkPort(port):
    if (port <= 10000 or port >= 65535):
        exit("Must enter a number between 10000 and 65535")




#   Name: acceptArgs
#   Description: Function used to parse command line arguments in client and server
#   Parameters: argv - command line arguments
#   Returns: host - the host to connect to, port - the port to connect to
def acceptArgs(argv):
    if argv[0] == "./client":
        if len(sys.argv) != 3:
            exit("Usage: <host> <port>")
        else:
            host = sys.argv[1]
            port = int(sys.argv[2])
            checkPort(port)
            return host,port
    elif argv[0] == "./server":
        if len(sys.argv) != 2:
            exit("Usage: <port>")
        else:
            port = int(sys.argv[1])
            checkPort(port)
            return port
    else:
        print(argv[0])
        exit("Invalid arguments, must enter correct executable (./client) or (./server)")




