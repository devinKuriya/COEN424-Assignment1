#Devin Kuriya 40111954
#Client Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

import abc
from http import client
from pydoc import cli
from socket import *
import os
import time
import json
import RFW_pb2
import RFD_pb2
import struct



def fileexists_check(path):
        if os.path.isfile(path)!=True:
            return False
        else:
            return True


#userInput_ServerName=input('Please input an ip address(localhost): \n')
#userInput_PortNumber=input('Please input a port number(12000): \n')

serverName='localhost'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)

#User inputs commands forever until bye command is used to break connection
while True:
    print("**********Inputs BenchmarkType and DataType are case sensitive. Copy one of the two options given**********")
    id=input('Please input an ID(if you wish to close client click enter): \n')
    BenchmarkType=input('Please input a BenchmarkType(DVD or NDBench): \n')
    WorkloadMetric=input('Please input a WorkloadMetric: \n')
    BatchUnit=input('Please input a BatchUnit: \n')
    BatchID=input('Please input a BatchID: \n')
    BatchSize=input('Please input a BatchSize: \n')
    DataType=input('Please input a DataType(training or testing): \n')
    DataAnalytics=input('Please input a DataAnalytics: \n')

    if(id==""):
        break
    else:
        test = RFW_pb2.Rfw()
        test.ID=id
        test.BenchmarkType=BenchmarkType
        test.WorkloadMetric=WorkloadMetric
        test.BatchUnit=BatchUnit
        test.BatchID=BatchID
        test.BatchSize=BatchSize
        test.DataType=DataType
        test.DataAnalytics=DataAnalytics

        #Send protobuf file
        clientSocket.sendto(test.SerializeToString(),(serverName,serverPort))
       
        #Receive RFW protobuf file
        message=clientSocket.recv(2048)

        RFD = RFD_pb2.Rfd()
        RFD.ParseFromString(message)
        print(RFD)
        #What to do with data?-->Put into file and aggreate all RFDs? Same for RFW?
   


print("Client/Server connection broken")
clientSocket.close()
   

    