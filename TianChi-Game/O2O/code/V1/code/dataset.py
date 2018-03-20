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

#将数据合并，以便统一对数据进行处理。都是线下数据
all_offline = pd.concat([train_offline,test])

#查看每一列的异常值
f = lambda x:sum(x.isnull())
all_offline.apply(f)

#Data的空值 赋值为null，统一空值的格式
all_offline['Date'] = all_offline['Date'].fillna('null')

#将online与offline的数据合并
pd.merge(all_offline,train_online,on=['Merchant_id','User_id'])

#通过合并数据，发现两者并无交集，题目要求只用线下预测，故排除线上online数据，
#只用offline数据

#根据赛题的要求，把正负样本标注出来
def is_used(column):
    if column['Date']!='null' and column['Coupon_id']!='null':
        return 1
    elif column['Date']=='null' and column['Coupon_id']!='null':
        return -1
    else:
        return 0

all_offline['is_used'] = all_offline.apply(is_used,axis=1)
    
#Coupon_id 优惠券ID的具体数值意义不大，因此我们把他转换成：是否有优惠券
def has_coup(x):
    if x['Coupon_id'] != 'null':
        return 1
    else:
        return 0
    
all_offline['has_coup']=all_offline.apply(has_coup,axis=1)

#由于Discount_rate优惠率的特殊格式:"150:20",很难使用算法来计算使用
#根据实际情况，优惠力度是能够影响优惠券的使用频率的。因此需要对Discount_rate进行转化
#根据Discount_rate标识出折扣率
import re
regex=re.compile('^\d+:\d+$')

def discount_percent(y):
    if y['Discount_rate'] == 'null' and y['Date_received'] == 'null':
        return 'null'
    elif re.match(regex,y['Discount_rate']):
        num_min,num_max=y['Discount_rate'].split(':')
        return float(num_max)/float(num_min)
    else:
        return y['Discount_rate']

all_offline['discount_percent'] = all_offline.apply(discount_percent,axis=1)

#在进一步想，优惠力度会影响优惠券使用的概率，x:y这种满减的类型，x具体是多少，势必也会影响优惠券使用率
#讲满x元的标出x元
def discount_limit(y):
    if y['Discount_rate'] == 'null' and y['Date_received'] == 'null':
        return 'null'
    elif re.match(regex,y['Discount_rate']):
        num_min,num_max=y['Discount_rate'].split(':')
        return num_min
    else:
        return 0

all_offline['discount_limit'] = all_offline.apply(discount_limit,axis=1)
all_offline.head(10)

#由于赛题需要的是，优惠券领取后15天的使用概率
#因此，我们在is_used的基础上，在对领券时间 Date_received 和使用时间Date，进行比较，判断是否在15天内使用
#时间比较
import datetime
#标注15天内使用优惠券的情况
def used_in_15days(z):
    if z['is_used'] == 1 and z['Date'] != 'null' and z['Date_received'] != 'null':
        days= (datetime.datetime.strptime(z['Date'],"%Y%m%d")-datetime.datetime.strptime(z['Date_received'],"%Y%m%d"))
        if days.days < 15:
            return 1
        else:
            return 0
    else:
        return 0
        
all_offline['used_in_15days']=all_offline.apply(used_in_15days,axis=1)

    
#再来观察discount_percent，discount_limit这2个特征，看数据的分布情况。
all_offline['discount_percent'].value_counts()
all_offline['discount_limit'].value_counts()

#将discount_percent分段
def discount_percent_layer(columns):
    if columns['discount_percent']=='null':
        return 'null'
    
    columns['discount_percent']=float(columns['discount_percent'])
    if columns['discount_percent'] <= 0.1:
        return 0.1
    elif columns['discount_percent'] <= 0.2:
        return 0.2
    elif columns['discount_percent'] <= 0.3:
        return 0.3
    elif columns['discount_percent'] <= 0.4:
        return 0.4
    else:
        return 0.5

all_offline['discount_percent_layer']=all_offline.apply(discount_percent_layer,axis=1)
#all_offline['discount_percent_layer']=all_offline.apply(discount_percent_layer)
all_offline['discount_percent_layer'].value_counts()

#将discount_limit分段
def discount_limit_layer(columns):
    if columns =='null':
        return 'null'
    
    columns=int(columns)
    if columns <= 10:
        return 10
    elif columns <= 20:
        return 20
    elif columns <= 30:
        return 30
    elif columns <= 50:
        return 50
    elif columns <= 100:
        return 100
    elif columns <= 200:
        return 200
    else:
        return 300

all_offline['discount_limit_layer']=all_offline['discount_limit'].apply(discount_limit_layer)
all_offline['discount_limit_layer'].value_counts()

#总结
#此时 Coupon_id 被处理成 has_coup（1代表领取优惠券，0代表没有领取优惠券）
#Date,Date_received 被处理成 used_in_15days。表示是否在15天内使用过优惠券
#Discount_rate 被处理成 discount_percent（折扣率），discount_limit（满多少）
#Merchant_id，User_id 是unicode值,不需要进行处理

#剩下Distance，看下Distance的分布情况
all_offline['Distance'].value_counts()

#看分布，无需进行过多处理，最后直接one-hot处理
#保存数据，以便后期使用起来方便
train_finall,test_finall = all_offline[:train_offline.shape[0]],all_offline[train_offline.shape[0]:]
all_offline.to_csv(r'output\all_offline.csv')
train_finall.to_csv(r'output\train_finall.csv')
test_finall.to_csv(r'output\test_finall.csv')






all_offline=pd.read_csv(r'output\all_offline.csv')

#one_hot处理
all_offline_new=all_offline.drop(
        ['Coupon_id','Date','Date_received','Discount_rate','Merchant_id',
         'User_id','discount_percent','discount_limit'],axis=1)
all_offline_new=pd.get_dummies(all_offline_new)



    
#把测试集跟验证集分开
train01,test01=all_offline_new[:len(train_offline)],all_offline_new[len(train_offline):]

#把没有领券的去掉
train02=train01[train01['has_coup']==1]

#由于特征集 都是领券的人，故把 has_coup 字段删掉
train02=train02.drop(['has_coup'],axis=1)
test01=test01.drop(['has_coup'],axis=1)

x_train=train02.drop(['used_in_15days'],axis=1)
y_train=pd.DataFrame({"used_in_15days":train02['used_in_15days']})
x_text=test01.drop(['used_in_15days'],axis=1)

#建模
from sklearn.linear_model import LinearRegression

clf=LinearRegression()
clf.fit(x_train,y_train)

#用模型进行预测
predict=clf.predict(x_text)


result=pd.read_csv('ccf_offline_stage1_test_revised.csv')
result['probability']=predict

result=result.drop(['Merchant_id','Discount_rate','Distance'],axis=1)


#发现最终预测有负值，直接归为0
result['probability']=result['probability'].apply(lambda x: 0 if x<0 else x)

result.to_csv(r'output/sample_submission.csv',index=False)


