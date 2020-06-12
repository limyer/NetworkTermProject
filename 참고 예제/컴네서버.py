from socket import *
import threading

host = '192.168.43.142'
port = 12000
t=[]
player = []
addr0 =[]
addr1 =[]
index = 0

class Cserver(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.s_socket=socket
        self.card_table = [-1,-1]
        self.RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']]

    def run(self):
        global index
        # 연결
        self.c_socket, addr = self.s_socket.accept()
        print(addr[0], addr[1], '이 연결되었습니다')
        addr0.append(addr[0])
        addr1.append(addr[1])
        print(index)
        index += 1
        create_thread(self.s_socket)
        # 플레이어 추가
        data = self.c_recv()
        player.append(data)
        print(player)
        # 플레이어가 2명이면 play 전송
        while True:
            if len(player) == 2:
                self.c_send('play')
                break
        print('next step')
        # step2 선후공 결정
        while True:
            card = self.c_recv()
            c_card = check_card(card)
            print(c_card)
            if c_card == -1:
                self.c_send('you lose')
                break
            else:
                num = check_addr(addr[0], addr[1])
                self.card_table[num]=c_card
                print('num: ',num)
                
                while True:
                    if len(self.card_table) == 2:
                        '''에러발생 card_table[0] = 먼저온사람 card_table[1] = 나중에온사람
                           이 위에 까지는 별 문제가 없다. 이 부분에서 에러가 났다.
                           카드는 0,1,2 의 형태로 저장 되어있으며 0=묵,1=가위,2=보 로 저장되어있다
                           RSP_resultboard[0][1]이면, 먼저온사람은 묵을 나중에온사람은 가위를 낸것이다.
                           인덱스에 맞추어 결과를 저장했다.'''
                        
                        res = self.RSP_resultboard[self.card_table[0],self.card_table[1]]
                        self.c_send(res)
                        break
        

    def c_recv(self):
        try:
            get_data = self.c_socket.recv(1024)
            if not get_data:
                print('quit')

            print(get_data.decode())

        except ConnectionResetError as e:
            print('quit')
        return get_data

    def c_send(self, put_data):
        self.c_socket.send(put_data.encode())

def create_thread(s_socket):
    global index
    t.append(Cserver(s_socket))
    t[index].daemon = True
    t[index].start()

def check_card(data):
    if data == b'0':
        return 0
    elif data == b'1':
        return 1
    elif data == b'2':
        return 2
    else:
        return -1

def check_addr(addr_0, addr_1):
    if addr_0 == addr0[0] and addr_1 == addr1[0]:
        return 0
    else:
        return 1

s_socket = socket(AF_INET, SOCK_STREAM)
s_socket.bind((host,port))
s_socket.listen(1)
create_thread(s_socket)
while True:
    try:
        for i in t:
            i.c_send('put_data'.encode())
    except Exception as e:
        pass
for f in t:
    try:
        j.c_socket.close()
    except Exception as e:
        pass
s_socket.close()
