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
clientSocket=socket(AF_INET,SOCK_DGRAM)

#User inputs commands forever until bye command is used to break connection
while True:
    format=input('Message format Protobuff(p) or JSON(j): \n')
    clientSocket.sendto(format.encode(),(serverName,serverPort))
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
            with open('Client/RFW.json', 'r+') as f:
                data = json.load(f)
                data['RFW']["ID"]=id
                data['RFW']["BenchmarkType"]=BenchmarkType
                data['RFW']["WorkloadMetric"]=WorkloadMetric
                data['RFW']["BatchUnit"]=BatchUnit
                data['RFW']["BatchID"]=BatchID
                data['RFW']["BatchSize"]=BatchSize
                data['RFW']["DataType"]=DataType
                data['RFW']["DataAnalytics"]=DataAnalytics
                print("JSON file updated")
                f.seek(0)        
                json.dump(data, f, indent=1)
                f.truncate()  
                f.close()   
            
            filename="RFW.json"
            if(fileexists_check("Client/"+filename)):
                requestmessage=f"{str(filename)}"

            clientSocket.sendto(requestmessage.encode(),(serverName,serverPort))
            f = open("Client/"+filename,'rb')
            l = f.read(1024)
            while (l):
                clientSocket.sendto(l,(serverName,serverPort))
                print('Sent')
                l = f.read(1024)
            f.close()
            print('Done sending')
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
            clientSocket.sendto(test.SerializeToString(),(serverName,serverPort))
            

        #Receive RFD
        
        if(format=="j"):
            with open("Client/RFD.json", 'wb') as f:
                data = clientSocket.recv(2048)
                f.write(data)
                print("RFD.json has been downloaded successfully.")
        else:
            message=clientSocket.recv(2048)
            RFD = RFD_pb2.Rfd()
            RFD.ParseFromString(message)
            print(RFD)
        #What to do with data?-->Put into file and aggreate all RFDs? Same for RFW?
   


print("Client/Server connection broken")
clientSocket.close()
   

    