
'''
functions-module[1-3]: 【值，字符串】
    EG: -
    Chinese: 对某一列按照数据完整性过滤(删除dict[col]这一列中有缺失的行)
demonstration:
     _____________________________you can run like this______________________
    |  python filter3_integ.py col                                       |_____________
    | python filter3_integ.py X_Force './../new_data.pkl' 'pkl/filter3_integ.pkl'        |
    _____________________________________________________________________________________    
Date:
    2021/11/6 19:45
Check:
    debug-ok 11/6 19:46√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
import sys
from re import match

class Filter_Integ():
    def __init__(self):
        # init-argv
        self.col=sys.argv[1]
        self.csv_read_path = sys.argv[2]
        self.csv_write_path = sys.argv[3]
        # init-others
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        # self.csv_data['X_Force'][0:3]=np.NaN # debug-use
    # 选中某一个属性值（某一列），按数据完整度过滤（即要求删除不完整的行）【功能3】
    def filter_integrity(self, col):
        csv_filter_inte=self.csv_data.dropna(axis='index', how='any', subset=[col]) # 删除dict[col]这一列中有缺失的行
        return csv_filter_inte
    def function(self):
        # do-filter-value
        new_data = self.filter_integrity(self.col)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use
if __name__=='__main__':
    filter_integ = Filter_Integ()
    filter_integ.function()