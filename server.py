#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv
import statistics
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

def find_percentile(samples):
    length=len(samples)
    intlist=[0]*length
    count=0
    for x in samples:
        intlist[count]=np.double(x)
        count+=1
    print(intlist)
    print(f'Percentile:{np.percentile(intlist,np.double(data_analytic))}')
    return np.percentile(intlist,np.double(data_analytic))

def find_std(samples):
    length=len(samples)
    intlist=[0]*length
    count=0
    for x in samples:
        intlist[count]=int(x)
        count+=1
    print(f'Standard Deviation:{np.std(intlist)}')
    return np.std(intlist)
    

    

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
        #responsemessage="Message received"
        #serverSocket.sendto(responsemessage.encode(),clientAddress)
        filename=mM
        with open("Server/"+filename, 'w') as f:
            data = serverSocket.recv(4096)
            f.write(data.decode())
            print(f.name+" has been downloaded successfully.")
        
        #variable assignment
        with open('Server/RFW.json', 'r') as file:
            data=json.load(file)
            id=data['RFW']["ID"]
            BenchmarkType=data['RFW']["BenchmarkType"]
            WorkloadMetric=data['RFW']["WorkloadMetric"]
            BatchUnit=data['RFW']["BatchUnit"]
            BatchID=data['RFW']["BatchID"]
            BatchSize=data['RFW']["BatchSize"]
            DataType=data['RFW']["DataType"]
            DataAnalytics=data['RFW']["DataAnalytics"]
            
        file.close()
        
        #file processing
        
        filename=f'{BenchmarkType}-{DataType}.csv'
        
        last_batch_id=int(BatchID)+int(BatchUnit)
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
                        print(f'Before: {count}')
                        data_samples[count]=np.double(row[Colnum])
                        print(data_samples)
                        line_count+=1
                        count+=1
                    else:
                        break
                rowcount+=1
            print(f'Lines processed: {line_count}')
            print(str(data_samples))    
        #Calculate analytics
        originalds=data_samples
        print(f'Unsorted: {data_samples}')
        data_samples.sort()
        print(f'Sorted: {data_samples}')        

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
            data_analytic=find_percentile(data_samples)
        
        
        #Write to RFD.json
        with open('Server/RFD.json', 'r+') as f:
            data = json.load(f)
            data['RFD']["ID"]=id
            data['RFD']["LastBatchID"]=str(last_batch_id)
            data['RFD']["DataSamples"]=data_samples
            data['RFD']["DataAnalytic"]=str(data_analytic)
            print("JSON file updated")
            f.seek(0)        
            json.dump(data, f, indent=1)
            f.truncate()     


        #Send RFD.json to client
        filename="RFD.json"
        #serverSocket.sendto(filename.encode(),clientAddress)
        f = open("Server/"+filename,'rb')
        l = f.read(1024)
        while (l):
            serverSocket.sendto(l,clientAddress)
            print('Sending...')
            l = f.read(1024)
        f.close()
        print('Done sending')

    #Not a valid command
    else:
        print("Not a valid message")
        print(mM)
        serverSocket.sendto("Not a valid message".encode(),clientAddress)
    
    
           
        
   
    
    
    

