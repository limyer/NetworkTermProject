import threading as th
import os


def start_timer(count):
    count+=1
    timer=th.Timer(1,start_timer, args=[count])
    timer.start()
    
    if count==5:
        timer.cancel()
        return True


