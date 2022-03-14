'''
functions-module[1-6]: 【字符串】
    EG: -
    Chinese: 对某一列的数据用正则表达式进行过滤后替换该数据
demonstration:
     _____________________________you can run like this______________________
    |  python filter6_re.py col_name re_                                      |_______________________
    | python filter6_re.py str_col 'b[abo]y_n\S*_[a-z]+r' './../new_data.pkl' 'pkl/filter6_re.pkl'                    |
    ________________________________________________________________________________________________
Date:
    2021/11/6 19:23
    
    python filter6_re.py x_Force '(0|[1-9]\d*)(.\d{1,2})?' './../new_data.pkl' 'pkl/filter6_re.pkl'
Check:
    debug-ok 11/6 19:28√
'''
from ast import copy_location
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from time import time # others
import re
import sys
from re import X, match, search

class Filter_Re():
    def __init__(self):
        # init-argv
        self.col_name = sys.argv[1]
        self.re_ = sys.argv[2]
        self.csv_read_path = sys.argv[3]
        self.csv_write_path = sys.argv[4]
        # read-pickle
        self.csv_data = pd.read_pickle(self.csv_read_path)
    def filter_re(self):
        # init
        col_name = self.col_name
        copy_ = self.csv_data[col_name]
        # do
        result_idx = copy_.map(self.match_)
        return self.csv_data[result_idx]
    def match_(self, x):
        if re.match(self.re_, x):
            return True
        else:
            return False
    def function(self):
        # do-filter-value
        new_data = self.filter_re()
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use

if __name__ == '__main__':
    filter_value = Filter_Re()
    filter_value.function()



