import numpy as np
import matplotlib.pyplot as plt


def ant_colony_tsp(distances, start_city):
    num_cities = distances.shape[0]
    pheromone = np.ones((num_cities, num_cities)) / num_cities
    best_distance = np.inf
    best_path = None
    num_iterations = 100
    num_ants = 10
    alpha, beta, rho = 1.0, 2.0, 0.5
    iteration_distances = []
    for it in range(num_iterations):
        paths = []
        for i in range(num_ants):
            path = [start_city]
            remaining_cities = set(range(num_cities))
            remaining_cities.remove(start_city)
            while remaining_cities:
                city = path[-1]
                p = pheromone[city, list(remaining_cities)] ** alpha
                d = distances[city, list(remaining_cities)] ** beta
                probs = p / d
                probs /= probs.sum()
                next_city = np.random.choice(list(remaining_cities), p=probs)
                path.append(next_city)
                remaining_cities.remove(next_city)
            distance = sum(distances[path[i], path[i + 1]] for i in range(len(path) - 1))
            if distance < best_distance:
                best_distance = distance
                best_path = path
            paths.append((path, distance))
        pheromone *= (1 - rho)
        for path, distance in paths:
            for i in range(len(path) - 1):
                pheromone[path[i], path[i + 1]] += 1.0 / distance
                pheromone[path[i + 1], path[i]] += 1.0 / distance
        iteration_distances.append(best_distance)
    plt.plot(range(num_iterations), iteration_distances)
    plt.show()
    return best_path, best_distance


# 以下是示例用法：
distances = np.array([[0, 5, 4, 3, 6, 8], [5, 0, 7, 6, 8, 4], [4, 7, 0, 5, 3, 5],
                      [3, 6, 5, 0, 5, 6], [6, 8, 3, 5, 0, 7], [8, 4, 5, 6, 7, 0]])
start_city = 0
best_path, best_distance = ant_colony_tsp(distances, start_city)
print("start_city:", start_city)
print("Best path:", best_path)
print("Best distance:", best_distance)
