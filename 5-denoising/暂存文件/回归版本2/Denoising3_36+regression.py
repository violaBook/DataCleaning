'''
------------------------------------------------------------------------------------------------------
functions-module[5-3]: 【值】
    EG: first use 3∂-principle to get noise-index, then modify the noise with linear-regression.
    中文: 通过计算三倍标准差判定离群点，再用梯度提升回归树方法回归预测对离群点进行修改
------------------------------------------------------------------------------------------------------
demonstration:
     _____________________________you can run like this__________________________
    |   python denoising3_36+regression.py col_name use_model_name read_data_path write_data_path                            |
    | python denoising3_36+regression.py X_Force 'GBRT_Denoise_X_Force.pkl' './../t_data.pkl' 'pkl/Denoising3_36+regression.pkl'   |
------------------------------------------------------------------------------------------------------
样例: 
    python denoising3_36+regression.py xForce 'GBRT_Denoise_xForce.pkl' './c7.pkl' 'pkl/Denoising3_xForce.pkl'
    python denoising3_36+regression.py yForce 'GBRT_Denoise_yForce.pkl' './c7.pkl' 'pkl/Denoising3_yForce.pkl'
    python denoising3_36+regression.py zForce 'GBRT_Denoise_zForce.pkl' './c7.pkl' 'pkl/Denoising3_zForce.pkl'
    python denoising3_36+regression.py xVibration 'GBRT_Denoise_xVibration.pkl' './c7.pkl' 'pkl/Denoising3_xVibration.pkl'
    python denoising3_36+regression.py yVibration 'GBRT_Denoise_yVibration.pkl' './c7.pkl' 'pkl/Denoising3_yVibration.pkl'
    python denoising3_36+regression.py zVibration 'GBRT_Denoise_zVibration.pkl' './c7.pkl' 'pkl/Denoising3_zVibration.pkl'
    python denoising3_36+regression.py aeRMS 'GBRT_Denoise_aeRMS.pkl' './c7.pkl' 'pkl/Denoising3_aeRMS.pkl'
------------------------------------------------------------------------------------------------------
参数格式:
    col_name(列名) 
	use_model_name(调用模型名，在step1生成)
	read_data_path(读取数据路径)
	write_data_path(写回数据路径)
------------------------------------------------------------------------------------------------------

'''
# 3∂原则判定离群点+回归预测：输入参数格式：col （待处理数据列号）
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
import pandas as pd
from sys import argv
import joblib
import time

list_noise=[]

class Denoising_Regression():
    def __init__(self):
        # # init-argv
        self.col_name = argv[1]
        self.LOAD_GBRT = argv[2]
        self.csv_read_path = argv[3]
        self.csv_write_path = argv[4]
        # init-others
        self.csv_data = pd.read_pickle(self.csv_read_path)
        # deal-col
        self.satisfied_colnames = self.csv_data.select_dtypes(exclude=['datetime64[ns]','object']).columns.tolist()
    # 决策树回归：用预测值替代噪声  （用c1文件夹中的前6个文件来训练回归模型）
    def denoising_regression(self, col):
        model = joblib.load(self.LOAD_GBRT)
        # 把除待预测列的其他几列列名存入列表中
        self.satisfied_colnames.remove(col)
        pre_list = self.csv_data[self.satisfied_colnames].values[list_noise]
        predictions = model.predict(pre_list)
        # 用predictions覆盖原来的值
        for i, prediction in enumerate(predictions):  # predictions的元素是元组
            self.csv_data[col].values[list_noise[i]] = prediction
        self.csv_data.to_pickle(self.csv_write_path)
        print('noise_after_replace:\n', self.csv_data.loc[list_noise,:])

    # 检测偏离均值三倍标准差的数据，将异常的数据放入list中，待处理
    # 在3∂原则下，异常值如超过3倍标准差，那么可以将其视为异常值。
    def denosisng_mean_std(self, col):
        mean = self.csv_data[col].mean()
        std = self.csv_data[col].std()
        minvalue = mean - 3 * std
        maxvalue = mean + 3 * std
        i=0
        for item in self.csv_data[col]:
            if item<minvalue or item>maxvalue:
                list_noise.append(i)
            i += 1
        print("previous_noise_data:\n ", self.csv_data.loc[list_noise,:])
    def function(self):
        # 去噪
        self.denosisng_mean_std(self.col_name)
        if len(list_noise)!=0:
            self.denoising_regression(self.col_name)
        # others
        # profiler.stop()
        # profiler.print()
        # print(self.csv_data) # debug-use

if __name__=='__main__':
    denoising_regression = Denoising_Regression()
    denoising_regression.function()
    