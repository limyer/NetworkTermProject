from socket import *
import threading
ADDR=('192.168.43.142',12000)
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect(ADDR)

def clientThread():
    print(clientSocket.recv(2048).decode())

t=threading.Thread(target=clientThread)
t.daemon=True
t.start()
    
    
sentence='a'
while sentence!='.':
    sentence=input("Input : ")
    clientSocket.send(sentence.encode())
    data = clientSocket.recv(2048)
    print('Receive from server: ',data.decode())
clientSocket.close()
