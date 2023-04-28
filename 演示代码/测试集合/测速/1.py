"""
************************
***  author:Yeller   ***
***  date:2023/04/04 ***
************************
"""


class Point:
    def __init__(self, name, location, battery, consume,
                 max_battery, threshold, velocity):
        self.name = name
        self.location = location
        self.battery = battery

        self.max_battery = max_battery
        self.consume = consume
        self.threshold = threshold
        self.velocity = velocity

import random

import numpy as np
from scipy.spatial.distance import squareform, pdist


class AntColonyOptimization:
    def __init__(self, distance_matrix, num_ants=10, alpha=1.0, beta=2.0, rho=0.5, q=100, initial_pheromone=0.1):
        """
        初始化函数
        distance_matrix: 城市之间的距离矩阵
        num_ants: 蚂蚁数量，默认为10只
        alpha: 表示信息素启发因子，默认为1.0
        beta: 表示距离启发因子，默认为2.0
        rho: 表示信息素挥发速度，默认为0.5
        q: 表示信息素增加强度系数，默认为100
        initial_pheromone: 表示初始化信息素量，默认为0.1
        """
        self.distance_matrix = distance_matrix
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.initial_pheromone = initial_pheromone

    def _update_pheromone(self, pheromone_matrix, ant_routes, best_route):
        """
        更新信息素矩阵
        pheromone_matrix: 当前的信息素矩阵
        ant_routes: 所有蚂蚁访问过的路径列表
        best_route: 最优路径的蚂蚁编号
        """
        for i in range(len(pheromone_matrix)):
            for j in range(i + 1, len(pheromone_matrix)):
                # 挥发信息素
                pheromone_matrix[i][j] *= (1 - self.rho)
                pheromone_matrix[j][i] = pheromone_matrix[i][j]

                if i in ant_routes[best_route] and j in ant_routes[best_route]:
                    # 更新信息素，加上最优路径上经过的信息素
                    pheromone_matrix[i][j] += self.q / self.distance_matrix[i][j]
                    pheromone_matrix[j][i] = pheromone_matrix[i][j]

                # 信息素量下限
                if pheromone_matrix[i][j] < self.initial_pheromone:
                    pheromone_matrix[i][j] = self.initial_pheromone
                    pheromone_matrix[j][i] = self.initial_pheromone

        return pheromone_matrix

    def _choose_next_city(self, pheromone_matrix, current_city, tabu_list):
        """
        选择下一个要访问的城市
        pheromone_matrix: 当前的信息素矩阵
        current_city: 当前所在的城市编号
        tabu_list: 已经访问过的城市列表
        """
        prob = [0 for i in range(len(pheromone_matrix))]
        total_prob = 0.0
        for i in range(len(prob)):
            if i == current_city or i in tabu_list:
                continue
            prob[i] = pow(pheromone_matrix[current_city][i], self.alpha) * pow(
                1 / self.distance_matrix[current_city][i], self.beta)
            total_prob += prob[i]
        if total_prob == 0:
            return -1
        rand_prob = random.uniform(0, total_prob)
        temp_prob = 0.0
        for i in range(len(prob)):
            if i == current_city or i in tabu_list:
                continue
            temp_prob += prob[i]
            if temp_prob >= rand_prob:
                return i

    def run(self, start_city=0, max_iteration=100):
        """
        蚁群算法主函数
        start_city: 起始城市编号，默认为0
        max_iteration: 最大迭代次数，默认为100
        """
        # 初始化信息素矩阵
        pheromone_matrix = [[self.initial_pheromone for j in range(len(self.distance_matrix))] for i in
                            range(len(self.distance_matrix))]

        best_route = []  # 最优路径
        best_distance = float("inf")  # 最优路径长度

        for iteration in range(max_iteration):
            ant_routes = []  # 所有蚂蚁的路径列表
            ant_distances = []  # 所有蚂蚁对应的路径长度列表

            # 蚂蚁寻路
            for ant in range(self.num_ants):
                tabu_list = [start_city]  # 禁忌城市列表
                path_distance = 0.0  # 当前蚂蚁经过的路径长度
                for i in range(len(self.distance_matrix) - 1):
                    next_city = self._choose_next_city(pheromone_matrix, tabu_list[-1], tabu_list)
                    if next_city == -1:
                        break
                    tabu_list.append(next_city)
                    path_distance += self.distance_matrix[tabu_list[-2]][next_city]
                ant_routes.append(tabu_list)
                ant_distances.append(path_distance)

            # 获取最优路径蚂蚁的编号
            best_ant_index = ant_distances.index(min(ant_distances))
            if ant_distances[best_ant_index] < best_distance:
                best_distance = ant_distances[best_ant_index]
                best_route = ant_routes[best_ant_index]

            # 更新信息素矩阵
            pheromone_matrix = self._update_pheromone(pheromone_matrix, ant_routes, best_ant_index)

        return best_route, best_distance


import matplotlib.pyplot as plt


def draw_ant_path(points, ant_path, title):
    """
    绘制蚂蚁迭代过程路径图
    :param points: 各城市坐标点
    :param ant_path: 蚂蚁迭代过程中产生的路径
    :param title: 图像标题
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # 绘制各城市坐标点
    xs = [i[0] for i in points]
    ys = [i[1] for i in points]
    ax.scatter(xs, ys)

    # 绘制蚂蚁路径
    for j in range(1, len(ant_path)):
        city_i = ant_path[j - 1]
        city_j = ant_path[j]
        x = [points[city_i][0], points[city_j][0]]
        y = [points[city_i][1], points[city_j][1]]
        ax.plot(x, y, 'r')

    # 添加标题和坐标轴标签
    plt.rcParams['text.usetex'] = True  # 启用LaTeX渲染器
    plt.rcParams['font.family'] = ['SimHei']
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()


# # 初始化距离矩阵
# distance_matrix = [
#     [0, 4, 2, 5],
#     [4, 0, 1, 3],
#     [2, 1, 0, 2],
#     [5, 3, 2, 0]
# ]

coords = np.array([[39.9042, 116.4074],  # 北京的经度和纬度
                   [31.2304, 121.4737],  # 上海的经度和纬度
                   [23.1291, 113.2644],  # 广州的经度和纬度
                   [22.5431, 114.0579]])  # 深圳的经度和纬度
dist_mat = squareform(pdist(coords, metric='euclidean'))
print(dist_mat)

# 初始化蚁群算法对象
aco = AntColonyOptimization(dist_mat)

# 执行蚁群算法
best_route, best_distance = aco.run(start_city=0)
draw_ant_path(coords, best_route, 'ite')

# 输出结果
print("Best route:", best_route)
print("Best distance:", best_distance)
