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



#Function used to check if file exists
def fileexists_check(path):
        if os.path.isfile(path)!=True:
            return False
        else:
            return True



serverName='localhost'
serverPort=1200
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

request=0#USed to limit participant to 1 request per connection
#User inputs for one request per connection
while(request==0):
    format=input('Message format Protobuff(p) or JSON(j): \n')
    clientSocket.send(format.encode())
    print("**********Inputs BenchmarkType and DataType are case sensitive. Copy one of the two options given**********")
    #RFW inputs from user
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
            #Format JSON request
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
            #Send request
            clientSocket.send(encoded)
            print("Done sending")
            #Save request on client side
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
            
            #Save and Send protobuf file
            with open("Client/RFWproto.txt", 'w') as f:
                f.write(str(test))
            temp=test.SerializeToString()
            clientSocket.send(temp)
            

        #Receive RFD
        
        if(format=="j"):#JSON format
            data = clientSocket.recv(1000000000)
            if(fileexists_check("Client/RFD.json")):#Check if file exists, if not need to add [ to beginning
                with open("Client/RFD.json", 'ab+') as f:
                    f.seek(-1,os.SEEK_END)#Find ] character at end
                    f.truncate()#remove ] character
                    f.write((',').encode())#Add comma
                    f.write(('\n').encode())#Skip line for formatting
                    f.write(data)#Add data entry, not decoded
                    f.write((']').encode())#Add ] back
                    f.close()#Close file

            else:
                with open("Client/RFD.json", 'wb+') as f:#If file is not created, this code is used, difference is adding[ for formatting
                    f.write(('[').encode())#Need string as bytes since wb+ is used
                    f.write(data)#Add data entry, not decoded
                    f.write((']').encode())
                    f.close()#Close file

        else:
            message=clientSocket.recv(1000000000)
            RFD = RFD_pb2.Rfd()
            RFD.ParseFromString(message)
            with open("Client/RFDproto.txt", 'a') as f:
                f.write('\n')
                f.write(str(RFD))
            print(RFD)
    request=1
    clientSocket.close()
    print("Client/Server connection broken")

   

    