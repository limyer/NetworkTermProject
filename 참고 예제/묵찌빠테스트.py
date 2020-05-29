RSP_cardboard = ['묵','찌','빠'] # 묵, 찌, 빠를 저장해 놓은 리스트 이것으로 묵, 찌, 빠를 판별하고 각각 0, 1, 2로 치환시켜준다
RSP_resultboard = [['draw','win','lose'],['lose','draw','win'],['win','lose','draw']] # 치환된 묵, 찌, 빠를 인덱스로 삼어 가위바위보의 결과를 돌려준다 player_a가 먼저 player_b가 나중에 인덱스로서 주어진다
player_list = [] # 플레이어가 누구인지 저장해 놓는다
log=[] # 묵찌빠 게임의 과정을 저장해 놓는다
win_table=[] # 어떤 플레이어가 승리했는지 저장해 놓는다 이를 이용하여 게임의 승패를 결정한다

def insert_player(player):
    # 플레이어를 등록한다

    # 플레이어가 이미 2명이 모여있을 때 추가적으로 플레이어를 받으려고 하면 거절한다
    if len(player_list) >= 2:
        #client_socket.send(b"Sorry, It's full")
        print("No more memory")
        return -1

    # 플레이어를 플레이어 목록에 append한다
    else:
        player_list.append(player)
        return 0
    

def check_winner(player_a_card,player_b_card):
    # 플레이어들이 낸 카드를 토대로 가위바위보의 승패를 결정한다

    #비겼을 경우 로그에 무승부를 기록
    if RSP_resultboard[player_a_card][player_b_card] == 'draw':
        log.append('draw')

    #비겼을 경우 로그에 player_a가 이겼다는 것을 기록    
    elif RSP_resultboard[player_a_card][player_b_card] == 'win':
        log.append(player_list[0] + ' win')
        
    #비겼을 경우 로그에 player_b가 이겼다는 것을 기록     
    else:
        log.append(player_list[1] + ' win')

    # 가위바위보의 결과를 돌려준다
    return RSP_resultboard[player_a_card][player_b_card] #player_a의 기준

def check_card(player_card):
    # 플레이어가 입력한 카드가 묵, 찌, 빠인지 아닌지를 검사

    # 플레이어가 입력한 카드가 묵, 찌, 빠인 경우
    if player_card in RSP_cardboard:

        # 묵인 경우 0을 돌려준다
        if player_card == RSP_cardboard[0]:
            return 0

        # 찌인 경우 1을 돌려준다
        elif player_card == RSP_cardboard[1]:
            return 1

        # 빠인 경우 2을 돌려준다
        else:
            return 2

    # 플레이어가 입력한 카드가 묵, 찌, 빠가 아닌 경우 -1을 돌려준다  
    else:
        return -1

def main():
    check_card_res = [0,0] # 플레이어의 카드를 확인한다 인덱스 0은 player_a 인덱스 1은 player_b를 나타낸다
    step = 0 # 묵찌빠의 단계를 나타낸다 선후공 = 0 승패결정 = 1
    attacker = ''# 공격자를 표시한다
    round = 1 # 라운드의 기본 값은 1로 총 3번의 라운드가 있다
    count = 0 # 라운드를 출력한 횟수를 표시한다 0 = 라운드를 표시하지 않았으므로 라운드를 출력한다 1 = 라운드가 이미 출력되었으므로 다시 출력하지 않는다

    # 플레이어의 수는 2명이므로 2번 반복 - 서버/클라이언트 간의 통신이 아니므로 반복문을 사용하여 플레이어를 등록
    for i in range(2):
        player = input("Enter your name: ")
        check = insert_player(player)
    if check == -1:
        return 0
        
    while True:
        # 라운드 표시
        if round == 1 and count == 0:
            print('round 1')
            count = 1
            
        elif round == 2 and count == 0:
            print('round 2')
            count = 1
            
        elif round == 3 and count == 0:
            print('round 3')
            count = 1
            
        else:
            pass
        
        # 카드를 받는다
        player_a_card = input("Enter your card in 묵 찌 빠: ")
        player_b_card = input("Enter your card in 묵 찌 빠: ")
        player_a_card = check_card(player_a_card)
        player_b_card = check_card(player_b_card)

        # 옳지 않은 카드를 냈을 경우 스텝 상관없이 기권패 처리
        if player_a_card not in [0,1,2]:
            check_card_res[0] = -1
            print(player_list[0]+' lose')
            break
        
        if player_b_card not in [0,1,2]:
            check_card_res[1] = -1
            print(player_list[1] + ' lose')
            break
        
        RSP_res = check_winner(player_a_card,player_b_card)
        
        # step 0 선후공 결정
        if step == 0:
            if RSP_res == 'win':
                print(player_list[0] + ' your are now attacker')
                attacker = player_list[0]
                step += 1
                
            elif RSP_res == 'lose':
                print(player_list[1] + ' your are now attacker')
                attacker = player_list[1]
                step += 1
                
            else:
                print('draw try angain')

        # step 1 라운드의 승패 결정        
        elif step == 1:
            # player_b가 이기고 있다가 player_a가 이긴 경우 공격권을 player_a가 가지게 된다
            if attacker == player_list[1] and RSP_res == 'win':
                print('attacker change ' + player_list[0] + ' is attacker now')
                attacker = player_list[0]
                
            # player_a가 이기고 있다가 player_b가 이긴 경우 공격권을 player_b가 가지게 된다
            elif attacker == player_list[0] and RSP_res == 'lose':
                print('attacker change ' + player_list[1] + ' is attacker now')
                attacker = player_list[1]

            # player들이 낸 카드가 같은 경우 공격자(attacker)의 승리로 win_table에 공격자(attacker)를 append한다
            elif player_a_card ==  player_b_card:
                print(attacker + ' is win')
                win_table.append(attacker)
                round += 1
                count = 0

                # 라운드가 3번 진행 되었을 경우 최종 승패를 확인한다
                if len(win_table) == 3:
                    a = 0
                    b = 0
                    for i in win_table:
                        if i == player_list[0]:
                            a += 1
                        else:
                            b += 1

                    # player_a가 승리한 횟수가 더 많을 경우 player_a를 최종 승리자로 한다.        
                    if a > b:
                        print('Finall winner is ' + player_list[0] + ' congratulation')
                        print(player_list)
                        print(log)
                        print(win_table)
                        break

                    # player_b가 승리한 횟수가 더 많을 경우 player_b를 최종 승리자로 한다.   
                    else:
                        print('Finall winner is ' + player_list[1] + ' congratulation')
                        print(player_list)
                        print(log)
                        print(win_table)
                        break

                # 라운드가 3번 진행 되지 않았을 경우 step을 0 으로 초기화 함으로써 라운드를 반복한다
                step -= 1

            # 공격권이 바뀌는 경우, 게임이 끝난 경우를 제외한 모든 경우 그냥 넘긴다
            else:
                pass

        # 플레이어의 이름, 로그, 라운드별 승리자를 기록해두는 리스트를 출력함 - 로그 확인용
        '''print(player_list)
        print(log)
        print(win_table)'''

    # 원래는 게임을 계속할 것인지를 물어 봐야하나 그것은 구현해 놓지 않았음

if __name__ == '__main__':
    main()
