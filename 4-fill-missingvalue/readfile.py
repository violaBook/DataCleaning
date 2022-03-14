import pandas as pd
import time
import sys
import numpy as np

if __name__=='__main__':
    name = sys.argv[1]
    read_file_name = './pkl/'+name+'.pkl'
    csv_data = pd.read_pickle(read_file_name)
    print(csv_data)

'''
可以直接输入以下命令查看文件数据:
python readfile.py fill1_mean
python readfile.py fill2_kmeans_mean
'''