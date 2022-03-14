'''
functions-module[1-1]: 【值】
    EG: -
    Chinese: 给定一个范围对某一列满足要求的数据进行过滤
demonstration:
     _____________________________you can run like this______________________
    |  python filter1_value.py col_name min_data max_data                   |_______________________
    | python filter1_value.py X_Force 0.888 0.999 './../test_data.pkl' 'pkl/filter1_value.pkl'      |
    ________________________________________________________________________________________________
Date:
    2021/11/6 19:23
Check:
    debug-ok 11/6 19:28√
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
from time import time # others
import sys
from re import match

class Filter_Value():
    def __init__(self):
        # init-argv
        self.col_name = sys.argv[1]
        self.value_low=sys.argv[2]
        self.value_high=sys.argv[3]
        self.csv_read_path = sys.argv[4]
        self.csv_write_path = sys.argv[5]
        # read-pickle
        self.csv_data = pd.read_pickle(self.csv_read_path)
        self.col_names = self.csv_data.columns.tolist()
    def filter_value(self, col_name, value_low, value_high):
        value_low=value_low
        value_high=value_high
        csv_data_value_meets_condition = self.csv_data.loc[((self.csv_data[col_name] >= float(value_low)) & (self.csv_data[col_name] <= float(value_high))), :]
        return csv_data_value_meets_condition
    def if_is_numerical_col(self):
        numeric_example = ['float', 'double', 'int']
        flag_numerical = False 
        index = self.col_names.index(self.col_name)
        type_list = self.csv_data.dtypes.astype(str)
        type_require = type_list[index]
        for type_ in numeric_example:
            if match(type_, type_require) != None:
                flag_numerical = True
                break
        if flag_numerical == True:
            print('<you have choose the numerical column, it runs properly>')
        else:
            print('<please input numeric next time~>')
    def function(self):
        # judge-if-is-numerical
        self.if_is_numerical_col()
        # do-filter-value
        new_data = self.filter_value(self.col_name, self.value_low, self.value_high)
        # write-csv
        new_data.to_pickle(self.csv_write_path)
        # others
        profiler.stop()
        profiler.print()
        # print(new_data) # debug-use

if __name__ == '__main__':
    filter_value = Filter_Value()
    filter_value.function()



