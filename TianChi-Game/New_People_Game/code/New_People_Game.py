# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:38:16 2018

@author: wentao.yao01
"""

"""
import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir(r'E:\softwear\GitHub\TianChi-Game\TianChi-Game\New_People_Game\data')
"""

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, make_scorer,f1_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#导入处理完的数据
user_item = pd.read_csv('user_item.csv')
train_date = pd.read_csv('train_datatable.csv')
train_date = train_date.drop(['user_id','item_id'],axis=1)
train_date = train_date[train_date['DAY18_buy'] < 2]

X_all=train_date.drop(['DAY18_buy'],axis=1)
y_all=train_date['DAY18_buy']

n=0.2
#trainingData, testData=train_date[:int(round(0.8*len(train_date)))],train_date[int(round(0.8*len(train_date))):]
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=n, random_state=3)

#x_train= trainingData.drop(['DAY18_buy','user_id','item_id'],axis=1)
#y_train= trainingData['DAY18_buy']

#x_test= testData.drop(['DAY18_buy','user_id','item_id'],axis=1)
#y_test= testData['DAY18_buy']

#决策树分类器
from sklearn.tree import DecisionTreeClassifier as DTC
clf = DTC(class_weight="balanced",max_depth=5,max_features=4)
clf= clf.fit(X_train,y_train)

#预测
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))


#随机森林分类器
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
clf=RandomForestClassifier()
clf=clf.fit(X_train,y_train)
#预测
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))


clf=ExtraTreesClassifier()
clf=clf.fit(X_train,y_train)
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))




#预测最后的结果
train_date_predict = pd.read_csv('day1718_19_predict_data.csv')
train_date_predict_1 = train_date_predict.drop(['user_id','item_id'],axis=1)
a = clf.predict(train_date_predict_1)

train_date_predict['flag']=a
result = train_date_predict[train_date_predict['flag'] >0]

#导出结果数据
result.to_csv(r'result-v2.csv',index=False)


#计算ROC曲线下面的面积，也被称为AUC或AUROC
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, test_predictions)

#画出ROC曲线图
from sklearn.metrics import roc_curve #导入ROC曲线函数
fpr, tpr, thresholds = roc_curve(y_test, test_predictions, pos_label=1)
plt.plot(fpr, tpr, linewidth=2, label = 'ROC of CART', color = 'green') #作出ROC曲线
plt.xlabel('False Positive Rate') #坐标轴标签
plt.ylabel('True Positive Rate') #坐标轴标签
plt.ylim(0,1.05) #边界范围
plt.xlim(0,1.05) #边界范围
plt.legend(loc=4) #图例
plt.show() #显示作图结果




#导出树模型图
with open("tree.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

import pydotplus
dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("tree.pdf")

c=clf.predict(testData.ix[:,2:6])

testData['label']=pd.DataFrame(c)