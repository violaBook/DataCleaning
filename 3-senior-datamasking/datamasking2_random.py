'''
functions-module[3-2]: 【值】
    EG: input col-num, re-fill the col-values with random values.
    Chinese: 某列数据随机化(基本上相差不大,上下稍微浮动) 
demonstration:
       _____________________________you can run like this__________
    |  python datamasking2_random.py col_name                      |___________________________
    | python datamasking2_random.py X_Force './../new_data.pkl' 'pkl/datamasking2_random.pkl'  |
    ___________________________________________________________________________________________
Date: 
    2021/11/6 22:32
Check:
    debug-ok 2021/11/6 22:39√
'''
import pandas as pd # data-addressing
import numpy as np
from time import time # others
from sys import argv
from random import random
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

class Masking_Random():
    def __init__(self):
        # init-argv
        self.col_name = argv[1]
        self.read_file_path = argv[2]
        self.write_file_path = argv[3]
        # init-others
        self.csv_data = pd.read_pickle(self.read_file_path)
        self.col_names = self.csv_data.columns.tolist()
        self.k = 0.01 # 浮动范围，建议小于0.1
    # 数据随机化(将一列数据加上随机生成的一个小数)
    def DataRandomization(self, col_name):
        self.csv_data[col_name] = self.csv_data[col_name].astype(float)
        dlt = self.csv_data[col_name].max() - self.csv_data[col_name].min()
        self.csv_data[col_name] = self.csv_data[col_name] + (random()-0.5)*self.k*dlt
    def function(self):
        # self.csv_data[self.col_name] = self.csv_data[self.col_name]*1000 # debug-use
        # do-random
        self.DataRandomization(self.col_name)
        # write-csv
        self.csv_data.to_pickle(self.write_file_path)
        profiler.stop()
        profiler.print()
        # print(self.csv_data) # debug-use
# main
if __name__=='__main__':
    masking_random = Masking_Random()
    masking_random.function()
    
    


    