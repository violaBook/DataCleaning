'''
functions-module[1-6]: 【字符串】
    EG: -
    Chinese: 对某一列的数据用正则表达式进行过滤
demonstration:
     _____________________________you can run like this______________________
    |  python rep5_re.py col_name re_                                      |_______________________
    | python rep5_re.py str_col 'b[abo]y_n\S*_[a-z]+r' 'rep5~' './../new_data.pkl' 'pkl/rep5_re.pkl'  |
    ________________________________________________________________________________________________
Date:
    2021/11/10 16:40
Check:
    debug-ok 11/10 16:40√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from re import match
import sys

class Replace_Re():
    def __init__(self):
        # init-argv
        self.col_name = sys.argv[1]
        self.re_ = sys.argv[2]
        self.rep_val = sys.argv[3]
        self.csv_read_path = sys.argv[4]
        self.csv_write_path = sys.argv[5]
        # read-pickle
        self.csv_data = pd.read_pickle(self.csv_read_path)
    def replace_re(self):
        # init
        col_name = self.col_name
        copy_ = self.csv_data[col_name]
        # do
        result_idx = copy_.map(self.match_)
        self.csv_data[self.col_name][result_idx] = self.rep_val
    def match_(self, x):
        if match(self.re_, x):
            return True
        else:
            return False
    def function(self):
        # do-filter-value
        self.replace_re()
        # write-csv
        self.csv_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(self.csv_data[self.col_name]) # debug-use

if __name__ == '__main__':
    filter_value = Replace_Re()
    filter_value.function()



