from socket import * # 2020-06-13 최환효 업데이트
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
gameround = 0
RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']] # 가위바위보 승/무/패 테이블
player_name = ['','']




def socketThread():
    global index
    global clientS
    global clientCard
    global stage1
    global score
    global check
    global retry
    global gameround
    global player_name
    clientSocket,addr=serverSocket.accept()
    playerNumber=index
    clientS.append(clientSocket)
    print(f'player {playerNumber+1} connected {addr}')
    
    clientSocket.send('enter your name:'.encode())
    name=clientSocket.recv(2048).decode() #이름 지정
    print(f'player {playerNumber+1} name: {name}')
    index+=1
    player_name[playerNumber] = name
    print(index)
    
    while True:
        if index==2:
            print(name, ' ', playerNumber)
            break

    #step 1 선후공 결정
    for gameround in range(3):
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
                gameround +=1
                if attacker == 0:
                    score[0] += 1
                    if playerNumber == 0:
                        clientSocket.send('You win!\n'.encode())
                    else:
                        clientSocket.send('You lose\n'.encode())
                elif attacker == 1:
                    score[1] +=1
                    if playerNumber == 0:
                        clientSocket.send('You lose\n'.encode())
                    else:
                        clientSocket.send('You win!\n'.encode())
                break
            
            
        print(score)
        print('round fin')
        # 초기화
        check = 0
        retry = 0
        
        # 누가 이겼는지 출력 구현필요
        if score[0] == 4:
            print(f'player 1 win!')
            winner = player_name[0] + 'win the game'
            clientSocket.send(winner.encode())
            break
        
        elif score[1] == 4:
            print(f'player 2 win!')
            winner = player_name[1] + 'win the game'
            clientSocket.send(winner.encode())
            break
    
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

i=0        
while i<2:
    t.append(threading.Thread(target=socketThread))
    t[i].daemon=True
    t[i].start()
    i+=1
    print('i: ',i)
print('RSP game set fin')
