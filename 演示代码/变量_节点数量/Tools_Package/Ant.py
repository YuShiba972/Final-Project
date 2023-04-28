"""
************************
***  author:Yeller   ***
***  date:2023/04/21 ***
************************
"""
import copy
import numpy as np


class AntColony:
    def __init__(self, distances, start_city=0, num_iterations=50,
                 num_ants=25, alpha=5.0, beta=2.0, rho=0.5):
        self.distances = distances
        self.start_city = start_city
        self.num_iterations = num_iterations
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.iteration_best = []
        self.iteration_avgbest = []

    def run(self):
        num_cities = self.distances.shape[0]
        pheromone = np.ones((num_cities, num_cities)) / num_cities
        pheromone = pheromone
        # print('初始(第1代蚂蚁参照)信息素矩阵为：\n', pheromone)
        best_distance = np.inf  # 将最优距离初始化为负无穷
        best_path = None
        for it in range(self.num_iterations):
            # print('第{}次迭代开始'.format(it + 1))
            paths = []
            for i in range(self.num_ants):
                # print('第{}只蚂蚁开始行动'.format(i + 1))
                path = [self.start_city]
                remaining_cities = set(range(num_cities))
                remaining_cities.remove(self.start_city)
                #####################################################################################
                # 当代蚂蚁轮盘赌寻路
                while remaining_cities:
                    city = path[-1]
                    # print('城市索引：', city)
                    p = pheromone[city, list(remaining_cities)] ** self.alpha
                    # print('信息素因子：', pheromone[city, list(remaining_cities)])
                    d = self.distances[city, list(remaining_cities)] ** self.beta
                    # print('距离因子：', self.distances[city, list(remaining_cities)])
                    probs = p / d
                    probs /= probs.sum()
                    # print('各个城市被选择的概率：', probs)

                    # print('**************\n')
                    next_city = np.random.choice(list(remaining_cities), p=probs)
                    path.append(next_city)
                    remaining_cities.remove(next_city)
                #####################################################################################
                # print('这只蚂蚁的路径为：', path)
                distance = sum(self.distances[path[i], path[i + 1]] for i in range(len(path) - 1))
                if distance < best_distance:  # 如果当前路径更长，则更新最优路径和距离
                    best_distance = distance
                    best_path = path
                paths.append((path, distance))
            # print('本次迭代中每只蚂蚁的路径列表为：\n', paths)
            self.iteration_avgbest.append(np.mean(list(map(lambda x: x[1], paths))))
            self.iteration_best.append(best_distance)
            #####################################################################################
            # 信息素挥发更新
            pheromone *= (1 - self.rho)
            # print('第{}代蚂蚁挥发后的信息素矩阵为：\n{}'.format(it + 1, pheromone))
            # 当代信息素矩阵更新
            for path, distance in paths:
                for i in range(len(path) - 1):
                    pheromone[path[i], path[i + 1]] += 1.0 / distance
                    pheromone[path[i + 1], path[i]] += 1.0 / distance
            # print('下一代代蚂蚁参照的信息素大小为{}：'.format(pheromone))
        #####################################################################################
        return best_path, best_distance


def ACO_first(points_list, datas, heu_mat, max_battery=10800, consume=5, thred=0.2, v=0.5, eff=30,
              num_iterations=50, alpha=5.0, beta=2.0, rho=0.5):
    ant = AntColony(heu_mat, num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho,
                    num_ants=int(heu_mat.shape[0] * 1.5))
    best_path, best_distance = ant.run()
    best_points = list(map(lambda x: x, [points_list[i] for i in best_path]))
    goals_l = best_points[1::]

    origin_energy = list(map(lambda x: x.battery, goals_l))

    pl = copy.copy(best_points)
    #######################################################
    current = best_points[0]  # 当前节点初始化
    visited = [best_points[0].location]  # 当前访问列表初始化
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
            point.battery = point.battery - int((tem_dis / v)) * consume - int((max_battery - current.battery) / eff)
        # 低于阈值的节点判定
        for point in goals_l:
            if point.battery < thred * max_battery:
                point.battery = thred * max_battery
        # 当前充满的节点判定
        current.battery = max_battery
    # print('ACO:', sum(dis_l), sum(charge_l), '\n', dis_l)
    # print('*' * 100)
    #######################   性能评定  ###################################

    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)
    # Gain1 = sum(list(charge_l[i] / dis_l[i] if dis_l[i] != 0 else 1 for i in range(len(charge_l))))

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


def charge_first(points_list, datas, max_battery=10800, consume=5, thred=0.2, v=0.5, eff=30):
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
        min_battery = 99999
        tem_dis = 0
        # 寻找下一个节点,遍历未经过的点,得到current,访问过的需要减去
        for point in pl:  # 在未访问过的点集合中循环寻找
            if point.battery < min_battery:
                min_battery = point.battery
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
            point.battery = point.battery - int((tem_dis / v)) * consume - int((max_battery - current.battery) / eff)
        # 低于阈值的节点判定
        for point in goals_l:
            if point.battery < thred * max_battery:
                point.battery = thred * max_battery
        # 当前充满的节点判定
        current.battery = max_battery
    # print('MMAS-CM:', sum(dis_l), sum(charge_l), '\n', dis_l)

    #######################   性能评定  ###################################

    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)
    # Gain1 = sum(list(charge_l[i] / dis_l[i] if dis_l[i] != 0 else 1 for i in range(len(charge_l))))

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


def path_first(points_list, datas, max_battery=10800, consume=5, thred=0.2, v=0.5, eff=30):  # NJNP
    goals_l = points_list[1::]
    origin_energy = list(map(lambda x: x.battery, goals_l))
    # print(origin_energy)
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
            point.battery = point.battery - int((min_dis / v)) * consume - int((max_battery - current.battery) / eff)
        # 低于阈值的节点判定
        for point in goals_l:
            if point.battery < thred * max_battery:
                point.battery = thred * max_battery
        # 当前充满的节点判定
        current.battery = max_battery
    # print('NJNP:', sum(dis_l), sum(charge_l), '\n', dis_l)

    # 性能评定
    # 1.收益比:一个充电周期内有效充电量总和/距离和
    Gain1 = sum(charge_l) / sum(dis_l)
    # Gain1 = sum(list(charge_l[i] / dis_l[i] if dis_l[i] != 0 else 1 for i in range(len(charge_l))))

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