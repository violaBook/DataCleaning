'''
functions-module[4-3]: 【值】
    EG: firstly cluster, then use mean values to fill the clusters
    中文：先聚类，后对每个聚类类别的数据用其均值填补空值
demonstration:
     you can run like this:
        _____________________________you can run like this____________
    |   python fill3_kmeans_mean.py                                      |____________
    | python fill3_kmeans_mean.py './../new_data.pkl' 'pkl/fill3_kmeans_mean.pkl'                |                                           |
    _______________________________________________________________________________
Date: 
    2021/11/11 15:00
Debug:
    python fill3_kmeans_mean.py './../error_data.pkl' 'pkl/fill3_kmeans_mean.pkl'
    ok
'''
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
from numpy import array, reshape, nan
from pandas.core.frame import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from time import time 
from pandas import concat, read_pickle, Series
from copy import copy
from sys import argv


class Same_Mean_Fill():
    def __init__(self): # 0.3s
        # init-argv
        self.read_file_path = argv[1]
        self.write_file_path = argv[2]
        # init-others
        self.idx_ = []
        # 参数
        self.k = 2  # 聚类类别
        self.b = 500  # 聚类最大循环次数
        # 读数据
        self.csv_data = read_pickle(self.read_file_path)
        print(self.csv_data)
        # 调试的空值插入(debug-use)
        # self.csv_data.iloc[[0,2,3], 0] = nan # debug-use
        # self.csv_data.iloc[[1,2,3,4], 1] = nan # debug-use
        # self.csv_data.iloc[[0,1,2,3,4], 2] = nan # debug-use
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
            self.csv_data.to_pickle(self.write_file_path)
            exit(0)   
        # 初始化策略
        self.strategy = 'mean'     
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
        r = concat(
            [data_zs_tmp, Series(model.labels_, index=self.cluster_data.index)], axis=1)
        r.columns = list(self.cluster_data.columns) + [u'聚类类别']  # 重命名表头
        # 求每个聚类对应下标
        for i in range(k):
            r_ndarray = array(r[u'聚类类别'])
            idx = (r_ndarray == i)
            self.idx_.append(idx)
        return r
        
    # 缺失值填补(按照聚类类别依次处理) 
    def same_mean_fill(self, r, k,  strategy): # 0.81s
        # 初始化, p_tmp_list(★is core★)用于暂存聚类多列赋值的数据
        p_tmp_list = []
        p_tmp = r[u'聚类类别']
        p_tmp = DataFrame(p_tmp)
        for j in range(len(self.nan_columns)):
            p_tmp_list.append(copy(p_tmp))
        # 预测缺失值,返回没有空值列的预测(含所有数据)
        imp_mean = SimpleImputer(missing_values=nan, strategy=strategy)
        for i in range(k):
            # 定位
            data_typei = self.csv_data[self.nan_columns][self.idx_[i]] # data_typei = self.csv_data[self.nan_columns][r[u'聚类类别'] == i] 等价
            # 缺失值插补
            elem = imp_mean.fit_transform(data_typei) # 所有聚类fit后的元素值
            # p_tmp_list的赋值
            elem_T = elem.T
            for j in range(elem.shape[1]):
                x = elem_T[j]
                x_shaped = reshape(x,(len(x),1))
                p_tmp_list[j][self.idx_[i]] = x_shaped
        # 用暂存的p_tmp_list数据赋值给csv_data
        for j in range(len(self.nan_columns)):
            self.csv_data[self.nan_columns[j]]=p_tmp_list[j]
    def function(self): 
        # 同类均值插补实现
        data_zs = self.get_data_zs()
        r = self.KMeansCluster(data_zs, self.k, self.b)
        self.same_mean_fill(r, self.k, self.strategy)
        # 写回数据库
        self.csv_data.to_pickle(self.write_file_path)
        # 其他
        profiler.stop()
        profiler.print()
        # print(self.csv_data) # debug-use

# main
if __name__=='__main__':
    sm_fill = Same_Mean_Fill()
    sm_fill.function()
    
