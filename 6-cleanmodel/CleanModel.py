""" 【值】
    ------------------------------------------------------------------------------
    python CleanModel.py  common mean subbox 'X_Force' './../new_data.pkl' 'pkl/CleanModel.pkl'
    ------------------------------------------------------------------------------
    参数1：【a用于~缺失值填补~】        common为均值/中位数插补,advanced为同类均值/中位数插补
        'common'/'advanced'
    参数2：【a用于~缺失值填补~】        mean为均值插补,median为中位数插补
        'mean'/'median'        
    ------------------------------------------------------------------------------
    参数3：【b用于~数据去噪~】          subbox为分箱去噪,cluster为聚类去噪
        'subbox'/'cluster'      
    参数4：【b用于~数据去噪~】          略
        列名
    ------------------------------------------------------------------------------
    参数5：【c设置路径】                略
        读文件路径 
    参数6：【c设置路径】                略
        写文件路径
    ------------------------------------------------------------------------------
"""
from os import read
from numpy.lib.function_base import median
import pandas as pd # data-addressing
import numpy as np
from pandas.io.pytables import SeriesFixed
from sklearn.impute import SimpleImputer # sklearn
from time import time # others
from re import match
import sys
from sklearn.cluster import KMeans
from copy import copy

from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

class Mean_fill():
    def __init__(self, csv_data, strategy1):
        # read-csv
        self.csv_data = csv_data
        self.satisfied_colnames = self.csv_data.select_dtypes(exclude=['datetime64[ns]','object']).columns.tolist()
        self.strategy = strategy1 
    # mean-fill
    def mean_fill(self, cols, strategy):
        # 初始化
        data_ndarray = self.csv_data[cols].values
        # 使用模型
        imp_mean = SimpleImputer(missing_values=np.nan, strategy=strategy)
        # imp_mean.fit(data_ndarray)
        self.csv_data[cols] = imp_mean.fit_transform(data_ndarray)
    def function(self):
        # del_datetime&str
        numeric_example = ['float', 'int'] # 数值类型
        datetime_example = ['datetime64', 'datetime'] # 日期类型
        str_example = ['object'] # 文本类型
        # do-datainvalidation
        # self.csv_data.iloc[0:5, 1] = np.nan # debug-use
        self.mean_fill(cols=self.satisfied_colnames, strategy=self.strategy)
        return self.csv_data
