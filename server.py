#!/usr/bin/env python3

# Name:        Nathanael Garner
# Course:      CSC328
# Semester:    Fall 2023
# Assignment:  Final

import library
import sys
import socket
import threading
import time
import json
import signal

# Name:         validateNickname
# Desciption:   validates a nickname supplied by the client, looking for a unique nickname. Added nicknames are tracked by a dictionary of registered clients.
# Parmeters:    nickname - the nickname to validate
#               clientsocket - the socket descriptor of the current client
#               address - the address of the current client, for use with the log file
#               clientData - dictionary of registered clients
# Return:       none
def validateNickname(nickname, clientsocket, address, clientData):
    # check if nickname is unique
    for client in clientData["clients"]:
        if client["nickname"] == nickname:
            # nickname has been used already, so inform the client
            msgLen = 5
            clientsocket.sendall(msgLen.to_bytes(2, 'big') + b'RETRY')

            return
            
    # nickname has not been used, so inform the client
    msgLen = 5
    clientsocket.sendall(msgLen.to_bytes(2, 'big') + b'READY')

    # append new nickname to dictionary of registered clients
    clientData["clients"].append({"socket": clientsocket, "nickname": nickname})

    # record client connection in log file
    with open("log.txt", "a") as logs:
        logs.write("%d: %s connected at %s\n" % (time.time(), nickname, address[0]))

# Name:         closeClient
# Description:  removes a client from internal dictionary of registered clients and closes the corresponding socket descriptor
# Parameters:   nickname - the nickname of the client to close
#               clientData - dictionary of registered clients
# Return:       none
def closeClient(nickname, clientData):
    # close socket and remove from dictionary of registered clients
    for client in clientData["clients"]:
        if client["nickname"] == nickname:
            client["socket"].close()
            clientData["clients"].remove(client)

            # record disconnect to log
            with open("log.txt", "a") as logs:
                logs.write("%d: %s disconnected\n" % (time.time(), nickname))


# Name:         sendMessage
# Description:  sends a message that has been recieved by the client to all clients except current one
# Parameters:   message - the message to be sent, in JSON format with keys of nickname and message
#               clientsocket - the socket descriptor of the current client
#               clientData - dictionary of registerd clients
# Return:       none
def sendMessage(message, clientsocket, clientData):
    msg = json.loads(message)
    # print message to log file
    with open("log.txt", "a") as logs:
        logs.write("%d: %s sent \"%s\"\n" % (time.time(), msg["nickname"], msg["message"]))

    for client in clientData["clients"]:
        if client["socket"] != clientsocket:
            client["socket"].sendall(len(message).to_bytes(2, 'big') + message.encode())

# Name:         client
# Description:  does server operations for each connected client, including registering nicknames, closing clients, and sending messages
# Parameters:   clientsocket - the socket descriptor of the current client
#               address - the address of the current client, for use with the log file
#               clientData - dictionary of registered clients
# Return:       none
def client(clientsocket, address, clientData):
    # send hello message on connection
    msgLen = 5
    clientsocket.sendall(msgLen.to_bytes(2, 'big') + b'HELLO')

    while True:
        # read server message detailing action for server to take
        msgLen = int.from_bytes(library.reallyread(clientsocket, 2), 'big')
        msg = library.reallyread(clientsocket, msgLen).decode()
        
        # choose behavior depending on action recieved from the client
        
        # register client's nickname
        if msg.split(" ")[0] == "NICK":
            validateNickname(msg.split(" ", 1)[1], clientsocket, address, clientData)

        # close client
        elif msg.split(" ")[0] == "BYE":
            closeClient(msg.split(" ", 1)[1], clientData)

            # end loop of closed client
            break

        # send messages to other clients
        else:
            sendMessage(msg, clientsocket, clientData)

# Name:         runServer
# Descripton:   performs server operations, including setting up the server and sockets
# Parameters:   host - the host address for the server
#               port - the port for the server
# Return:       none
def runServer(host, port):
    # set up socket
    with socket.socket()  as s:
        s.bind((host, port))
        s.listen()

        # inform clients that server will shutdown, then wait 5 seconds
        def handler(signum, frame):
            try:
                for client in clientData["clients"]:
                    msgLen = 10
                    client["socket"].sendall(msgLen.to_bytes(2, 'big') + b'SHUTDOWN 5')
                time.sleep(5)
            except:
                pass

            s.close()
            exit(" The server has been shut down.")

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        # wipe log file
        open('log.txt', 'w').close()

        # keep track of clients
        clientData = {"clients": []}

        # create multiple processes for clients
        while True:
            clientsocket, address = s.accept()
            t = threading.Thread(target=client, args=[clientsocket, address, clientData])
            t.start()

if __name__ == "__main__":
    try:
        # acceptArgs validates user input and sets the port
        port = library.acceptArgs(sys.argv)
        runServer('',port)

    # TODO: use library code for error checking
    except OSError as err:
        library.handleError(err,f'Server: {err}')
