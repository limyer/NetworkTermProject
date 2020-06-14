##일단 코드 쓰기 전에 통신 코드 개요부터 먼저 올립니다.(남서아)
# 수정본
# 알고리즘과 해당 알고리즘에서 사용될 코드의 목록입니다.
# 여기에 맞는 프로그램으로 짜야 합니다.


# 이름 먼저 받기 (Stage 0)
#   서버] 이름 입력하라고 보낸다 <- 이 부분 필요 없음 (삭제)
#1. 서버] 이름 입력 대기 상태

#2. 클라] 이름 입력해서 전송 (Code: "Username: " + username)

#3. 서버] 전송받은 이름 "토큰"으로 뽑아내어서 각각 저장 (예: "Username:" 이부분만 빼고 저장)

#4  서버] 이름 전송 받고 클라이언트가 두 개 접속인지 확인, 두 개 접속했을 경우 두 클라이언트에 게임 시작 코드 전송 (Code: "Stage 0 to 1")
#4-1. 서버] 두 개 이상 접속일 경우 연결 해제 코드 전송 (Code: "Break") 
#4-2. 클라] Break 코드 시 연결 해제

#5  서버, 클라] 3초 대기 후 다음 스테이지로 이동



# 가위바위보 (Stage 1)
#1. 서버] 이용자(스레드) 1, 2에 가위바위보 입력하라고 보낸다. (Code: "Receiving Stage 1")

#2. 클라] 10초 이내에 가위바위보 값 입력 (Code: "Stage 1 Input: " + "ROCK" or "SCISSORS" or "PAPER")
#2-1.클라] 10초 이내로 결정하지 못할 시 코드 전송 (Code: "Stage 1 Input: " + "Undecided")
#2-2 서버] 스레드에서 10초 이내로 전송을 하지 않을 경우, 혹은 Undecided 코드가 왔을 경우 스테이지 재시작 코드 전송 (Code: "Restart")
#2-3 서버, 클라] Restart 코드가 왔을 경우 (보냈을 경우) 재시작을 알리고 #2로 돌아감

#3. 서버] 입력받은 두 가위바위보 값 서버 내에서 비교한 후 각자의 스레드 1, 2에 이겼다/아니다/무승부 코드 전송해준다. (Code: "Stage 1: " + "Win" or "Lose" or "Draw")
#3-1. 서버, 클라] Draw 코드가 왔을 경우 (보냈을 경우) 재시작을 알리고 #2로 돌아감

#4. 서버] 승리자가 있다면 다음 스테이지 이동 코드 전송 (Code: "Stage 1 to 2")

#5 서버, 클라] 3초 대기 후 다음 스테이지로 이동



# 묵찌빠 (Stage 2)
#1. 서버] 가위바위보 이긴사람의 번호를 서버에 저장

#2. 서버] 현재 누구 턴인지 각 스레드에서 전송 (Code: "Your Turn" or "Not Your Turn")
#2-1 클라] 서버의 메시지에 따라 클라이언트에 표시

#3. 서버] 이용자에 묵찌빠 값 입력하라고 보낸다. (Code: "Receiving Stage 2")

#4. 클라] 10초 이내에 묵찌빠 값 입력 (Code: "Stage 2 Input: " + "ROCK" or "SCISSORS" or "PAPER")
#4-1.클라] 10초 이내로 결정하지 못할 시 코드 전송 (Code: "Stage 2 Input: " + "Undecided")
#4-2 서버] 스레드에서 10초 이내로 전송을 하지 않을 경우, 혹은 Undecided 코드가 왔을 경우 스테이지 재시작 코드 전송 (Code: "Restart")
#4-3 서버, 클라] Restart 코드가 왔을 경우 (보냈을 경우) 재시작을 알리고 #2로 돌아감

#5. 서버] 입력받은 묵찌빠 값 비교하고 같은 입력이 아니라면 현재 턴이 누구인지 판단하여 저장하고 각 스레드에서 전송 (Code: "Your Turn" or "Not Your Turn")
#5-1. 서버, 클라] #2-1부터 반복

#6. 서버] 만일 같은 입력이 등장했다면 턴을 가진 사람의 점수를 +1, 승리 코드 전송 (Code: "Stage 2: " + "Win" or "Lose")
#6-1 서버] 턴을 가진 사람의 점수를 +1 했는데 3점이 넘을 경우 루프 탈출, #6의 승리 코드 대신 최종 승리코드 전송 (Code: "Final: " + "Win" or "Lose")
#6-2 클라] 서버의 메시지에 따라 클라이언트에 표시
#6-2 클라] 소켓을 닫고 스테이지 0으로 이동
#6-3 서버] 스테이지 0으로 이동

#7. 서버] 3점이 넘지 않았을 경우 현재 스코어 전송 (Code: "{username1} Score: {Score1} " + "{username2} Score: {Score2}")
#7-1 클라] 서버의 메시지에 따라 클라이언트에 표시
#7-2 서버] 스테이지 돌아가는 코드 전송하고 스테이지 1으로 이동 (Code: "Stage 2 to 1")
#7-3 클라] 스테이지 1로 이동



