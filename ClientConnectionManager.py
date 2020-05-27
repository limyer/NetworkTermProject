from socket import  *

class ClientConnectionManager:
    def __init__(self, HOST, PORT):
        self.serverHost = HOST
        self.serverPort = PORT