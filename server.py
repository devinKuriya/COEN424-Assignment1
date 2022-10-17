#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv
from urllib import response
from xml.etree.ElementPath import find
import numpy as np
from pyparsing import line
import RFW_pb2
import RFD_pb2

def find_avg(samples):
    length=len(samples)
    sum=0
    for x in samples:
        sum+=np.double(x)
    return sum/length

def max_min(samples,options):
    result=np.double(samples[0])
    if(options==0):#min
        for x in samples:
            if(result>=np.double(x)):
                result=np.double(x)
        return result
    elif(options==1):#max
        for x in samples:
            if(result<=np.double(x)):
                result=np.double(x)
        return result

def find_percentile(samples,DA):
    samples.sort()
    temp=list(DA)
    temp2=''
    p = temp.index("p")  # find position of the letter "a"
    del(temp[p])
    for element in temp: 
        temp2 += str(element)
    return np.percentile(np.array(np.double(samples)),int(temp2))

def find_std(samples):#Finding as if samples were the population
    samples.sort()
    return np.std(np.double(samples))
    

    
#Socket binding
serverPort=12000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)



print('Server ready to receive on port:'+str(serverPort))
while True:#Server will run till manually closed
    clientconnection,clientAddress=serverSocket.accept()
    temporaray=clientconnection.recv(2048)
    format=temporaray.decode('latin-1')
    print(format)
    request=clientconnection.recv(1000000000)
   
    #Check request is not empty
    if len(request)!="":
        if(format=="j"):
            #variable assignment
            data=json.loads(request)
            id=data["ID"]
            BenchmarkType=data["BenchmarkType"]
            WorkloadMetric=data["WorkloadMetric"]
            BatchUnit=data["BatchUnit"]
            BatchID=data["BatchID"]
            BatchSize=data["BatchSize"]
            DataType=data["DataType"]
            DataAnalytics=data["DataAnalytics"]
            with open("Server/RFW.json", 'w') as file:
               json.dump(data,file,indent=1)
            file.close()
        else:
            test = RFW_pb2.Rfw()
            test.ParseFromString(request)
            print(test)
            #variable assignment
            id=test.ID
            BenchmarkType=test.BenchmarkType
            WorkloadMetric=test.WorkloadMetric
            BatchUnit=test.BatchUnit
            BatchID=test.BatchID
            BatchSize=test.BatchSize
            DataType=test.DataType
            DataAnalytics=test.DataAnalytics
            with open("Server/RFWproto.txt", 'w') as f:
                f.write(str(test))
        #file processing
        
        filename=f'{BenchmarkType}-{DataType}.csv'
        
        last_batch_id=(int(BatchID)+int(BatchSize))-1
        data_samples=[0]*(int(BatchUnit)*int(BatchSize))
        data_analytic=0

        if(WorkloadMetric=="CPUUtilization_Average"):
            Colnum=0
        elif(WorkloadMetric=="NetworkIn_Average"):
            Colnum=1
        elif(WorkloadMetric=="NetworkOut_Average"):
            Colnum=2
        elif(WorkloadMetric=="MemoryUtilization_Average"):
            Colnum=3


        with open('Server/'+filename) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            #line_count = (int(BatchUnit)*int(BatchSize))*((int(BatchID)-1))
            line_count = (int(BatchUnit)*(int(BatchID)-1))
            print(f'Line count first:{line_count}')
            count=0
            rowcount=0
            #condition=((int(BatchUnit)*int(BatchSize)*int(BatchID)))
            condition=(int(BatchUnit)*int(BatchSize))+line_count-1
            for row in csv_reader:
                if rowcount==line_count:
                    if line_count<=condition:
                        data_samples[count]=np.double(row[Colnum])
                        line_count+=1
                        count+=1
                    else:
                        break
                rowcount+=1
            print(f'Lines processed: {line_count}') 
            
            counter=0
            d1=[0]*(len(data_samples))
            for x in data_samples:
                d1[counter]=data_samples[counter]
                counter+=1
            
  

        #####Fix it so lists give us integers
        if(DataAnalytics=="avg"):
            data_analytic=find_avg(data_samples)
        elif(DataAnalytics=="max"):
            data_analytic=max_min(data_samples,1)
        elif(DataAnalytics=="min"):
            data_analytic=max_min(data_samples,0)
        elif(DataAnalytics=="std"):
            data_analytic= find_std(data_samples)
        else:
            data_analytic=find_percentile(data_samples,DataAnalytics)
        
        if(format=="j"):
            #Write to RFD.json
           JSONresponse = {
                "ID":id,
                "LastBatchID":last_batch_id,
                "DataSamples":d1,
                "DataAnalytic":data_analytic
           }
           print(JSONresponse)
           responsemessage=json.dumps(JSONresponse)
           with open("Server/RFD.json", 'w') as file:
               file.write(responsemessage)
           file.close()
           encodedresponse=responsemessage.encode('latin-1')
           clientconnection.send(encodedresponse)
           
            
        else:
            #Set Values for RFD
            RFD = RFD_pb2.Rfd()
            RFD.ID=id
            RFD.LastBatchID=str(last_batch_id)
            RFD.DataSamples.extend(d1)
            RFD.DataAnalytic=str(data_analytic)
            #Send back to client
            with open("Server/RFDproto.txt", 'w') as f:
                f.write(str(RFD))
            encoded=RFD.SerializeToString()
            clientconnection.send(encoded)
            print('Message Sent!')

    #Not a valid command
    else:
        print("Not a valid message")
        print(request)
        clientconnection.sendto("Not a valid message".encode(),clientAddress)
    
    
           
        


