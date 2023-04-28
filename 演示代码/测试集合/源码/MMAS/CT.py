import random
import math

def ant_colony(distance_matrix, city_list, num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_deposit):
    num_cities = len(city_list)
    pheromone_matrix = [[1.0 / (num_cities * num_cities) for j in range(num_cities)] for i in range(num_cities)]
    best_distance = float('inf')
    best_path = []
    for iteration in range(num_iterations):
        ant_paths = []
        for ant in range(num_ants):
            start_city = random.randint(0, num_cities-1)
            current_city = start_city
            unvisited_cities = set(range(num_cities))
            unvisited_cities.remove(current_city)
            path = [current_city]
            path_distance = []
            while unvisited_cities:
                next_city = choose_next_city(current_city, unvisited_cities, pheromone_matrix, distance_matrix, alpha, beta)
                path.append(next_city)
                path_distance.append(distance_matrix[current_city][next_city])
                unvisited_cities.remove(next_city)
                current_city = next_city
            ant_paths.append((path, calculate_path_distance(path_distance)))
        for i in range(num_cities):
            for j in range(num_cities):
                pheromone_matrix[i][j] *= (1 - evaporation_rate)
        for path, distance in ant_paths:
            for i in range(num_cities-1):
                pheromone_matrix[path[i]][path[i+1]] += pheromone_deposit / distance
        ant_paths.sort(key=lambda x: x[1])
        if ant_paths[0][1] < best_distance:
            best_distance = ant_paths[0][1]
            best_path = ant_paths[0][0]
    path_distances = [distance_matrix[best_path[i]][best_path[i+1]] for i in range(len(best_path)-1)]
    return best_distance, [city_list[i] for i in best_path], path_distances

def choose_next_city(current_city, unvisited_cities, pheromone_matrix, distance_matrix, alpha, beta):
    choices = []
    for city in unvisited_cities:
        pheromone = pheromone_matrix[current_city][city]
        distance = distance_matrix[current_city][city]
        heuristic = 1.0 / distance
        probability = pheromone ** alpha * heuristic ** beta
        choices.append((city, probability))
    total_prob = sum(prob for city, prob in choices)
    norm_choices = [(city, prob / total_prob) for city, prob in choices]
    r = random.uniform(0, 1)
    for city, norm_prob in norm_choices:
        if r < norm_prob:
            return city
        r -= norm_prob
    return norm_choices[-1][0]

def calculate_path_distance(path_distance):
    distance = 0
    for i in range(len(path_distance)):
        distance += path_distance[i]
    return distance

distance_matrix = [
    [0, 2, 9, 10, 6],
    [2, 0, 4, 8, 10],
    [9, 4, 0, 3, 8],
    [10, 8, 3, 0, 7],
    [6, 10, 8, 7, 0]
]
city_list = ['A', 'B', 'C', 'D', 'E']
num_ants = 10
num_iterations = 100
alpha = 1
beta = 5
evaporation_rate = 0.5
pheromone_deposit = 10

best_distance, best_path, path_distances = ant_colony(distance_matrix, city_list, num_ants, num_iterations, alpha, beta, evaporation_rate, pheromone_deposit)

print(f"Shortest distance: {best_distance}")
print(f"Shortest path: {best_path}")
print(f"Path distances: {path_distances}")
