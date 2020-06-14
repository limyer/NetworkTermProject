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
STAGE1TO2CODE = 'Stage 1 to 2' # (Code: "Stage 1 to 2")
RESTARTCODE = 'Restart' # (Code: "Restart")
STAGE1STARTCODE = 'Receiving Stage 1'
REWRITECODE = 'Rewrite'
CANCELCODE = 'Cancel'
UNDECIDEDCODE = 'Undecided'
ROCKCODE = 'ROCK'
SCISSORSCODE = 'SCISSORS'
PAPERCODE = 'PAPER'
STAGE1WINCODE = 'Stage1: Win'
STAGE1DRAWCODE = 'Stage1: Draw'
STAGE1LOSECODE = 'Stage1: Lose'

# RSP서버 클래스
# 서버의 동작은 전부 여기 정의해주세요
class RSPServer:
    stage=0
    connectionCount = 0
    threadList = []
    usernameList = []
    addressList = []
    endStage0Flag = False
    endStage1Flag = False
    endStage2Flag = False
    startStageFlag = True
    playerInput = ["", ""]
    playerInputReceived = [False, False]
    currentPlayerTurn = [False, False]

    def __init__(self):
        self.connectionManager = ServerConnectionManager(HOST, PORT)
        print('The server is ready to receive')
    
    def end_server(self):
        self.connectionManager.close_socket()

    def open_socket(self):
        print('waiting to be connected\n')
        clientThread = self.accept_socket()
        if clientThread != "None" or clientThread != None:
            RSPServer.threadList.append(clientThread)
            self.run_client_thread(clientThread)
            print(RSPServer.threadList)
            return
        return

    def accept_socket(self):
        try:
            clientSocket, addr = self.connectionManager.serverSocket.accept()
            clientSocket.settimeout(30)
            print('Connected by:', addr[0], ':', addr[1])
            if addr[0] in RSPServer.addressList:
                print("Reconnection Occured, Restarting Thread")
                index = RSPServer.addressList.index(addr[0])
                self.remove_from_list(index)
            clientThread = self.make_client_thread(clientSocket)
            RSPServer.addressList.append(addr[0])
            return clientThread
        except error:
            return "None"

    def make_client_thread(self, clientSocket):
        if len(RSPServer.threadList) >= 2:
            self.connectionManager.receive_message(clientSocket)
            self.connectionManager.send_message(clientSocket, BREAKCODE)
            clientSocket.close()
            return "None"
        else:
            username = self.get_username(clientSocket)
            if username == None or username in RSPServer.usernameList:
                self.connectionManager.send_message(clientSocket, REWRITECODE)
                self.open_socket()
                return "None"

            RSPServer.usernameList.append(username)
            clientThread = threading.Thread(target=self.game_run, args=(clientSocket, username))
            return clientThread

    def get_username(self, clientSocket):
        # (Code: "Username: " + username)
        usernameRaw = self.connectionManager.receive_message(clientSocket)
        if usernameRaw != "Username: ":
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
                    self.stage0Thread.setDaemon(True)
                    self.stage0Thread.start()
                elif RSPServer.stage == 1:
                    self.stage1Thread = threading.Thread(target=self.stage1, args=(clientSocket, username))
                    self.stage1Thread.setDaemon(True)
                    self.stage1Thread.start()
                elif RSPServer.stage == 2:
                    self.stage2Thread = threading.Thread(target=self.stage2, args=(clientSocket, username))
                    self.stage2Thread.setDaemon(True)
                    self.stage2Thread.start()
        except error:
            print('Error occured: Restart game')
            self.connectionManager.send_message(clientSocket, RESTARTCODE)
            self.game_run(self, clientSocket, username)


    def stage0(self, clientSocket, username):
        if not RSPServer.endStage0Flag:
            print(username + " is in Stage 0")
            if (len(RSPServer.threadList)) == 2:
                self.connectionManager.send_message(clientSocket, STAGE0TO1CODE)
                RSPServer.connectionCount += 1
                print("Stage 0 end")
                if RSPServer.connectionCount == 2:
                    RSPServer.endStage0Flag = True
                    time.sleep(3)
                    RSPServer.stage = 1
                    RSPServer.endStage1Flag = False
                    RSPServer.startStageFlag = True
                    RSPServer.connectionCount = 0
            if self.connectionManager.receive_message(clientSocket) == CANCELCODE:
                index = RSPServer.usernameList.index(username)
                self.remove_from_list(index)
        return
    
    def stage1(self, clientSocket, username):
        if not RSPServer.endStage1Flag:
            print(username + " is in Stage 1")
            if RSPServer.startStageFlag:
                self.connectionManager.send_message(clientSocket, STAGE1STARTCODE)
                RSPServer.startStageFlag = False
            else:
                msg = self.connectionManager.receive_message(clientSocket)
                if msg == None or "":
                    return    
                msg = msg.split()
                index = RSPServer.usernameList.index(username)
                if len(msg) == 2 and not RSPServer.playerInputReceived[index]:
                    if msg[1] == UNDECIDEDCODE:
                        self.connectionManager.send_message(clientSocket, RESTARTCODE)
                        RSPServer.playerInputReceived = [False, False]
                    else:
                        if msg[1] == ROCKCODE:
                            RSPServer.playerInput[index] = ROCKCODE
                        elif msg[1] == SCISSORSCODE:
                            RSPServer.playerInput[index] = SCISSORSCODE
                        elif msg[1] == PAPERCODE:
                            RSPServer.playerInput[index] = PAPERCODE
                        RSPServer.playerInputReceived[index] = True
                if RSPServer.playerInputReceived == [True, True]:
                    result = self.stage1_result(index)
                    if result == "Draw":
                        self.connectionManager.send_message(clientSocket, STAGE1DRAWCODE)
                    else:
                        if result == "Win":
                            self.connectionManager.send_message(clientSocket, STAGE1WINCODE)
                        elif result == "Lose":
                            self.connectionManager.send_message(clientSocket, STAGE1LOSECODE)
                        time.sleep(3)
                        # self.connectionManager.send_message(clientSocket, STAGE1TO2CODE)
                        # print("Stage 1 end")
                        # RSPServer.endStage1Flag = True
                        # time.sleep(3)
                        # RSPServer.stage = 2
                        # RSPServer.endStage2Flag = False
                        # RSPServer.startStageFlag = True
                    RSPServer.playerInputReceived = [False, False]
                    RSPServer.playerInput = ["", ""]
        return

    def stage1_result(self, index):
        opponentIndex = (1 if index==0 else 0)
        myChoice = RSPServer.playerInput[index]
        oppChoice = RSPServer.playerInput[opponentIndex]
        if myChoice == oppChoice:
            return "Draw"
        elif myChoice == ROCKCODE:
            if oppChoice == SCISSORSCODE:
                return "Win"
            elif oppChoice == PAPERCODE:
                return "Lose"
        elif myChoice == SCISSORSCODE:
            if oppChoice == PAPERCODE:
                return "Win"
            elif oppChoice == ROCKCODE:
                return "Lose"
        elif myChoice == PAPERCODE:
            if oppChoice == ROCKCODE:
                return "Win"
            elif oppChoice == SCISSORSCODE:
                return "Lose"


    def stage2(self, clientSocket, username):
        print(username + " is in Stage 2")
        time.sleep(3)
        RSPServer.stage = 2
        print("Server End")

    def remove_from_list(self,index):
        RSPServer.usernameList.remove(RSPServer.usernameList[index])
        RSPServer.addressList.remove(RSPServer.addressList[index])
        RSPServer.threadList.remove(RSPServer.threadList[index])
        

    
        
    



# 서버 오브젝트 생성 후 동작
if __name__ == '__main__':
    i = 0
    server = RSPServer()
    while True:
        server.open_socket()

    print('RSP game set fin')
    server.end_server()



