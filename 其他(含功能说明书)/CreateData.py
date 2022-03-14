import pandas as pd
import sys
import numpy as np

if __name__=='__main__':
    read_file_name = './' + 'test_data' + '.pkl'
    write_file_name = './' + 'error_data' + '.pkl'
    csv_data = pd.read_pickle(read_file_name)
    # print(csv_data)
    csv_data['X_Force'][0] = -1234
    csv_data['X_Force'][1:10000] = np.nan
    csv_data['Y_Force'][3000:50000] = np.nan
    csv_data['Z_Force'][7236:234567] = np.nan

    # 写入datetime数据
    csv_data['start_time'] = pd.to_datetime('2021-11-11 0:0:0')
    csv_data['end_time'] = pd.to_datetime('2022-12-12 0:0:0')

    csv_data['start_time'][0:100000] = pd.to_datetime('2021-1-1 1:2:3')
    csv_data['start_time'][100001:500000] = pd.to_datetime('2021-5-5 2:3:4')
    csv_data['start_time'][500001:] = pd.to_datetime('2021-9-9 4:5:6')

    csv_data['end_time'][0:100000] = pd.to_datetime('2022-2-2 6:7:8')
    csv_data['end_time'][100001:500000] = pd.to_datetime('2022-6-6 7:8:9')
    csv_data['end_time'][500001:] = pd.to_datetime('2022-10-10 8:9:10')

    csv_data['start_time'] = csv_data['start_time'].astype('datetime64[ns]')
    csv_data['end_time'] = csv_data['end_time'].astype('datetime64[ns]')

    # 写入字符串数据
    csv_data['str_col'] = 'boy_next_door'


    csv_data.loc[0:400000, 'str_col'] = 'boy_next_door'
    csv_data.loc[400001:500002, 'str_col'] = 'lether*man'
    csv_data.loc[500003:, 'str_col'] = 'ddf_start!'
    # csv_data['str_col'] = 'hello_boy_next_door_my_name_is_van'
    # csv_data['str_col'] = csv_data['str_col'].astype('object')
    csv_data.to_pickle(write_file_name)

    # read-csv
    csv_read_path = './error_data.pkl' 
    see_data = pd.read_pickle(csv_read_path)
    print(see_data)
