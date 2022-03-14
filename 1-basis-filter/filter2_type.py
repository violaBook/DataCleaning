'''
functions-module[1-2]: 【值, 字符串，日期】
    EG: -
    Chinese: 给定一个数据类型对某一列满足要求的数据进行过滤
demonstration:
     _____________________________you can run like this______________________
    |  python filter2_type.py val_type                                      |_____________
    | python filter2_type.py datetime './../new_data.pkl' 'pkl/filter2_type.pkl'              |
    | val_type: float/datetime/string
    ________________________________________________________________________________________
Date:
    2021/11/6 19:35
Check:
    debug-ok 11/6 19:37√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from time import time # others
import sys
from re import match

class Filter_Type():
    def __init__(self):
        # init-argv
        self.data_type=sys.argv[1]
        self.csv_read_path = sys.argv[2]
        self.csv_write_path = sys.argv[3]
        # init
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
        self.col_types = self.csv_data.dtypes.astype('str').tolist()
        self.sure_len = 10000
        self.time0 = time()
        print('csv_data:\n', self.csv_data)
        # print("self.col_types.tolist(): ", self.col_types.tolist())

    # 选中某一个属性值（某一列），按数据类型过滤
    def filter_type(self, filter_type):
        # 初始化
        col_satisfied = []
        type_list = self.csv_data.dtypes.astype(str)
        time_re = '^[0-9]*-[0-9]*-[0-9]*[ ][0-9]*:[0-9]*:[0-9]*$'
        # 先判定是否是数值，不是数值需要用正则表达式判断类型
        if match('float', filter_type): # 判数值
            for i, type_ in enumerate(type_list):
                if match(filter_type, type_)!= None:
                    col_satisfied.append(i)
            return self.csv_data.iloc[:, col_satisfied]
        else: # 判日期还是字符串(用正则)
            # 先去除数值列
            del_i = []
            del_name = []
            for i, type_ in enumerate(type_list):
                if match(type_, 'float64')!= None:
                    del_i.append(i)
            for i_ in del_i:
                del_name.append(self.col_names[i_])
            for name_ in del_name:
                self.col_names.remove(name_)
            self.csv_data = self.csv_data.loc[:, self.col_names]
            # 判段类型
            if match('datetime', filter_type): # 判日期
                for i in range(self.csv_data.shape[1]):
                    is_time = True
                    if self.csv_data.shape[0] > self.sure_len:
                        data = self.csv_data.iloc[0:self.sure_len, i]
                    else:
                        data = self.csv_data.iloc[:, i]
                    for x in data:
                        if match(time_re, str(x)) != None:
                            pass
                        else:
                            is_time = False
                            break
                    if is_time == True:
                        col_satisfied.append(i)   
                return self.csv_data.iloc[:, col_satisfied]
            else: # 判字符串
                time_del = []
                del_time_name = []
                time0 = time()
                for i in range(self.csv_data.shape[1]):
                    is_time = True
                    if self.csv_data.shape[0] > self.sure_len:
                        data = self.csv_data.iloc[0:self.sure_len, i]
                    else:
                        data = self.csv_data.iloc[:, i]
                    for x in data:
                        if match(time_re, str(x)) != None:
                            pass
                        else:
                            is_time = False
                            continue
                    if is_time == True:
                        time_del.append(i) 
                for i in time_del:
                    del_time_name.append(self.col_names[i])
                for name_ in del_time_name:
                    self.col_names.remove(name_)
                self.time1 = time()
                print('filter time: ', self.time1-self.time0)
                return self.csv_data.loc[:, self.col_names]
    def function(self):
        # do-filter-value
        new_data = self.filter_type(self.data_type)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        print(new_data) # debug-use
if __name__ == '__main__':
    filter_type = Filter_Type()
    filter_type.function()

