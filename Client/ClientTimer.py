import threading as th
import os

class ClientTimer:
    def start_timer(self, count):
        count+=1
        print(count)
        timer=th.Timer(1,start_timer, args=[count])
        timer.start()
        
        if count==5:
            print('Stop')
            timer.cancel()
            return False
        
        os.system('cls')
        return True
