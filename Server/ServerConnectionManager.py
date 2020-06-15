from socket import *
from RSPServer import *


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



    # 메시지 전달 함수
    # 송신 성공 여부를 Boolean 값으로 반환
    def send_message(self, clientSocket, message):
        if self.socketMade:
            try:
                clientSocket.send(message.encode())
                print("Message Sent: <" + message + ">" )
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
                print("Received: <" + msg + ">")
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
