#-*- coding:utf-8 -*-

from socket import *

# 서버 연결 매니저 (Client Side)
class ClientConnectionManager:
    # 생성자 매개변수: HOST IP와 PORT 번호
    def __init__(self, HOST, PORT): 
        self.serverHost = HOST
        self.serverPort = PORT
        self.socketMade = False
    
    # 소켓을 만들고 서버와 연결
    # 타임아웃은 1초
    def make_connection(self):
        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.connect((self.serverHost,self.serverPort))
            self.socketMade = True
            self.clientSocket.settimeout(1)
            return True
        except error:
            return False

    # 메시지 전달 함수
    # 송신 성공 여부를 Boolean 값으로 반환
    def send_message(self, message):
        if self.socketMade:
            try:
                self.clientSocket.send(message.encode())
                return True
            except error:
                return False
        else:
            return False
    
    # 메시지 수신 함수
    # 수신 실패시 None 반환
    def receive_message(self):
        if self.socketMade:
            try:
                msg = self.clientSocket.recv(1024)
                return msg.decode()
            except timeout:
                return None
        else:
            return None

    # 소켓이 만들어져 있을 경우 소켓 연결 해제 
    def close_socket(self):
        if self.socketMade:
            self.clientSocket.close()
            self.socketMade = False
