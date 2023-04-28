"""
************************
***  author:Yeller   ***
***  date:2023/04/21 ***
************************
"""
import math
import random
import numpy as np
from lddya.Algorithm import ACO


def charge_and_get_bat_mat(points_list, max_battery, thred):
    tem_energy_list = []

    # 初始化出发点能量和消耗
    points_list[0].battery = 0
    points_list[0].consume = 0
    # 初始化随机生成目标点能量
    for i in range(len(points_list) - 1):
        tem_energy_list.append(random.randint(int(thred * max_battery), int(max_battery * 0.8)))
    # 能量数据注入点类
    for k, point in enumerate(points_list[1::]):
        point.battery = tem_energy_list[k]
    # 生成电量列表
    bat_l = list(map(lambda x: x.battery, points_list))
    # 生成电量矩阵
    bat_mat = np.repeat([bat_l], len(points_list), axis=0)
    # 优化电量矩阵，将左对角线元素替换至0，0元素的位置：半M形状
    np.fill_diagonal(bat_mat, 0)
    return points_list, bat_mat


def get_dis_datas_and_mat(filename):
    """
    @filename: 带有location和distance的文件
    @points_list: 点的列表
    """
    # 根据距离文件的行数读取点的数量:couunt_line = n*(n-1)
    with open(filename, 'r') as f:
        count_line = sum(1 for line in f)
    a = int(math.sqrt(count_line))
    b = count_line // a
    count_point = max(a, b)

    datas = []
    dis_l = []
    # 按顺序读取数据存入列表
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    # 按顺序存入距离列表
    for data in datas:
        dis_l.append(data[2])

    # 建立距离矩阵(含起点)
    dis_mat = np.zeros((count_point, count_point))
    for i in range(count_point):
        for j in range(count_point):
            if i == j:  # 左对角线元素为0
                dis_mat[i][j] = 0
            else:  # 其他元素填入列表中的元素
                if dis_l:
                    dis_mat[i][j] = dis_l.pop(0)
                else:
                    dis_mat[i][j] = 0
    return datas, dis_mat


def ACO_Generate_distance(bar_data_file, points_list, newtxt='distance.txt', write=True):  # 获取单个目标点到所有点的   最短距离集合
    points = list(map(lambda x: x.location, points_list))
    datas = []
    for point in points:
        tem = points.copy()  # 新分配内存区域
        tem.remove(point)
        for goal_point in tem:
            aco = ACO(map_data=bar_data_file, start=point, end=goal_point, ant_num=int(1.5 * len(points_list)))
            aco.run()
            datas.append([point, goal_point, aco.way_len_best, aco.way_data_best])

    print(newtxt, '程序执行完毕')
    if write:
        with open(newtxt, mode='w') as f:
            # path_data依次为，起点，终点，路径长度，路径列表
            for data in datas:
                f.writelines(str(data) + '\n')
    else:
        return datas


class Map:
    def __init__(self, fp: str) -> None:
        self.data = self.load_map_file(fp)

    @classmethod
    def load_map_file(self, fp: str) -> np.ndarray:
        """
        从map文件中读取地图数据
        """
        with open(fp, 'r') as f:
            data = [list(line.strip('\n')) for line in f.readlines()]
        return np.array(data, dtype=np.int64)
