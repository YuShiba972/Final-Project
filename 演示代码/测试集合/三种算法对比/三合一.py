"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""
import copy
import random
import numpy as np


def read_path_map(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    return datas


class Point:
    def __init__(self, battery=0, charge=0.5, consume=0, color=None, name='', location=None, mesg=None):
        if mesg is None:
            mesg = []
        if location is None:
            location = []
        if color is None:
            color = [0, 0, 0]
        self.name = name
        self.location = location
        self.battery = battery
        self.charge = charge
        self.consume = consume
        self.color = color
        self.mesg = mesg


def charge_first(points_list, max_battery=10800, consume=200, thred=0.2, v=1):
    goals_l = points_list[1::]
    pl = copy.copy(points_list)

    # 初始化电池电量、电池消耗、门限

    # max_battery = 10800
    # consume = 200
    # thred = 0.2
    # v = 1
    # 随机生成节点初始能量(3000,10800J)和消耗速率均为(100J/s)
    origin_energy = []
    for i in range(len(goals_l)):
        origin_energy.append(random.randint(int(thred * max_battery), max_battery))
    # 能量、消耗数据注入点类
    for k, point in enumerate(goals_l):
        point.battery = origin_energy[k]
        point.consume = consume

    #######################################################
    # MMAS-CM能量优先算法，节点能量最少优先最近优先
    current = A  # 当前节点初始化
    visited = [A.location]  # 当前访问列表初始化
    pl.remove(current)  # 终止列表初始化，遍历后的点就移除pl

    # 列表初始化
    dis_l = []  # 单步距离列表
    charge_l = []  # 单步充电量列表
    seq_l = [A.name]  # 遍历次序列表

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


def path_first(points_list, max_battery=10800, consume=200, thred=0.2, v=1):  # NJNP
    goals_l = points_list[1::]
    pl = copy.copy(points_list)

    origin_energy = []
    # 随机生成节点电量
    for i in range(len(goals_l)):
        origin_energy.append(random.randint(int(thred * max_battery), max_battery))
    # 能量、消耗数据注入点类
    for k, point in enumerate(goals_l):
        point.battery = origin_energy[k]
        point.consume = consume

    #######################################################
    # NJNP距离优先算法
    current = A  # 当前节点初始化
    visited = [A.location]  # 当前访问列表初始化
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


def draw1(va_list, va_name):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, thred=va)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, thred=va)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.show()


def draw2(va_list, va_name):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, consume=va)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, consume=va)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.show()


def draw3(va_list, va_name):
    MMAS_ylab1 = []
    MMAS_ylab2 = []
    MMAS_ylab3 = []
    MMAS_ylab4 = []
    NJNP_ylab1 = []
    NJNP_ylab2 = []
    NJNP_ylab3 = []
    NJNP_ylab4 = []

    for va in va_list:
        MMAS_Gain1_l = []
        MMAS_Gain2_l = []
        MMAS_Gain3_l = []
        MMAS_Gain4_l = []

        NJNP_Gain1_l = []
        NJNP_Gain2_l = []
        NJNP_Gain3_l = []
        NJNP_Gain4_l = []

        for i in range(100):
            MMAS_Gain1, MMAS_Gain2, MMAS_Gain3, MMAS_Gain4 = \
                charge_first(points_list=points_list, max_battery=va)
            MMAS_Gain1_l.append(MMAS_Gain1)
            MMAS_Gain2_l.append(MMAS_Gain2)
            MMAS_Gain3_l.append(MMAS_Gain3)
            MMAS_Gain4_l.append(MMAS_Gain4)

            NJNP_Gain1, NJNP_Gain2, NJNP_Gain3, NJNP_Gain4 = \
                charge_first(points_list=points_list, max_battery=va)
            NJNP_Gain1_l.append(NJNP_Gain1)
            NJNP_Gain2_l.append(NJNP_Gain2)
            NJNP_Gain3_l.append(NJNP_Gain3)
            NJNP_Gain4_l.append(NJNP_Gain4)

        MMAS_ylab1.append(np.mean(np.array(MMAS_Gain1_l)))
        MMAS_ylab2.append(np.mean(np.array(MMAS_Gain2_l)))
        MMAS_ylab3.append(np.mean(np.array(MMAS_Gain3_l)))
        MMAS_ylab4.append(np.mean(np.array(MMAS_Gain4_l)))

        NJNP_ylab1.append(np.mean(np.array(NJNP_Gain1_l)))
        NJNP_ylab2.append(np.mean(np.array(NJNP_Gain2_l)))
        NJNP_ylab3.append(np.mean(np.array(NJNP_Gain3_l)))
        NJNP_ylab4.append(np.mean(np.array(NJNP_Gain4_l)))

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.subplot(221)
    plt.plot(va_list, MMAS_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, MMAS_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim(0.5, 2)  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, MMAS_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, MMAS_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, NJNP_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.show()


if __name__ == "__main__":
    # datas存储形式[[起点1，终点1，距离，路径列表]，[起点1，终点2，距离，路径列表]，[起点2，终点3，距离，路径列表]...]
    datas = read_path_map('mapss.txt')

    # 初始化节点类
    # 初始化起点
    A = Point(name='A', location=[0, 0])
    # 初始化目标点
    B = Point(name='B', location=[4, 9])
    C = Point(name='C', location=[16, 10])
    D = Point(name='D', location=[10, 11])
    E = Point(name='E', location=[7, 5])
    F = Point(name='F', location=[8, 8])
    G = Point(name='G', location=[9, 12])
    points_list = [A, B, C, D, E, F, G]

    # 横轴变量求值
    threds = [0.05, 0.1, 0.15, 0.20, 0.25]
    consumes = [50, 100, 150, 200, 250]
    max_batteries = [5400, 7200, 9000, 10800, 13600]

    draw1(threds, '门限')
    draw2(consumes, '消耗')
    draw3(max_batteries, '最大电量')
