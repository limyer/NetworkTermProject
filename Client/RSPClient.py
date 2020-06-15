#-*- coding:utf-8 -*-

from socket import*
from ClientConnectionManager import *
import tkinter as tk
from tkinter import font  as tkfont 
import tkinter.ttk

# lose_code='lose'
# code=0

HOST = '127.0.0.1'
PORT = 12000
USERNAMECODE = "Username: "
BREAKCODE = 'Break' # (Code: "Break") 
STAGE0TO1CODE = 'Stage 0 to 1' # (Code: "Stage 0 to 1")
STAGE1TO2CODE = 'Stage 1 to 2' # (Code: "Stage 1 to 2")
STAGE2TO1CODE = 'Stage 2 to 1' # (Code: "Stage 2 to 1")
RESTARTCODE = 'Restart' # (Code: "Restart")
STAGE1STARTCODE = 'Receiving Stage 1'
STAGE2STARTCODE = 'Receiving Stage 2'
REWRITECODE = 'Rewrite'
CANCELCODE = 'Cancel'
UNDECIDEDCODE = 'Undecided'
ROCKCODE = 'ROCK'
SCISSORSCODE = 'SCISSORS'
PAPERCODE = 'PAPER'
STAGE1WINCODE = 'Stage1: Win'
STAGE1DRAWCODE = 'Stage1: Draw'
STAGE1LOSECODE = 'Stage1: Lose'
STAGE2TURNCODE = 'Turn'
STAGE2NOTTURNCODE = 'Not Turn'
STAGE2WINCODE = 'Stage2: Win'
STAGE2DRAWCODE = 'Stage2: Draw'
STAGE2LOSECODE = 'Stage2: Lose'
FINALWINCODE = 'Final: Win'
FINALLOSECODE = 'Final: LOSE'
TIMEOUT = 70

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
            "progressbarCancelID": None,
            "count": 1,
            "timeOutCount": tk.IntVar(),
            "connectionLabel":tk.StringVar(),
            "usernameLabel":tk.StringVar(),
            "score":tk.StringVar(),
            "myScore":0,
            "oppScore":0,
            "myTurn": False,
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
        for F in (StartPage, ConnectionPage, ErrorPage, Stage1Page, Stage2Page, VictoryPage, DefeatPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # 모든 프레임이 같은 장소에 올라감
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    # 주어진 페이지 이름에 맞춰 프레임 raise
    def show_frame(self, page_name):
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
        self.controller.shared_data["usernameLabel"].set("유저 이름을 입력해주세요")

        # 안내 라벨
        welcomeLabel=tk.Label(self, text="묵찌빠 게임에 오신 것을 환영합니다")
        welcomeLabel.pack()

        informLabel=tk.Label(self, text="서버 IP와 포트 번호를 입력해주세요")
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
        usernameLabel=tk.Label(self, textvariable=self.controller.shared_data["usernameLabel"])
        usernameLabel.pack()

        # 유저 이름 엔트리
        usernameInput = tk.Entry(self, width=50, textvariable=self.controller.shared_data["username"])
        usernameInput.pack()

        # 연결 버튼
        connectButton = tk.Button(self, text="연결", command=self.connection_establishment , overrelief="solid", width=15, repeatdelay=1000, repeatinterval=100)
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
        label = tk.Label(self, text="연결 중", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # 연결 중임을 알리는 라벨
        connectionLabel=tk.Label(self, textvariable=connectionLabel)
        connectionLabel.pack()

        # 연결 취소 버튼
        button = tk.Button(self, text="취소",
                           command=self.cancel_connection )
        button.pack()

    # raise 되고 실행되는 함수
    def after_raised(self):
        connectionManager = self.controller.shared_data["connectionManager"]

        count = self.controller.shared_data["count"]
        try:
            # username이 성공적으로 전달 됐을 경우
            if connectionManager.send_message(USERNAMECODE + self.controller.shared_data["username"].get()):
                # receive_code 스레드로 재귀 실행 시작
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
        self.controller.shared_data["connectionLabel"].set("서버와 연결을 기다리는 중입니다, " + username + ", " + str(count))
        print(self.controller.shared_data["count"])

        # 실제로 메시지 수신
        msg = connectionManager.receive_message()

        # 서버가 두 명이 접속하여 성공했음을 알림
        if msg == STAGE0TO1CODE:
            self.cancel_thread()
            self.controller.shared_data["connectionLabel"].set("게임 시작 중...")
            # 3초 후에 게임 페이지로 이동
            self.after(3000, self.controller.show_frame("Stage1Page"))
        # 클라이언트가 두 명 이상이기 때문에 서버가 거부 
        elif msg == BREAKCODE:
            self.cancel_thread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        elif msg == REWRITECODE:
            self.cancel_thread()
            self.controller.show_frame("StartPage")
            self.controller.shared_data["usernameLabel"].set("이름을 다시 입력해주세요")
            self.controller.shared_data["connected"] = False
        # 지정된 타임아웃이 아직 안되었을 경우
        elif count < TIMEOUT:
            # 타임아웃 종료까지 1초에 한번 코드를 받음
            self.controller.shared_data["cancelID"] = self.after(1000, self.receive_code)
        # 타임아웃
        elif count >= TIMEOUT:
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
        self.cancel_thread()
        self.controller.show_frame("StartPage")
        self.controller.shared_data["connectionManager"].send_message(CANCELCODE)
        self.controller.shared_data["usernameLabel"].set("유저 이름을 입력해주세요")
        self.controller.shared_data["connectionManager"].close_socket()


# 연결 에러가 발생할 경우 이동하는 페이지
class ErrorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 에러 라벨
        label = tk.Label(self, text="연결 에러", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        # 시작 페이지로 이동 버튼
        button = tk.Button(self, text="시작 페이지로 이동",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    # raise 되고 실행되는 함수
    def after_raised(self):
        return


# Stage 1 게임 실행 페이지
# 그리드 레이아웃으로 구성
class Stage1Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        score = self.controller.shared_data["score"]

        # 스코어 라벨
        self.scoreLabel = tk.Label(self, textvariable=score, font=controller.title_font, width=30)
        self.scoreLabel.grid(row=0, column=0, pady=10,sticky="n", rowspan=3,columnspan=3)

        # 안내 라벨
        self.informLabel = tk.Label(self, text="가위 바위 보를 시작합니다")
        self.informLabel.grid(row=3, column=0, pady=10,sticky="n", rowspan=2,columnspan=3)

        # 가위바위보 버튼
        self.scissorsButton = tk.Button(self, text="가위", width=10, height=10,
                           command=lambda: self.choice_made("SCISSORS"), repeatdelay=100)
        self.scissorsButton.grid(row=5, column=0, sticky="s")

        self.rockButton = tk.Button(self, text="바위",width=10, height=10,
                           command=lambda: self.choice_made("ROCK"), repeatdelay=100)
        self.rockButton.grid(row=5, column=1,sticky="s")

        self.paperButton = tk.Button(self, text="보",width=10, height=10,
                           command=lambda: self.choice_made("PAPER"), repeatdelay=100)
        self.paperButton.grid(row=5, column=2, sticky="s")

        # 타임아웃 안내 진행바
        self.progressbar=tkinter.ttk.Progressbar(self, length=300, maximum=100, variable=self.controller.shared_data["timeOutCount"],mode="determinate")
        self.progressbar.grid(row=6, column=0, pady=5, columnspan=3)


    def after_raised(self):
        count = self.controller.shared_data["count"]

        # 카운트 +1
        self.controller.shared_data["count"] += 1

        connectionManager = self.controller.shared_data["connectionManager"]
        username = self.controller.shared_data["username"].get()

        msg = connectionManager.receive_message()

        # 서버가 게임 시작을 알림
        if msg == STAGE1STARTCODE:
            self.cancel_thread()
            self.start_stage1() 

        elif count < TIMEOUT:
            # 타임아웃 종료까지 1초에 한번 코드를 받음
            self.controller.shared_data["cancelID"] = self.after(100, self.after_raised)
        # 타임아웃
        elif count >= TIMEOUT:
            self.cancel_thread()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        return

    def choice_made(self, choice):
        connectionManager = self.controller.shared_data["connectionManager"]
        self.informLabel.config(text="선택: " + choice.upper() + ", 상대 플레이어의 선택을 기다립니다")
        connectionManager.send_message("Stage1Input: " + choice)
        self.disable_buttons()
        self.after(1, self.receive_code)

    def receive_code(self):
        connectionManager = self.controller.shared_data["connectionManager"]
        msg = connectionManager.receive_message()
        
        self.controller.shared_data["cancelID"] = self.after(100, self.receive_code)

        if msg == STAGE1DRAWCODE:
            self.informLabel.config(text="비겼습니다. 다시 가위바위보를 시작합니다.")
            self.reset()
            self.after(1000, self.after_raised)
        elif msg == RESTARTCODE:
            self.informLabel.config(text="다시 가위바위보를 시작합니다.")
            self.reset()
            self.after(1000, self.after_raised)
        elif msg== STAGE1WINCODE:
            self.controller.shared_data["myTurn"] = True
        elif msg== STAGE1LOSECODE:
            self.controller.shared_data["myTurn"] = False
        elif msg== STAGE1TO2CODE:
            self.reset()
            self.after(1000, lambda: self.controller.show_frame("Stage2Page"))

        return

    def start_stage1(self):
        self.enable_buttons()
        self.score_update()
        self.controller.shared_data["timeOutCount"].set(0)
        self.progressbar.start(100)
        self.after(1, self.stop_progressbar)

    def stop_progressbar(self):
        connectionManager = self.controller.shared_data["connectionManager"]
        self.controller.shared_data["progressbarCancelID"] = self.after(50, self.stop_progressbar)
        if self.controller.shared_data["timeOutCount"].get() == 99:
            self.progressbar.stop()
            self.cancel_progrssThread()
            self.controller.shared_data["timeOutCount"].set(0)
            self.informLabel.config(text="시간 종료!")
            self.disable_buttons()
            connectionManager.send_message("Stage1Input: Undecided")
            self.after(1, self.receive_code)

    def score_update(self):
        score = self.controller.shared_data["score"]
        myScore = self.controller.shared_data["myScore"]
        oppScore = self.controller.shared_data["oppScore"]
        score.set("내 점수: " + str(myScore) + ", 상대 점수 " + str(oppScore))
    
    def enable_buttons(self):
        self.rockButton.config(state="normal")
        self.scissorsButton.config(state="normal")
        self.paperButton.config(state="normal")

    def disable_buttons(self):
        self.rockButton.config(state="disabled")
        self.scissorsButton.config(state="disabled")
        self.paperButton.config(state="disabled")

    def cancel_progrssThread(self):
        if self.controller.shared_data["progressbarCancelID"] != None:
            self.after_cancel(self.controller.shared_data["progressbarCancelID"])
            self.controller.shared_data["progressbarCancelID"] = None

    def cancel_thread(self):
        if self.controller.shared_data["cancelID"] != None:
            self.after_cancel(self.controller.shared_data["cancelID"])
            self.controller.shared_data["cancelID"] = None
            self.controller.shared_data["count"] = 0
    
    def reset(self):
        self.cancel_progrssThread()
        self.cancel_thread()
        self.controller.shared_data["timeOutCount"].set(0)


class Stage2Page(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        score = self.controller.shared_data["score"]

        # 스코어 라벨
        self.scoreLabel = tk.Label(self, textvariable=score, font=controller.title_font, width=30)
        self.scoreLabel.grid(row=0, column=0, pady=10,sticky="n", rowspan=3,columnspan=3)

        # 안내 라벨
        self.informLabel = tk.Label(self, text="가위 바위 보를 시작합니다")
        self.informLabel.grid(row=3, column=0, pady=10,sticky="n", rowspan=2,columnspan=3)

        # 가위바위보 버튼
        self.scissorsButton = tk.Button(self, text="가위", width=10, height=10,
                           command=lambda: self.choice_made("SCISSORS"), repeatdelay=100)
        self.scissorsButton.grid(row=5, column=0, sticky="s")

        self.rockButton = tk.Button(self, text="바위",width=10, height=10,
                           command=lambda: self.choice_made("ROCK"), repeatdelay=100)
        self.rockButton.grid(row=5, column=1,sticky="s")

        self.paperButton = tk.Button(self, text="보",width=10, height=10,
                           command=lambda: self.choice_made("PAPER"), repeatdelay=100)
        self.paperButton.grid(row=5, column=2, sticky="s")

        # 타임아웃 안내 진행바
        self.progressbar=tkinter.ttk.Progressbar(self, length=300, maximum=100, variable=self.controller.shared_data["timeOutCount"],mode="determinate")
        self.progressbar.grid(row=6, column=0, pady=5, columnspan=3)


    def after_raised(self):
        if self.controller.shared_data["myTurn"]:
            self.informLabel.config(text="당신의 턴입니다.")
        else:
            self.informLabel.config(text="상대의 턴입니다.")
        
        count = self.controller.shared_data["count"]

        # 카운트 +1
        self.controller.shared_data["count"] += 1

        connectionManager = self.controller.shared_data["connectionManager"]
        username = self.controller.shared_data["username"].get()

        msg = connectionManager.receive_message()

        # 서버가 게임 시작을 알림
        if msg == STAGE2STARTCODE:
            self.reset()
            self.start_stage2() 
        elif msg == STAGE2TURNCODE:
            self.controller.shared_data["myTurn"] = True
        elif msg == STAGE2NOTTURNCODE:
            self.controller.shared_data["myTurn"] = False
        elif count < TIMEOUT:
            # 타임아웃 종료까지 1초에 한번 코드를 받음
            self.controller.shared_data["cancelID"] = self.after(100, self.after_raised)
        # 타임아웃
        elif count >= TIMEOUT:
            self.reset()
            self.controller.show_frame("ErrorPage")
            self.controller.shared_data["connected"] = False
        return

    def start_stage2(self):
        self.enable_buttons()
        self.score_update()
        self.controller.shared_data["timeOutCount"].set(0)
        self.progressbar.start(100)
        self.after(1, self.stop_progressbar)

    def choice_made(self, choice):
        connectionManager = self.controller.shared_data["connectionManager"]
        if self.controller.shared_data["myTurn"]:
            self.informLabel.config(text="당신의 턴, 선택: " + choice.upper() + ", 상대 플레이어의 선택을 기다립니다")
        else:
            self.informLabel.config(text="상대의 턴, 선택: " + choice.upper() + ", 상대 플레이어의 선택을 기다립니다")
        self.informLabel.config(text="선택: " + choice.upper() + ", 상대 플레이어의 선택을 기다립니다")
        connectionManager.send_message("Stage2Input: " + choice)
        self.disable_buttons()
        self.after(1, self.receive_code)

    def receive_code(self):
        connectionManager = self.controller.shared_data["connectionManager"]
        msg = connectionManager.receive_message()
        
        self.controller.shared_data["cancelID"] = self.after(100, self.receive_code)

        if msg == STAGE2DRAWCODE:
            self.informLabel.config(text="비겼습니다. 다시 묵찌빠를 시작합니다.")
            self.reset()
            self.after(1000, self.after_raised)
        elif msg == RESTARTCODE:
            self.informLabel.config(text="다시 묵찌빠를 시작합니다.")
            self.reset()
            self.after(1000, self.after_raised)
        elif msg== STAGE2WINCODE:
            self.informLabel.config(text="당신의 승리입니다!")
        elif msg== STAGE2LOSECODE:
            self.informLabel.config(text="당신의 패배입니다...")
        elif msg == FINALWINCODE:
            self.reset()
            self.after(1000, lambda: self.controller.show_frame("VictoryPage"))
        elif msg == FINALLOSECODE:
            self.reset()
            self.after(1000, lambda: self.controller.show_frame("DefeatPage"))
        elif msg== STAGE2TO1CODE:
            self.reset()
            self.after(1000, lambda: self.controller.show_frame("Stage1Page"))
        elif msg != None and msg != "":
            msg = msg.split()
            if msg[0] == "Score:":
                self.controller.shared_data["myScore"] = int(msg[1])
                self.controller.shared_data["oppScore"] = int(msg[3])
                self.score_update()
        return

    def stop_progressbar(self):
        connectionManager = self.controller.shared_data["connectionManager"]
        self.controller.shared_data["progressbarCancelID"] = self.after(50, self.stop_progressbar)
        if self.controller.shared_data["timeOutCount"].get() == 99:
            self.progressbar.stop()
            self.cancel_progrssThread()
            self.controller.shared_data["timeOutCount"].set(0)
            self.informLabel.config(text="시간 종료!")
            self.disable_buttons()
            connectionManager.send_message("Stage1Input: Undecided")
            self.after(1, self.receive_code)

    def score_update(self):
        score = self.controller.shared_data["score"]
        myScore = self.controller.shared_data["myScore"]
        oppScore = self.controller.shared_data["oppScore"]
        score.set("내 점수: " + str(myScore) + ", 상대 점수 " + str(oppScore))
    
    def enable_buttons(self):
        self.rockButton.config(state="normal")
        self.scissorsButton.config(state="normal")
        self.paperButton.config(state="normal")

    def disable_buttons(self):
        self.rockButton.config(state="disabled")
        self.scissorsButton.config(state="disabled")
        self.paperButton.config(state="disabled")

    def cancel_progrssThread(self):
        if self.controller.shared_data["progressbarCancelID"] != None:
            self.after_cancel(self.controller.shared_data["progressbarCancelID"])
            self.controller.shared_data["progressbarCancelID"] = None

    def cancel_thread(self):
        if self.controller.shared_data["cancelID"] != None:
            self.after_cancel(self.controller.shared_data["cancelID"])
            self.controller.shared_data["cancelID"] = None
            self.controller.shared_data["count"] = 0
    
    def reset(self):
        self.cancel_progrssThread()
        self.cancel_thread()
        self.controller.shared_data["timeOutCount"].set(0)



class VictoryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="최종 승리!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="시작 페이지로",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
    
    def afterRaised(self):
        return


class DefeatPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="최종 패배..", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="시작 페이지로",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
    
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

