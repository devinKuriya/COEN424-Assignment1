from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv
import statistics
import numpy as np
import RFW_pb2
import RFD_pb2
import numpy as np

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
    return np.percentile(np.array(np.double(samples)),int(DA))

def find_std(samples):#Finding as if samples were the population
    samples.sort()
    return np.std(np.double(samples))


serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
space=" "


print('Server ready to receive on port:'+str(serverPort))
while True:
    message,clientAddress=serverSocket.recvfrom(2048)
    print(f'Message1: {message}')
    test = RFW_pb2.Rfw()
    test.ParseFromString(message)

    #not empty
    if test.ID!="":

        #variable assignment
        id=test.ID
        BenchmarkType=test.BenchmarkType
        WorkloadMetric=test.WorkloadMetric
        BatchUnit=test.BatchUnit
        BatchID=test.BatchID
        BatchSize=test.BatchSize
        DataType=test.DataType
        DataAnalytics=test.DataAnalytics
        

        #file processing
        filename=f'{BenchmarkType}-{DataType}.csv'
        
        last_batch_id=int(BatchID)+int(BatchSize)-1
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
            line_count = (int(BatchUnit)*int(BatchSize))*(int(BatchID)-1)
            count=0
            rowcount=0
            condition=((int(BatchUnit)*int(BatchSize)*int(BatchID)))
            for row in csv_reader:
                if rowcount==line_count:
                    if line_count<condition:
                        data_samples[count]=np.double(row[Colnum])
                        line_count+=1
                        count+=1
                    else:
                        break
                rowcount+=1
            print(f'Lines processed: {line_count}') 
            print(data_samples) 
        #Calculate analytics

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


        #Set Values for RFD
        RFD = RFD_pb2.Rfd()
        RFD.ID=id
        RFD.LastBatchID=str(last_batch_id)
        RFD.DataSamples.extend(data_samples)
        RFD.DataAnalytic=str(data_analytic)

        #Send back to client
        serverSocket.sendto(RFD.SerializeToString(),clientAddress)
        print('Message Sent!')




    #Not a valid command
    else:
        print("Not a valid message")
        print(test)
        serverSocket.sendto("Not a valid message".encode(),clientAddress)
    
    
           
        
   
    
    
    

