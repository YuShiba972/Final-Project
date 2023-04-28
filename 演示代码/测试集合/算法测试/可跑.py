import numpy as np
import matplotlib.pyplot as plt


class AntColony:
    def __init__(self, distances, start_city=0, num_iterations=100, num_ants=10, alpha=1.0, beta=2.0, rho=0.5):
        self.distances = distances
        self.start_city = start_city
        self.num_iterations = num_iterations
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

    def run(self):
        num_cities = self.distances.shape[0]
        pheromone = np.ones((num_cities, num_cities)) / num_cities
        best_distance = np.inf
        best_path = None
        iteration_distances = []
        for it in range(self.num_iterations):
            paths = []
            for i in range(self.num_ants):
                path = [self.start_city]
                remaining_cities = set(range(num_cities))
                remaining_cities.remove(self.start_city)
                while remaining_cities:
                    city = path[-1]
                    p = pheromone[city, list(remaining_cities)] ** self.alpha
                    d = self.distances[city, list(remaining_cities)] ** self.beta
                    probs = p / d
                    probs /= probs.sum()
                    next_city = np.random.choice(list(remaining_cities), p=probs)
                    path.append(next_city)
                    remaining_cities.remove(next_city)
                distance = sum(self.distances[path[i], path[i + 1]] for i in range(len(path) - 1))
                if distance < best_distance:
                    best_distance = distance
                    best_path = path
                paths.append((path, distance))
            pheromone *= (1 - self.rho)
            for path, distance in paths:
                for i in range(len(path) - 1):
                    pheromone[path[i], path[i + 1]] += 1.0 / distance
                    pheromone[path[i + 1], path[i]] += 1.0 / distance
            iteration_distances.append(best_distance)
        plt.plot(range(self.num_iterations), iteration_distances)
        plt.show()
        distances_of_best_path = [self.distances[best_path[i], best_path[i+1]] for i in range(len(best_path)-1)]
        print("Distances of each step in best path:", distances_of_best_path)
        return best_path, best_distance


# 以下是示例用法：
distances = np.array([[0, 2, 3, 5], [2, 0, 4, 1], [3, 4, 0, 2], [5, 1, 2, 0]])

aco = AntColony(distances)
best_path, best_distance = aco.run()

# print("start_city:", start_city)
print("Best path:", best_path)
print("Best distance:", best_distance)
