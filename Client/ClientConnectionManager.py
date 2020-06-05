from socket import  *
import ClientTimer

class ClientConnectionManager:
    def __init__(self, HOST, PORT):
        self.serverHost = HOST
        self.serverPort = PORT
    
    def makeConnection(self):
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        try:
            self.clientSocket.connect((self.serverHost,self.serverPort))
            return True
        except error:
            return False
