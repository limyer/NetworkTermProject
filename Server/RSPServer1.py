from socket import *
import threading

ADDR=('',12000)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(1)

index=0 #접속한 사람 수
t=[] #쓰레드
score=[0,0]
clientS=[]
clientCard=['','']
stage=0
stage1=0





def socketThread():
    global index
    global clientS
    global clientCard
    global stage1
    clientSocket,addr=serverSocket.accept()
    playerNumber=index
    index+=1
    clientS.append(clientSocket)
    print(f'player {playerNumber+1} connected {addr}')
    
    clientSocket.send('enter your name:'.encode())
    name=clientSocket.recv(2048).decode() #이름 지정
    print(f'player {playerNumber+1} name: {name}')
    
    while True:
        if index==2:
            clientSocket.send('enter your card'.encode())
            clientCard[playerNumber]=clientSocket.recv(2048).decode()
            stage1=1
            if stage==3:
                break
            
    
            
        
        
        
        
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
        return 2
    elif RSPStage1(player1,player2)==whoWon:
        return whoWon
    else:
        if whoWon==0:
            return 1
        elif whoWon==1:
            return 0
        
        
i=0        
while i<2:
    t.append(threading.Thread(target=socketThread))
    t[i].daemon=True
    t[i].start()
    i+=1

whoWon=2
while True:
    if score[0] or score[1]==3:
       stage=3
    
    if clientCard[0]!='' and clientCard[1]!='' and stage==0 and stage1==1:
        if RSPStage1(clientCard[0],clientCard[1])==2:
            clientS[0].send('무승부 stage1'.encode())
            clientS[1].send('무승부 stage1'.encode())
            stage1=0
        else:
            whoWon=RSPStage1(clientCard[0],clientCard[1])
            clientS[0].send(f'{whoWon+1}번 승 stage1'.encode())
            clientS[1].send(f'{whoWon+1}번 승 stage1'.encode())
            stage=1
            stage1=0
    
    if stage==1 and stage1==1:
        if RSPStage2(clientCard[0],clientCard[1],whoWon)==2:
            score[whoWon]+=1
            clientS[0].send(f'{whoWon+1}번 승 stage2'.encode())
            clientS[1].send(f'{whoWon+1}번 승 stage2'.encode())
            stage=0
            stage1=0
        elif RSPStage2(clientCard[0],clientCard[1],whoWon)!=whoWon:
            whoWon=RSPStage2(clientCard[0],clientCard[1],whoWon)
            clientS[0].send(f'{whoWon+1}번이 공격 stage2'.encode())
            clientS[1].send(f'{whoWon+1}번이 공격 stage2'.encode())
            stage1=0
        else:
            clientS[0].send(f'{whoWon+1}번이 공격 stage2'.encode())
            clientS[1].send(f'{whoWon+1}번이 공격 stage2'.encode())
            stage1=0
            
        
        
    if score[0]==3 or score[1]==3:
        stage==3
        
    if stage==3:
        if score[0]==3:
            clientS[0].send(f'You Win!'.encode())
            clientS[1].send(f'You Lose!'.encode())
        if score[1]==3:
            clientS[1].send(f'You Win!'.encode())
            clientS[0].send(f'You Lose!'.encode())
        cleintS[0].close()
        cleintS[1].close()
        break
