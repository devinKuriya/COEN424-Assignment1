#Devin Kuriya 40111954
#Server Code
#I certify that this is my own submission and meets Gina Cody School's expectation of Originality

from http import client
import json
from multiprocessing.connection import wait
from socket import *
import csv

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
            print(filename)
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
        
        filename='Server/'+BenchmarkType+'-'+WorkloadMetric
        
        with open('Server/'+filename) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')


        #Write to RFD.json

        #Send RFD.json to client


    #Not a valid command
    else:
        print("Not a valid message")
        print(mM)
        serverSocket.sendto("Not a valid message".encode,clientAddress)
    
    
           
        
   
    
    
    

