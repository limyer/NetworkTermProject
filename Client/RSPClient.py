from socket import*
import threading as th
from ClientConnectionManager import *
from ClientTimer import *
import tkinter as tk
from tkinter import font  as tkfont 

# lose_code='lose'
# code=0

HOST = '127.0.0.1'
PORT = 12000

class RSPClient(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data={
            "username": tk.StringVar(),
            "userHOST": tk.StringVar(),
            "userPORT": tk.StringVar(),
        }

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("RSP Game")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, ConnectionPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        welcomeLabel=tk.Label(self, text="Welcome to RSP game.")
        welcomeLabel.pack()

        informLabel=tk.Label(self, text="Type server IP address and PORT number")
        informLabel.pack()

        IPInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["userHOST"])
        IPInput.insert(0,HOST)
        IPInput.pack()

        portInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["userPORT"])
        portInput.insert(0,PORT)
        portInput.pack()

        usernameLabel=tk.Label(self, text="Type username")
        usernameLabel.pack()

        usernameInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["username"])
        usernameInput.pack()


        connectButton = tk.Button(self, text="Connect", command=lambda: controller.show_frame("ConnectionPage"), overrelief="solid", width=15, repeatdelay=1000, repeatinterval=100)
        connectButton.pack()
    

    


class ConnectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        username = self.controller.shared_data["username"]

        label = tk.Label(self, text="Connecting", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        usernameLabel=tk.Label(self, textvariable=username)
        usernameLabel.pack()

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()









if __name__== "__main__":
    app = RSPClient()
    app.mainloop()




    # def check_retry(self):
    #     while 1:
    #         ifCheck=input('Do you want to start a new game? Yes or No')
    #         if ifCheck=='Yes':
    #             return 0
    #             break
    #         elif ifCheck=='No':
    #             return -1
    #             break
    #         else:
    #             print('You wrote wrong answer')

    # def input_player_card(self):
    #     player_card=input('Write your card within 5 seconds:')
    #     check_time()
    #     if check_time==-1:
    #         print('Time over, you lose')
    #         clientSocket,send(lose_card.encode())
    #         return -1
    #     elif check_time==0:
    #         if player_card in card:
    #             print('Your card is',player_card)
    #             clientSocket.send(player_card.encode())
    #             return 0
    #         else:
    #             print('You write wrong card, you lose')
    #             clientSocket.send(lose_card.encode())
    #             return -1

    # def makePlayerName(self):
    #         player_name=input('Enter your name:')
    #         print('Your name is',player_name)
    #         check_player=input('Is it right? yes or no:')
    #         if check_player=='yes':
    #             self.manager.makeConnection()
    #             #연결 실패시 프로그램 종료 연결 성공시 이름을 전송
    #             clientSocket.send(player_name.encode())
    #             return True
    #         else:
    #             return False

    # while 1:
    #     manager = ClientConnectionManager(HOST, PORT)


    #     while 1: # 이름 전송


    #     while 1:
    #         #플레이어의 패를 확인
    #         player_card_result=input_player_card()
    #         if player_card_result==-1:
    #             code=-1
    #             break
    #         #상대방의 패를 확인
    #         recv_enemy_card=clientSocket.recv(1024)
    #         if recv_enemy_card==b'you win':
    #             print('Enemy say lose, you win')
    #             code=-1
    #             break
    #         else:
    #             print("enemy's card is",recv_enemy)
    #         #결과 확인
    #         recv_result=clientSocket.recv(1024)
    #         #선후공이 정해지지 않았을 시 처음으로 돌아가 같은 작업 반복, 선후공이 결정나면 본격적인 게임 시작
    #         if recv_result==b'draw try one more time':
    #             print(recv_result)
    #             continue
    #         else:
    #             print(recv_result) # you win you are attacker or you lose you are deffender
    #             break
    #     if code==-1
    #         retry=check_retry()
    #         if retry==-1:
    #             break
    #         else:
    #             code=0
    #             continue
    #     while 1:
    #         #플레이어의 패를 확인
    #         player_card_result=input_player_card()
    #         if player_card_result==-1:
    #             code=-1
    #             break
    #         #상대방의 패를 확인
    #         recv_enemy_card=clientSocket.recv(1024)
    #         if recv_enemy_card==b'you win':
    #             print('Enemy say lose, you win')
    #             code=-1
    #             break
    #         else:
    #             print("enemy's card is",recv_enemy)
    #         #결과 확인
    #         recv_result=clientSocket.recv(1024)
    #         #플레이어가 승리시
    #         if recv_result==b'win':
    #             print(player_name,'win!')
    #             break
    #         #플레이어가 패배시
    #         elif recv_result=b'lose':
    #             print(player_name,'lose')
    #             break
    #         #선후공이 바뀌거나 유지 될때
    #         else:
    #             print(recv_result)
    #             continue
    #     #재시작 하거나 클라이언트를 종료
    #     code=check_retry()
    #     if code==-1:
    #         clientSocket.close()
    #         break
    #     elif code==0:
    #         clientSocket.close()
    #         continue
