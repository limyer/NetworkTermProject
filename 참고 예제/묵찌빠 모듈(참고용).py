#!/usr/bin/env python
# coding: utf-8

# In[3]:


def RSP0(a,b):
    if a==b:
        return 2
    elif (a=='묵' and b=='찌') or (a=='찌' and b=='빠') or (a=='빠' and b=='묵'):
        return 0
    elif (b=='묵' and a=='찌') or (b=='찌' and a=='빠') or (b=='빠' and a=='묵'):
        return 1
    else:
        return 3


# In[ ]:




