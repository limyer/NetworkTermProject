from socket import*
from ClientConnectionManager import *
import tkinter as tk
from tkinter import font  as tkfont 
import tkinter.ttk

# lose_code='lose'
# code=0

HOST = '127.0.0.1'
PORT = 12000
BREAKCODE = 'BREAK'
OKCODE = 'OK'
TIMEOUT = 11

# RSP 클라이언트
# Shared_Data에 클라이언트 정보 통합 저장
# 프레임을 만들고 Controller로 작동
class RSPClient(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # 공용 저장소
        self.shared_data={
            "username": tk.StringVar(),
            "userHOST": tk.StringVar(),
            "userPORT": tk.StringVar(),
            "connectionManager": None,
            "connected": False,
            "cancelID": None,
            "count": 1,
            "timeOutCount": tk.IntVar(),
            "connectionLabel":tk.StringVar(),
            "score":tk.StringVar(),
            "myScore":0,
            "oppScore":0,
        }

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("RSP Game")

        # 컨테이너를 기반으로 위에 프레임을 쌓아 올리면서 사용
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        # 페이지 목록
        for F in (StartPage, ConnectionPage, ErrorPage, GamePage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # 모든 프레임이 같은 장소에 올라감
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # 주어진 페이지 이름에 맞춰 프레임 raise
        frame = self.frames[page_name]
        frame.tkraise()
        frame.after_raised()
    
    def get_page(self, page_class):
        return self.frames[page_class]


# 시작 페이지
# 서버 IP와 포트, user 이름을 받아 서버에 연결
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 안내 라벨
        welcomeLabel=tk.Label(self, text="Welcome to RSP game.")
        welcomeLabel.pack()

        informLabel=tk.Label(self, text="Type server IP address and PORT number")
        informLabel.pack()

        # IP 주소 엔트리
        IPInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["userHOST"])
        IPInput.insert(0,HOST)
        IPInput.pack()

        # 포트 번호 엔트리
        portInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["userPORT"])
        portInput.insert(0,PORT)
        portInput.pack()

        # 안내 라벨
        usernameLabel=tk.Label(self, text="Type username")
        usernameLabel.pack()

        # 유저 이름 엔트리
        usernameInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["username"])
        usernameInput.pack()

        # 연결 버튼
        connectButton = tk.Button(self, text="Connect", command=self.connection_establishment , overrelief="solid", width=15, repeatdelay=1000, repeatinterval=100)
        connectButton.pack()

    # connect 버튼 눌렸을 경우 실행하는 함수
    def connection_establishment(self):
        self.controller.shared_data["connectionManager"] = ClientConnectionManager(self.controller.shared_data["userHOST"].get(), int(self.controller.shared_data["userPORT"].get()))
        connectionManager = self.controller.shared_data["connectionManager"]
        if connectionManager.make_connection():
            self.controller.show_frame("ConnectionPage")
            self.controller.shared_data["connected"] = True
        else:
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
    
    # raise 되고 실행되는 함수
    def after_raised(self):
        return
            

# 연결 시도 중일 때 뜨는 페이지
# 타임아웃이 완료될 때까지, 혹은 서버가 코드를 보낼 때까지 대기
class ConnectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        connectionLabel = self.controller.shared_data["connectionLabel"]

        # 안내 라벨
        label = tk.Label(self, text="Connecting", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # 연결 중임을 알리는 라벨
        connectionLabel=tk.Label(self, textvariable=connectionLabel)
        connectionLabel.pack()

        # 연결 취소 버튼
        button = tk.Button(self, text="Cancel",
                           command=self.cancel_connection )
        button.pack()

    # raise 되고 실행되는 함수
    def after_raised(self):
        connectionManager = self.controller.shared_data["connectionManager"]

        count = self.controller.shared_data["count"]
        try:
            # username이 성공적으로 전달 됐을 경우
            if connectionManager.send_message(self.controller.shared_data["username"].get()):
                # receivercode 스레드로 재귀 실행 시작
                self.after(1, self.receive_code)
            # 전달 실패 시
            else:
                self.cancel_thread()
                self.controller.show_frame("ErrorPage")
                self.controller.shared_data["connected"] = False
            return
        except error:
            self.cancel_thread()
            return

    # 실제로 코드를 받으며 카운트를 재는 함수
    def receive_code(self):
        count = self.controller.shared_data["count"]
        connectionManager = self.controller.shared_data["connectionManager"]
        username = self.controller.shared_data["username"].get()

        # 카운트 +1
        self.controller.shared_data["count"] += 1

        # 연결 중 라벨 업데이트
        self.controller.shared_data["connectionLabel"].set("Waiting to be connected, " + username + ", " + str(count))
        print(self.controller.shared_data["count"])

        # 실제로 메시지 수신
        msg = connectionManager.receive_message()
        print(msg)

        # 서버가 두 명이 접속하여 성공했음을 알림
        if msg == OKCODE:
            self.cancel_thread()
            self.controller.shared_data["connectionLabel"].set("Game Starting...")
            # 3초 후에 게임 페이지로 이동
            self.after(3000, self.controller.show_frame("GamePage"))
        # 클라이언트가 두 명 이상이기 때문에 서버가 거부 
        elif msg == BREAKCODE:
            self.cancel_thread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        # 지정된 타임아웃이 아직 안되었을 경우
        elif count < TIMEOUT:
            # 타임아웃 종료까지 1초에 한번 코드를 받음
            self.controller.shared_data["cancelID"] = self.after(1000, self.receive_code)
        # 타임아웃
        else:
            self.cancel_thread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        return
    
    # 현재 존재하는 스레드를 끝냄
    # 타임아웃 카운트 초기화
    def cancel_thread(self):
        if self.controller.shared_data["cancelID"] != None:
            self.after_cancel(self.controller.shared_data["cancelID"])
            self.controller.shared_data["cancelID"] = None
            self.controller.shared_data["count"] = 0
    
    # 연결 실패시 스레드를 끝내고 소켓 해제
    def cancel_connection(self):
        self.cancelThread()
        self.controller.show_frame("StartPage")
        self.controller.shared_data["connectionManager"].close_socket()


# 연결 에러가 발생할 경우 이동하는 페이지
class ErrorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 에러 라벨
        label = tk.Label(self, text="Connection Error", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        # 시작 페이지로 이동 버튼
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    # raise 되고 실행되는 함수
    def after_raised(self):
        return


# 실제 게임 실행 페이지
class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        score = self.controller.shared_data["score"]

        # 스코어 라벨
        scoreLabel = tk.Label(self, textvariable=score, font=controller.title_font, width=30)
        scoreLabel.grid(row=0, column=0, pady=10,sticky="n", rowspan=3,columnspan=3)

        # 안내 라벨
        self.informLabel = tk.Label(self, text="Make your choice")
        self.informLabel.grid(row=3, column=0, pady=10,sticky="n", rowspan=2,columnspan=3)

        # 가위바위보 버튼
        self.rockButton = tk.Button(self, text="Rock", width=10, height=10,
                           command=lambda: self.choice_made("rock"), repeatdelay=100)
        self.rockButton.grid(row=5, column=0, sticky="s")

        self.scissorsButton = tk.Button(self, text="Scissor",width=10, height=10,
                           command=lambda: self.choice_made("scissors"), repeatdelay=100)
        self.scissorsButton.grid(row=5, column=1,sticky="s")

        self.paperButton = tk.Button(self, text="Paper",width=10, height=10,
                           command=lambda: self.choice_made("paper"), repeatdelay=100)
        self.paperButton.grid(row=5, column=2, sticky="s")

        # 타임아웃 안내 진행바
        self.progressbar=tkinter.ttk.Progressbar(self, length=300, maximum=100, variable=self.controller.shared_data["timeOutCount"],mode="determinate")
        self.progressbar.grid(row=6, column=0, pady=5, columnspan=3)


    def after_raised(self):
        self.score_update()
        self.progressbar.start(100)
        self.after(1, self.stop_progressbar)
        return
    
    def stop_progressbar(self):
        self.controller.shared_data["cancelID"] = self.after(50, self.stop_progressbar)
        if self.controller.shared_data["timeOutCount"].get() == 99:
            self.progressbar.stop()
            self.cancel_thread()
            self.controller.shared_data["timeOutCount"].set(0)
            self.informLabel.config(text="Timeout! Waiting for the other player")
            self.disable_buttons()

    def score_update(self):
        score = self.controller.shared_data["score"]
        myScore = self.controller.shared_data["myScore"]
        oppScore = self.controller.shared_data["oppScore"]
        score.set("My Score " + str(myScore) + ", Opponent Score " + str(oppScore))
    
    def disable_buttons(self):
        self.rockButton.config(state="disabled")
        self.scissorsButton.config(state="disabled")
        self.paperButton.config(state="disabled")
    
    def choice_made(self, choice):
        connectionManager = self.controller.shared_data["connectionManager"]
        self.progressbar.stop()
        self.cancel_thread()
        self.controller.shared_data["timeOutCount"].set(0)
        self.informLabel.config(text="Choice made: " + choice.upper())
        self.disable_buttons()


    def cancel_thread(self):
        if self.controller.shared_data["cancelID"] != None:
            self.after_cancel(self.controller.shared_data["cancelID"])
            self.controller.shared_data["cancelID"] = None
            



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
