from socket import * 
import threading
# 라운드 구현 필요
# 클래스 형식으로 하고 싶었으나 여기는 def안에서 다 돌아가게 작성되어있어 부득이하게 주석으로 표시함
ADDR=('192.168.43.142',12000)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(1)

index=0 #접속한 사람 수
t=[] #쓰레드
score=[0,0]
clientS=[]
clientCard=[-5,-5]
stage=0
stage1=0
check = 0 # 두명 모두 값을 입력했는지를 확인
retry = 0 # 몇번 다시했나 체크 
attacker = -1 # 공격자 저장
RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']] # 가위바위보 승/무/패 테이블





def socketThread():
    global index
    global clientS
    global clientCard
    global stage1
    global check
    global retry
    clientSocket,addr=serverSocket.accept()
    playerNumber=index
    clientS.append(clientSocket)
    print(f'player {playerNumber+1} connected {addr}')
    
    clientSocket.send('enter your name:'.encode())
    name=clientSocket.recv(2048).decode() #이름 지정
    print(f'player {playerNumber+1} name: {name}')
    index+=1
    print(index)
    
    while True:
        if index==2:
            print(name, ' ', playerNumber)
            break

    #step 1 선후공 결정
    print('step 1')
    while True:
        if retry == 0:
            clientSocket.send('enter your card'.encode())
        else:
            pass
        data = clientSocket.recv(2048).decode()
        print(data)
        clientCard[playerNumber]= return_int(data)
        check += 1
        while True:
            if check == 2:
                break
        print(clientCard)
        res = RSP_resultboard[clientCard[0]][clientCard[1]]
        if res == 'win':
            attacker = 0
            if playerNumber == 0:
                clientSocket.send('you are attacker\n enter your card'.encode())
            else:
                clientSocket.send('you are deffender\n enter your card'.encode())
            break
        elif res == 'lose':
            attacker = 1
            if playerNumber == 0:
                clientSocket.send('you are deffender\n enter your card'.encode())
            else:
                clientSocket.send('you are attacker\n enter your card'.encode())
            break
        elif res == 'draw':
            clientSocket.send('try again'.encode())
            retry += 1
            check = 0
            continue
    
    # 초기화
    check = 0
    retry = 0
    # step 2 승패 결정
    print('step 2')
    while True:
        print(retry)
        if retry == 0:
            clientSocket.send('enter your card'.encode())
        else:
            pass
        data = clientSocket.recv(2048).decode()
        print(data)
        clientCard[playerNumber]= return_int(data)
        check += 1
        while True:
            if check == 2:
                break
        print(clientCard)
        res = RSP_resultboard[clientCard[0]][clientCard[1]]
        if res == 'win':
            retry += 1
            attacker = 0
            if playerNumber == 0:
                clientSocket.send('you are attacker\n enter your card'.encode())
            else:
                clientSocket.send('you are deffender\n enter your card'.encode())
            continue
        
        elif res == 'lose':
            retry += 1
            attacker = 1
            if playerNumber == 0:
                clientSocket.send('you are deffender\n enter your card'.encode())
            else:
                clientSocket.send('you are attacker\n enter your card'.encode())
            continue
            
        elif res == 'draw':
            if attacker == 0:
                if playerNumber == 0:
                    clientSocket.send('You win!'.encode())
                else:
                    clientSocket.send('You lose'.encode())
            elif attacker == 1:
                if playerNumber == 0:
                    clientSocket.send('You lose'.encode())
                else:
                    clientSocket.send('You win!'.encode())
            break
    
    print('round fin')
    # 누가 이겼는지 출력 구현필요
    
# 받은 data를 str에서 int로 바꾸어 준다            
def return_int(data):
    if data == '0':
        return 0
    elif data == '1':
        return 1
    elif data == '2':
        return 2
    else:
        return -1
        
# 밑의 코드는 쓰지 않아도 된다 
'''def RSPStage1(player1,player2):
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
            return 0'''
        
        
i=0        
while i<2:
    t.append(threading.Thread(target=socketThread))
    t[i].daemon=True
    t[i].start()
    i+=1
    print('i: ',i)
print('RSP game set fin')
# 밑의 주석은 필요가 없다 그 이유는 이미 위의 코드로인해 두개의 쓰래드가 생성되고, 계속 돌고 있기 때문에 밑의 코드를 구현할 이유가 없다.
'''whoWon=2
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
'''
