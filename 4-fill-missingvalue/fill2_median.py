'''
functions-module[4-2]: 【值】
    EG: use the median col-values to fill the NAN
    中文：用每一列的均值/平均值填补空值
demonstration:
     _____________________________you can run like this____________
    |   python fill2_median.py                                      |____________
    | python fill2_median.py './../new_data.pkl' 'pkl/fill2_median.pkl'             | 
    _______________________________________________________________________________
Date: 
    2021/10/31 11:00
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd # data-addressing
import numpy as np
from sklearn.impute import SimpleImputer # sklearn
from time import time # others
from re import match
import sys

class Median_Fill():
    def __init__(self):
        self.read_file_path = sys.argv[1]
        self.write_file_path = sys.argv[2]
        # read-csv
        self.csv_data = pd.read_pickle(self.read_file_path)
        self.satisfied_colnames = self.csv_data.select_dtypes(exclude=['datetime64[ns]','object']).columns.tolist()
        self.strategy = 'median' 
    # median-fill
    def median_fill(self, cols, strategy):
        # 初始化
        data_ndarray = self.csv_data[cols].values
        # 使用模型
        imp_median = SimpleImputer(missing_values=np.nan, strategy=strategy)
        # imp_median.fit(data_ndarray)
        self.csv_data[cols] = imp_median.fit_transform(data_ndarray)
    def function(self):
        # del_datetime&str
        numeric_example = ['float', 'int'] # 数值类型
        datetime_example = ['datetime64', 'datetime'] # 日期类型
        str_example = ['object'] # 文本类型
        # do-datainvalidation
        # self.csv_data.iloc[0:5, 1] = np.nan # debug-use
        self.median_fill(cols=self.satisfied_colnames, strategy=self.strategy)
        # write-csv
        self.csv_data.to_pickle(self.write_file_path)
        profiler.stop()
        profiler.print()
        # print(self.csv_data[self.satisfied_colnames]) # debug-use

# main
if __name__=='__main__':
    m_fill = Median_Fill()
    m_fill.function()
    