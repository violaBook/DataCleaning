'''
functions-module[5-1]: 【值】
    EG:first use the module to get the subbox, then use the mean-data to refill data according to subbox's mean-data
    中文: 先进行分箱，再用均值对不同分箱的数据进行填充
demonstration:
     _____________________________you can run like this__________________________
    |   python Denosing1_SubBox.py col_name                                       |
    | python denoising1_SubBox.py X_Force './../t_data.pkl' 'pkl/Denoising1_SubBox.pkl'   |
    ____________________________________________________________________________
Date: 
    2021/10/31 15:54
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np 
from sys import argv # others
from time import time

#分箱：其实并没有消除异常值，而是将异常值分入某一类中，然后用临近值光滑它，这样在数据分析时不会因为个别的异常值影响整体的结果
class Denoising_SubBox():
    def __init__(self):
        # init-argv
        self.col= argv[1]
        self.csv_read_path = argv[2]
        self.csv_write_path = argv[3]
        # argv
        self.box_num = 5
        # init-others
        self.csv_data = pd.read_pickle(self.csv_read_path)

    def denoising_subbox(self, col):
        # 初始化
        box_num = self.box_num
        csv_data_col_ndarray = self.csv_data.loc[:, col].values
        csv_data_col_ndarray = csv_data_col_ndarray.astype(np.float64)
        # 使用模型
        box, bins=pd.cut(csv_data_col_ndarray, bins=box_num, retbins=True)
        time1 = time()
        # 将所有分箱类别存入一个列表中
        for i in range(len(bins)-1):
            # 获取每个分箱的索引
            idx = (csv_data_col_ndarray >= bins[i]) & (csv_data_col_ndarray <= bins[i+1])
            # 对每个分箱的索引求均值
            csv_data_col_ndarray[idx] = np.mean(csv_data_col_ndarray[idx])
        # 赋值csv_data
        self.csv_data[col] = csv_data_col_ndarray
        # 写数据库
        self.csv_data.to_pickle(self.csv_write_path)

    def function(self):
        # do-function
        self.denoising_subbox(self.col)
        # others
        profiler.stop()
        profiler.print()
        # print(self.csv_data) # debug-use

if __name__=='__main__':
    denoising_subbox = Denoising_SubBox()
    denoising_subbox.function()