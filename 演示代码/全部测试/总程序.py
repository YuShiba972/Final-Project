"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import copy

from matplotlib import pyplot as plt

from ArcRouting import Point
import random
import numpy as np
import random
from lddya.Algorithm import ACO
from lddya.Draw import ShanGeTu
from PIL import Image
import itertools
from PIL import Image, ImageDraw, ImageFont


def charge_first(points_list, datas, max_battery=10800, consume=200, thred=0.2, v=0.5):
    goals_l = points_list[1::]
    origin_energy = list(map(lambda x: x.battery, goals_l))
    pl = copy.copy(points_list)

    # 初始化电池电量、电池消耗、门限

    # max_battery = 10800
    # consume = 200
    # thred = 0.2
    # v = 1

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
    Gain4 = np.std(np.array(charge_l))
    return Gain1, Gain2, Gain3, Gain4


def path_first(points_list, datas, max_battery=10800, consume=200, thred=0.2, v=0.5):  # NJNP
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
    Gain4 = np.std(np.array(charge_l))
    return Gain1, Gain2, Gain3, Gain4


def read_dis(filename, points_list):
    """
    @filename: 带有location和distance的文件
    @points_list: 点的列表
    """
    datas = []
    dis_l = []
    n = len(points_list)
    # 按顺序读取数据存入列表
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    # 按顺序存入距离列表
    for data in datas:
        dis_l.append(data[2])

    # 建立距离矩阵(含起点)
    dis_origin = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:  # 左对角线元素为0
                dis_origin[i][j] = 0
            else:  # 其他元素填入列表中的元素
                if dis_l:
                    dis_origin[i][j] = dis_l.pop(0)
                else:
                    dis_origin[i][j] = 0
    # 优化距离矩阵(不含起点)
    dis_mat = dis_origin[1:n, 1:n]
    return dis_origin


def read_battery(points_list, max_battery=10800, consume=200, thred=0.2):
    goals_l = points_list
    origin_energy = []
    n = len(goals_l)
    # 随机生成能量
    for i in range(len(goals_l)):
        origin_energy.append(random.randint(int(thred * max_battery), max_battery))
    # 能量、消耗数据注入点类
    for k, point in enumerate(goals_l):
        point.battery = origin_energy[k]
        point.consume = consume
    # 生成电量列表
    bat_l = list(map(lambda x: x.battery, goals_l))
    # 生成电量矩阵
    bat_mat = np.repeat([bat_l], n, axis=0)
    # 优化电量矩阵，将左对角线元素替换至0
    np.fill_diagonal(bat_mat, 0)
    return goals_l, bat_mat


class AntColony:
    def __init__(self, distances, start_city=0, num_iterations=100, num_ants=5, alpha=1.0, beta=2.0, rho=0.5):
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
        plt.plot(range(self.num_iterations), iteration_distances)
        plt.show()
        distances_of_best_path = [self.distances[best_path[i], best_path[i + 1]] for i in range(len(best_path) - 1)]
        # print("Distances of each step in best path:", distances_of_best_path)
        return best_path, best_distance


def ACO_first(points_list, datas, max_battery=10800, consume=200, thred=0.2, v=1):
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
    Gain4 = np.std(np.array(charge_l))
    return Gain1, Gain2, Gain3, Gain4


def read_path_map(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    return datas


def draw1(va_list, va_name,datas):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        ACO_Gain1_l = []
        ACO_Gain2_l = []
        ACO_Gain3_l = []
        ACO_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, thred=va,datas=datas)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, thred=va,datas=datas)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = \
                charge_first(points_list=best_points, thred=va,datas=datas)
            ACO_Gain1_l.append(ACO_Gain1)
            ACO_Gain2_l.append(ACO_Gain2)
            ACO_Gain3_l.append(ACO_Gain3)
            ACO_Gain4_l.append(ACO_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

        ACO_ylab1.append(np.mean(np.array(ACO_Gain1_l)))
        ACO_ylab2.append(np.mean(np.array(ACO_Gain2_l)))
        ACO_ylab3.append(np.mean(np.array(ACO_Gain3_l)))
        ACO_ylab4.append(np.mean(np.array(ACO_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围


def draw2(va_list, va_name,datas):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        ACO_Gain1_l = []
        ACO_Gain2_l = []
        ACO_Gain3_l = []
        ACO_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, consume=va,datas=datas)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, consume=va,datas=datas)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = \
                charge_first(points_list=best_points, consume=va,datas=datas)
            ACO_Gain1_l.append(ACO_Gain1)
            ACO_Gain2_l.append(ACO_Gain2)
            ACO_Gain3_l.append(ACO_Gain3)
            ACO_Gain4_l.append(ACO_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

        ACO_ylab1.append(np.mean(np.array(ACO_Gain1_l)))
        ACO_ylab2.append(np.mean(np.array(ACO_Gain2_l)))
        ACO_ylab3.append(np.mean(np.array(ACO_Gain3_l)))
        ACO_ylab4.append(np.mean(np.array(ACO_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.show()


def draw3(va_list, va_name, datas):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        ACO_Gain1_l = []
        ACO_Gain2_l = []
        ACO_Gain3_l = []
        ACO_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, max_battery=va, datas=datas)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, max_battery=va, datas=datas)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = \
                charge_first(points_list=best_points, max_battery=va, datas=datas)
            ACO_Gain1_l.append(ACO_Gain1)
            ACO_Gain2_l.append(ACO_Gain2)
            ACO_Gain3_l.append(ACO_Gain3)
            ACO_Gain4_l.append(ACO_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

        ACO_ylab1.append(np.mean(np.array(ACO_Gain1_l)))
        ACO_ylab2.append(np.mean(np.array(ACO_Gain2_l)))
        ACO_ylab3.append(np.mean(np.array(ACO_Gain3_l)))
        ACO_ylab4.append(np.mean(np.array(ACO_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.show()


class Point:
    def __init__(self, name='', location=None, battery=0, consume=0, ):
        self.name = name
        self.location = location
        self.battery = battery
        self.consume = consume


class Map:
    def __init__(self, fp: str) -> None:
        self.data = self.load_map_file(fp)

    def load_map_file(self, fp: str) -> np.ndarray:
        """
        从map文件中读取地图数据
        """
        with open(fp, 'r') as f:
            data = [list(line.strip('\n')) for line in f.readlines()]
        return np.array(data, dtype=np.int64)


def generate_points(filename='Map_In10.txt', n=5, thred=0.2, max=10800):
    # 从文件中读取矩阵
    with open(filename, 'r') as f:
        matrix = [list(line.strip()) for line in f.readlines()]
    rows, cols = len(matrix), len(matrix[0])
    # 获取矩阵中非1元素的索引
    indices = [(i, j) for i in range(rows) for j in range(cols) if matrix[i][j] != '1']
    # 从索引中生成n个唯一坐标
    coordinates = random.sample(indices, n)
    # 按字典顺序对坐标进行排序
    coordinates[0] = (0, 0)
    # coordinates = sorted(coordinates)
    # 创建Point实例
    points = []
    for i, coord in enumerate(coordinates):
        if i == 0:
            name = 'A'
        else:
            name = chr(ord('A') + i)
        points.append(Point(name=name, location=list(coord)))
    # 打印坐标和实例信息
    # print("生成的坐标:")
    # for coord in coordinates:
    #     print(coord)
    print("生成的Point实例:")
    for point in points:
        print(f"名称: {point.name}, 坐标: {point.location}")

    # 检查生成的坐标是否与矩阵中的1元素冲突
    conflicts = [coord for coord in coordinates if matrix[coord[0]][coord[1]] == '1']
    if conflicts:
        print("与矩阵中的1元素冲突:")
        for conflict in conflicts:
            print(conflict)
    else:
        print("随机生成的目标点不在禁行区内.")
    for point in points:
        point.battery = random.randint(int(thred * max), max)
    # points[0] = None
    return points


def cycle_run(map_data, points, newname='maps.txt'):  # 获取单个目标点到所有点的   最短距离集合
    datas = []
    for point in points:
        tem = points.copy()  # 新分配内存区域
        tem.remove(point)
        for goal_point in tem:
            aco = ACO(map_data=map_data, start=point, end=goal_point)
            aco.run()
            datas.append([point, goal_point, aco.way_len_best, aco.way_data_best])

    with open(newname, mode='w') as f:
        # path_data依次为，起点，终点，路径长度，路径列表
        for data in datas:
            f.writelines(str(data) + '\n')


if __name__ == "__main__":
    ###########################################################

    filename = 'map.txt'  # 指定地图文件
    points_list = generate_points(n=15, filename=filename)  # 随机生成坐标点
    # draw_map(points_list, filename=filename)  # 查看生成的障碍物地图以及目标点地图
    cycle_run(map_data=Map(fp=filename).data, points=[i.location for i in points_list])  # 蚁群算法生成距离数据

    points_list, bat_mat = read_battery(points_list)

    # 读取距离矩阵并存储
    datas = read_path_map('maps.txt')
    dis_mat = read_dis('maps.txt', points_list)
    ###########################################################

    # 启发函数矩阵构造
    dis_mat[np.diag_indices_from(dis_mat)] = 1
    bat_mat[np.diag_indices_from(bat_mat)] = 1
    heu_mat = dis_mat / bat_mat
    heu_mat[np.diag_indices_from(heu_mat)] = 0
    ###########################################################
    aco = AntColony(heu_mat)
    best_path, best_distance = aco.run()
    best_points = list(map(lambda x: x, [points_list[i] for i in best_path]))

    threds = [x / 10 for x in range(11)]
    consumes = [50, 100, 150, 200, 250]
    max_batteries = list(range(3000, 10001, 1000))

    draw1(threds, '门限',datas)
    draw2(consumes, '消耗',datas)
    draw3(max_batteries, '最大电量', datas)

    plt.show()
