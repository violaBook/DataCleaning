'''
functions-module[2-3]: 【值】
    EG: module will replace required-replace-value in col-value with new-value.
    Chinese: 将某一列的某个范围的值替换为给定的一个值
demonstration:
     _____________________________you can run like this______________________
    |  python rep3_range_val.py col_name min_data max_data new_data                   |________________
    | python rep3_range_val.py X_Force 0.772 0.888 131.4 './../new_data.pkl' './pkl/rep3_range_val.pkl'  |
    ____________________________________________________________________________________________
Date:
    2021/11/10 14:08
Check:
    debug-ok 11/10 14:20√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd 
import numpy as np
from time import time 
import sys
from re import match

class Rep3_Range_Val():
    def __init__(self):
        # init-argv
        self.col = sys.argv[1]
        self.val_min, self.val_max, self.val_re = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
        self.csv_read_path = sys.argv[5]
        self.csv_write_path = sys.argv[6]
        # read
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        
    def range_value_replace(self, col, val_min, val_max, val_re):
        # 格式转换
        col_values = self.csv_data[col].values
        col_values = col_values.astype(np.float64)
        # 数值替换
        idx = (val_min <= col_values) & (col_values <= val_max)
        self.csv_data[col][idx] = val_re
        return self.csv_data
    def function(self):
        # do-filter-value
        new_data = self.range_value_replace(self.col, self.val_min, self.val_max, self.val_re)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use

if __name__=='__main__':
    rep1_single_val = Rep3_Range_Val()
    rep1_single_val.function()