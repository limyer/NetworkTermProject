# 컴네서버.py에서 받은 addr, addr0, addr1을 받는다.
class Log():
    def __init__(self):
        self.log=[]
        self.data = ''

    def LogAppend(self, dat, player):
        # 받은 데이터를 로그에 추가함
        self.data = player + '이(가) ' + dat + ' 데이터를 보냄'
        self.log.append(self.data)
        
    def LogSend(self, dat, player):
        # 서버에서 보낸 내용을 로그에 추가함
        self.data = 'Server send ' + dat + '을(를) ' + player + ' 에게 보냄'
        self.log.append(self.data)
        
    def PrintLog(self):
        # 로그 출력
        print(self.log)

    def LogReset(self):
        # 로그 초기화
        self.log = []

