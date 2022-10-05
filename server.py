#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
from multiprocessing.connection import wait
import os
import base64
import time
from socket import *

serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
space=" "
print('Server ready to receive on port:'+str(serverPort))
while True:
    message,clientAddress=serverSocket.recvfrom(2048)
    mM=message.decode()
    
    #HELP
    if mM!="":
        print(mM)
        responsemessage="Message received"
        serverSocket.sendto(responsemessage.encode(),clientAddress)
    

    #Not a valid command
    else:
        print("Not a valid message")
        print(mM)
        serverSocket.sendto("Not a valid message".encode,clientAddress)
    
    
           
        
   
    
    
    

