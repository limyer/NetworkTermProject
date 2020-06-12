from socket import *
import threading

ADDR=('',12000)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(1)

index=0 #접속한 사람 수
t=[] #쓰레드
score=[0,0]





def socketThread():
    global index
    clientSocket,addr=serverSocket.accept()
    playerNumber=index
    index+=1
    print(f'player {playerNumber+1} connected {addr}')
    
    clientSocket.send('enter your name:'.encode())
    name=clientSocket.recv(2048).decode() #이름 지정
    print(f'player {playerNumber+1} name: {name}')
        
        
        
        
def RSPStage1(player1,player2):
    if player1==player2:
        return 2 #비길 경우 2
    elif (player1=='묵' and player2=='찌') or (player1=='찌' and player2=='빠') or (player1=='빠' and player2=='묵'):
        return 0 #1번이 이길 경우 0
    elif (player2=='묵' and player1=='찌') or (player2=='찌' and player1=='빠') or (player2=='빠' and player1=='묵'):
        return 1 #2번이 이길 경우 1
    else:
        return 3 #예외
    
def RSPStage2(player1,player2,whoWon): #stage1의 리턴 0, 1을 넣는다.
    global score
    if RSPStage1(player1,player2)==2:
        score[whoWon]+=1
        return 2
    elif RSPStage1(player1,player2)==whoWon:
        return whoWon
    else:
        if whoWon==0:
            return 1
        elif whoWon==1:
            return 0
        
def RSPMain(player1,player2):
        
        

if __name__ == '__main__':
    i=0        
    while i<2:
        t.append(threading.Thread(target=socketThread))
        t[i].daemon=True
        t[i].start()
        i+=1
    RSPMain()