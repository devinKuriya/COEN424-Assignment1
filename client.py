#Devin Kuriya 40111954
#Client Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

import abc
from http import client
from pydoc import cli
from socket import *
import os
import time

userInput_ServerName=input('Please input an ip address(localhost): \n')
userInput_PortNumber=input('Please input a port number(12000): \n')


serverName=userInput_ServerName
serverPort=int(userInput_PortNumber)
clientSocket=socket(AF_INET,SOCK_DGRAM)

#User inputs commands forever until bye command is used to break connection
while True:
    message=input('Please input a command: \n')
    if(message=="Bye"):
        break
    else:
        clientSocket.sendto(message.encode(),(serverName,serverPort))
        message,serverAddress=clientSocket.recvfrom(2048)
        mM=message.decode()
        print(mM)
   


print("Client/Server connection broken")
clientSocket.close()
   

    