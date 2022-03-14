# 以下是回归的模型训练过程，通过此过程生成模型并保存为pkl文件
""" 
    python '数据源.py'
"""

from pandas.core import indexing
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
from sys import argv
import pandas as pd
from re import IGNORECASE, match
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    pickle_write_path = './t1_data.pkl'
    col_names = ['X_Force','Y_Force','Z_Force','X_Vibration','Y_Vibration','Z_Vibration','AE_RMS']

    list_ = []
    for i in range(1, 2):
        pickle_read_path = './c1' + '/c_1_00' + str(i) +'.csv'
        pickle_data = pd.read_csv(pickle_read_path, header=None, names=col_names)
        list_.append(pickle_data)
        print(pickle_data)
    new_data = pd.concat(list_, axis=0, ignore_index=True, )
    new_data.astype('float')
    new_data.columns = col_names
    print(new_data.dtypes)
    new_data.reset_index()
    # for i in range(1, 9):
        # new_data = pd.concat([pickle_data[i],new_data[i+1]], axis=0)
    # new_data.rename(index={'0':'X_Force','1':'Y_Force','2':'Z_Force','3':'X_Vibration','4':'Y_Vibration','5':'Z_Vibration','6':'AE_RMS'})
    # new_data.to_csv(csv_write_path, index=False)
    new_data.columns = ['xForce', 'yForce', 'zForce', 'xVibration', 'yVibration', 'zVibration', 'aeRMS']
    new_data.to_pickle(pickle_write_path)

    
    pickle_data = pd.read_pickle(pickle_write_path)
    print(pickle_data)
