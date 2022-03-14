# 以下是回归的模型训练过程，通过此过程生成模型并保存为pkl文件
""" 
    python '数据源.py'
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


if __name__ == '__main__':
    list_ = []
    for i in range(1, 7):
        pickle_read_path = './c1' + '/c_1_00' + str(i) +'.csv'
        pickle_data = pd.read_csv(pickle_read_path, header=None, names=['X_Force','Y_Force','Z_Force','X_Vibration','Y_Vibration','Z_Vibration','AE_RMS'])
        list_.append(pickle_data)
        print(pickle_data)
    new_data = pd.concat(list_, axis=0, ignore_index=True)
    new_data.astype('float')
    print(new_data.dtypes)
    
    # for i in range(1, 9):
        # new_data = pd.concat([pickle_data[i],new_data[i+1]], axis=0)
    new_data.to_csv('t_data.csv')
    new_data.to_pickle('t_data.pkl')
    print(new_data)