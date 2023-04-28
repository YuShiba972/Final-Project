"""
************************
***  author:Yeller   ***
***  date:2023/03/11 ***
************************
"""
import numpy as np  # 导入numpy模块，用于矩阵计算
import matplotlib.pyplot as plt  # 导入matplotlib模块，用于可视化


class AntColonyTSP:  # 定义AntColonyTSP类
    def __init__(self, distances, start_city, num_iterations=100, num_ants=10, alpha=1.0, beta=2.0, rho=0.5):
        # 初始化函数，接收距离矩阵，起始城市，迭代次数，蚂蚁数量，alpha和beta参数，以及信息素挥发因子rho
        self.distances = distances  # 初始化距离矩阵
        self.start_city = start_city  # 初始化起始城市
        self.num_iterations = num_iterations  # 初始化迭代次数
        self.num_ants = num_ants  # 初始化蚂蚁数量
        self.alpha = alpha  # 初始化alpha参数
        self.beta = beta  # 初始化beta参数
        self.rho = rho  # 初始化信息素挥发因子rho

    def run(self):  # 定义run函数，执行蚁群算法
        num_cities = self.distances.shape[0]  # 获取城市数量
        pheromone = np.ones((num_cities, num_cities)) / num_cities  # 初始化信息素矩阵
        best_distance = np.inf  # 初始化最短路径距离为无穷大
        best_path = None  # 初始化最短路径为None
        iteration_distances = []  # 初始化每次迭代的最短距离列表
        for it in range(self.num_iterations):  # 迭代num_iterations次
            paths = []  # 初始化路径列表
            for i in range(self.num_ants):  # 对于每只蚂蚁
                path = [self.start_city]  # 初始化路径为起始城市
                remaining_cities = set(range(num_cities))  # 初始化未访问城市集合
                remaining_cities.remove(self.start_city)  # 移除起始城市
                while remaining_cities:  # 当还有未访问城市时
                    city = path[-1]  # 获取当前城市
                    p = pheromone[city, list(remaining_cities)] ** self.alpha  # 计算信息素和距离的乘积
                    d = self.distances[city, list(remaining_cities)] ** self.beta  # 计算距离的beta次方
                    probs = p / d  # 计算选择每个城市的概率
                    probs /= probs.sum()  # 将概率归一化
                    next_city = np.random.choice(list(remaining_cities), p=probs)  # 根据概率选择下一个城市
                    path.append(next_city)  # 将选择的下一个城市添加到路径中
                    remaining_cities.remove(next_city)  # 从未访问城市中移除该城市
                distance = sum(self.distances[path[i], path[i + 1]] for i in range(len(path) - 1))
                # 计算该蚂蚁行走路径的距离
                if distance < best_distance:
                    # 如果该路径距离小于全局最优路径距离，则更新最优路径
                    best_distance = distance
                    best_path = path
                paths.append((path, distance))
            # 更新信息素
            pheromone *= (1 - self.rho)
            for path, distance in paths:
                for i in range(len(path) - 1):
                    pheromone[path[i], path[i + 1]] += 1.0 / distance
                    pheromone[path[i + 1], path[i]] += 1.0 / distance
            # 将最优路径的距离加入到列表中，以用于画图
            iteration_distances.append(best_distance)
        # 画出迭代图
        plt.plot(range(self.num_iterations), iteration_distances)
        plt.show()
        # 计算最优路径每一步的距离
        distances_of_best_path = [self.distances[best_path[i], best_path[i + 1]] for i in range(len(best_path) - 1)]
        # 打印出最优路径每一步的距离
        print("Distances of each step in best path:", distances_of_best_path)
        # 返回最优路径和距离
        return best_path, best_distance


# 以下是示例用法：
distances = np.array([[0, 2, 3, 5], [2, 0, 4, 1], [3, 4, 0, 2], [5, 1, 2, 0]])
start_city = 0

aco = AntColonyTSP(distances, start_city)
best_path, best_distance = aco.run()

print("start_city:", start_city)
print("Best path:", best_path)
print("Best distance:", best_distance)

