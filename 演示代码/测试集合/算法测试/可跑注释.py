"""
************************
***  author:Yeller   ***
***  date:2023/03/17 ***
************************
"""
from matplotlib import pyplot as plt
import numpy as np

class AntColony:
    def __init__(self, distances, start_city=0, num_iterations=100, num_ants=10, alpha=1.0, beta=2.0, rho=0.5):
        """
        初始化蚁群算法的参数和距离矩阵
        :param distances: 距离矩阵
        :param start_city: 开始城市，默认为第一个城市
        :param num_iterations: 迭代次数，默认为100
        :param num_ants: 蚂蚁数量，默认为10
        :param alpha: alpha值，用于控制信息素的重要性，默认为1.0
        :param beta: beta值，用于控制距离的重要性，默认为2.0
        :param rho: rho值，用于控制信息素挥发的速度，默认为0.5
        """
        self.distances = distances
        self.start_city = start_city
        self.num_iterations = num_iterations
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

    def run(self):
        # 获取城市数目
        num_cities = self.distances.shape[0]
        # 初始化信息素
        pheromone = np.ones((num_cities, num_cities)) / num_cities
        # 初始化最佳路径距离
        best_distance = np.inf
        # 初始化最佳路径
        best_path = None
        # 用于存储每次迭代的最佳路径距离
        iteration_distances = []
        # 开始迭代
        for it in range(self.num_iterations):
            # 用于存储每只蚂蚁的路径和距离
            paths = []
            # 遍历每只蚂蚁
            for i in range(self.num_ants):
                # 初始化路径，从起点出发
                path = [self.start_city]
                # 初始化未访问的城市集合
                remaining_cities = set(range(num_cities))
                remaining_cities.remove(self.start_city)
                # 当还有未访问的城市时
                while remaining_cities:
                    # 获取当前所在城市
                    city = path[-1]
                    # 计算每个未访问城市的概率，通过信息素和距离的乘积计算概率
                    p = pheromone[city, list(remaining_cities)] ** self.alpha
                    d = self.distances[city, list(remaining_cities)] ** self.beta
                    probs = p / d
                    probs /= probs.sum()
                    # 根据概率选择下一个城市
                    next_city = np.random.choice(list(remaining_cities), p=probs)
                    # 将下一个城市加入路径，从未访问城市中移除
                    path.append(next_city)
                    remaining_cities.remove(next_city)
                # 计算当前路径的距离
                distance = sum(self.distances[path[i], path[i + 1]] for i in range(len(path) - 1))
                # 如果当前路径更优，则更新最佳路径距离和最佳路径
                if distance < best_distance:
                    best_distance = distance
                    best_path = path
                # 将当前路径和距离存入路径列表
                paths.append((path, distance))
            # 更新信息素
            pheromone *= (1 - self.rho)
            for path, distance in paths:
                # 在路径上增加信息素
                for i in range(len(path) - 1):
                    pheromone[path[i], path[i + 1]] += 1.0 / distance
                    pheromone[path[i + 1], path[i]] += 1.0 / distance
            # 存储当前迭代的最佳路径距离
            iteration_distances.append(best_distance)
        # 绘制迭代过程中最佳路径距离的变化
        plt.plot(range(self.num_iterations), iteration_distances)
        plt.show()
        # 获取最佳路径每一步的距离，并输出
        distances_of_best_path = [self.distances[best_path[i], best_path[i + 1]] for i in range(len(best_path) - 1)]
        print("Distances of each step in best path:", distances_of_best_path)
        return best_path, best_distance


distances = np.array([[0, 2, 3, 5], [2, 0, 4, 1], [3, 4, 0, 2], [5, 1, 2, 0]])

aco = AntColony(distances)
best_path, best_distance = aco.run()

# print("start_city:", start_city)
print("Best path:", best_path)
print("Best distance:", best_distance)

