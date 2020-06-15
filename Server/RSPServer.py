# 컴퓨터네트워크 묵찌빠 ver 2.0
# 최종 수정: 2020 06 15 - 임예랑
from socket import *
from _thread import *
import time
import threading
from ServerConnectionManager import *

HOST = ''
PORT = 12000
TIMEOUT = 30
WINNINGSCORE = 3

BREAKCODE = 'Break' # (Code: "Break") 
STAGE0TO1CODE = 'Stage 0 to 1' # (Code: "Stage 0 to 1")
STAGE1TO2CODE = 'Stage 1 to 2' # (Code: "Stage 1 to 2")
STAGE2TO1CODE = 'Stage 2 to 1' # (Code: "Stage 2 to 1")
RESTARTCODE = 'Restart' # (Code: "Restart")
STAGE1STARTCODE = 'Receiving Stage 1'
STAGE2STARTCODE = 'Receiving Stage 2'
REWRITECODE = 'Rewrite'
CANCELCODE = 'Cancel'
UNDECIDEDCODE = 'Undecided'
ROCKCODE = 'ROCK'
SCISSORSCODE = 'SCISSORS'
PAPERCODE = 'PAPER'
STAGE1WINCODE = 'Stage1: Win'
STAGE1DRAWCODE = 'Stage1: Draw'
STAGE1LOSECODE = 'Stage1: Lose'
STAGE2TURNCODE = 'Turn'
STAGE2NOTTURNCODE = 'Not Turn'
STAGE2WINCODE = 'Stage2: Win'
STAGE2DRAWCODE = 'Stage2: Draw'
STAGE2LOSECODE = 'Stage2: Lose'
FINALWINCODE = 'Final: Win'
FINALLOSECODE = 'Final: LOSE'

