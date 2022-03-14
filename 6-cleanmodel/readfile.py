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
python readfile.py CleanModel
'''