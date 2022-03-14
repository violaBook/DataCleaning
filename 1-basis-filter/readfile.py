import pandas as pd
import time
import sys
import numpy as np

if __name__=='__main__':
    name = sys.argv[1]
    read_file_name = './pkl/'+name+'.pkl' # 模块一数据
    # read_file_name = './../'+'new_data'+'.pkl' # debug-use
    csv_data = pd.read_pickle(read_file_name)
    print(csv_data)
'''
可以直接输入以下命令查看文件数据:
python readfile.py filter1_value
python readfile.py filter2_type
python readfile.py filter3_integ
python readfile.py filter4_time
python readfile.py filter5_duplicate
'''