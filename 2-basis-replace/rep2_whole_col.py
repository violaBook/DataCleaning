'''
functions-module[2-2]: 【值，字符串，日期】
    EG: module will replace required-replace-value in col-value with new-value.
    Chinese: 模块将用你输入的新值对这列中所有元素进行替换
demonstration:
     _____________________________you can run like this_______________
    |  python rep2_whole_col.py col_name new_data                     |____________________
    | python rep2_whole_col.py X_Force 131.4 './../new_data.pkl' './pkl/rep2_whole_col'  |
    _______________________________________________________________________________________
Date:
    2021/11/6 20:33
Check:
    debug-ok 11/6 20:35√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from time import time # others
import sys
from re import match

class Rep2_Whole_Col():
    def __init__(self):
        # init-argv
        self.col, self.val_re = sys.argv[1], sys.argv[2]
        self.csv_read_path = sys.argv[3]
        self.csv_write_path = sys.argv[4]
        # init-others
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
    def whole_column_replace(self, col, val_re):
        # init
        col_type = str(self.csv_data[col].dtypes) # col_type-init
        numeric_example = ['float', 'double', 'int'] # 数值类型
        datetime_example = ['datetime64', 'datetime'] # 日期类型
        str_example = ['object'] # 文本类型
        for i, numeric in enumerate(numeric_example):
            if match(numeric, col_type):
                if i==0:
                    val_re = float(val_re)
                if i==1:
                    val_re = float(val_re)
                if i==2:
                    val_re = int(val_re)
        for dtime in datetime_example:
            if match(dtime, col_type):
                val_re = val_re
        for string in str_example:
            if match(string, col_type):
                val_re = str(val_re)
        # do-replace
        self.csv_data[col] = val_re
        return self.csv_data
    def function(self):
        # do-filter-value
        new_data = self.whole_column_replace(self.col, self.val_re)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use

if __name__=='__main__':
    rep2_whole_col = Rep2_Whole_Col()
    rep2_whole_col.function()