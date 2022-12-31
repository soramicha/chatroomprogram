import socket
import threading
import os
from screen import *

# create a socket, which is an endpoint of a two-way communication link
# use socket.AF_INET6 for IPV6 and socket.DGRAM for UDP connections
# we need to create a connection using TCP (Transmission Control Protocol)
myend = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET means I use IPV4 and SOCK_STREAM means I'm using TCP
stat = 0 # zero means no one said bye yet

def getipaddress():
    # get ip address of the device by opening a temporary socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temporarysocket:
        temporarysocket.connect(("8.8.8.8", 80))
        return temporarysocket.getsockname()[0]

def binding(mydeviceip):
    for port in range(2000, 65535):
        try:
            myend.bind((mydeviceip, port))
        except:
            continue
        else:
            return int(port)

def receivemessage(screen, username, connection):
    while True:
        # if there's a message to receive, recieve it
        message = connection.recv(4096) # returns in bytes
        message = str(message, 'utf-8')

        if "Connected! You are ready to talk" in message:
            screen.showmessage(message, 3)
        else:
            screen.showmessage(message, 2) # the number represents the number of bytes it can receive

        if error(screen, connection, message) == 0:
            sendmessage(screen, username, connection)

def sendmessage(screen, username, connection):
    while True:
        if stat == 2:
            os._exit(1)
        else:
            # send a message
            message = screen.getinput() # receive in bytes
            realmessage = username + ": " + message
            screen.showmessage(realmessage, 1)
            connection.sendall(bytes(realmessage, 'utf-8')) # convert string into bytes

        if error(screen, connection, message) == 0:
            os._exit(1)

def error(screen, connection, message):
    global stat
    if "bye" in message:
        stat += 1
        if stat == 2:
            screen.close()
            print("\nConnection ended! Hope you had a nice conversation!\n")
            connection.sendall(b"\nConnection ended! Hope you had a nice conversation!\n")
            return 0
    return 1

# check if username isn't empty, return False if it is empty, otherwise return True
def checkusername(username):
    if not username:
        return False
    else:
        return True

def main():
    # ask user for their username
    username = input("Before starting a connection, please enter your username: ")

    while checkusername(username) == False:
        username = input("Enter a proper username. Please try again: ")

    # get ip address
    mydeviceip = getipaddress()

    # next, find my port number and bind it (max possible port numbers is up to 65535, 0 - 1023 are already well known ports)
    portnum = binding(mydeviceip)

    # now we listen for any connections
    myend.listen()

    # create a screen
    screen = Screen()
    screen.messageshowstatus(1) # 1 = no echo

    # wait for a connection
    screen.showmessage("Waiting for a connection..." + str(mydeviceip) + ":" + str(portnum), 3)
    connection, theiraddress = myend.accept() # the connection is a different socket and port number

    screen.messageshowstatus(2) # 2 = echo

    with connection:
        # make two new threads, one for recieving messages, one for sending messages
        threading.Thread(target=receivemessage, args=[screen, username, connection]).start()
        sendmessage(screen, username, connection)

if __name__ == "__main__":
    main()