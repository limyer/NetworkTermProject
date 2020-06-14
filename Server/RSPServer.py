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

# RSP서버 클래스
# 서버의 동작은 전부 여기 정의해주세요
class RSPServer:
    stage=0
    connectionCount = 0
    threadList = []
    usernameList = []

    def start_server(self):
        self.serverManager = ServerConnectionManager(HOST, PORT)
        print('The server is ready to receive')
    
    def end_server(self):
        self.serverManager.close_socket()

    def open_socket(self):
        print('waiting to be connected')
        clientThread = self.serverManager.accept_socket()
        if clientThread != "None":
            RSPServer.threadList.append(clientThread)
            self.serverManager.run_client_thread(clientThread)

    
    def game_run(self, clientSocket, username):
        try:
            self.stage0(self, clientSocket, username)
        except error:
            print('Error occured: Restart game')
            self.serverManager.send_message(clientSocket, RESTARTCODE)
            self.game_run(self, clientSocket, username)


    def stage0(self, clientSocket, username):
        print(username + " has started Stage 0")
        RSPServer.stage = 0
        while True:
            if len(RSPServer.threadList) == 2:
                self.serverManager.send_message(clientSocket, STAGE0TO1CODE)
                print("Stage 0 end")
                break
        return
    
    def stage1(self, clientSocket, username):
        time.sleep(3)
        RSPServer.stage = 1
        self.serverManager.send_message(clientSocket, STAGE0TO1CODE)


    


    
        
    



# 서버 오브젝트 생성 후 동작
if __name__ == '__main__':
    i = 0
    server = RSPServer()
    server.start_server()
    while True:
        server.open_socket()

    print('RSP game set fin')
    server.end_server()



