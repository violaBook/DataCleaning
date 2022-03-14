# 以下是回归的模型训练过程，通过此过程生成模型并保存为pkl文件
""" 
    python test.py X_Force './c1/c_1_011.csv'
"""

from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
from sys import argv
import pandas as pd
from re import match
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import matplotlib.pyplot as plt
import numpy as np


class Regression_Model_Train():
    def __init__(self):
        # init-argv
        self.col = argv[1]
        self.pickle_read_path = argv[2]
        # 参数
        self.n_estimators = 100
        # read-pickle
        self.pickle_data = pd.read_csv(self.pickle_read_path, header=None, names=['X_Force','Y_Force','Z_Force','X_Vibration','Y_Vibration','Z_Vibration','AE_RMS'])
        self.columns = self.pickle_data.columns.tolist()
        print(self.pickle_data)
        # self.columns为数值类型且不存在空的列名
        # type_list = self.pickle_data.dtypes.astype(str).tolist()
        # type_del = ['datetime', 'object']
        # del_list = []
        # for i, type_ in enumerate(type_list):
        #     for type_d in type_del:
        #         if match(type_d, type_) != None:
        #             del_list.append(self.columns[i])
        # for del_ in del_list:
        #     self.columns.remove(del_)

    def function(self): # 把用于预测未知值的列提取出来作为X，待预测的列作为Y
        # 初始化
        # model = joblib.load('./GBRT_FILE/GBRT_Denoise_X_Force.pkl')
        model = joblib.load('GBRT_model_XVIBRATION.pkl')
        col = self.col
        print(self.columns, col)
        self.columns.remove(col)
        list_traning = self.columns
        # 处理列
        print(list_traning)
        X = self.pickle_data[list_traning]
        Y = self.pickle_data[col] # 除选中的待去噪列，其他列作为预测参考值
        # 训练
        # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=1)
        # model = GradientBoostingRegressor(n_estimators=self.n_estimators)
        print("-------------------------------------------------------------------")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~调参~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print('file name: ', self.pickle_read_path)
        # score0 = model.score(X_train,Y_train)
        score1 = model.score(X,Y) 
        # score2 = model.score(X_test,Y_test) 
        print('n_estimators: ', self.n_estimators)
        #以下代码是为了测试模型预测准确度
        # print("R^2 of train, %.5f" % (score0)) 
        print("R^2 of all, %.5f" % (score1)) 
        # print("R^2 of test, %.5f" % (score2)) 
if __name__=='__main__':
    regression_model_train = Regression_Model_Train()
    regression_model_train.function()
    # 打印
    # profiler.stop()
    # profiler.print()