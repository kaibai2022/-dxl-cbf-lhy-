#!/usr/bin/env python
# coding: utf-8

# In[13]:
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import pandas as pd
from IPython import get_ipython

data_all=pd.read_csv(r"C:\Users\11430\Desktop\UserBehavior.csv",header=None)
data_all.columns=['user_id','item','category','type','timestamp']
data_all=data_all[data_all['type']=='buy']
del data_all['item']
del data_all['type']
del data_all['timestamp']


# In[14]:


data_all.drop_duplicates(inplace=True)
data_all.to_csv(r'E:\data_all.csv',index=False, header= False)


# In[15]:


data_all=pd.read_csv(r'E:\data_all.csv',header=None)
data_all.columns=['user_id','category']
data_all.head()


# In[16]:


len(data_all.category.unique())
data_buy=data_all.groupby('category').count()['user_id']
data_buy=data_buy.sort_values(ascending=False)
data_buy=pd.DataFrame(data_buy)
data_buy.columns=['count']
data_buy.reset_index(inplace=True)
data1=data_buy.head(26)
del data1['count']


# In[17]:


a=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
data1['item']=a
data1.head()


# In[18]:


data=data_all.merge(data1,on='category',how='inner')
data.head()


# In[19]:


data_user=data.groupby('user_id').count()['item']
data_user=data_user.sort_values(ascending=False)
data_user=pd.DataFrame(data_user)
data_user.columns=['count']
data_user.reset_index(inplace=True)
data2=data_user[data_user['count']>=5]
data2.head()


# In[20]:


data_new=data.merge(data2,on='user_id',how='inner')
del data_new['count']
del data_new['category']
data_new.head()


# In[21]:


i=0
rating=[]
while i<=20015:
    y=random.randint(1,5)#1-5之间抽样随机数
    rating.append(y)
    i=i+1
data_new.insert(1,'rating',rating)
data_new.head()


# In[22]:


data_new.to_csv(r'E:\data_new.csv',index=False, header= False)


# In[23]:


import pandas as pd
pd.options.display.width =200  # pd 输出宽度，默认为80
pd.set_option('precision', 4)  # 控制台打印时显示的3位小数

get_ipython().run_line_magic('matplotlib', 'inline')

train = dict()  # 用户-物品的评分矩阵
for line in open(r'E:\data_new.csv'):
    user, score, item = line.strip().split(",")
    train.setdefault(user, {})
    train[user][item] = int(float(score))
for k,v in train.items() :
    print("Key: " + k)
    print("Value: " + str(v)+'\n')


# In[24]:


# 建立物品-物品的共现矩阵
C = dict()  # 物品-物品的共现矩阵
N = dict()  # 物品被多少个不同用户购买
for user, items in train.items():
    for i in items.keys():
        N.setdefault(i, 0)
        N[i] += 1
        C.setdefault(i, {})
        for j in items.keys():
            if i == j: continue
            C[i].setdefault(j, 0)
            C[i][j] += 1
            # 计算相似度矩阵
for k,v in N.items() :
    print("Key: " + k)
    print("Value: " + str(v)+'\n')


# In[25]:


for k,v in C.items() :
    print("Key: " + k)
    print("Value: " + str(v)+'\n')


# In[26]:


W = dict()
for i, related_items in C.items():
    W.setdefault(i, {})
    for j, cij in related_items.items():
        W[i][j] = cij / (math.sqrt(N[i] * N[j]))
for k,v in W.items() :
    print("Key: " + k)
    print("Value: " + str(v)+'\n')


# In[27]:


rank = dict()
action_item = train['875260']  # 用户user产生过行为的item和评分
for item, score in action_item.items():
    for j, wj in sorted(W[item].items(), key=lambda x: x[1], reverse=True)[0:3]:
        if j in action_item.keys():
            continue
        rank.setdefault(j, 0)
        rank[j] += score * wj
        
final = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:10])

print('用户购买过的产品和评分 ：' + str(action_item) +'\n')
print('最后推荐给用户的产品及评分 ：'+ str(final))


# In[ ]:




