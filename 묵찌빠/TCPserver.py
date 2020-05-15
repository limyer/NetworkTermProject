from socket import *
import random as r
step=0
pvsc=[0,0]
win=[0,0]
RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']]
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while 1:
      com=r.randint(0,2)
      connectionSocket, addr = serverSocket.accept()
      player = connectionSocket.recv(1024)
      if player==b'0':
            player_card=0
      elif player==b'1':
            player_card=1
      elif player==b'2':
            player_card=2
      print(player,'\n',com,'\n',player_card)
      print(RSP_resultboard[player_card][com])
      #capitalizedSentence = sentence.upper()
      #connectionSocket.send(capitalizedSentence)
      if step==0:
            if player_card!=com:
                  if RSP_resultboard[player_card][com]=='win':
                        pvsc[0]=1
                        connectionSocket.send('you win! you are now attacker'.encode())
                  else:
                        pvsc[1]=1
                        connectionSocket.send('you lose... you are now deffender'.encode())
                  step+=1
            else:
                  connectionSocket.send('draw try one more time'.encode())
      elif step==1:
            if pvsc[0]==1:
                  if RSP_resultboard[player_card][com]=='lose':
                        pvsc[0]=0
                        pvsc[1]=1
                        connectionSocket.send('you lose... you are now deffender'.encode())
                  elif RSP_resultboard[player_card][com]=='draw':
                        win[0]=1
                        connectionSocket.send('Oh you win!!'.encode())
                        connectionSocket.close()
                        break
            if pvsc[1]==1:
                  if RSP_resultboard[player_card][com]=='win':
                        pvsc[1]=0
                        pvsc[0]=1
                        connectionSocket.send('you win! you are now attacker'.encode())
                  elif RSP_resultboard[player_card][com]=='draw':
                        win[1]=1
                        connectionSocket.send('Oh com win..'.encode())
                        connectionSocket.close()
                        break
if win[0]==1:
      print('player win')
else:
      print('com win')
