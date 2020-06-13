# 컴네서버.py에서 받은 addr, addr0, addr1을 받는다.

# 만일 로그.txt를 어떤 디렉토리에 생성하고 싶다면 C:/Python/로그.txt 를 로그.txt 대신에 넣어주면 된다.

# 로그.txt를 완전히 디렉토리까지 지우는 것은 넣지 않음 우리는 데이터가 어떻게 돌아가는지 확인해야하므로
# 로그.txt 자체를 지우는 것은 옳지 않다고 생각함 만일 로그.txt 자체를 지우고 싶다면
# from os import unlink를 사용한다.
class Log():
    def __init__(self):
        self.log = '' # 로그가 열리고 닫히는 변수
        self.data = '' # 로그에 넣을 데이터가 저장되는 장소
        self.L_R = '' # 로그를 읽는데 쓰는 변수

    def CreateLog(self):
        # 로그 생성
        self.log = open('로그.txt', 'w')
        self.log.close()
    
    def LogAppend(self, dat, player):
        # 받은 데이터를 로그에 추가함
        self.log = open('로그.txt', 'a')
        self.data = player + '이(가) 데이터 ' + dat + '를 보냄\n'
        self.log.write(self.data)
        self.log.close()
        
    def LogSend(self, dat, player):
        # 서버에서 보낸 내용을 로그에 추가함
        self.log = open('로그.txt', 'a')
        self.data = 'Server send ' + dat + '을(를) ' + player + ' 에게 보냄\n'
        self.log.write(self.data)
        self.log.close()
        
    def PrintLog(self):
        # 로그 출력
        print('print log')
        self.log = open('로그.txt', 'r')
        self.L_R = self.log.read()
        print(self.L_R)
        print()
        self.log.close()

    def LogReset(self):
        # 로그 초기화
        self.log = open('로그.txt', 'w+t')
        self.log.close()

    '''def DelLog(self):
        # 로그 파일 자체를 지우고 싶을 때 사용
        unlink('로그.txt')'''

'''# 로그 클래스 선언
l=Log()

# 로그 생성
l.CreateLog()

# 예제 짝수일 때 A 홀수일 때 B가 플레이어이고 데이터는 홀 짝으로 나뉨
for i in range(10):
    if i % 2 == 0:
        player = 'A'
    else:
        player = 'B'
    data = '%d' % i
    
    # 로그에 추가한다.
    l.LogAppend(data,player)

    # 서버에서 보낸 데이터를 로그에 추가한다
    l.LogSend('ok', player)

    # 데이터 확인용
    print(data, player)

# 로그 출력
l.PrintLog()

# 로그 리셋
l.LogReset()

# 로그 출력 로그가 리셋되었는지 확인
l.PrintLog()
'''
