'''
functions-module[2-3]: 【日期】
    EG: module will replace required-replace-value in col-value with new-value.
    Chinese: 将某一列的某个时间范围的值替换为给定的一个值
demonstration:
     _____________________________you can run like this______________________
    |  python rep4_range_time.py col_name min_time max_time new_time                   |________________
    | python rep4_range_time.py start_time '2021-1-1 1:1:1' '2021-6-1 1:1:4' '2066-6-6 1:1:4' './../new_data.pkl' './pkl/rep4_range_time.pkl'  |
    ____________________________________________________________________________________________
Date:
    2021/11/10 15:00
Check:
    debug-ok 11/10 15:14√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd 
import numpy as np
from time import time 
import datetime
import sys
from re import match

class Rep3_Range_Time():
    def __init__(self):
        # init-argv
        self.col = sys.argv[1]
        self.time_min, self.time_max, self.time_re = sys.argv[2], sys.argv[3], sys.argv[4]
        self.csv_read_path = sys.argv[5]
        self.csv_write_path = sys.argv[6]
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        
    def replace_range_time(self, col, time_min, time_max, time_re):
        # 格式转换
        low_time = pd.datetime.strptime(time_min,'%Y-%m-%d %H:%M:%S')
        high_time = pd.datetime.strptime(time_max, '%Y-%m-%d %H:%M:%S')
        re_time = pd.datetime.strptime(time_re, '%Y-%m-%d %H:%M:%S')
        # 数值替换
        idx = (low_time <= self.csv_data[self.col]) & (self.csv_data[self.col] <= high_time)
        self.csv_data[col][idx] = re_time
        return self.csv_data
    def function(self):
        # do-filter-value
        new_data = self.replace_range_time(self.col, self.time_min, self.time_max, self.time_re)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use

if __name__=='__main__':
    rep1_single_val = Rep3_Range_Time()
    rep1_single_val.function()