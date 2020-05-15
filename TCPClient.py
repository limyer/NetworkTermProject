from socket import *
serverName = ''
serverPort = 12000
def inputcard():
    player_card=input('write your card: ')
    if player_card=='묵':
        print("your card: 묵")
        card='0'
        clientSocket.send(card.encode())
    elif player_card=='찌':
        print("your card: 찌")
        card='1'
        clientSocket.send(card.encode())
    elif player_card=='빠':
        print("your card: 빠")
        card='2'
        clientSocket.send(card.encode())
    else:
        print('you wrote wrong card')
        inputcard()
res=['묵','찌','빠']
while 1:
    player_name=input('Welecome RSP game!\nEnter your name:')
    print('your name is',player_name)
    checkPN=input('is it wirte? yes or no:')
    if checkPN=='yes':
        break
print('you have 3 cards, 묵, 찌, 빠')
while 1:
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    inputcard() # 이곳에서 자신의 패가 전송 된다.
    modifiedSentence=clientSocket.recv(1024)
    print(modifiedSentence.decode())
    if modifiedSentence==b'Oh com win..':
        clientSocket.close()
        break
    if modifiedSentence==b'Oh you win!!':
        clientSocket.close()
        break

