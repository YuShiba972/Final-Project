import numpy as np
from matplotlib import pyplot as plt


class AntColonyOptimizer:
    def __init__(self, num_ants, num_iterations, evaporation_rate, alpha, beta):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta

    def optimize(self, city_names, distance_matrix, start_city):
        num_cities = len(city_names)
        city_indices = list(range(num_cities))
        start_city_index = city_names.index(start_city)

        # 初始化信息素矩阵和启发式信息矩阵
        pheromone_matrix = np.ones((num_cities, num_cities))
        visibility_matrix = 1 / (distance_matrix + 1e-8)

        # 迭代优化
        best_path = None
        best_length = float('inf')
        for iteration in range(self.num_iterations):
            # 记录每只蚂蚁的路径和长度
            ant_paths = np.zeros((self.num_ants, num_cities), dtype=int)
            ant_lengths = np.zeros(self.num_ants)

            # 每只蚂蚁寻找一条路径
            for ant in range(self.num_ants):
                # 选择起点城市
                current_city = start_city_index
                visited_cities = [current_city]

                # 选择下一个城市直到所有城市都被访问
                for _ in range(num_cities-1):
                    # 计算每个城市的选择概率
                    unvisited_cities = list(set(city_indices) - set(visited_cities))
                    pheromone_values = pheromone_matrix[current_city, unvisited_cities]
                    visibility_values = visibility_matrix[current_city, unvisited_cities]
                    attractiveness_values = np.power(pheromone_values, self.alpha) * np.power(visibility_values, self.beta)
                    probability_values = attractiveness_values / np.sum(attractiveness_values)

                    # 根据选择概率选择下一个城市
                    next_city = np.random.choice(unvisited_cities, p=probability_values)
                    visited_cities.append(next_city)
                    current_city = next_city

                # 记录路径和长度
                ant_paths[ant] = visited_cities
                ant_lengths[ant] = sum(distance_matrix[visited_cities[:-1], visited_cities[1:]])

            # 更新信息素矩阵
            pheromone_matrix *= self.evaporation_rate
            for ant in range(self.num_ants):
                for i in range(num_cities-1):
                    city1, city2 = ant_paths[ant, i], ant_paths[ant, i+1]
                    pheromone_matrix[city1, city2] += 1 / ant_lengths[ant]

            # 记录最优路径和长度
            best_ant_index = np.argmin(ant_lengths)
            if ant_lengths[best_ant_index] < best_length:
                best_path = [city_names[index] for index in ant_paths[best_ant_index]]
                best_length = ant_lengths[best_ant_index]

        return best_path, best_length

    def plot_iteration_distance(self):
        """
        绘制迭代图

        """
        fig, ax = plt.subplots()
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Distance')
        ax.set_title('Iteration vs Distance')
        ax.plot(range(self.num_iterations), self.best_length)
        plt.show()

