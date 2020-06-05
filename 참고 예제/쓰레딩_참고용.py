#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import threading
import time

def testF():
    first=time.time()
    while z==0:
        if abs(first-time.time())>2:
            print('testing')
            first=time.time()
            
z=0
t=threading.Thread(target=testF)
t.daemon=True
t.start()

while True:
    a=input()
    if a=='.':
        break

z=1


# In[ ]:




