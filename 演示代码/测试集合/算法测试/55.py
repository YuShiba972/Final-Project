"""
************************
***  author:Yeller   ***
***  date:2023/03/11 ***
************************
"""
import numpy as np
import random
import matplotlib.pyplot as plt


class AntColonyOptimization:
    def __init__(self, dist_matrix, cities, ant_count=10, alpha=1, beta=2, evaporation=0.5, Q=100, iterations=100):
        self.dist_matrix = dist_matrix
        self.cities = cities
        self.ant_count = ant_count
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.Q = Q
        self.iterations = iterations
        self.pheromone_matrix = np.ones_like(self.dist_matrix) / len(self.cities)
        self.global_best_distance = float('inf')
        self.global_best_path = None

    def ant_tour(self, start_city):
        distance = 0
        visited_cities = [start_city]
        unvisited_cities = [city for city in range(len(self.cities)) if city != start_city]

        while unvisited_cities:
            probabilities = self.probability(start_city, visited_cities, unvisited_cities)
            next_city = random.choices(unvisited_cities, probabilities)[0]
            visited_cities.append(next_city)
            unvisited_cities.remove(next_city)
            distance += self.dist_matrix[start_city][next_city]
            start_city = next_city

        distance += self.dist_matrix[visited_cities[-1]][visited_cities[0]]
        return visited_cities, distance

    def probability(self, current_city, visited_cities, unvisited_cities):
        pheromone = self.pheromone_matrix[current_city][unvisited_cities]
        distance = self.dist_matrix[current_city][unvisited_cities]
        attractiveness = 1 / distance
        probabilities = (pheromone ** self.alpha) * (attractiveness ** self.beta)
        probabilities /= np.sum(probabilities)
        return probabilities

    def update_pheromone_matrix(self, paths):
        pheromone_matrix = np.zeros_like(self.dist_matrix)

        for path, distance in paths:
            for i in range(len(path) - 1):
                from_city, to_city = path[i], path[i + 1]
                pheromone_matrix[from_city][to_city] += self.Q / distance

        pheromone_matrix *= self.evaporation
        pheromone_matrix += self.pheromone_matrix * (1 - self.evaporation)
        self.pheromone_matrix = pheromone_matrix

    def run(self, start_city):
        global_best_distance = float('inf')
        global_best_path = None
        distance_list = []

        for iteration in range(self.iterations):
            paths = [self.ant_tour(start_city) for _ in range(self.ant_count)]
            paths.sort(key=lambda x: x[1])
            best_path, best_distance = paths[0]

            if best_distance < global_best_distance:
                global_best_distance = best_distance
                global_best_path = best_path

            self.update_pheromone_matrix(paths)
            distance_list.append(best_distance)

        plt.plot(distance_list)
        plt.title("Iteration Distance")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        plt.show()

        return global_best_path, global_best_distance

