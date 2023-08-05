# -*- coding: utf-8 -*-
# @Time     : 2021/4/22 19:13
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : pca.py
# @info     :

import numpy as np
def PCA(dataMat, topNfeat=9999999):
    '''
    :param dataMat: 待压缩的数据矩阵
    :param topNfeat: 压缩后的维度
    :return: 降维后的低维数据，原始数据的重构数据（一般与原始数据不同，有一定的信息损失）
    '''
    meanVals = np.mean(dataMat,axis=0)
    meanRemoved = dataMat - meanVals
    covMat = np.cov(meanRemoved,rowvar=0)
    eigVals, eigVects = np.linalg.eig(np.mat(covMat))
    eigValInd = np.argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:,eigValInd]
    lowDDataMat  = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat,reconMat

def PCA2(X):
    '''
    主成分分析
    :param X: 矩阵X，其中该矩阵中存储训练数据，每一行为一条训练数据
    :return: 投影矩阵（按照维度的重要性排序）、方差和均值
    '''
    # 获取维数
    num_data, dim = X.shape
    # 数据中心化
    mean_X = X.mean(axis=0)
    X = X - mean_X


    if dim > num_data:
        # PCA- 使用紧致技巧
        M = np.dot(X, X.T)  # 协方差矩阵
        e, EV = np.linalg.eigh(M)  # 特征值和特征向量
        tmp = np.dot(X.T, EV).T  # 这就是紧致技巧
        V = tmp[::-1]  # 由于最后的特征向量是我们所需要的，所以需要将其逆转
        S = np.sqrt(e)[::-1]  # 由于特征值是按照递增顺序排列的，所以需要将其逆转
        for i in range(V.shape[1]):
            V[:, i] /= S
    else:
        # PCA- 使用 SVD 方法
        U, S, V = np.linalg.svd(X)
        V = V[:num_data]  # 仅仅返回前 nun_data 维的数据才合理
        # 返回投影矩阵、方差和均值
    return V, S, mean_X
