# 컴퓨터네트워크 묵찌빠 ver 1.0
# 최종 수정: 2020 05 15 15:54 - 임예랑
from socket import *
from _thread import *
import time
import threading
from ServerConnectionManager import *

HOST = ''
PORT = 12000

BREAKCODE = 'Break' # (Code: "Break") 
STAGE0TO1CODE = 'Stage 0 to 1' # (Code: "Stage 0 to 1")
RESTARTCODE = 'Restart' # (Code: "Restart")
STAGE1STARTCODE = 'Receiving Stage 1'
REWRITECODE = 'Rewrite'
CANCELCODE = 'Cancel'

# RSP서버 클래스
# 서버의 동작은 전부 여기 정의해주세요
class RSPServer:
    stage=0
    connectionCount = 0
    threadList = []
    usernameList = []
    addressList = []

    def __init__(self):
        self.serverManager = ServerConnectionManager(HOST, PORT)
        print('The server is ready to receive')
    
    def end_server(self):
        self.serverManager.close_socket()

    def open_socket(self):
        print('waiting to be connected\n')
        clientThread = self.accept_socket()
        if clientThread != "None":
            RSPServer.threadList.append(clientThread)
            self.run_client_thread(clientThread)
            print(RSPServer.threadList)
            return
        return

    def accept_socket(self):
        try:
            clientSocket, addr = self.serverManager.serverSocket.accept()
            clientSocket.settimeout(30)
            print('Connected by:', addr[0], ':', addr[1])
            if addr[0] in RSPServer.addressList:
                print("Reconnection Occured, Restarting Thread")
                indexOfThread = RSPServer.addressList.index(addr[0])
                RSPServer.addressList.remove(RSPServer.addressList[indexOfThread])
                RSPServer.threadList.remove(RSPServer.threadList[indexOfThread])
                RSPServer.usernameList.remove(RSPServer.usernameList[indexOfThread])
            clientThread = self.make_client_thread(clientSocket)
            RSPServer.addressList.append(addr[0])
            return clientThread
        except error:
            return "None"

    def make_client_thread(self, clientSocket):
        if len(RSPServer.threadList) >= 2:
            self.serverManager.receive_message(clientSocket)
            self.serverManager.send_message(clientSocket, BREAKCODE)
            clientSocket.close()
            return "None"
        else:
            username = self.get_username(clientSocket)
            if username == "":
                return "None"
            while True:
                if username in RSPServer.usernameList:
                    self.serverManager.send_message(clientSocket, REWRITECODE)
                    self.open_socket()
                    return
                else:
                    break
            RSPServer.usernameList.append(username)
            clientThread = threading.Thread(target=self.game_run, args=(clientSocket, username))
            return clientThread

    def get_username(self, clientSocket):
        # (Code: "Username: " + username)
        usernameRaw = self.serverManager.receive_message(clientSocket)
        if usernameRaw != None:
            username = usernameRaw.split()[1]
            return username
        else:
            return None

    def run_client_thread(self, clientThread):
        clientThread.daemon = True
        clientThread.start()
    
    def game_run(self, clientSocket, username):
        try:
            print("Thread start\n")
            RSPServer.stage = 0
            while username in RSPServer.usernameList:
                time.sleep(0.5)
                if RSPServer.stage == 0:
                    self.stage0Thread = threading.Thread(target=self.stage0, args=(clientSocket, username))
                    self.stage0Thread.daemon = True
                    self.stage0Thread.start()
                elif RSPServer.stage == 1:
                    self.stage1Thread = threading.Thread(target=self.stage1, args=(clientSocket, username))
                    self.stage0Thread.daemon = True
                    self.stage1Thread.start()
                elif RSPServer.stage == 2:
                    self.stage2Thread = threading.Thread(target=self.stage2, args=(clientSocket, username))
                    self.stage0Thread.daemon = True
                    self.stage2Thread.start()
                

        except error:
            print('Error occured: Restart game')
            self.serverManager.send_message(clientSocket, RESTARTCODE)
            self.game_run(self, clientSocket, username)

    def stage0(self, clientSocket, username):
        print(username + " has started Stage 0")
        if (len(RSPServer.threadList)) == 2:
            self.serverManager.send_message(clientSocket, STAGE0TO1CODE)
            print("Stage 0 end")
            RSPServer.stage = 1
        if self.serverManager.receive_message(clientSocket) == CANCELCODE:
            usernameIndex = RSPServer.usernameList.index(username)
            RSPServer.usernameList.remove(RSPServer.usernameList[usernameIndex])
        return
    
    def stage1(self, clientSocket, username):
        print(username + " has started Stage 1")
        time.sleep(3)
        RSPServer.stage = 1
        self.serverManager.send_message(clientSocket, STAGE0TO1CODE)

    
        
    



# 서버 오브젝트 생성 후 동작
if __name__ == '__main__':
    i = 0
    server = RSPServer()
    while True:
        server.open_socket()

    print('RSP game set fin')
    server.end_server()



