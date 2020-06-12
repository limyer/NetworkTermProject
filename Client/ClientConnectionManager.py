from socket import *

class ClientConnectionManager:
    def __init__(self, HOST, PORT):
        self.serverHost = HOST
        self.serverPort = PORT
        self.socketMade = False
    
    def makeConnection(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.socketMade = True
        try:
            self.clientSocket.connect((self.serverHost,self.serverPort))
            self.clientSocket.settimeout(1)
            return True
        except error:
            return False

    def sendMessage(self, message):
        if self.socketMade:
            try:
                self.clientSocket.send(message.encode())
                return True
            except error:
                return False
        else:
            return False
    
    def receiveMessage(self):
        try:
            msg = self.clientSocket.recv(1024)
            return msg.decode()
        except timeout:
            return None

    def closeSocket(self):
        self.clientSocket.close()
