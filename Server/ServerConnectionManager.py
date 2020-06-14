from socket import *
from RSPServer import *

BREAKCODE = 'Break' # (Code: "Break") 
STAGE0TO1CODE = 'Stage 0 to 1' # (Code: "Stage 0 to 1")
RESTARTCODE = 'Restart' # (Code: "Restart")
REWRITECODE = 'Rewrite'

# 서버 연결 매니저 (Server Side)
class ServerConnectionManager:
    # 생성자 매개변수: HOST IP와 PORT 번호
    # 서버는 기본 호스트 IP ''
    def __init__(self, HOST, PORT): 
        self.serverHost = HOST
        self.serverPort = PORT
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((HOST, PORT))
        self.serverSocket.listen(2)
        self.socketMade = True

    def accept_socket(self):
        try:
            clientSocket, addr = self.serverSocket.accept()
            clientSocket.settimeout(30)
            print('Connected by:', addr[0], ':', addr[1])
            clientThread = self.make_client_thread(clientSocket)
            return clientThread
        except error:
            return "None"

    def make_client_thread(self, clientSocket):
        if len(RSPServer.threadList) >= 2:
            self.receive_message(clientSocket)
            self.send_message(clientSocket, BREAKCODE)
            clientSocket.close()
            return "None"
        else:
            username = self.get_username(clientSocket)
            if username == None:
                return "None"
            while True:
                if username in RSPServer.usernameList:
                    self.send_message(clientSocket, REWRITECODE)
                    username = self.get_username(clientSocket)
                    if username == None:
                        return "None"
                else:
                    break
            RSPServer.usernameList.append(username)
            clientThread = threading.Thread(target=RSPServer.game_run, args=(RSPServer, clientSocket, username))
            return clientThread

    def get_username(self, clientSocket):
        # (Code: "Username: " + username)
        usernameRaw = self.receive_message(clientSocket)
        if usernameRaw != None:
            username = usernameRaw.split()[1]
            return username
        else:
            return None


    def run_client_thread(self, clientThread):
        clientThread.daemon = True
        clientThread.run()
        


    # 메시지 전달 함수
    # 송신 성공 여부를 Boolean 값으로 반환
    def send_message(self, clientSocket, message):
        if self.socketMade:
            try:
                clientSocket.send(message.encode())
                return True
            except error:
                return False
        else:
            return False
    
    # 메시지 수신 함수
    # 수신 실패시 None 반환
    def receive_message(self, clientSocket):
        if self.socketMade:
            try:
                msg = clientSocket.recv(1024).decode()
                print("Received: " + msg)
                return msg
            except timeout:
                return None
        else:
            return None

    # 소켓이 만들어져 있을 경우 서버 소켓 해제
    def close_socket(self):
        if self.socketMade:
            self.serverSocket.close()
            self.socketMade = False
