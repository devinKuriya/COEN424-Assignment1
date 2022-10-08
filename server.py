#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv
import statistics

def find_avg(samples):
    length=len(samples)
    sum=0
    for x in samples:
        sum+=int(x)
    return sum/length

def max_min(samples,options):
    result=0
    if(options==0):#min
        for x in samples:
            if(result>=int(x)):
                result=int(x)
        return result
    elif(options==1):#max
        for x in samples:
            if(result<=int(x)):
                result=int(x)
        return result

def find_std(samples):
    #stat.stdev(data_samples)
    length=len(samples)
    intlist=[0]*length
    count=0
    for x in samples:
        intlist[count]=int(x)
    print(statistics.stdev(intlist))
    return statistics.stdev(intlist)

    

        



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
        responsemessage="Message received"
        serverSocket.sendto(responsemessage.encode(),clientAddress)
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
        
        #file processing
        
        filename=f'{BenchmarkType}-{DataType}.csv'
        
        last_batch_id=0
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
            line_count = 0
            for row in csv_reader:
                if line_count<int(BatchUnit)*int(BatchSize):
                    data_samples[line_count]=row[Colnum]
                    line_count+=1
                else:
                    break
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

        #Add percentile

        #Write to RFD.json
        with open('Server/RFD.json', 'r+') as f:
            data = json.load(f)
            data['RFD']["ID"]=id
            data['RFD']["LastBatchID"]=last_batch_id
            data['RFD']["DataSamples"]=data_samples
            data['RFD']["DataAnalytic"]=data_analytic
            print("JSON file updated")
            f.seek(0)        
            json.dump(data, f, indent=1)
            f.truncate()     


        #Send RFD.json to client
        filename="RFW.json"
        serverSocket.sendto(filename.encode(),clientAddress)
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
    
    
           
        
   
    
    
    

