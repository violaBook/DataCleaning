import pandas as pd
import numpy as np
from re import match


if __name__ == "__main__":
    x = '11'
    print(2*'22'+x)
    print('boy next door')

""" def cutoff(multiply): # 乘数后截断小数,若不想要乘法就取参数1
    # float和int转化为字符串类型
    for i, numeric in enumerate(numeric_example):
        if match(numeric, col_type):
            csv_data[col] = csv_data[col]*multiply
            if i==0: # float
                csv_data[col] = csv_data[col].astype(int)
            if i==1: # int
                pass
        csv_data[col] = csv_data[col].astype(str) 
        # csv_data[col] = csv_data[col].map(lambda x: str(x)) # same
def encrypt(x): # 加密
    if cut_post == 'end':
        y = x[:cut_pre] + '******'
    else:
        y = x[:cut_pre] + '*'*(cut_post-cut_pre) + x[cut_post:]
    return y
def hide(x): # 隐藏
    if cut_post == 'end':
        y = x[:cut_pre]
    else:
        y = x[:cut_pre] + x[cut_post:]
    return y

if __name__ == '__main__':
    # read-csv
    read_file_path = './../new_data.pkl'
    write_file_path = 'pkl/datamasking1_invalidataion.pkl'
    col = 'X_Force' # debug-argv
    csv_data = pd.read_pickle(read_file_path)
    col_names = csv_data.columns.tolist()
    # init
    is_numeric = False # default 0, not-argv
    is_encrypt = False # debug-argv
    numeric_example = ['float', 'int']
    col_type = str(csv_data[col].dtypes)
    for i, numeric in enumerate(numeric_example):
        if match(numeric, col_type):
            is_numeric=True
    # init-params
    cut_pre = 3 # debug-argv
    cut_post = 7 # debug-argv
    if cut_post != 'end': 
        cut_pre -= 1
    # do-cutoff
    if is_numeric==True:
        cutoff(123451) # debug-number:123451, formal-number:1
    # do-encrypt
    if is_encrypt==True:
        csv_data[col] = csv_data[col].map(encrypt)
    else:
        csv_data[col] = csv_data[col].map(hide)
    print(csv_data[col]) """