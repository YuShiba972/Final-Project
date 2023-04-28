"""
************************
***  author:Yeller   ***
***  date:2023/03/19 ***
************************
"""
import copy
import math
import random

import numpy as np
from lddya.Algorithm import ACO
from lddya.Draw import ShanGeTu
from PIL import Image


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

    @staticmethod
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


class Point:
    def __init__(self, name='', location=None, battery=0, consume=0,
                 max_battery=10800, threshold=0.2, velocity=1):
        self.name = name
        self.location = location
        self.battery = battery

        self.max_battery = max_battery
        self.consume = consume
        self.threshold = threshold
        self.velocity = velocity

    @staticmethod
    def charge_and_get_bat_mat(points_list, max_battery=10800, consume=200, thred=0.2):
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

    @staticmethod
    def points15_bar10():
        A = Point(name='A', location=[0, 0])
        B = Point(name='B', location=[14, 11])
        C = Point(name='C', location=[6, 14])
        D = Point(name='D', location=[1, 18])
        E = Point(name='E', location=[7, 12])
        F = Point(name='F', location=[5, 4])
        G = Point(name='G', location=[12, 2])
        H = Point(name='H', location=[11, 12])
        I = Point(name='I', location=[19, 4])
        J = Point(name='J', location=[4, 5])
        K = Point(name='K', location=[16, 11])
        L = Point(name='L', location=[15, 6])
        M = Point(name='M', location=[16, 18])
        N = Point(name='N', location=[16, 5])
        O = Point(name='O', location=[3, 19])
        points_list = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O]
        return points_list

    @staticmethod
    def points5_bar10():
        A = Point(name='A', location=[0, 0])
        B = Point(name='B', location=[14, 11])
        C = Point(name='C', location=[6, 14])
        D = Point(name='D', location=[1, 18])
        E = Point(name='E', location=[7, 12])
        points_list = [A, B, C, D, E]
        return points_list

    @staticmethod
    def points6_bar10():
        A = Point(name='A', location=[0, 0])
        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[19, 2])
        D = Point(name='D', location=[8, 4])
        E = Point(name='E', location=[4, 8])
        F = Point(name='F', location=[15, 15])
        points_list = [A, B, C, D, E, F]
        return points_list

    @staticmethod
    def points_ori():
        A = Point(name='A', location=[0, 0])
        B = Point(name='B', location=[4, 9])
        C = Point(name='C', location=[16, 10])
        D = Point(name='D', location=[10, 11])
        E = Point(name='E', location=[7, 5])
        F = Point(name='F', location=[8, 8])
        G = Point(name='F', location=[9, 12])
        points_list = [A, B, C, D, E, F, G]
        return points_list


def draw_map(points, bar_data_file):
    location_l = [x.location for x in points]
    # print(location_l)
    m = Map(bar_data_file)
    m.load_map_file(bar_data_file)
    result_figure = ShanGeTu(m.data)

    # blank = result_figure.white_BG()  # 空白背景
    shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=shangetu)  # 修改Surface参数以修改背景
    shangetu_bar_goal = result_figure.goal_point(location_l, Surface=shangetu_bar)  # 画目标点
    result_figure.save(Surface=shangetu_bar_goal, filename='map.jpg')

    # image = Image.open('map.jpg')  # 打开图像文件
    # image.show()  # 显示图像


def ACO_Generate_distance(bar_data_file, points_list, newtxt='distance.txt', write=True):  # 获取单个目标点到所有点的   最短距离集合
    # bar_data_file
    points = list(map(lambda x: x.location, points_list))
    datas = []
    for point in points:
        tem = points.copy()  # 新分配内存区域
        tem.remove(point)
        for goal_point in tem:
            aco = ACO(map_data=bar_data_file, start=point, end=goal_point)
            aco.run()
            datas.append([point, goal_point, aco.way_len_best, aco.way_data_best])

    if write:
        with open(newtxt, mode='w') as f:
            # path_data依次为，起点，终点，路径长度，路径列表
            for data in datas:
                f.writelines(str(data) + '\n')
    else:
        return datas


def generate_points(filename, n=5):
    # 从文件中读取矩阵
    with open(filename, 'r') as f:
        matrix = [list(line.strip()) for line in f.readlines()]
    rows, cols = len(matrix), len(matrix[0])
    # 获取矩阵中非1元素的索引
    indices = [(i, j) for i in range(rows) for j in range(cols) if matrix[i][j] != '1']
    # 从索引中生成n个唯一坐标
    coordinates = random.sample(indices, n)
    # 按字典顺序对坐标进行排序
    coordinates[0] = (0, 0)
    # coordinates = sorted(coordinates)
    # 创建Point实例
    points = []
    for i, coord in enumerate(coordinates):
        if i == 0:
            name = 'A'
        else:
            name = chr(ord('A') + i)
        points.append(Point(name=name, location=list(coord)))

    print("生成的Point实例:")
    for point in points:
        print(f"名称: {point.name}, 坐标: {point.location}")

    # 检查生成的坐标是否与矩阵中的1元素冲突
    conflicts = [coord for coord in coordinates if matrix[coord[0]][coord[1]] == '1']
    if conflicts:
        print("与矩阵中的1元素冲突:")
        for conflict in conflicts:
            print(conflict)
    else:
        print("随机生成的目标点不在禁行区内.")
    return points


# def get_heu_mat(bat_mat, dis_mat):
#     dis_mat[dis_mat == 0] = 1
#     heu_mat = bat_mat / dis_mat
#     return heu_mat

