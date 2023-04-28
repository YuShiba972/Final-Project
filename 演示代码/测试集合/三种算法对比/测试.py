"""
************************
***  author:Yeller   ***
***  date:2023/03/01 ***
************************
"""
import numpy as np
from matplotlib import pyplot as plt


def proc(dataMat, dimension):  # 输入参数为原始数据矩阵以及其相应的维度
    # 数据中心化处理
    meanVal = np.mean(dataMat, axis=0)
    newData = dataMat - meanVal
    # cov用于求协方差矩阵，参数rowvar = 0说明数据一行代表一个样本
    covMat = np.cov(newData, rowvar=bool(0))
    # np.linalg.eig用于求矩阵的特征值和特征向量
    eigVals, eigVects = np.linalg.eig(np.mat(covMat))
    # 对特征值从小到大排列
    eigValIndice = np.argsort(eigVals)
    # 得到最大的n个特征值的下标
    n_eigValIndice = eigValIndice[-1:-(dimension + 1): -1]
    # 得到下标对应的特征向量
    n_eigVects = eigVects[:, n_eigValIndice]
    # 低维特征空间的数据
    lowDDataMat = newData * n_eigVects
    return lowDDataMat


if __name__ == "__main__":
    # origin_energy = [1000, 1000, 1000, 8000, 9000, 10000]
    # dis = [1, 2, 3, 8, 9, 10]
    origin_energy = [1000, 1000, 1000, 8000, 9000, 10000]
    dis = [1, 2, 3, 3, 2, 1]
    consume = [500, 500, 500, 500, 500, 500, 500]
    label = [0, 0, 0, 1, 1, 1]
    l = list(zip(origin_energy, dis, consume))
    high_data = np.array(l)
    # print(high_data)
    lowDDataMat = proc(high_data, 2)

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    x = []
    y = []
    for i in range(len(lowDDataMat)):
        x.append(lowDDataMat[i, 0])
        y.append(lowDDataMat[i, 1])
    print(x)
    print(y)

    colors = ['red', 'yellow', 'blue']  # 设置颜色
    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    # for i in range(3):
    #     plt.scatter(c='blue')
    plt.plot(x[0:3], y[0:3], 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(x[3:6], y[3:6], 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示图例
    plt.title('PCA降维后的二维鸢尾花数据集')  # 显示标题
    plt.show()  # 显示散点图
