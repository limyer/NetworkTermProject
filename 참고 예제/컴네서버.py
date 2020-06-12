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
        self.myindex = -1
        self.RSP_resultboard=[['draw','win','lose'],['lose','draw','win'],['win','lose','draw']]
    def run(self):
        global index
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
        while True:
            if len(player) == 2:
                self.c_send('play')
                break
        print('next step')
        self.step2(addr)
        print('next step')
        self.step3(addr)
        
        
    def step2(self, addr):
        # 선후공 결정
        print(player)
        while True:
            card = self.c_recv()
            c_card = self.check_card(card)
            print(c_card)
            if c_card==3:
                # 3이면 기권패 처리, 클라에서는 버튼선택 이므로 구현 하지 않아도 된다
                return 0
            add=self.check_addr(addr[0], addr[1])
            print(add)
            card_table[add] = c_card
            print(card_table)
            log.append(c_card)
            while True:
                if len(log) == 2:
                    break
            res = self.check_res()
            if res == 'draw':
                self.send_res(res)
                continue
            else:
                self.send_res(res)
                break
        # 카드 테이블 초기화
        card_table[0] = -1
        card_table[1] = -1
            
                
            
        
    def step3(self, addr): # 라운드 승패 결정
        add=self.check_addr(addr[0], addr[1])
        #print(add)
        while True:
            card_table[0] = -1
            card_table[1] = -1
            card = self.c_recv()
            c_card = self.check_card(card)
            print(c_card)
            card_table[add] = c_card
            print(card_table)
            log.append(c_card)
            while True:
                if len(log) % 2 == 0:
                    print('fin break')
                    break
            res = self.check_res()
            if res == 'draw':
                self.c_send('%s win' % player[attacker])
                break
            else:
                self.send_res(res)
    
            
                
            
    def send_res(self, res):
        if res == 'win':
            self.c_send('win')
        elif res == 'draw':
            self.c_send('draw')
        else:
            self.c_send('lose')
            
    def check_res(self):
        if -1 not in card_table:
            res = self.RSP_resultboard[card_table[0]][card_table[1]]
            if res == 'win':
                attacker = 0
            elif res == 'lose':
                attacker = 1
            if self.myindex == 0:
                return res
            else:
                if res == 'win':
                    return 'lose'
                        
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
