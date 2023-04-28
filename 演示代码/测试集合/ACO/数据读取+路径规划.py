"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""

# 将txt转换为列表数组存储
import numpy as np


def read_path_map(filename):
    datas = []
    with open(filename, 'r') as f:
        for line in f:
            data = line.strip().split('/')
            location, destination, distance, battery = eval(data[0]), eval(data[1]), eval(data[2]), eval(data[3])
            datas.append([location, destination, distance, battery])
    return datas


class Point:
    def __init__(self, battery=0, charge=0.5, consume=0, color=None, name='', location=None):
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


def dis_depends(current, points):
    points.remove(current)
    if points:
        step_tem = None
        # path_tem = None
        min_dis = 999
        for i in datas:
            if i[0] == current:
                if i[2] < min_dis:
                    min_dis = i[2]
                    step_tem = i[1]
                    # path_tem = i[3]
        current = step_tem
        # path.append(path_tem)
        visited.append(current)
        path_len.append(min_dis)
    else:
        dis_depends(current, points)

    return visited


if __name__ == "__main__":
    # datas存储形式[[起点1，终点1，距离，路径列表]，[起点1，终点2，距离，路径列表]，[起点2，终点3，距离，路径列表]...]
    datas = read_path_map('maps.txt')

    A = Point(name='A', location=[0, 0], color=[255, 0, 0], charge=0.3)
    B = Point(name='B', location=[4, 9], color=[0, 255, 0], charge=0.3)
    C = Point(name='C', location=[16, 10], color=[0, 0, 255], charge=0.3)
    D = Point(name='D', location=[10, 11], color=[255, 255, 0], charge=0.3)
    points_list = [A, B, C, D]
    points = list(map(lambda x: x.location, points_list))
    visited = [[0, 0]]
    current = [0, 0]
    path = [[0, 0]]
    path_len = []
    print(dis_depends(current,points))
    # step_tem = None
    # path_tem = None
    # min_dis = 999
    # for k, i in enumerate(datas):
    #     if i[0] == current:
    #         if i[2] < min_dis:
    #             min_dis = i[2]
    #             step_tem = i[1]
    #             path_tem = i[3]
    #     if i[1] == current:
    #         if i[2] < min_dis:
    #             min_dis = i[2]
    #             step_tem = i[0]
    #             path_tem = i[3]
    # if step_tem not in visited:
    #     current = step_tem
    #     path.append(path_tem)
    #     path_len.append(min_dis)
    #     visited.append(current)
    # print(visited, path_len)

    # print(path, current)
