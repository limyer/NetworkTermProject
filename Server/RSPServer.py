# 컴퓨터네트워크 묵찌빠 ver 1.0
# 최종 수정: 2020 05 15 15:54 - 임예랑
# 수정해서 깃허브 Push할 때마다 변경해주세요
# 아직 고칠 부분 많음

from socket import *
from _thread import *
import random as r

pvsc=[0,0]
win=[0,0]
RSP_resultboard=[['win','lose'],['win', 'lose'],['win','lose']]


# 쓰레드 생성될 때 하는 동작
def threaded(clientSocket, addr):
    print('Connected by:', addr[0], ':', addr[1])

# RSP서버 클래스
# 서버의 동작은 전부 여기 정의해주세요
class RSPServer:
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    stage=0
    connectionCount = 0

    def startServer(self):
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1)
        print('The server is ready to receive')
    
    def endServer(self):
        serverSocket.close()

    # 쓰레드에서 소켓 만들도록 함
    def openSocket(self):
        print('waiting to be connected')
        clientSocket, addr = serverSocket.accept()
        threadA = start_new_thread(threaded, (clientSocket, addr))
    



# 서버 오브젝트 생성 후 동작
server = RSPServer()
server.startServer()
server.openSocket()


# 서버 클래스에 함수로 정의
# 수정해주세요
# while 1:
#       com=r.randint(0,2)
#       player = connectionSocket.recv(1024)
#       if player==b'0':
#             player_card=0
#       elif player==b'1':
#             player_card=1
#       elif player==b'2':
#             player_card=2
#       print(player,'\n',com,'\n',player_card)
#       print(RSP_resultboard[player_card][com])
#       #capitalizedSentence = sentence.upper()
#       #connectionSocket.send(capitalizedSentence)
#       if step==0:
#             if player_card!=com:
#                   if RSP_resultboard[player_card][com]=='win':
#                         pvsc[0]=1
#                         connectionSocket.send('you win! you are now attacker'.encode())
#                   else:
#                         pvsc[1]=1
#                         connectionSocket.send('you lose... you are now deffender'.encode())
#                   step+=1
#             else:
#                   connectionSocket.send('draw try one more time'.encode())
#       elif step==1:
#             if pvsc[0]==1:
#                   if RSP_resultboard[player_card][com]=='lose':
#                         pvsc[0]=0
#                         pvsc[1]=1
#                         connectionSocket.send('you lose... you are now deffender'.encode())
#                   elif RSP_resultboard[player_card][com]=='draw':
#                         win[0]=1
#                         connectionSocket.send('Oh you win!!'.encode())
#                         connectionSocket.close()
#                         break
#             if pvsc[1]==1:
#                   if RSP_resultboard[player_card][com]=='win':
#                         pvsc[1]=0
#                         pvsc[0]=1
#                         connectionSocket.send('you win! you are now attacker'.encode())
#                   elif RSP_resultboard[player_card][com]=='draw':
#                         win[1]=1
#                         connectionSocket.send('Oh com win..'.encode())
#                         connectionSocket.close()
#                         break
# if win[0]==1:
#       print('player win')
# else:
#       print('com win')

# 서버 끝날 때 하는 동작
server.endServer()