'''
functions-module[3-1]: 【值，字符串】
    EG: input col-num, invalid the col-values.
    Chinese: 某列数据无效化
demonstration:
       _____________________________you can run like this________________
    |  python datamasking1_invalidation.py col_name menu cut_pre cut_post  |________________________________________
    | python datamasking1_invalidation.py X_Force hide 2 5 './../new_data.pkl' './pkl/datamasking1_invalidation.pkl'             |
    | python datamasking1_invalidation.py X_Force encrypt 2 end './../new_data.pkl' './pkl/datamasking1_invalidation.pkl'       |
    | python datamasking1_invalidation.py str_col encrypt 2 4 './../new_data.pkl' './pkl/datamasking1_invalidation.pkl'         |
    |                                       params:                                                                 |
    |       col_name=>列名, menu=>hide(隐藏)/encrypt(打码), cut_pre=>整数(起始点), cut_post=>整数/'end'(结束点)        |
    ________________________________________________________________________________________________________________
Date: 
    2021/11/6 22:04
Check:
    debug-ok 11/6 22:31
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from time import time # others
from sys import argv
from re import match

class Masking_Invaildation():
    def __init__(self):
        # init-argv
        self.col = argv[1]
        self.menu = argv[2]
        self.cut_pre = int(argv[3])
        self.cut_post = argv[4]
        self.read_file_path = argv[5]
        self.write_file_path = argv[6]
        # init-others
        self.csv_data = pd.read_pickle(self.read_file_path)
        self.col_names = self.csv_data.columns.tolist()
        self.numeric_example = ['float', 'int']
        self.col_type = str(self.csv_data[self.col].dtypes)
        self.cut_len = 1 # formal-use
        # self.cut_len = 12315 # debug-use(数据太小,放大数据让测试效果更明显)
    def cutoff(self, multiply): # 乘数后截断小数,若不想要乘法就取参数1
        # float和int转化为字符串类型
        for i, numeric in enumerate(self.numeric_example):
            if match(numeric, self.col_type):
                self.csv_data[self.col] = self.csv_data[self.col]*multiply
                if i==0: # float
                    self.csv_data[self.col] = self.csv_data[self.col].astype(int)
                if i==1: # int
                    pass
                self.csv_data[self.col] = self.csv_data[self.col].astype(str) # ?
            # csv_data[col] = csv_data[col].map(lambda x: str(x)) # same
    def encrypt(self, x): # 加密
        if self.cut_post == 'end':
            y = x[:int(self.cut_pre)] + '******'
        else:
            y = x[:int(self.cut_pre)] + '*'*(int(self.cut_post)-int(self.cut_pre)) + x[int(self.cut_post):]
        return y
    def hide(self, x): # 隐藏
        if self.cut_post == 'end':
            y = x[:int(self.cut_pre)]
        else:
            y = x[:int(self.cut_pre)] + x[int(self.cut_post):]
        return y
    def function(self):
        is_numeric = False # default 0, not-argv
        for i, numeric in enumerate(self.numeric_example):
            if match(numeric, self.col_type):
                is_numeric=True
                break
        # cut_post:offset-1 
        if self.cut_post != 'end': 
            cut_pre = int(self.cut_pre) - 1   
        # do-cutoff(if numeric)
        if is_numeric==True:
            self.cutoff(self.cut_len) # debug-number:123451, formal-number:1
        # do-encrypt/hide
        if self.menu == 'hide':
            self.csv_data[self.col] = self.csv_data[self.col].map(self.hide)
        else:
            self.csv_data[self.col] = self.csv_data[self.col].map(self.encrypt)
        # write-csv
        self.csv_data.to_pickle(self.write_file_path)
        profiler.stop()
        profiler.print()
        # print(self.csv_data) # debug-use

if __name__ == '__main__':
    masking_invaildation = Masking_Invaildation()
    masking_invaildation.function()
