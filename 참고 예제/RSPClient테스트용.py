from socket import *
import threading
ADDR=('192.168.43.142',12000)
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect(ADDR)   

sentence='a'
while sentence!='.':
    data = clientSocket.recv(2048)
    print('Receive from server: ',data.decode())
    # 라운드 결과를 받으면 enter your card를 받기 위해 한번더 data를 받는다
    if data == b'You win!\n' or data == b'You lose\n':
        data = clientSocket.recv(2048)
        print('Receive from server: ',data.decode())
    sentence=input("Input : ")
    clientSocket.send(sentence.encode())
clientSocket.close()
