import socket # 쓰레드와 쓰레드간의 통신
from _thread import *
player_list=[] # 플레이어의 이름
log=[] # 로그
count = 0
Ip_list=[] # addr[0]
Ip2_list=[] # addr[1]
porb = 0
ques = 0 # data를 체크한다
player_card=[-1,-1] # 0 = 먼저 온사람, 1 = 나중에 온사람
RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']]
# 쓰레드에서 실행되는 코드입니다. 
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True:
        data = recv_data()
        print('Received from ' + addr[0],':',addr[1] , data.decode())

        # 연결이 해제되었을 경우 클라 종료 쓰레드 종료
        ques = check_recv_data(data)
        if ques == -1:
            break
        else:
            pass
        
        check = check_datatype(data)
        if check == 1:
            
            # 플레이어 등록
            client_socket.send('ok'.encode())
            name = client_socket.recv(1024)
            porb = append_player(name)
            if porb == -1:
                print('fail')
                client_socket.send('fail'.encode())
            elif porb == 1:
                print('ok')
                client_socket.send('ok'.encode())
                print(player_list)
                # 플레이어가 모이면 play코드를 보내어 다음단계로 넘어가게한다
        elif check == 2:
            client_socket.send('ok'.encode())
        #send_data(data)
        
    client_socket.close() 
def recv_data():
    data = client_socket.recv(1024)
    return data

def check_recv_data(data):
    if not data:
        print('Disconnected by ' + addr[0],':',addr[1])
        return -1
    else:
        return 1

def send_data(data):
    client_socket.send(data.encode())

def append_player(name):
    if len(player_list) < 2:
        print('append %s' %name)
        player_list.append(name)
        return 1
    else:
        print('full')
        return -1

def check_datatype(data):
    if data == b'name':
        return 1
    
    elif data == b'card':
        return 2

    elif data == b'check_player':
        return -1

def check_card(data):
    if data == b'0':
        return 0
    
    elif data == b'1':
        return 1

    elif data == b'2':
        return 2
    elif data == b'die':
        print('game over')
        return -1

def check_player(addr):
    if addr[0] == Ip_list[0] and addr[1] == Ip2_list[0]:
        return 0
    elif addr[0] == Ip_list[1] and addr[1] == Ip2_list[1]:
        return 1
    else:
        return -1

def insert_card(card, index):
    player_card[index]=card

def step1():
    client_socket.send('ok'.encode())
    card = client_socket.recv(1024)
    card = check_card(card)
    index = check_player(addr)
    if card == 0:
        insert_card(card, index)
            
    elif card == 1:
        insert_card(card, index)
                
    elif card == 2:
        insert_card(card, index)
            
    elif card == -1:
        return 0
    else:
        return 0
        

HOST = '192.168.43.142'
PORT = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 


    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close()
