from socket import*
from ClientConnectionManager import *
import tkinter as tk
from tkinter import font  as tkfont 

# lose_code='lose'
# code=0

HOST = '127.0.0.1'
PORT = 12000
BREAKCODE = 'BREAK'
OKCODE = 'OK'
TIMEOUT = 11

class RSPClient(tk.Tk):
# RSP 클라이언트
# Shared_Data에 클라이언트 정보 통합 저장
# 프레임을 만들고 Controller로 작동
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data={
            "username": tk.StringVar(),
            "userHOST": tk.StringVar(),
            "userPORT": tk.StringVar(),
            "connectionManager": None,
            "connected": False,
            "cancelID": None,
            "count": 1,
            "connectionLabel":tk.StringVar(),
        }

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("RSP Game")

        # 컨테이너를 기반으로 위에 프레임을 쌓아 올리면서 사용
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, ConnectionPage, ErrorPage, GamePage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # 모든 프레임이 같은 장소에 올라감
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.afterRaised()
    
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


        connectButton = tk.Button(self, text="Connect", command=self.ConnectionEstablishment , overrelief="solid", width=15, repeatdelay=1000, repeatinterval=100)
        connectButton.pack()

    def ConnectionEstablishment(self):
        self.controller.shared_data["connectionManager"] = ClientConnectionManager(self.controller.shared_data["userHOST"].get(), int(self.controller.shared_data["userPORT"].get()))
        connectionManager = self.controller.shared_data["connectionManager"]
        if connectionManager.makeConnection():
            self.controller.show_frame("ConnectionPage")
            self.controller.shared_data["connected"] = True
        else:
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
    
    def afterRaised(self):
        return
            

class ConnectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        connectionLabel = self.controller.shared_data["connectionLabel"]

        label = tk.Label(self, text="Connecting", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        connectionLabel=tk.Label(self, textvariable=connectionLabel)
        connectionLabel.pack()

        button = tk.Button(self, text="Cancel",
                           command=self.cancelConnection )
        button.pack()

    def afterRaised(self):
        connectionManager = self.controller.shared_data["connectionManager"]

        count = self.controller.shared_data["count"]
        try:
            if connectionManager.sendMessage(self.controller.shared_data["username"].get()):
                self.after(1, self.receiveCode)
            else:
                self.cancelThread()
                self.controller.show_frame("ErrorPage")
                self.controller.shared_data["connected"] = False
            return
        except error:
            self.cancelThread()
            return

    
    def receiveCode(self):
        count = self.controller.shared_data["count"]
        connectionManager = self.controller.shared_data["connectionManager"]
        username = self.controller.shared_data["username"].get()
        self.controller.shared_data["count"] += 1

        self.controller.shared_data["connectionLabel"].set("Waiting to be connected, " + username + ", " + str(count))
        print(self.controller.shared_data["count"])
        msg = connectionManager.receiveMessage()
        print(msg)
        if msg == OKCODE:
            self.cancelThread()
            self.controller.shared_data["connectionLabel"].set("Game Starting...")
            self.after(3000, self.controller.show_frame("GamePage"))
        elif msg == BREAKCODE:
            self.cancelThread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        elif count < TIMEOUT:
            self.controller.shared_data["cancelID"] = self.after(1000, self.receiveCode)
        else:
            self.cancelThread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        return
    
    def cancelThread(self):
        if self.controller.shared_data["cancelID"] != None:
            self.after_cancel(self.controller.shared_data["cancelID"])
            self.controller.shared_data["cancelID"] = None
            self.controller.shared_data["count"] = 0
    
    def cancelConnection(self):
        self.cancelThread()
        self.controller.show_frame("StartPage")
        self.controller.shared_data["connectionManager"].closeSocket()


class ErrorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Connection Error", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def afterRaised(self):
        return


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        scorelabel = tk.Label(self, text="My Score 0, Enemy Score 0", font=controller.title_font, width=30)
        scorelabel.grid(row=0, column=0, pady=10,sticky="n", rowspan=3,columnspan=3)
        label = tk.Label(self, text="Make your choice")
        label.grid(row=3, column=0, pady=10,sticky="n", rowspan=2,columnspan=3)

        rockButton = tk.Button(self, text="Rock", width=10, height=10,
                           command=lambda: controller.show_frame("StartPage"))
        rockButton.grid(row=5, column=0, sticky="s")

        scissorsButton = tk.Button(self, text="Scissor",width=10, height=10,
                           command=lambda: controller.show_frame("StartPage"))
        scissorsButton.grid(row=5, column=1,sticky="s")

        paperButton = tk.Button(self, text="Paper",width=10, height=10,
                           command=lambda: controller.show_frame("StartPage"))
        paperButton.grid(row=5, column=2, sticky="s")

    
    def afterRaised(self):

        return


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
    
    def afterRaised(self):
        return


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
