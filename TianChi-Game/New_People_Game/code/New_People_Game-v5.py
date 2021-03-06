# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:38:16 2018

@author: wentao.yao01
此版本是由2014.11.18-12.17 -->> 2014.12.18

xgboost
"""


import os
#获取当前工作目录
os.getcwd()
#修改当前目录
os.chdir(r'E:\softwear\GitHub\TianChi-Game\TianChi-Game\New_People_Game\data')


import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, make_scorer,f1_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#导入处理完的数据
data_handle_trina = pd.read_csv('data_handle_trina.csv')
data_handle_test = pd.read_csv('data_handle_test.csv')
data_handle_test_1 = data_handle_test.drop(['user_id','item_id','buy'],axis=1)

X_all=data_handle_trina.drop(['buy','user_id','item_id'],axis=1)
y_all=data_handle_trina['buy']

n=0.2
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=n, random_state=3)

'''
y_train.describe(include='all')
np.isnull(X_train)
np.isnan(X_train).any()
'''


#xgboost
import xgboost as xgb
xgb_val = xgb.DMatrix(X_test,label=y_test)
xgb_train = xgb.DMatrix(X_train, label=y_train)
xgb_test = xgb.DMatrix(data_handle_test_1)

#'eval_metric':'merror','lambda':3,
param = {'max_depth':5,
         'min_child_weight':1,
         'eta':0.02,
         'silent':0,
         'booster':'gbtree',
	      'objective': 'binary:logistic',
         'gamma':0,
         'subsample':0.85,
         'colsample_bytree':0.8,
         'colsample_bylevel':1,
         'scale_pos_weight':1,
         'seed':10}

num_round = 100
#watchlist = [(xgb_train, 'train'),(xgb_val, 'val')]
model = xgb.train(param, xgb_train, num_round)#, watchlist)

# 计算 auc 分数、预测
#test_predictions = model.predict(xgb_test)
data_handle_test['flag'] = model.predict(xgb_test)
result = data_handle_test[data_handle_test['flag']>0.5]
result = result[['user_id','item_id']]

from sklearn.preprocessing import MinMaxScaler
data_handle_test.flag = MinMaxScaler().fit_transform(data_handle_test.flag)
data_handle_test.sort_values(by=['buy','flag'],inplace=True)

result.to_csv("result-v5.csv",index=None)


#计算ROC曲线下面的面积，也被称为AUC或AUROC
from sklearn.metrics import roc_auc_score
roc_auc_score(data_handle_test['buy'], data_handle_test['flag'])

#画出ROC曲线图
from sklearn.metrics import roc_curve #导入ROC曲线函数
fpr, tpr, thresholds = roc_curve(data_handle_test['buy'], data_handle_test['flag'], pos_label=1)
plt.plot(fpr, tpr, linewidth=2, label = 'ROC of CART', color = 'green') #作出ROC曲线
plt.xlabel('False Positive Rate') #坐标轴标签
plt.ylabel('True Positive Rate') #坐标轴标签
plt.ylim(0,1.05) #边界范围
plt.xlim(0,1.05) #边界范围
plt.legend(loc=4) #图例
plt.show() #显示作图结果

#==============================================================================
# 
# #决策树分类器
# from sklearn.tree import DecisionTreeClassifier as DTC
# clf = DTC(class_weight="balanced",max_depth=8,max_features=2)
# clf= clf.fit(X_train,y_train)
# 
# #预测
# test_predictions=clf.predict(X_test)
# print("测试集准确率:  %s " % f1_score(y_test, test_predictions))
# 
# 
# #随机森林分类器
# from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
# clf=RandomForestClassifier(class_weight="balanced",max_depth=5,max_features=4)
# clf=clf.fit(X_train,y_train)
# #预测
# test_predictions=clf.predict(X_test)
# print("测试集准确率:  %s " % f1_score(y_test, test_predictions))
# 
# 
# clf=ExtraTreesClassifier()
# clf=clf.fit(X_train,y_train)
# test_predictions=clf.predict(X_test)
# print("测试集准确率:  %s " % f1_score(y_test, test_predictions))
# 
# 
# 
# #设置待选的参数
# from sklearn.tree import DecisionTreeClassifier as DTC
# from sklearn.grid_search import GridSearchCV
# from sklearn.model_selection import StratifiedKFold
# decision_tree_classifier = DTC()
# parameter_grid = {'max_depth':[1,2,3,4,5,6,7,8],'max_features':[1,2,3,4,5,6,7]}
# cross_validation = StratifiedKFold(n_splits = 20)
# 
# #将不同参数带入
# gridsearch = GridSearchCV(decision_tree_classifier,
#                           param_grid = parameter_grid,
#                           cv = 20)
# gridsearch.fit(X_train,y_train)
# 
# #得分最高的参数值，并构建最佳的决策树
# best_param = gridsearch.best_params_
# best_decision_tree_classifier = DTC(max_depth=best_param['max_depth'],max_features=best_param['max_features'])
# 
# 
# 
# 
# #预测最后的结果
# data_handle_test_1 = data_handle_test.drop(['user_id','item_id','buy'],axis=1)
# a = clf.predict(data_handle_test_1)
# 
# data_handle_test_1['flag']=a
# result = data_handle_test_1[data_handle_test_1['flag'] >0]
# 
# #导出结果数据
# result.to_csv(r'result-v2.csv',index=False)
# 
#==============================================================================





'''
#导出树模型图
with open("tree.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

import pydotplus
dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("tree.pdf")

c=clf.predict(testData.ix[:,2:6])

testData['label']=pd.DataFrame(c)
'''