class Same_Mean_Fill():
    def __init__(self, csv_data, strategy1): # 0.3s
        # init-others
        self.idx_ = []
        # 参数
        self.k = 2  # 聚类类别
        self.b = 500  # 聚类最大循环次数
        # 读数据
        self.csv_data = csv_data
        # 调试的空值插入(debug-use)
        self.csv_data.iloc[[0,2,3], 0] = np.nan # debug-use
        self.csv_data.iloc[[1,2,3,4], 1] = np.nan # debug-use
        self.csv_data.iloc[[0,1,2,3,4], 2] = np.nan # debug-use
        # 获取数值列 [numerical_colnames]
        self.numerical_colnames = self.csv_data.select_dtypes(exclude=['datetime64[ns]','object']).columns.tolist()
        self.cluster_data = self.csv_data[self.numerical_colnames]  # 数值列(all)
        # 获取用于聚类数据(非空数值列)[cluster_data]
        self.cluster_data = self.cluster_data.loc[:, ~self.cluster_data.isna().any(axis=0)] # 无空值列(all)
        del_columns = self.cluster_data.columns.tolist() # 无空值列名
        # 获取空值列 [nan_columns]
        self.nan_columns = [x for x in self.numerical_colnames] # 复制数值列
        for del_ in del_columns: 
            self.nan_columns.remove(del_) # 处理完后只剩下空值列,因为nan_columns将数值型列中所有没有空值的剔除
        if len(self.nan_columns) == 0:
            print('congratulations, no nan at all! exit!')
            exit(0)   
        # 初始化策略
        self.strategy = strategy1    
    def get_data_zs(self): # 0.09s
        data_zs = 1.0 * (self.cluster_data - self.cluster_data.mean()) / self.cluster_data.std()  # 数据标准化
        return data_zs
    # KMeans聚类,返回预测值
    def KMeansCluster(self, data_zs, k, b): # 0.83s
        # 预处理后数据数据
        data_zs_tmp = data_zs
        # 预测
        data_nonan_ndarray = self.cluster_data.values
        model = KMeans(n_clusters=k, max_iter=b)
        model.fit_predict(data_nonan_ndarray)
        # 增加一列'聚类类别',构成新dataframe:r
        r = pd.concat(
            [data_zs_tmp, pd.Series(model.labels_, index=self.cluster_data.index)], axis=1)
        r.columns = list(self.cluster_data.columns) + [u'聚类类别']  # 重命名表头
        # 求每个聚类对应下标
        for i in range(k):
            r_ndarray = np.array(r[u'聚类类别'])
            idx = (r_ndarray == i)
            self.idx_.append(idx)
        return r
        
    # 缺失值填补(按照聚类类别依次处理) 
    def same_mean_fill(self, r, k,  strategy): # 0.81s
        # 初始化, p_tmp_list(★is core★)用于暂存聚类多列赋值的数据
        p_tmp_list = []
        p_tmp = r[u'聚类类别']
        p_tmp = pd.DataFrame(p_tmp)
        for j in range(len(self.nan_columns)):
            p_tmp_list.append(copy(p_tmp))
        # 预测缺失值,返回没有空值列的预测(含所有数据)
        imp_mean = SimpleImputer(missing_values=np.nan, strategy=strategy)
        for i in range(k):
            # 定位
            data_typei = self.csv_data[self.nan_columns][self.idx_[i]] # data_typei = self.csv_data[self.nan_columns][r[u'聚类类别'] == i] 等价
            # 缺失值插补
            elem = imp_mean.fit_transform(data_typei) # 所有聚类fit后的元素值
            # p_tmp_list的赋值
            elem_T = elem.T
            for j in range(elem.shape[1]):
                x = elem_T[j]
                x_shaped = np.reshape(x,(len(x),1))
                p_tmp_list[j][self.idx_[i]] = x_shaped
        # 用暂存的p_tmp_list数据赋值给csv_data
        for j in range(len(self.nan_columns)):
            self.csv_data[self.nan_columns[j]]=p_tmp_list[j]
    def function(self): 
        # 同类均值插补实现
        data_zs = self.get_data_zs()
        r = self.KMeansCluster(data_zs, self.k, self.b)
        self.same_mean_fill(r, self.k, self.strategy)
        return self.csv_data 
class Denoising_SubBox():
    def __init__(self, csv_data, col):
        # init-argv
        self.col= col
        # init-others
        self.csv_data = csv_data
    def denoising_subbox(self, col):
        # 初始化
        box_num=5
        csv_data_col_ndarray = self.csv_data.loc[:, col].values
        csv_data_col_ndarray = csv_data_col_ndarray.astype(np.float64)
        # 使用模型
        box, bins=pd.cut(csv_data_col_ndarray, bins=box_num, retbins=True)
        time1 = time()
        # 将所有分箱类别存入一个列表中
        for i in range(len(bins)-1):
            # 获取每个分箱的索引
            idx = (csv_data_col_ndarray >= bins[i]) & (csv_data_col_ndarray <= bins[i+1])
            # 对每个分箱的索引求均值
            csv_data_col_ndarray[idx] = np.mean(csv_data_col_ndarray[idx])
        # 赋值csv_data
        self.csv_data[col] = csv_data_col_ndarray
        return self.csv_data
    def function(self):
        # do-function
        csv_data = self.denoising_subbox(self.col)
        return csv_data
