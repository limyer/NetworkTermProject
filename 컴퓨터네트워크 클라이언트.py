from socket import*
import threading as th
serverName=''
serverPort=12000
card=['묵','찌','빠']
lose_code='lose'
code=0
def check_retry():
    while 1:
        check_retry=input('Are you want to play one more time? yes or no:')
        if check_retry=='yes':
            return 0
            break
        elif check_retry=='no':
            return -1
            break
        else:
            print('You write wrong answer')
def check_time():
    
def input_player_card():
    player_card=input('Write your card within 5 seconds:')
    check_time()
        if check_time==-1:
            print('Time over, you lose')
            clientSocket,send(lose_card.encode())
            return -1
        elif check_time==0:
            if player_card in card:
                print('Your card is',player_card)
                clientSocket.send(player_card.encode())
                return 0
            else:
                print('You write wrong card, you lose')
                clientSocket.send(lose_card.encode())
                return -1

while 1:
    print('Welecome RSP game!')
    
    while 1: # 이름 전송
        player_name=input('Enter your name:')
        print('Your name is',player_name)
        check_player=input('Is it right? yes or no:')
        if check_player=='yes':
            print('Connecting...')
            clientSocket=socket(AF_INET,SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))
            #연결 실패시 프로그램 종료 연결 성공시 이름을 전송
            clientSocket.send(player_name.encode())
            break

    while 1:
        #플레이어의 패를 확인
        player_card_result=input_player_card()
        if player_card_result==-1:
            code=-1
            break
        #상대방의 패를 확인
        recv_enemy_card=clientSocket.recv(1024)
        if recv_enemy_card==b'you win':
            print('Enemy say lose, you win')
            code=-1
            break
        else:
            print("enemy's card is",recv_enemy)
        #결과 확인
        recv_result=clientSocket.recv(1024)
        #선후공이 정해지지 않았을 시 처음으로 돌아가 같은 작업 반복, 선후공이 결정나면 본격적인 게임 시작
        if recv_result==b'draw try one more time':
            print(recv_result)
            continue
        else:
            print(recv_result) # you win you are attacker or you lose you are deffender
            break
    if code==-1
        retry=check_retry()
        if retry==-1:
            break
        else:
            code=0
            continue
    while 1:
        #플레이어의 패를 확인
        player_card_result=input_player_card()
        if player_card_result==-1:
            code=-1
            break
        #상대방의 패를 확인
        recv_enemy_card=clientSocket.recv(1024)
        if recv_enemy_card==b'you win':
            print('Enemy say lose, you win')
            code=-1
            break
        else:
            print("enemy's card is",recv_enemy)
        #결과 확인
        recv_result=clientSocket.recv(1024)
        #플레이어가 승리시
        if recv_result==b'win':
            print(player_name,'win!')
            break
        #플레이어가 패배시
        elif recv_result=b'lose':
            print(player_name,'lose')
            break
        #선후공이 바뀌거나 유지 될때
        else:
            print(recv_result)
            continue
    #재시작 하거나 클라이언트를 종료
    code=check_retry()
    if code==-1:
        clientSocket.close()
        break
    elif code==0:
        clientSocket.close()
        continue
