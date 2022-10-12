from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv
import statistics
import numpy as np

serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
space=" "


print('Server ready to receive on port:'+str(serverPort))
while True:
    message,clientAddress=serverSocket.recvfrom(2048)
    test=message.decode()
    
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
        print(id)
        print(BenchmarkType)
        print(WorkloadMetric)
        print(BatchUnit)
        print(BatchID)
        print(BatchSize)
        print(DataType)
        print(DataAnalytics)
        
        filename=f'{BenchmarkType}-{DataType}.csv'
        data_samples=[0]*(int(BatchUnit)*int(BatchSize))
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


    #Not a valid command
    else:
        print("Not a valid message")
        print(test)
        serverSocket.sendto("Not a valid message".encode(),clientAddress)
    
    
           
        
   
    
    
    

