import pandas as pd
import sys
import numpy as np

if __name__=='__main__':
    # 初始化
    read_file_name = './' + 'csv_data' + '.csv'
    write_file_name = './' + '2_time' + '.csv'
    new_data = pd.read_csv(read_file_name)
    print(new_data)
    # 写数据
    # 1
    new_data = new_data.loc[0:60, :]
    new_data['start_time'] = pd.to_datetime('2021-11-11 0:0:0')
    new_data['end_time'] = pd.to_datetime('2022-12-12 0:0:0')
    # 2
    new_data['start_time'][0:10] = pd.to_datetime('2021-1-1 1:2:3')
    new_data['start_time'][11:35] = pd.to_datetime('2021-5-5 2:3:4')
    new_data['start_time'][36:60] = pd.to_datetime('2021-9-9 4:5:6')
    # 3
    new_data['end_time'][0:5] = pd.to_datetime('2022-2-2 6:7:6')
    new_data['end_time'][6:10] = pd.to_datetime('2022-4-6 7:8:4')
    new_data['end_time'][11:15] = pd.to_datetime('2022-7-7 8:9:2')
    new_data['end_time'][16:37] = pd.to_datetime('2023-9-13 8:9:3')
    new_data['end_time'][38:60] = pd.to_datetime('2023-12-11 8:9:1')
    # 写csv
    print(new_data)
    new_data.to_csv(write_file_name)


    