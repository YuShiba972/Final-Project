"""
************************
***  author:Yeller   ***
***  date:2023/03/08 ***
************************
"""

import numpy as np

cities = [[0, 0], [16, 10], [4, 9], [10, 11]]  # 城市坐标矩阵

def read_path_map(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    return datas


def get_disl(lst, n):
    for i in range(n):
        for j in range(n):
            if i == j:  # 左对角线元素为0
                arr[i][j] = 0
            else:  # 其他元素填入列表中的元素
                if lst:
                    arr[i][j] = lst.pop(0)
                else:
                    arr[i][j] = 0
    return arr


x = read_path_map('mapss.txt')

dis_l = []
for i in x:
    dis_l.append(i[2])
print(dis_l)

n = len(cities)
arr = np.zeros((n, n))

dis = get_disl(dis_l, 4)
print(dis)
