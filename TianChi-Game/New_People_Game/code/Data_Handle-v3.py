# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:16:19 2018

@author: wentao.yao01
"""
import pandas as pd
import numpy as np
import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir(r'E:\softwear\GitHub\TianChi-Game\TianChi-Game\New_People_Game\data')

#由于双12数据异常，故删掉
#删选出item_table中包含的商品类，并把时间切割成 day 与 hour
if __name__ == '__main__':
	user_table = pd.read_csv('tianchi_fresh_comp_train_user.csv')
	item_table = pd.read_csv('tianchi_fresh_comp_train_item.csv')
	user_table = user_table[user_table.item_id.isin(list(item_table.item_id))]
	user_table['days'] = user_table['time'].apply(lambda x:x.split(' ')[0])
	user_table['hours'] = user_table['time'].apply(lambda x:x.split(' ')[1])
	user_table = user_table[user_table['days'] != '2014-12-12']
	user_table = user_table[user_table['days'] != '2014-12-11']
	user_table.to_csv('drop1112_sub_item.csv',index=None)


