"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""
import random

import numpy as np
import copy


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


if __name__ == "__main__":
    # datas存储形式[[起点1，终点1，距离，路径列表]，[起点1，终点2，距离，路径列表]，[起点2，终点3，距离，路径列表]...]
    datas = read_path_map('mapss.txt')

    A = Point(name='A', location=[0, 0], color=[255, 0, 0], charge=0.1)
    B = Point(name='B', location=[4, 9], color=[0, 255, 0], charge=0.3)
    C = Point(name='C', location=[16, 10], color=[0, 0, 255], charge=0.4)
    D = Point(name='D', location=[10, 11], color=[255, 255, 0], charge=0.5)
    E = Point(name='E', location=[7, 5], color=[255, 0, 255], charge=0.5)
    F = Point(name='E', location=[8, 8], color=[255, 0, 255], charge=0.5)
    G = Point(name='G', location=[9, 12], color=[255, 0, 255], charge=0.5)
    points_list = [A, B, C, D, E, F, G]
    goals_l = points_list[1::]
    pl = copy.copy(points_list)

    # 初始化电池电量、电池消耗、门限

    max_battery = 10800
    consume = 200
    thred = 0.2
    v = 1
    # 随机生成节点初始能量(3000,10800J)和消耗速率均为(100J/s)
    origin_energy = []
    for i in range(len(goals_l)):
        origin_energy.append(random.randint(int(thred * max_battery), max_battery))
    # 能量、消耗数据注入点类
    for k, point in enumerate(goals_l):
        point.battery = origin_energy[k]
        point.consume = consume

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
        print(Gain1, Gain2, Gain3, Gain4)

    # # 画图函数
    # import matplotlib.pyplot as plt
    # plt.rc("font", family='FangSong')  # 中文正常显示
    #
    # x, y = [], []
    # for data in result:
    #     x.append(data[0])
    #     y.append(data[1])
    #
    # plt.plot(x, y, 'b*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    # plt.legend()  # 显示上面的label
    # plt.xlabel('充电周期')  # x_label
    # plt.ylabel('收益比')  # y_label
    # plt.ylim(100, 2000)  # 仅设置y轴坐标范围
    # # plt.ylim(-1,1)#仅设置y轴坐标范围
    # plt.show()
