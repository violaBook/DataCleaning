'''
functions-module[3-4]: 【值】
    EG: input col-num, round 1 dot, others fill with *.
    Chinese: 数值型数据左右移位
demonstration:
    _____________________________you can run like this__________
    |  python datamasking4_shifting.py col_name direction shift_len          |_______________________
    | python datamasking4_shifting.py X_Force left 7 './../new_data.pkl' 'pkl/datamasking2_random.pkl'  |
     _______________________________________________________________________________________
Date: 
    2021/11/6 22:59
Check:
    debug-ok 2021/11/6 23:05√
maybe-optimize:
    -
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
from sys import argv
from re import match
class Masking_Shifting():
    def __init__(self):
        # init-argv
        self.col = argv[1]
        self.shift_direction = argv[2]
        self.shift_len = int(argv[3])
        # init-others
        self.read_file_path = argv[4] # debug-argv
        self.write_file_path = argv[5] # debug-argv
        self.csv_data = pd.read_pickle(self.read_file_path)
        self.col_names = self.csv_data.columns.tolist()
        self.is_numeric = False # default 0, not-argv
        self.numeric_example = ['float', 'int']
        self.col_type = str(self.csv_data[self.col].dtypes)
        # print(self.csv_data[self.col]) # debug-use

    def shift_left(self, x): # 加密
        y = x * pow(10, self.shift_len)
        return y
    def shift_right(self, x): # 加密
        y = x * pow(10, self.shift_len*-1)
        return y
    def function(self):
        # do-shifting
        if self.shift_direction == 'left':
            self.csv_data[self.col] = self.csv_data[self.col].map(self.shift_left)
        else:
            self.csv_data[self.col] = self.csv_data[self.col].map(self.shift_right)
        # others
        self.csv_data.to_pickle(self.write_file_path)
        profiler.stop()
        profiler.print()
        # print(self.csv_data[self.col]) # debug-use
if __name__ == '__main__':
    masking_shifting = Masking_Shifting()
    masking_shifting.function()