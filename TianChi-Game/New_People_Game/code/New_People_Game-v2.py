# -*- coding: utf-8 -*-
"""
Created on Fri Feb 02 10:38:16 2018

@author: wentao.yao01
此版本是由2014.11.18-12.17 -->> 2014.12.18
目前效果不理想
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
data_handle_trina = pd.read_csv('data_handle_trina.csv')
data_handle_test = pd.read_csv('data_handle_test.csv')

#查看0,1的数量
pd.value_counts(data_handle_trina['buy'])

X_all=data_handle_trina.drop(['buy','user_id','item_id'],axis=1)
y_all=data_handle_trina['buy']

n=0.2
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=n, random_state=3)

'''
y_train.describe(include='all')
np.isnull(X_train)
np.isnan(X_train).any()
'''

#决策树分类器 min_samples_split=100,min_samples_leaf=35,class_weight="balanced",
from sklearn.tree import DecisionTreeClassifier as DTC
clf = DTC(class_weight="balanced",max_depth=5,max_features=4)
clf= clf.fit(X_train,y_train)

#预测
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))


#随机森林分类器
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
clf=RandomForestClassifier(class_weight="balanced",max_depth=5,max_features=4)
clf=clf.fit(X_train,y_train)
#预测
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))


clf=ExtraTreesClassifier()
clf=clf.fit(X_train,y_train)
test_predictions=clf.predict(X_test)
print("测试集准确率:  %s " % f1_score(y_test, test_predictions))



#设置待选的参数        
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import StratifiedKFold
decision_tree_classifier = DTC()
parameter_grid = {'max_depth':[1,2,3,4,5],'max_features':[1,2,3,4]}
cross_validation = StratifiedKFold(n_splits = 10)

#将不同参数带入
gridsearch = GridSearchCV(decision_tree_classifier,
                          param_grid = parameter_grid,
                          cv = 10)
gridsearch.fit(X_train,y_train)

#得分最高的参数值，并构建最佳的决策树
best_param = gridsearch.best_params_
best_decision_tree_classifier = DTC(max_depth=best_param['max_depth'],max_features=best_param['max_features'])




#模型评估
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

        

#预测最后的结果
data_handle_test_1 = data_handle_test.drop(['user_id','item_id','buy'],axis=1)
a = clf.predict(data_handle_test_1)

data_handle_test['flag']=a
result = data_handle_test[data_handle_test['flag'] >0]
result = result[['user_id','item_id']]
#导出结果数据
result.to_csv(r'result-v3.csv',index=False)






'''
#导出树模型图
#第一种办法
from sklearn import tree
with open("tree.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)

#第二种办法
import pydotplus
from sklearn import tree
dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("tree.pdf")


#第三种办法，无实测
from IPython.display import Image
dot_data = tree.export_graphviz(clf, out_file=None,
                         feature_names=iris.feature_names,
                         class_names=iris.target_names,
                         filled=True, rounded=True,
                         special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())



#无用
c=clf.predict(testData.ix[:,2:6])
testData['label']=pd.DataFrame(c)
'''



