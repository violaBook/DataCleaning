'''
functions-module[2-1]: 【值，字符串，日期】
    EG: module will replace required-replace-value in col-value with new-value.
    Chinese: 模块将用你输入的新值对这列中所有要求替换的值进行替换(将某一列的某个特定的值替换为另外一个值)
demonstration:
     _____________________________you can run like this______________________
    |  python rep1_single_val.py col_name pre_data post_data                   |________________
    | python rep1_single_val.py X_Force 0.772 131.4 './../new_data.pkl' './pkl/rep1_single_val'  |
    ____________________________________________________________________________________________
Date:
    2021/11/6 20:25
Check:
    debug-ok 11/6 20:29√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from time import time # others
import sys
from re import match

class Rep1_Single_Val():
    def __init__(self):
        # init-argv
        self.col, self.val, self.val_re = sys.argv[1], sys.argv[2], sys.argv[3]
        self.csv_read_path = sys.argv[4]
        self.csv_write_path = sys.argv[5]
        # col, val, val_re = 'str_col hello hi' # test-use
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        
    def single_value_replace(self, col, val, val_re):
        # init
        col_type = str(self.csv_data[col].dtypes) # col_type-init
        numeric_example = ['float', 'int'] # 数值类型
        datetime_example = ['datetime64', 'datetime'] # 日期类型
        str_example = ['object'] # 文本类型
        for i, numeric in enumerate(numeric_example):
            if match(numeric, col_type):
                if i==0:
                    val = float(val)
                    val_re = float(val_re)
                if i==1:
                    val = int(val)
                    val_re = int(val_re)
        for dtime in datetime_example:
            if match(dtime, col_type):
                val = val
                val_re = val_re
        for string in str_example:
            if match(string, col_type):
                val = str(val)
                val_re = str(val_re)
        # single-value-rep
        self.csv_data.loc[self.csv_data[col]==val, col] = val_re
        return self.csv_data
    def function(self):
        # do-filter-value
        new_data = self.single_value_replace(self.col, self.val, self.val_re)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        print(new_data) # debug-use

if __name__=='__main__':
    rep1_single_val = Rep1_Single_Val()
    rep1_single_val.function()