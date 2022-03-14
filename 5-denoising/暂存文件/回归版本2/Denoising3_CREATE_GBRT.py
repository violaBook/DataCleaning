# 以下是回归的模型训练过程，通过此过程生成模型并保存为pkl文件
""" 
    -------------------------------------------------------------------
    python Denoising3_CREATE_GBRT.py xForce 'c1.pkl' 
    python Denoising3_CREATE_GBRT.py yForce 'c1.pkl'   
    python Denoising3_CREATE_GBRT.py zForce 'c1.pkl' 
    python Denoising3_CREATE_GBRT.py xVibration 'c1.pkl' 
    python Denoising3_CREATE_GBRT.py yVibration 'c1.pkl' 
    python Denoising3_CREATE_GBRT.py zVibration 'c1.pkl' 
    python Denoising3_CREATE_GBRT.py aeRMS 'c1.pkl' 
    -------------------------------------------------------------------
    参数格式：
        col_name(列名) 
        read_data_path(读取数据路径)
    -------------------------------------------------------------------
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
        self.write_name_ = './GBRT_denoise_' + str(self.col) + '.pkl'
        # 参数
        self.n_estimators = 100
        # read-pickle
        self.pickle_data = pd.read_pickle(self.pickle_read_path)
        # print(self.pickle_data) # debug-use
        self.columns = self.pickle_data.columns.tolist()
        # self.columns为数值类型且不存在空的列名
        type_list = self.pickle_data.dtypes.astype(str).tolist()
        type_del = ['datetime', 'object']
        del_list = []
        for i, type_ in enumerate(type_list):
            for type_d in type_del:
                if match(type_d, type_) != None:
                    del_list.append(self.columns[i])
        for del_ in del_list:
            self.columns.remove(del_)
   
    def function(self): # 把用于预测未知值的列提取出来作为X，待预测的列作为Y
        # 初始化
        col = self.col
        other_col=[]
        # 处理列
        for col_elem in self.columns:
            if col_elem != col:
                other_col.append(col_elem)
        X = self.pickle_data[other_col]
        Y = self.pickle_data[col] # 除选中的待去噪列，其他列作为预测参考值
        # 训练
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=1)
        model = GradientBoostingRegressor(n_estimators=self.n_estimators)
        y = model.fit(X_train, Y_train)
        print('model.train_score_: ', model.train_score_)

        # 模型写回
        write_name_ = self.write_name_
        joblib.dump(model, write_name_)
        print("-------------------------------------------------------------------")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~调参~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        score0 = model.score(X_train,Y_train)
        score1 = model.score(X,Y) 
        score2 = model.score(X_test,Y_test) 
        print('n_estimators: ', self.n_estimators)
        #以下代码是为了测试模型预测准确度
        print("R^2 of train, %.5f" % (score0)) 
        print("R^2 of all, %.5f" % (score1)) 
        print("R^2 of test, %.5f" % (score2)) 

if __name__=='__main__':
    regression_model_train = Regression_Model_Train()
    regression_model_train.function()
    # 打印
    # profiler.stop()
    # profiler.print()