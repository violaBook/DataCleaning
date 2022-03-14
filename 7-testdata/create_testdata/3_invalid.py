import pandas as pd
import sys
import numpy as np

if __name__=='__main__':
    # 初始化
    read_file_name = './' + 'csv_data' + '.csv'
    write_file_name = './' + '3_invalid' + '.csv'
    new_data = pd.read_csv(read_file_name)
    print(new_data)
    # 写数据
    # 1
    new_data = new_data.loc[0:55, :]
    
    # 写入字符串数据
    new_data['text'] = 'come_on'
    new_data['text'][6:15] = 'the_outbreak'
    new_data['text'][16:30] = 'my_little'
    new_data['text'][31:55] = 'universe'
    # 写csv
    print(new_data)
    new_data.to_csv(write_file_name)


    