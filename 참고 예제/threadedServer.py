#!/usr/bin/env python
# coding: utf-8

# In[1]:


from socket import *
import threading

ADDR=('',12000)
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(2)

def socketThread():
    connectionSocket,addr=serverSocket.accept()
    print(f'{addr} connected')
    while True:
        sentence=connectionSocket.recv(2048)
        print(sentence.decode())
        
c1=threading.Thread(target=socketThread())
c2=threading.Thread(target=socketThread1())
c1.daemon=True
c2.daemon=True
c1.start()
c2.start()


# In[ ]:




