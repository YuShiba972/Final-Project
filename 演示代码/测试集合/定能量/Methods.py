"""
************************
***  author:Yeller   ***
***  date:2023/03/20 ***
************************
"""
import copy

import numpy as np


def charge_first(points_list, datas, max_battery=10800, consume=0, thred=0.2, v=1):
    goals_l = points_list[1::]
    origin_energy = list(map(lambda x: x.battery, goals_l))
    pl = copy.copy(points_list)
    #######################################################
    # MMAS-CM能量优先算法，节点能量最少优先最近优先
    current = points_list[0]  # 当前节点初始化
    visited = [points_list[0].location]  # 当前访问列表初始化
    pl.remove(current)  # 终止列表初始化，遍历后的点就移除pl

    # 列表初始化
    dis_l = []  # 单步距离列表
    charge_l = []  # 单步充电量列表
    seq_l = [points_list[0].name]  # 遍历次序列表

    while pl:  # 设置终止条件,未访问的节点为空
        min_battery = 99999
        tem_dis = 0
        tem_c = 0
        # 寻找下一个节点,遍历未经过的点,得到current,访问过的需要减去
        for point in pl:  # 在未访问过的点集合中循环寻找
            if point.battery < min_battery:
                min_battery = point.battery
                current = point
        seq_l.append(current.name)
        # 添加单步电量、访问列表、访问坐标
        pl.remove(current)
        visited.append(current.location)
        charge_l.append(max_battery - current.battery)
        # 利用location读取并添加单步距离
        for data in datas:
            if data[1] == current.location and \
                    data[0] == visited[visited.index(current.location) - 1]:
                tem_dis = (data[2])
                dis_l.append(tem_dis)
        # 更新各节点电量
        for point in goals_l:
            point.battery = point.battery - (tem_dis / v) * consume * 2
        # 低于阈值的节点判定
        for point in goals_l:
            if point.battery < thred * max_battery:
                point.battery = thred * max_battery
        # 当前充满的节点判定
        current.battery = max_battery

    #######################   性能评定  ###################################

    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)

    # 2.网络效益:一个周期后网络的总能量与网络初始能量之比
    final_energy = list(map(lambda x: x.battery, goals_l))
    en1 = sum(origin_energy)
    en2 = sum(final_energy)
    Gain2 = en2 / en1

    # 3.节点休眠比率:一个充电周期后休眠节点占所有节点的比率
    sleep = list(map(lambda x: x.battery, goals_l)).count(thred * max_battery)
    Gain3 = sleep / len(goals_l)

    # 4.节点剩余能量方差:一个周期后各个节点剩余能量方差
    Gain4 = np.std(np.array(final_energy))
    return Gain1, Gain2, Gain3, Gain4


def path_first(points_list, datas, max_battery=10800, consume=0, thred=0.2, v=1):  # NJNP
    goals_l = points_list[1::]
    origin_energy = list(map(lambda x: x.battery, goals_l))
    pl = copy.copy(points_list)

    #######################################################
    # NJNP距离优先算法
    current = points_list[0]  # 当前节点初始化
    visited = [points_list[0].location]  # 当前访问列表初始化
    pl.remove(current)  # 终止列表初始化，遍历后的点就移除pl

    # 列表初始化
    dis_l = []  # 单步距离列表
    charge_l = []  # 单步充电量列表

    while pl:
        min_dis = 9999
        next_location = 0
        # 寻找下一个节点,遍历未经过的点,得到current,访问过的需要减去

        # 获取下一个节点坐标,距离
        for data in datas:
            if data[0] == current.location and data[1] not in visited:
                if data[2] < min_dis:
                    next_location = data[1]
                    min_dis = data[2]

        # 由下一个坐标获取下一个节点类
        for point in points_list:
            if point.location == next_location:
                current = point

        # 添加单步距离\单步电量\访问列表、访问坐标
        dis_l.append(min_dis)
        charge_l.append(max_battery - current.battery)
        visited.append(current.location)
        pl.remove(current)

        for point in goals_l:
            point.battery = point.battery - (min_dis / v) * consume * 2
            # 低于阈值的节点判定
            for point in goals_l:
                if point.battery < thred * max_battery:
                    point.battery = thred * max_battery
            # 当前充满的节点判定
            current.battery = max_battery
    # print(dis_l)
    # print(charge_l)
    # print(visited)

    # 性能评定
    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)

    # 2.网络效益:一个周期后网络的总能量与网络初始能量之比
    final_energy = list(map(lambda x: x.battery, goals_l))
    en1 = sum(origin_energy)
    en2 = sum(final_energy)
    Gain2 = en2 / en1

    # 3.节点休眠比率:一个充电周期后休眠节点占所有节点的比率
    sleep = list(map(lambda x: x.battery, goals_l)).count(thred * max_battery)
    Gain3 = sleep / len(goals_l)

    # 4.节点剩余能量方差:一个周期后各个节点剩余能量方差
    Gain4 = np.std(np.array(final_energy))
    return Gain1, Gain2, Gain3, Gain4


class AntColony:
    def __init__(self, distances, start_city=0, num_iterations=100, num_ants=15, alpha=1.0, beta=2.0, rho=0.5):
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
        best_distance = -np.inf  # 将最优距离初始化为负无穷
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
                if distance > best_distance:  # 如果当前路径更长，则更新最优路径和距离
                    best_distance = distance
                    best_path = path
                paths.append((path, distance))
            pheromone *= (1 - self.rho)
            for path, distance in paths:
                for i in range(len(path) - 1):
                    pheromone[path[i], path[i + 1]] += 1.0 / distance
                    pheromone[path[i + 1], path[i]] += 1.0 / distance
            iteration_distances.append(best_distance)
        # plt.plot(range(self.num_iterations), iteration_distances)
        # plt.show()
        distances_of_best_path = [self.distances[best_path[i], best_path[i + 1]] for i in range(len(best_path) - 1)]
        # print("Distances of each step in best path:", distances_of_best_path)
        return best_path, best_distance


def ACO_first(points_list, datas, max_battery=10800, consume=0, thred=0.2, v=1):
    goals_l = points_list[1::]
    origin_energy = list(map(lambda x: x.battery, goals_l))
    pl = copy.copy(points_list)

    #######################################################
    # MMAS-CM能量优先算法，节点能量最少优先最近优先
    current = points_list[0]  # 当前节点初始化
    visited = [points_list[0].location]  # 当前访问列表初始化
    pl.remove(current)  # 终止列表初始化，遍历后的点就移除pl

    # 列表初始化
    dis_l = []  # 单步距离列表
    charge_l = []  # 单步充电量列表

    while pl:  # 设置终止条件,未访问的节点为空
        tem_dis = 0
        # 寻找下一个节点,遍历未经过的点,得到current,访问过的需要减去
        for point in pl:  # 在未访问过的点集合中循环寻找
            if point == pl[0]:
                current = point
                # 添加单步电量、访问列表、访问坐标
                pl.remove(current)
                visited.append(current.location)
                charge_l.append(max_battery - current.battery)
        # 利用location读取并添加单步距离
        for data in datas:
            if data[1] == current.location and \
                    data[0] == visited[visited.index(current.location) - 1]:
                tem_dis = (data[2])
                dis_l.append(tem_dis)

        # 更新各节点电量
        for point in goals_l:
            point.battery = point.battery - (tem_dis / v) * consume * 2
        # 低于阈值的节点判定
        for point in goals_l:
            if point.battery < thred * max_battery:
                point.battery = thred * max_battery
        # 当前充满的节点判定
        current.battery = max_battery

    #######################   性能评定  ###################################

    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)

    # 2.网络效益:一个周期后网络的总能量与网络初始能量之比
    final_energy = list(map(lambda x: x.battery, goals_l))
    en1 = sum(origin_energy)
    en2 = sum(final_energy)
    Gain2 = en2 / en1

    # 3.节点休眠比率:一个充电周期后休眠节点占所有节点的比率
    sleep = list(map(lambda x: x.battery, goals_l)).count(thred * max_battery)
    Gain3 = sleep / len(goals_l)

    # 4.节点剩余能量方差:一个周期后各个节点剩余能量方差
    Gain4 = np.std(np.array(final_energy))
    return Gain1, Gain2, Gain3, Gain4
