import socket
import re
import os
import threading
from screen import * # imports everything from screen

stopnow = 0

def connect(connection):
    try:
        mydeviceip = input("Enter IP Address: ")

        # make sure IP address is formatted correctly
        if len(re.findall(r"\.", mydeviceip)) != 3:
            print("\nIP address not formatted correctly. Please try again.\n")
            exit()

        # make sure IP is made up of numbers
        num = mydeviceip.split(".")
        for i in num:
            try:
                i = int(i)
                if i > 255:
                    print("\nIP address not formatted correctly. Please try again.\n")
                    exit()
            except ValueError:
                print("\nIP address not formatted correctly. Please try again.\n")
                exit()

        portnum = input("Port number: ")
        connection.connect((mydeviceip, int(portnum)))
    except BrokenPipeError:
        print("\nFailed to connect. Try again.\n")
        exit()
    except ConnectionRefusedError:
        print("\nFailed to connect. Try again.\n")
        exit()
    except socket.gaierror:
        print("\nFailed to connect. Try again.\n")
        exit()
    except ValueError:
        print("\nFailed to connect. Try again.\n")
        exit()

def receivemessage(screen, username, connection):
    global stopnow
    while True:
        try:
        # receive a message
            message = connection.recv(4096)
            # convert the byte into a string
            message = str(message, 'utf-8')
        except ConnectionResetError:
            screen.close()
            print("\nConnection ended! Hope you had a nice conversation!\n")
            os._exit(1)
        
        if "Connection ended! Hope you had a nice conversation!" in message:
            stopnow = 1
            screen.close()
            print(message)
            sendmessage(screen, username, connection)
        else:
            # print out the message that was sent by the other user
            screen.showmessage(message, 1)

def sendmessage(screen, username, connection):
    global stopnow
    while True:
        if stopnow == 1:
            os._exit(1)
        else:
            # send a message
            message = screen.getinput()
            realmessage = username + ": " + message
            screen.showmessage(realmessage, 2)
            connection.sendall(bytes(realmessage, 'utf-8'))

def mainfunction():
    # ask user for their username
    username = input("Before connecting to the server, please enter your username: ")

    # make sure username is not empty:
    while True:
        if not username:
            username = input("Enter a proper username. Please try again: ")
        else:
            break

    # create a socket for client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        # connect to the server
        connect(connection)
        
        # create a screen
        screen = Screen()

        # tell both users they are ready to talk
        connection.sendall(b'Connected! You are ready to talk.')
        screen.showmessage('Connected! You are ready to talk.', 3) # change it to show on screen on this side as well
        
        threading.Thread(target=receivemessage, args=[screen, username, connection]).start()
        sendmessage(screen, username, connection)

mainfunction()