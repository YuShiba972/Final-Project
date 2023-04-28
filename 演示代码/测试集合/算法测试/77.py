"""
************************
***  author:Yeller   ***
***  date:2023/03/11 ***
************************
"""
import numpy as np
import matplotlib.pyplot as plt

class AntColonyTSP:
    def __init__(self, distances, start_city, num_iterations=100, num_ants=10, alpha=1.0, beta=2.0, rho=0.5):
        self.distances = distances
        self.num_cities = distances.shape[0]
        self.start_city = start_city
        self.num_iterations = num_iterations
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromone = np.ones((self.num_cities, self.num_cities)) / self.num_cities
        self.best_distance = np.inf
        self.best_path = None
        self.iteration_distances = []

    def run(self):
        for it in range(self.num_iterations):
            paths = []
            for i in range(self.num_ants):
                path = [self.start_city]
                remaining_cities = set(range(self.num_cities))
                remaining_cities.remove(self.start_city)
                while remaining_cities:
                    city = path[-1]
                    p = self.pheromone[city, list(remaining_cities)] ** self.alpha
                    d = self.distances[city, list(remaining_cities)] ** self.beta
                    probs = p / d
                    probs /= probs.sum()
                    next_city = np.random.choice(list(remaining_cities), p=probs)
                    path.append(next_city)
                    remaining_cities.remove(next_city)
                distance = sum(self.distances[path[i], path[i+1]] for i in range(len(path)-1))
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path
                paths.append((path, distance))
            self.pheromone *= (1 - self.rho)
            for path, distance in paths:
                for i in range(len(path)-1):
                    self.pheromone[path[i], path[i+1]] += 1.0 / distance
                    self.pheromone[path[i+1], path[i]] += 1.0 / distance
            self.iteration_distances.append(self.best_distance)

    def plot_iteration_distances(self):
        plt.plot(range(self.num_iterations), self.iteration_distances)
        plt.show()

# 以下是示例用法：
distances = np.array([[0, 5, 4, 3, 6, 8], [5, 0, 7, 6, 8, 4], [4, 7, 0, 5, 3, 5],
                      [3, 6, 5, 0, 5, 6], [6, 8, 3, 5, 0, 7], [8, 4, 5, 6, 7, 0]])
start_city = 3
aco = AntColonyTSP(distances, start_city)
aco.run()
aco.plot_iteration_distances()
print("Best path:", aco.best_path)
print("Best distance:", aco.best_distance)
