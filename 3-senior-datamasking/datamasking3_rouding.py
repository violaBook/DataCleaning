'''
functions-module[3-3]: 【值,日期类型】
    EG: -
    Chinese: 对用户输入列的小数点取整或者日期类型格式化
demonstration:
       _____________________________you can run like this__________
    |  python datamasking3_rouding.py col_name                    |_______________________
    | python datamasking3_rouding.py Z_Force './../new_data.pkl' 'pkl/datamasking3_rouding.pkl'    |
    ________________________________________________________________________________________________
Date: 
    2021/11/6 22:46
Check:
    debug-ok 2021/11/6 22:58√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
from sys import argv

class Masking_Rounding():
    def __init__(self):
        # init-argv
        self.col_name = argv[1]
        self.read_file_path = argv[2]
        self.write_file_path = argv[3]
        # init-others
        self.csv_data = pd.read_pickle(self.read_file_path)
        self.col_names = self.csv_data.columns.tolist()
    def DataRounding(self, col_name):
        if self.csv_data[col_name].dtype!='datetime64[ns]':
            # self.csv_data[col_name] = self.csv_data[col_name].apply(lambda x: round(x,self.round_len))
            self.csv_data[col_name] = self.csv_data[col_name].apply(lambda x: int(x))
            # self.csv_data[col_name] = ["%.02f0000"% number for number in self.csv_data[col_name]]
        else:
            self.csv_data[col_name] = self.csv_data[col_name].dt.floor('h') # 将时间向下取整到小时
    def function(self):
        # do-rounding
        self.DataRounding(self.col_name)
        # write-csv
        self.csv_data.to_pickle(self.write_file_path)
        # others
        profiler.stop()
        profiler.print()
        # print(self.csv_data) # debug-use

# main
if __name__=='__main__':
    masking_rounding = Masking_Rounding()
    masking_rounding.function()

    