#以下是回归的模型训练过程，通过此过程生成模型并保存为pkl文件
""" 
python '原版.py'
 """
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from sklearn.ensemble import BaggingRegressor # Bagging回归
from sklearn import tree
from sklearn import ensemble
from sklearn import linear_model
from sklearn import ensemble

dict_title={'1':'X_Force','2':'Y_Force','3':'Z_Force','4':'X_Vibration','5':'Y_Vibration','6':'Z_Vibration','7':'AE_RMS'}# 标题名，如切换文件格式可在这里修改
list_noise=[]
col='4'

if __name__=='__main__':
    csv_train=pd.read_csv(r't_data.csv',header=None, names=['X_Force','Y_Force','Z_Force','X_Vibration','Y_Vibration','Z_Vibration','AE_RMS'])
    #把用于预测未知值的列提取出来作为X，待预测的列作为Y
    list_traning=[]
    len_title=len(dict_title)
    i=1
    while i<=len_title:
        if i!=int(col):
            list_traning.append(dict_title[str(i)])
        i+=1
    #print(list_traning)
    X = csv_train[list_traning]
    Y = csv_train[dict_title[col]] # 除选中的待去噪列，其他列作为预测参考值
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=1)
    model = ensemble.GradientBoostingRegressor(n_estimators=100)
    model.fit(X_train, Y_train)
    joblib.dump(model,'GBRT_model_XVIBRATION.pkl')
    print("ok!")

'''score1=model.score(X,Y)
    X1 = csv_data[list_traning]
    Y1 = csv_data[dict_title[col]]
    score2=model.score(X_test,Y_test)
    #以下代码是为了测试模型预测准确度
    print("R^2 of test, %.2f" % (score1))
    print("R^2 of test, %.2f" % (score2))'''
'''print(linreg.intercept_)
        print(linreg.coef_)'''  # 打印预测方程的参数
'''print(X_test)
    print(csv_data[list_traning])'''

'''    #以下代码通过绘图表示预测准确程度
    import matplotlib.pyplot as plt
    result=model_DecisionTreeRegressor.predict(X1)
    plt.figure()
    plt.plot(np.arange(len(result)), csv_data[dict_title[col]], 'go-', label='true value')
    plt.plot(np.arange(len(result)), result, 'ro-', label='predict value')
    #plt.title('score: %f' % score)
    plt.legend()
    plt.show()'''