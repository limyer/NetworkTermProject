import socket 

step = 0
HOST = '192.168.43.142'
PORT = 12000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 

table = [b'win', b'draw', b'lose']

def check_card(card):
    if card == '묵':
        print('your card is 묵')
        client_socket.send('0'.encode())
        
    elif card == '찌':
        print('your card is 찌')
        client_socket.send('1'.encode())
        
    elif card == '빠':
        print('your card is 빠')
        client_socket.send('2'.encode())
        
    else:
        print('wrong card')
        client_socket.send('-1'.encode())
        



while True:
    if step == 0:
        # 이름작성 및 게임에 들어갈 수 있는지를 확인
        name = input('Enter your name: ')
        client_socket.send('name'.encode())
        data = client_socket.recv(1024)
        
        if data == b'ok':
            client_socket.send(name.encode())
            
        else:
            print('error')
            break
            
        if data == b'ok':
            print('ok')
            print('connect ok, please wait other player')
            step += 1
            continue
            
            
        elif data == b'fail':
            print('connect fail')
            client_socket.send('break'.encode())
            break
        
    elif step == 1:
        # 선후공 결정
        card = input('Enter your card in 묵, 찌, 빠: ')
        client_socekt.send('card'.encode())
        ok = client_socket.recv(1024)
        if ok == b'ok':
            # 자신의 카드를 전송하고 클라에 출력한다
            check_card(card)
            data = client_socket.recv(1024)
            if b'win':
                # 공격자 표시
                step += 1
                continue
            elif b'draw':
                # 다시
                
            elif b'lose':
                # 수비자 표시
                step += 1
                continue
            elif b'break':
                # 잘못된 패를 냈기 때문에 게임에서 지게 된다.
                break
            
        else:
            # 핑, 연결해제 같은 문제로 클라이언트 종료
            print('error')
            break
    elif step == 2:
        # 본격적인 묵찌빠 게임 시작
        game = input('Enter your card in 묵, 찌, 빠: ')
        client_socekt.send('game'.encode())
        ok = client_socket.recv(1024)
        if ok == b'ok':
            check_
            
    elif step == 3:
        yorn = input('play again? ')
        if yorn == 'yes':
            step = 0
            continue
        
        else:
            break
    
        
                


    # 구현안된것들 핑, 서버가 강제종료, 클라가 강제종료 상대 클라가 종료 되었을 경우


client_socket.close()
