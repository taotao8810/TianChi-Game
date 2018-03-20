# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 16:09:19 2018

@author: wentao.yao01
"""

"""
import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir('C:\\Users\\wentao.yao01\\Desktop\\tianchi_date')
"""
import numpy as np
import pandas as pd
#%matplotlib inline

#导入数据
train_online = pd.read_csv('ccf_online_stage1_train.csv')
train_offline = pd.read_csv('ccf_offline_stage1_train.csv')
test = pd.read_csv('ccf_offline_stage1_test_revised.csv')

