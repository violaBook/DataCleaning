import pandas as pd
import sys
import numpy as np


if __name__=='__main__':
    # 初始化
    
    read_file_name = './csv_data.csv'
    write_file_name =  './4_denoise.csv'
    #
    new_data = pd.read_csv(read_file_name)
    # 写数据
    # 1
    new_data = new_data.loc[0:65, :]
    # 写入字符串数据
    new_data.loc[0:1, 'xForce'] = 11
    new_data.loc[0:2, 'yForce'] = 8
    new_data.loc[0:1, 'zForce'] = 5
    new_data.loc[0:2, 'xVibration'] = 2
    new_data.loc[0:3, 'yVibration'] = 5
    new_data.loc[0:2, 'aeRMS'] = 100

    # 写csv
    print(new_data)
    new_data.to_csv(write_file_name)


    