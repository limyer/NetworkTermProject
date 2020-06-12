from socket import *
import threading

ADDR=('',12000)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(1)

index=0 #접속한 사람 수
t=[] #쓰레드




def socketThread():
    clientSocket,addr=serverSocket.accept()
    print(f'{addr} connected')
    while True:
        sentence=clientSocket.recv(2048)
        print(sentence.decode())
        

        
while index<2:
    t.append(threading.Thread(target=socketThread))
    t[index].daemon=True
    t[index].start()
    index+=1

