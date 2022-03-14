'''
functions-module[3-5]: 【字符串】
    EG: -
    Chinese: 将用户输入列处理成统一编号的数据，掩盖了之前的数据内容
demonstration:
     _____________________________you can run like this__________
    |  python datamasking5_encoding.py col_name cut_pre cut_post   |_______________________
    | python datamasking5_encoding.py str_col 2 5 './../new_data.pkl' 'pkl/datamasking5_encoding.pkl'  |
    _______________________________________________________________________________________
Date: 
    2021/11/6 23:10
Check:
    debug-ok 2021/11/6 23:12√
'''
import pickle
import pandas as pd # data-addressing
import numpy as np
from time import time # others
import sys
from re import match
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

class encode():
    def __init__(self):
        # argv
        self.col = sys.argv[1]
        self.cut_pre = int(sys.argv[2])
        self.cut_post = int(sys.argv[3])
        self.csv_read_path = sys.argv[4]
        self.csv_write_path = sys.argv[5]
        # read-csv
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        # others
        self.cut_pre = self.cut_pre - 1 # 下标从1开始
        self.cut_post = self.cut_post # offset=1
        self.len = self.cut_post - self.cut_pre
        self.max_ = pow(10,self.len)
        # i-iterator
        # self.i_list  = [str(i).zfill(self.len) for i in range(0, self.max_)]
        # init
        self.i = 0
        self.is_numeric = False # default 0, not-argv
    def numeric_to_str(self, multiply): # 该功能因为接口问题，放弃使用
        numeric_example = ['float', 'int']
        col_type = str(self.csv_data[self.col].dtypes)
        # float和int转化为字符串类型
        for i, numeric in enumerate(numeric_example):
            if match(numeric, col_type):
                self.csv_data[self.col] = self.csv_data[self.col]*multiply
                if i==0: # float
                    self.csv_data[self.col] = self.csv_data[self.col].astype(int)
                if i==1: # int
                    pass
                self.csv_data[self.col] = self.csv_data[self.col].astype(str) 
                self.is_numeric = True
    def encoding(self, x): # 乘数后截断小数,若不想要乘法就取参数1
        # float和int转化为字符串类型
        str_i = str(self.i)
        rest_len = self.len - len(str_i)
        encoding = rest_len*'0'+ str_i
        y = x[:int(self.cut_pre)] + encoding + x[int(self.cut_post):]
        self.i = self.i + 1
        if self.i == self.max_:
            self.i = 0
        return y
    def function(self):
        # 浮点数转化为str
        self.numeric_to_str(1)
        # do-encrypt
        self.csv_data[self.col] = self.csv_data[self.col].apply(self.encoding)
        # write-csv
        self.csv_data.to_pickle(self.csv_write_path)
        profiler.stop()
        profiler.print()
        # print(self.csv_data[self.col]) # debug-use

if __name__ == '__main__':
    encode_ = encode()
    encode_.function()