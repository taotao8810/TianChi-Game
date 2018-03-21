# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:16:19 2018

@author: wentao.yao01
"""

'''
import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir(r'E:\softwear\GitHub\TianChi-Game\TianChi-Game\New_People_Game\data')
'''
import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir(r'D:\GitHub\TianChi-Game\New_People_Game\data')

import pandas as pd
import numpy as np

"""
#用户在商品全集上的移动端行为数据
train_item = pd.read_csv('tianchi_fresh_comp_train_item.csv')
#商品子集   
train_user = pd.read_csv('tianchi_fresh_comp_train_user.csv')

#根据P过滤掉D中的数据
user_item=pd.merge(train_user,train_item,on=['item_id'])
#导出文件，但是不包括索引
user_item.to_csv(r'user_item-v2.csv',index=False)
"""

file='user_item.csv'
user_item = pd.read_csv(file)

user_item= user_item.drop(['user_geohash','item_geohash'],axis=1)

#查看数据的情况
user_item.describe(include='all')

#处理空值



def f(x):
    return x.split(' ',1)[0]

user_item['time_1']=user_item['time'].apply(lambda x : f(x))

#打标签
def f1(y):
    if y == 1:
        return 1
    else:
        return 0
def f2(y):
    if y == 2:
        return 1
    else:
        return 0
def f3(y):
    if y == 3:
        return 1
    else:
        return 0
def f4(y):
    if y == 4:
        return 1
    else:
        return 0

user_item['liulan']= user_item['behavior_type'].apply(lambda y : f1(y))
user_item['shoucang']= user_item['behavior_type'].apply(lambda y : f2(y))
user_item['jiagou']= user_item['behavior_type'].apply(lambda y : f3(y))
user_item['buy']= user_item['behavior_type'].apply(lambda y : f4(y))


#切割训练集
#2014.11.18-12.17 -->> 2014.12.18
user_item_T_1 = user_item[user_item['time_1']<'2014-12-18']
user_item_T_2 = user_item[user_item['time_1']=='2014-12-18']

#2014.11.19-12.18 -->> 2014.12.19
test = user_item[user_item['time_1']<'2014-12-18']
test = user_item[user_item['time_1']>'2014-11-18']


#对数据做处理，根据user_id，item_id进行聚合，把liulan，shoucang，jiagou，求和。并删除其他不用的参数
user_item_1 = user_item_T_1.groupby([user_item_T_1['user_id'],user_item_T_1['item_id']]).sum().reset_index()
user_item_1 = user_item_1.drop(['item_category','behavior_type','buy'],axis=1)
user_item_2 = user_item_T_1['buy'].groupby([user_item_T_1['user_id'],user_item_T_1['item_id']]).max().reset_index()

#把user_item_1，user_item_2进行合并
user_item_3 = user_item_1.merge(user_item_2,on=['user_id','item_id'],how='inner')
#按浏览，收藏，加购物车， 按1,3,6比例来分
user_item_3['qiuhe'] = user_item_3['liulan']*1 + user_item_3['shoucang']*3 + user_item_3['jiagou']*6

           
#user_item_T_2处理
user_item_4 = user_item_T_2.groupby([user_item_T_2['user_id'],user_item_T_2['item_id']]).sum().reset_index()
user_item_4 = user_item_4.drop(['item_category','behavior_type','buy'],axis=1)
user_item_5 = user_item_T_2['buy'].groupby([user_item_T_2['user_id'],user_item_T_2['item_id']]).max().reset_index()

user_item_6 = user_item_4.merge(user_item_5,on=['user_id','item_id'],how='inner')
user_item_6['qiuhe'] = user_item_6['liulan']*1 + user_item_6['shoucang']*3 + user_item_6['jiagou']*6

#1.浏览占 浏览，收藏，加购物车 的占比  2.收藏占 浏览，收藏，加购物车 的占比  3.加购物车占 浏览，收藏，加购物车 的占比
user_item_3['ll_pre']=user_item_3['liulan']/(user_item_3['liulan']+user_item_3['shoucang']+user_item_3['jiagou'])
user_item_3['sc_pre']=user_item_3['shoucang']/(user_item_3['liulan']+user_item_3['shoucang']+user_item_3['jiagou'])
user_item_3['jg_pre']=user_item_3['jiagou']/(user_item_3['liulan']+user_item_3['shoucang']+user_item_3['jiagou'])


user_item_6['ll_pre']=user_item_6['liulan']/(user_item_6['liulan']+user_item_6['shoucang']+user_item_6['jiagou'])
user_item_6['sc_pre']=user_item_6['shoucang']/(user_item_6['liulan']+user_item_6['shoucang']+user_item_6['jiagou'])
user_item_6['jg_pre']=user_item_6['jiagou']/(user_item_6['liulan']+user_item_6['shoucang']+user_item_6['jiagou'])

#查看是否有NAN值,并删除NAN值
np.isnan(user_item_3).any()
np.isnan(user_item_6).any()

user_item_3 = user_item_3.dropna()
user_item_6 = user_item_6.dropna()
#导出结果数据
user_item_3.to_csv(r'data_handle_trina.csv',index=False)
user_item_6.to_csv(r'data_handle_test.csv',index=False)


