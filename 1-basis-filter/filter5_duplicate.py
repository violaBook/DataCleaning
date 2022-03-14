'''
functions-module[1-5]: 【值，日期，字符串】
    EG: -
    Chinese: 选中某一个属性值（某一列），去掉该列重复的行
demonstration:
     _____________________________you can run like this_________________
    |  python filter5_duplicate.py col_name                           |__________________
    | python filter5_duplicate.py X_Force './../new_data.pkl' 'pkl/filter5_duplicate.pkl'       |
    _____________________________________________________________________________________________
Date:
    2021/11/6 19:59
Check:
    debug-ok 11/6 20:03√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
import sys

class Filter_DropUP():
    def __init__(self):
        self.col=sys.argv[1]
        self.csv_read_path = sys.argv[2]
        self.csv_write_path = sys.argv[3]
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
    # 选中某一个属性值（某一列），去掉该列重复的行【功能5】
    def filter_dropdup(self, col):
        #0.1s左右
        self.csv_data.drop_duplicates(col, inplace=True,ignore_index=True)  # 本例也可写为data_frame_concat.drop_duplicates(inplace=True,ignore_index=True),即去掉完全重复的行数
        return self.csv_data
    def function(self):
        # do-filter-value
        new_data = self.filter_dropdup(self.col)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use
if __name__=='__main__':
    filter_dropup = Filter_DropUP()
    filter_dropup.function()