from socket import  *

class ClientConnectionManager:
    def __init__(self, HOST, PORT):
        self.serverHost = HOST
        self.serverPort = PORT
    
    def makeConnection(self):
        print('Connecting...')
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.serverHost,self.serverPort))