"""
************************
***  author:Yeller   ***
***  date:2023/03/10 ***
************************
"""
import numpy as np
import matplotlib.pyplot as plt

# define distance matrix
distance_matrix = np.array([
    [0, 4, 5, 7, 8],
    [4, 0, 4, 6, 7],
    [5, 4, 0, 3, 4],
    [7, 6, 3, 0, 3],
    [8, 7, 4, 3, 0]
])

# set parameters
num_ants = 10
num_iterations = 50
alpha = 1
beta = 5
evaporation_rate = 0.5
pheromone_deposit = 1

# define ant colony function
def ant_colony(distance_matrix, num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_deposit, start_city=None):
    num_cities = distance_matrix.shape[0]
    pheromone_matrix = np.ones((num_cities, num_cities))
    best_distance = float('inf')
    best_path = None
    distances = []
    for iteration in range(num_iterations):
        ant_paths = []
        for ant in range(num_ants):
            path = []
            visited = set()
            if start_city is None:
                current_city = np.random.randint(num_cities)
            else:
                current_city = start_city
            path.append(current_city)
            visited.add(current_city)
            for step in range(num_cities - 1):
                unvisited = list(visited.symmetric_difference(set(range(num_cities))))
                pheromone_values = pheromone_matrix[current_city, unvisited]
                distance_values = distance_matrix[current_city, unvisited]
                heuristic_info = 1.0 / distance_values
                probability = np.power(pheromone_values, alpha) * np.power(heuristic_info, beta)
                probability = probability / np.sum(probability)
                next_city = np.random.choice(unvisited, p=probability)
                path.append(next_city)
                visited.add(next_city)
                current_city = next_city
            ant_paths.append(path)
        pheromone_matrix *= (1.0 - evaporation_rate)
        for ant_path in ant_paths:
            distance = sum(distance_matrix[ant_path[i], ant_path[i+1]] for i in range(num_cities - 1))
            if distance < best_distance:
                best_distance = distance
                best_path = ant_path
            for i in range(num_cities - 1):
                pheromone_matrix[ant_path[i], ant_path[i+1]] += pheromone_deposit / distance
        distances.append(best_distance)
    return best_path, best_distance, distances

# run ant colony function with specified starting city
start_city = 2
best_path, best_distance, distances = ant_colony(distance_matrix, num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_deposit, start_city)

# print results
print('Starting city:', start_city)
print('Best path:', best_path)
print('Best distance:', best_distance)

# plot iteration vs. best distance
plt.plot(range(1, num_iterations + 1), distances)
plt.xlabel('Iteration')
plt.ylabel('Best distance')
plt.title('Ant Colony Optimization')
plt.show()

cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
distances = [[0, 2451, 713, 1632, 2415],
             [2451, 0, 1745, 1374, 366],
             [713, 1745, 0, 940, 1763],
             [1632, 1374, 940, 0, 1015],
             [2415, 366, 1763, 1015, 0]]

start_city = "Los Angeles"  # 指定起点

best_path, best_distance = ant_colony_optimization(distances, cities, start_city=start_city, iterations=100, num_ants=20, alpha=1, beta=2, evaporation_rate=0.5, q=100)

print("Starting city:", start_city)
print("Best path:", [cities[i] for i in best_path])
print("Best distance:", best_distance)

