from socket import*
import threading as th
from ClientConnectionManager import *
from ClientTimer import *
import tkinter as tk

lose_code='lose'
code=0

HOST = '127.0.0.1'
PORT = 12000

class RSPClient:
    def __init__(self, window):
        self.window = window
        self.window.title('RSP Game')
        self.window.geometry("640x400+100+100")

    def getHOSTPORT(self):
        welcomeLabel=tk.Label(self.window, text="Welcome to RSP game.")
        welcomeLabel.pack()

        informLabel=tk.Label(self.window, text="Type server IP address and PORT number to connect")
        informLabel.pack()

        IPInput = tk.Entry(self.window, width=50 )
        IPInput.insert(0,HOST)
        IPInput.pack()

        portInput = tk.Entry(self.window, width=50)
        portInput.insert(0,PORT)
        portInput.pack()

        connectButton = tk.Button(self.window, text="Connect", overrelief="solid", width=15, repeatdelay=1000, repeatinterval=100)
        connectButton.pack()



    def check_retry(self):
        while 1:
            ifCheck=input('Do you want to start a new game? Yes or No')
            if ifCheck=='Yes':
                return 0
                break
            elif ifCheck=='No':
                return -1
                break
            else:
                print('You wrote wrong answer')

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





def main():
    window = tk.Tk()
    client = RSPClient(window)
    client.getHOSTPORT()
    client.window.mainloop()

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


if __name__ == '__main__':
	main()