# RSP서버 클래스
class RSPServer:
    stage=0 # 현재 스테이지
    connectionCount = 0 # 코드 두개 보내졌는지 확인용
    threadList = [] # 현재 스레드 리스트
    usernameList = [] # 유저 이름 리스트
    addressList = [] # IP 주소 리스트
    scoreList = [0, 0]
    endStage0Flag = False # Stage0 끝났는지 확인
    endStage1Flag = False # Stage1 끝났는지 확인
    endStage2Flag = False # Stage2 끝났는지 확인
    startStageFlag = True # Stage의 시작인지 확인
    restartFlag = False # 재시작 플래그
    turnInformFlag = False #
    playerInput = ["", ""] # 서버가 받은 player 입력
    playerInputReceived = [False, False] # 플레이어의 입력을 받았는지 확인 여부
    stage1Result = ["", ""] # Stage1에서 결과
    stage2Result = ["", ""]
    currentPlayerTurn = [False, False] # 현재 누구 턴인지

    

    def __init__(self):
        self.connectionManager = ServerConnectionManager(HOST, PORT)
        print('The server is ready to receive')
    
    def end_server(self):
        self.connectionManager.close_socket()

    # 소켓을 열고 클라이언트 쓰레드 생성
    def open_socket(self):
        print('waiting to be connected\n')
        # 소켓을 받고 쓰레드를 함수 실행
        clientThread = self.accept_socket()
        # 쓰레드가 널이 아닐 경우
        if clientThread != "None" or clientThread != None:
            # 리스트에 쓰레드 추가
            RSPServer.threadList.append(clientThread)
            # 쓰레드 실행
            self.run_client_thread(clientThread)
            print(RSPServer.threadList)
            return
        return

    # 소켓을 받고 쓰레드를 만드는 함수
    def accept_socket(self):
        try:
            clientSocket, addr = self.connectionManager.serverSocket.accept()
            # 타임아웃 내로 응답 없을시 소켓 닫힘
            clientSocket.settimeout(TIMEOUT)
            print('Connected by:', addr[0], ':', addr[1])
            # IP 주소가 이미 리스트에 존재할 경우
            if addr[0] in RSPServer.addressList:
                print("Reconnection Occured, Restarting Thread")
                # 리스트에서 삭제 후 연결
                index = RSPServer.addressList.index(addr[0])
                self.remove_from_list(index)
            # 실제로 쓰레드를 만드는 작업 시작
            clientThread = self.make_client_thread(clientSocket)
            # IP 주소 리스트에 추가
            if clientThread != "None":
                RSPServer.addressList.append(addr[0])
            return clientThread
        except error:
            return "None"

    # 실제로 쓰레드가 만들어지는 함수
    def make_client_thread(self, clientSocket):
        # 쓰레드 리스트가 2개 이상 요소를 가질 경우
        if len(RSPServer.threadList) >= 2:
            # 유저이름을 먼저 받고
            self.connectionManager.receive_message(clientSocket)
            # Break 코드 전송후 소켓 해제
            self.connectionManager.send_message(clientSocket, BREAKCODE)
            clientSocket.close()
            return "None"
        # 2개 이하일 경우
        else:
            username = self.get_username(clientSocket)
            # 유저 이름이 ""로 들어오거나 중복될 경우
            if username == None or username in RSPServer.usernameList:
                # REWRITE 코드 전송
                self.connectionManager.send_message(clientSocket, REWRITECODE)
                # 재시작
                self.open_socket()
                return "None"

            # 유저이름 리스트에 추가
            RSPServer.usernameList.append(username)
            # 실제로 쓰레드 만들기
            clientThread = threading.Thread(target=self.game_run, args=(clientSocket, username))
            return clientThread

    # 유저이름을 헤더를 떼고 리턴하는 함수
    def get_username(self, clientSocket):
        # (Code: "Username: " + username)
        usernameRaw = self.connectionManager.receive_message(clientSocket)

        if usernameRaw != "Username: ":
            username = usernameRaw.split()[1]
            return username
        # 유저 이름이 빈 공간으로 왔을 경우
        else:
            return None

    # 쓰레드 실행 함수
    def run_client_thread(self, clientThread):
        clientThread.daemon = True
        clientThread.start()
    
    # 쓰레드 타겟 함수
    def game_run(self, clientSocket, username):
        try:
            print("Thread start\n")
            RSPServer.stage = 0
            # 유저이름이 삭제되면 쓰레드 종료
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
        # 스테이지 1 끝내는 플래그 (True일 경우 stage1 끝)
        if not RSPServer.endStage1Flag:
            # Receiving Stage 1으로 싱크 확인 플래그
            if RSPServer.startStageFlag:
                # 스테이지 1 시작코드 전송
                self.connectionManager.send_message(clientSocket, STAGE1STARTCODE)
                RSPServer.connectionCount += 1
                if RSPServer.connectionCount == 2:
                    RSPServer.startStageFlag = False
                    RSPServer.connectionCount = 0

            else:
                index = RSPServer.usernameList.index(username)
                opponentIndex = (1 if index==0 else 0)

                # 상대 클라와 내 클라 둘 다 입력을 끝냈을 때
                if RSPServer.playerInputReceived[index] and RSPServer.playerInputReceived[opponentIndex]:
                    myChoice = RSPServer.playerInput[index]
                    oppChoice = RSPServer.playerInput[opponentIndex]

                    # 결과 계산
                    if myChoice == oppChoice:
                        RSPServer.stage1Result[index] = "Draw"
                    elif myChoice == ROCKCODE:
                        if oppChoice == SCISSORSCODE:
                            RSPServer.stage1Result[index] = "Win"
                        elif oppChoice == PAPERCODE:
                            RSPServer.stage1Result[index] = "Lose"
                    elif myChoice == SCISSORSCODE:
                        if oppChoice == PAPERCODE:
                            RSPServer.stage1Result[index] = "Win"
                        elif oppChoice == ROCKCODE:
                            RSPServer.stage1Result[index] = "Lose"
                    elif myChoice == PAPERCODE:
                        if oppChoice == ROCKCODE:
                            RSPServer.stage1Result[index] = "Win"
                        elif oppChoice == SCISSORSCODE:
                            RSPServer.stage1Result[index] = "Lose"

                    # 결과
                    print(username + " " + RSPServer.stage1Result[index])

                    # 결과에 따라 동작
                    # 무승부일 때 스테이지 재시작
                    if RSPServer.stage1Result[index] == "Draw":
                        self.connectionManager.send_message(clientSocket, STAGE1DRAWCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.currentPlayerTurn = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                    # 누군가의 승리일 때 스테이지 2로 이동
                    else:
                        if RSPServer.stage1Result[index] == "Win":
                            self.connectionManager.send_message(clientSocket, STAGE1WINCODE)
                            RSPServer.currentPlayerTurn[index] = True
                        elif RSPServer.stage1Result[index] == "Lose":
                            self.connectionManager.send_message(clientSocket, STAGE1LOSECODE)
                            RSPServer.currentPlayerTurn[index] = False
                        # 스테이지 2로 넘어가는 동작
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                            print("Stage 1 end")
                            RSPServer.endStage1Flag = True
                            RSPServer.stage = 2
                            RSPServer.endStage2Flag = False
                            RSPServer.startStageFlag = True
                            RSPServer.turnInformFlag  =True
                        time.sleep(3)
                        self.connectionManager.send_message(clientSocket, STAGE1TO2CODE)

                    # 2초 슬립
                    time.sleep(2)

                # 상대 클라와 내 클라 둘 중에 하나가 입력을 끝냈을 때
                elif RSPServer.playerInputReceived[index] or RSPServer.playerInputReceived[opponentIndex]:
                    # RestartFlag가 살아있을 경우
                    if RSPServer.restartFlag:
                        # RESTART 코드 전송
                        self.connectionManager.send_message(clientSocket, RESTARTCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.currentPlayerTurn = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                    return

                # 상대 클라와 내 클라 둘 다 입력을 하지 않았을 때
                else:
                    # RestartFlag가 살아있을 경우
                    if RSPServer.restartFlag:
                        # RESTART 코드 전송
                        self.connectionManager.send_message(clientSocket, RESTARTCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.currentPlayerTurn = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                        return

                    # 메시지를 받음
                    msg = self.connectionManager.receive_message(clientSocket)
                    
                    # 받은 메시지가 비어있으면 리턴
                    if msg == None or "":
                        return    

                    # 공백 기준으로 자름
                    msg = msg.split()
                    
                    # 잘라서 두개의 요소가 나오고 내 입력이 비어있을 경우
                    if len(msg) == 2 and not RSPServer.playerInputReceived[index]:
                        # Undecided 코드가 오면 Restart 플래그를 세움
                        if msg[1] == UNDECIDEDCODE:
                            RSPServer.restartFlag = True
                        else:
                            if msg[1] == ROCKCODE:
                                RSPServer.playerInput[index] = ROCKCODE
                            elif msg[1] == SCISSORSCODE:
                                RSPServer.playerInput[index] = SCISSORSCODE
                            elif msg[1] == PAPERCODE:
                                RSPServer.playerInput[index] = PAPERCODE
                            # 입력이 되었다고 저장
                            RSPServer.playerInputReceived[index] = True
                            print("Player Input : " + str(RSPServer.playerInputReceived))              
        return


    def stage2(self, clientSocket, username):
        index = RSPServer.usernameList.index(username)
        opponentIndex = (1 if index==0 else 0)
        # 스테이지 2 끝내는 플래그 (True일 경우 stage2 끝)
        if not RSPServer.endStage2Flag:
            # Receiving Stage 2으로 싱크 확인 플래그
            if RSPServer.turnInformFlag:
                if RSPServer.currentPlayerTurn[index]:
                    self.connectionManager.send_message(clientSocket, STAGE2TURNCODE)
                elif not RSPServer.currentPlayerTurn[index]:
                    self.connectionManager.send_message(clientSocket, STAGE2NOTTURNCODE)
                RSPServer.connectionCount += 1
                if RSPServer.connectionCount == 2:
                    RSPServer.turnInformFlag = False
                    RSPServer.connectionCount = 0

            elif RSPServer.startStageFlag:
                # 스테이지 2 시작코드 전송
                self.connectionManager.send_message(clientSocket, STAGE2STARTCODE)
                RSPServer.connectionCount += 1
                if RSPServer.connectionCount == 2:
                    RSPServer.startStageFlag = False
                    RSPServer.connectionCount = 0

            else:
                # 상대 클라와 내 클라 둘 다 입력을 끝냈을 때
                if RSPServer.playerInputReceived[index] and RSPServer.playerInputReceived[opponentIndex]:

                    myChoice = RSPServer.playerInput[index]
                    oppChoice = RSPServer.playerInput[opponentIndex]

                    # 결과 계산
                    if myChoice == oppChoice:
                        if RSPServer.currentPlayerTurn[index]:
                            RSPServer.stage2Result[index] = "Win"
                        elif not RSPServer.currentPlayerTurn[index]:
                            RSPServer.stage2Result[index] = "Lose"

                    elif myChoice == ROCKCODE:
                        RSPServer.stage2Result[index] = "Draw"
                        if oppChoice == SCISSORSCODE:
                            if not RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = True
                        elif oppChoice == PAPERCODE:
                            if RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = False
                    
                            
                    elif myChoice == SCISSORSCODE:
                        RSPServer.stage2Result[index] = "Draw"
                        if oppChoice == PAPERCODE:
                            if not RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = True
                        elif oppChoice == ROCKCODE:
                            if RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = False

                    elif myChoice == PAPERCODE:
                        RSPServer.stage2Result[index] = "Draw"
                        if oppChoice == ROCKCODE:
                            if not RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = True
                        elif oppChoice == SCISSORSCODE:
                            if RSPServer.currentPlayerTurn[index]:
                                RSPServer.currentPlayerTurn[index] = False

                    # 결과
                    print(username + " " + RSPServer.stage2Result[index])

                    # 결과에 따라 동작
                    # 무승부일 때 스테이지 재시작
                    if RSPServer.stage2Result[index] == "Draw":
                        self.connectionManager.send_message(clientSocket, STAGE2DRAWCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.turnInformFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                    # 누군가의 승리일 때 스코어 변경
                    else:
                        if RSPServer.stage2Result[index] == "Win":
                            self.connectionManager.send_message(clientSocket, STAGE2WINCODE)

                        elif RSPServer.stage2Result[index] == "Lose":
                            self.connectionManager.send_message(clientSocket, STAGE2LOSECODE)

                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.scoreList[index] += 1
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                            print("Stage 2 end")
                            RSPServer.endStage0Flag = False
                            RSPServer.stage = 0
                            RSPServer.endStage2Flag = True
                            RSPServer.startStageFlag = True
                            RSPServer.turnInformFlag = True
                        time.sleep(3)

                        # 최종 승자 발생시
                        if RSPServer.scoreList[index] == WINNINGSCORE or RSPServer.scoreList[opponentIndex] == WINNINGSCORE:
                            if RSPServer.scoreList[index] == WINNINGSCORE:
                                self.connectionManager.send_message(clientSocket, FINALWINCODE)
                            elif RSPServer.scoreList[opponentIndex] == WINNINGSCORE:
                                self.connectionManager.send_message(clientSocket, FINALLOSECODE)
                            RSPServer.connectionCount += 1
                            if RSPServer.connectionCount == 2:
                                RSPServer.scoreList[index] += 1
                                RSPServer.startStageFlag = True
                                RSPServer.playerInputReceived = [False, False]
                                RSPServer.playerInput = ["", ""]
                                RSPServer.connectionCount = 0
                                RSPServer.restartFlag = False
                                print("Stage 2 end, Connection over")
                                RSPServer.endStage0Flag = False
                                RSPServer.stage = 0
                                RSPServer.endStage2Flag = True
                                RSPServer.startStageFlag = True
                            # 쓰레드 연결 해제, 스테이지 0으로 이동
                            self.remove_from_list(index)

                        # 최종 승자 아직 없음
                        else:
                            # 스코어 전송
                            self.connectionManager.send_message(clientSocket, "Score: " + str(RSPServer.scoreList[index]) + " OpponentScore: " + str(RSPServer.scoreList[opponentIndex]))

                            time.sleep(3)
                            # 스테이지 1로 이동
                            self.connectionManager.send_message(clientSocket, STAGE2TO1CODE)
                            RSPServer.connectionCount += 1
                            if RSPServer.connectionCount == 2:
                                RSPServer.scoreList[index] += 1
                                RSPServer.startStageFlag = True
                                RSPServer.playerInputReceived = [False, False]
                                RSPServer.playerInput = ["", ""]
                                RSPServer.connectionCount = 0
                                RSPServer.restartFlag = False
                                print("Stage 2 end, Connection over")
                                RSPServer.endStage0Flag = False
                                RSPServer.stage = 0
                                RSPServer.endStage2Flag = True
                                RSPServer.startStageFlag = True
                    # 2초 슬립
                    time.sleep(2)

                # 상대 클라와 내 클라 둘 중에 하나가 입력을 끝냈을 때
                elif RSPServer.playerInputReceived[index] or RSPServer.playerInputReceived[opponentIndex]:
                    # RestartFlag가 살아있을 경우
                    if RSPServer.restartFlag:
                        # RESTART 코드 전송
                        self.connectionManager.send_message(clientSocket, RESTARTCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                    return

                # 상대 클라와 내 클라 둘 다 입력을 하지 않았을 때
                else:
                    # RestartFlag가 살아있을 경우
                    if RSPServer.restartFlag:
                        # RESTART 코드 전송
                        self.connectionManager.send_message(clientSocket, RESTARTCODE)
                        RSPServer.connectionCount += 1
                        if RSPServer.connectionCount == 2:
                            RSPServer.startStageFlag = True
                            RSPServer.playerInputReceived = [False, False]
                            RSPServer.playerInput = ["", ""]
                            RSPServer.connectionCount = 0
                            RSPServer.restartFlag = False
                        return

                    # 메시지를 받음
                    msg = self.connectionManager.receive_message(clientSocket)
                    
                    # 받은 메시지가 비어있으면 리턴
                    if msg == None or "":
                        return    

                    # 공백 기준으로 자름
                    msg = msg.split()
                    
                    # 잘라서 두개의 요소가 나오고 내 입력이 비어있을 경우
                    if len(msg) == 2 and not RSPServer.playerInputReceived[index]:
                        # Undecided 코드가 오면 Restart 플래그를 세움
                        if msg[1] == UNDECIDEDCODE:
                            RSPServer.restartFlag = True
                        else:
                            if msg[1] == ROCKCODE:
                                RSPServer.playerInput[index] = ROCKCODE
                            elif msg[1] == SCISSORSCODE:
                                RSPServer.playerInput[index] = SCISSORSCODE
                            elif msg[1] == PAPERCODE:
                                RSPServer.playerInput[index] = PAPERCODE
                            # 입력이 되었다고 저장
                            RSPServer.playerInputReceived[index] = True
                            print("Player Input : " + str(RSPServer.playerInputReceived))              
        return




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

    print('RSP game fin')
    server.end_server()



