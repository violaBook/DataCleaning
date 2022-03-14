
'''
functions-module[1-4]: 【日期】
    EG: -
    Chinese: 输入两个时间戳，查询时间戳范围内的数据
demonstration:
     _____________________________you can run like this______________________
    |  python filter4_del_time.py col_name low_time high_time                         |_________________________________
    | python filter4_time.py end_time '2022-3-1 1:2:2' '2022-12-2 1:1:4' './../new_data.pkl' './pkl/filter4_time.pkl'   |
    ____________________________________________________________________________________________________________________
Date:
    2021/11/6 19:48
Check:
    debug-ok 11/6 19:58√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
from sys import argv

class Filter_Time():
    def __init__(self):
        # init-argv
        self.col = argv[1]
        self.low_time = argv[2]
        self.high_time = argv[3]
        self.csv_read_path = argv[4]
        self.csv_write_path = argv[5]
        # init-others
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()

    def filter_time(self, low_time, high_time):
        low_time=pd.datetime.strptime(low_time,'%Y-%m-%d %H:%M:%S')
        high_time = pd.datetime.strptime(high_time, '%Y-%m-%d %H:%M:%S')
        target = self.csv_data[(low_time < self.csv_data[self.col]) & (self.csv_data[self.col] < high_time)]
        return target
    def function(self):
        # do-filter-value
        new_data = self.filter_time(self.low_time, self.high_time)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        print(new_data) # debug-use

if __name__=='__main__':
    filter_time = Filter_Time()
    filter_time.function()