class Denoising_Cluster():
    def __init__(self, pickle_data, col):
        # 参数
        self.threshold = 2  # 离散点阈值
        self.k = 2  # 聚类类别
        self.b = 500  # 聚类最大循环次数
        # read-pickle
        self.pickle_data = pickle_data
        self.columns = self.pickle_data.columns.tolist()
        # self.columns为数值类型且不存在空的列名
        type_list = self.pickle_data.dtypes.astype(str).tolist()
        type_del = ['datetime', 'object']
        del_list = []
        for i, type_ in enumerate(type_list):
            for type_d in type_del:
                if match(type_d, type_) != None:
                    del_list.append(self.columns[i])
        for del_ in del_list:
            self.columns.remove(del_)
        # 每个聚类的idx_列表
        self.idx_ = []
        self.cluster_data = self.pickle_data[self.columns]
        # others
        self.list_discrete_list = []
        self.list_discrete_all = []
    # 聚类：通过聚类识别噪声点（k-means） 根据所有列的数据信息对数据点进行聚类，检测出离群点后删除
    def get_data_zs(self):
        data_zs = 1.0 * (self.cluster_data - self.cluster_data.mean()) / self.cluster_data.std()  # 数据标准化
        # data_zs = pickle_data
        return data_zs
    def model_data_zs(self, data_zs, k, b):
        '以下部分是肘部法则确定聚类数的代码，最后确定为k=2'
        '''SSE=[]
        for k in range(1,9):
            model = KMeans(n_clusters=k, n_jobs=4, max_iter=b)
            y_pred = model.fit(data_zs)
            print(k,":")
            print(model.inertia_)
            SSE.append(model.inertia_)
        X = range(1, 9)
        plt.xlabel('k')
        plt.ylabel('SSE')
        plt.plot(X, SSE, 'o-')
        plt.show()'''
        data_zs_temp = data_zs
        model = KMeans(n_clusters=k, max_iter=b)
        model.fit(data_zs_temp)
        # 标准化数据及其类别
        r = pd.concat(
            [data_zs_temp, pd.Series(model.labels_, index=self.cluster_data.index)], axis=1)
        # 每个样本对应的类别
        r.columns = list(self.cluster_data.columns) + [u'聚类类别']  # 重命名表头
        for i in range(k):
            r_ndarray = np.array(r[u'聚类类别'])
            idx = (r_ndarray == i)
            self.idx_.append(idx)
        return model, r
    def make_norm(self, model, k, r):
        norm = []
        # p_tmp用于最后赋值
        p_tmp = r.loc[:, u'聚类类别']
        p_tmp = pd.DataFrame(p_tmp)
        for i in range(k):
            data = r[self.columns][r[u'聚类类别'] == i].values
            # 初始化
            row_center = model.cluster_centers_[i] 
            data = r[self.columns][r[u'聚类类别'] == i]
            # 计算距离,转化为相对距离
            norm_tmp = data - row_center  # step1:计算到中心点的距离(得矩阵)
            norm_tmp_np = norm_tmp.values
            norm_tmp_dist = np.sqrt(np.sum(np.square(norm_tmp_np),axis=1))
            elem = norm_tmp_dist / np.median(norm_tmp_dist)
            # 重塑形状,赋值
            elem_reshape = np.reshape(elem,(len(elem),1))
            p_tmp[self.idx_[i]] = elem_reshape
        return p_tmp
    def find_descrete_point(self, norm, threshold):
        idx = (norm > threshold)
        discrete_points = norm[idx]
        # print('discrete_point: ', discrete_points)
        flag = 0
        noise_index = ~discrete_points.isna().any(axis=1)
        return noise_index
    def do_main(self, data_zs,  k , b, threshold):
        model_, r_ = self.model_data_zs(data_zs, k, b) # 建模 # 0.4s
        norm_ = self.make_norm(model_, k, r_) # 计算各点到簇中心的距离 # 4.9s
        list_discrete_ = self.find_descrete_point(norm_,threshold) # 找出离群点 # 0.15s
        return self.pickle_data.loc[~list_discrete_, :]
    def function(self):
        # 初始化
        threshold = self.threshold
        k = self.k
        b = self.b
        threads = []
        # 执行聚类去噪
        data_zs = self.get_data_zs()       
        new_data = self.do_main(data_zs,  k , b, threshold)
        return new_data
    


if __name__ == "__main__":
    #--------------------------------------------------
    # 初始化-缺失值插补
    choice1 = sys.argv[1] # input 'common' or 'advanced'
    strategy1 = sys.argv[2] # input 'mean' or 'median'
    # 初始化-数据去噪
    choice2 = sys.argv[3]
    col = sys.argv[4]
    # 初始化-文件读写源
    read_file_path = sys.argv[5]
    write_file_path = sys.argv[6]
    # 初始化-读数据库
    csv_data = pd.read_pickle(read_file_path)
    #--------------------------------------------------
    # step1: 缺失值插补
    if choice1 == "advanced":
        same_mean_fill = Same_Mean_Fill(csv_data, 'mean')
        new_data1 = same_mean_fill.function()
    else:
        mean_fill = Mean_fill(csv_data, 'mean')
        new_data1 = mean_fill.function()
    print(new_data1)
    #--------------------------------------------------
    # step2: 数据去噪
    if choice2 == 'subbox':
        subbox_denoising = Denoising_SubBox(csv_data, col)
        new_data2 = subbox_denoising.function()
    else:
        cluster_denoising = Denoising_Cluster(csv_data, col)
        new_data2 = cluster_denoising.function()
    print(new_data2)
    #--------------------------------------------------
    # 收尾化-写数据库
    new_data2.to_pickle(write_file_path)