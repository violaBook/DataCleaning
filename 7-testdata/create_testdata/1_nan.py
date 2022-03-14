import pandas as pd
import sys
import numpy as np

if __name__=='__main__':
    read_file_name = './' + 'csv_data' + '.csv'
    write_file_name = './' + 'nan' + '.csv'
    csv_data = pd.read_csv(read_file_name)
    print(csv_data)
    new_data = csv_data.loc[0:50, :]
    new_data.loc[[0,1,2,4,5,6], 'xForce'] = np.nan
    new_data.loc[[0,2,3,5,8], 'zForce'] = np.nan
    new_data.loc[0:20, 'xVibration'] = np.nan
    new_data.loc[:,'yVibration'] = np.nan
    print(new_data)
    new_data.to_csv(write_file_name)
