#Devin Kuriya 40111954
#Client Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

import abc
from http import client
from pydoc import cli
from socket import *
import os
import json
import RFW_pb2
import RFD_pb2



def fileexists_check(path):
        if os.path.isfile(path)!=True:
            return False
        else:
            return True


#userInput_ServerName=input('Please input an ip address(localhost): \n')
#userInput_PortNumber=input('Please input a port number(12000): \n')

serverName='localhost'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#User inputs commands forever until bye command is used to break connection
while True:
    format=input('Message format Protobuff(p) or JSON(j): \n')
    clientSocket.send(format.encode())
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
        if(format=="j"):
            #Send as JSON file
            JSONrequest = {
            "ID":id,
            "BenchmarkType":BenchmarkType,
            "WorkloadMetric":WorkloadMetric,
            "BatchUnit":BatchUnit,
            "BatchID":BatchID,
            "BatchSize":BatchSize,
            "DataType":DataType,
            "DataAnalytics":DataAnalytics
            }
            print(JSONrequest)
            requestmessage=json.dumps(JSONrequest)
            encoded=requestmessage.encode('latin-1')
            clientSocket.send(encoded)
            print("Done sending")
            with open("Client/RFW.json", 'w') as file:
               json.dump(JSONrequest,file,indent=1)
            file.close()
        else:
            #Set protobuf object
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
            with open("Client/RFWproto.txt", 'w') as f:
                f.write(str(test))
            temp=test.SerializeToString()
            clientSocket.send(temp)
            

        #Receive RFD
        
        if(format=="j"):
            data = clientSocket.recv(1000000000)
            with open("Client/RFD.json", 'w') as f:
                f.write(data.decode('latin-1'))
            print("RFD.json has been downloaded successfully.")
        else:
            message=clientSocket.recv(1000000000)
            RFD = RFD_pb2.Rfd()
            RFD.ParseFromString(message)
            with open("Client/RFDproto.txt", 'w') as f:
                f.write(str(RFD))
            print(RFD)
        
   


print("Client/Server connection broken")
clientSocket.close()
   

    