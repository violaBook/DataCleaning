'''
functions-module[5-2]: 【值】
    EG: cluster by the float-number-col-values, find the discrete point and delete it.
    中文: 对所有数字列聚类分析，找出离群点并删除离群点
argv params:
    none
demonstration:
     _____________________________you can run like this__________________________
    |   python Denosing_SubBox.py                                               |
    |  python denoising2_cluster.py './../t_data.pkl' 'pkl/Denoising2_cluster.pkl' |
    ___________________________________________________________________________
Date: 
    2021/10/31 15:57
'''
# 聚类程序无需输入参数，会直接对除时间信息的所有列进行聚类分析，识别出离群点，然后将它们删除

from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
from time import time
from pandas import concat, read_pickle, Series, DataFrame
from sys import argv
from re import match
from sklearn.cluster import KMeans
# from functools import reduce
# from numpy import mod, vectorize
# import numpy as np
from numpy import array, sqrt, sum, square, reshape, median

class Denoising_Cluster():
    def __init__(self):
        # init-argv
        self.pickle_read_path = argv[1]
        self.pickle_write_path = argv[2]
        # 参数
        self.threshold = 2  # 离散点阈值
        self.k = 2  # 聚类类别
        self.b = 500  # 聚类最大循环次数
        # read-pickle
        self.pickle_data = read_pickle(self.pickle_read_path)
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
        r = concat(
            [data_zs_temp, Series(model.labels_, index=self.cluster_data.index)], axis=1)
        # 每个样本对应的类别
        r.columns = list(self.cluster_data.columns) + [u'聚类类别']  # 重命名表头
        for i in range(k):
            r_ndarray = array(r[u'聚类类别'])
            idx = (r_ndarray == i)
            self.idx_.append(idx)
        return model, r
    def make_norm(self, model, k, r):
        norm = []
        # p_tmp用于最后赋值
        p_tmp = r.loc[:, u'聚类类别']
        p_tmp = DataFrame(p_tmp)
        for i in range(k):
            data = r[self.columns][r[u'聚类类别'] == i].values
            # 初始化
            row_center = model.cluster_centers_[i] 
            data = r[self.columns][r[u'聚类类别'] == i]
            # 计算距离,转化为相对距离
            norm_tmp = data - row_center  # step1:计算到中心点的距离(得矩阵)
            norm_tmp_np = norm_tmp.values
            norm_tmp_dist = sqrt(sum(square(norm_tmp_np),axis=1))
            elem = norm_tmp_dist / median(norm_tmp_dist)
            # 重塑形状,赋值
            elem_reshape = reshape(elem,(len(elem),1))
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
        # 数据写回文件
        new_data.to_pickle(self.pickle_write_path)
        # 打印时间
        profiler.stop()
        profiler.print()
        # print(self.pickle_data) # debug-use

if __name__=='__main__':
    denoising_cluster = Denoising_Cluster()
    denoising_cluster.function()
    