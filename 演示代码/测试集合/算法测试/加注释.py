"""
************************
***  author:Yeller   ***
***  date:2023/03/11 ***
************************
"""
import numpy as np
import matplotlib.pyplot as plt


# 蚂蚁算法类
class AntColonyTSP:
    # 初始化方法，传入距离矩阵，起点，迭代次数，蚂蚁数量，信息素因子alpha，距离因子beta，信息素衰减系数rho
    def __init__(self, distances, start_city, num_iterations=100, num_ants=10, alpha=1.0, beta=2.0, rho=0.5):
        self.distances = distances  # 距离矩阵
        self.start_city = start_city  # 起点
        self.num_iterations = num_iterations  # 迭代次数
        self.num_ants = num_ants  # 蚂蚁数量
        self.alpha = alpha  # 信息素因子
        self.beta = beta  # 距离因子
        self.rho = rho  # 信息素衰减系数

    # 运行蚂蚁算法
    def run(self):
        num_cities = self.distances.shape[0]  # 城市数量
        pheromone = np.ones((num_cities, num_cities)) / num_cities  # 初始化信息素矩阵
        best_distance = np.inf  # 最优路径的距离
        best_path = None  # 最优路径
        iteration_distances = []  # 每次迭代的最优距离列表
        for it in range(self.num_iterations):  # 迭代
            paths = []  # 蚂蚁路径列表
            for i in range(self.num_ants):  # 蚂蚁搜索路径
                path = [self.start_city]  # 初始路径为起点
                remaining_cities = set(range(num_cities))  # 未访问城市集合
                remaining_cities.remove(self.start_city)  # 从未访问城市集合中删除起点
                while remaining_cities:  # 未访问城市集合不为空
                    city = path[-1]  # 当前城市为路径的最后一个城市
                    # 计算选择下一个城市的概率
                    p = pheromone[city, list(remaining_cities)] ** self.alpha
                    d = self.distances[city, list(remaining_cities)] ** self.beta
                    probs = p / d
                    probs /= probs.sum()
                    # 根据概率随机选择下一个城市
                    next_city = np.random.choice(list(remaining_cities), p=probs)
                    path.append(next_city)  # 添加选择的城市到路径中
                    remaining_cities.remove(next_city)  # 从未访问城市集合中删除已选择的城市
                    # 计算蚂蚁的路径距离
                    for ant in ants:
                        ant_distance = 0  # 初始化蚂蚁的路径距离为0
                        for i in range(num_cities - 1):  # 遍历所有城市，计算蚂蚁经过的路径距离
                            from_city = ant.path[i]  # 蚂蚁从哪个城市出发
                            to_city = ant.path[i + 1]  # 蚂蚁要到达哪个城市
                            ant_distance += distances[from_city][to_city]  # 计算蚂蚁从from_city到to_city的距离
                        # 加上从最后一个城市回到起点的距离
                        from_city = ant.path[-1]
                        to_city = ant.path[0]
                        ant_distance += distances[from_city][to_city]
                        ant.total_distance = ant_distance  # 保存蚂蚁的路径距离

                    # 更新全局最优解和最优路径
                    for ant in ants:
                        if ant.total_distance < best_distance:  # 若蚂蚁的路径距离优于全局最优解
                            best_distance = ant.total_distance  # 更新全局最优解
                            best_path = ant.path[:]  # 更新最优路径
                    # 根据蚂蚁的路径距离和信息素更新信息素
                    for i in range(num_cities - 1):
                        for j in range(i + 1, num_cities):
                            pheromone = 0
                            # 计算当前路径被所有蚂蚁经过的总距离的倒数
                            for ant in ants:
                                if (ant.path[i] == i and ant.path[j] == j) or (ant.path[j] == i and ant.path[i] == j):
                                    pheromone += Q / ant.total_distance
