"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""


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
    datas = read_path_map('maps.txt')

    A = Point(name='A', location=[0, 0], color=[255, 0, 0], charge=0.1)
    B = Point(name='B', location=[4, 9], color=[0, 255, 0], charge=0.3)
    C = Point(name='C', location=[16, 10], color=[0, 0, 255], charge=0.4)
    D = Point(name='D', location=[10, 11], color=[255, 255, 0], charge=0.5)
    points_list = [A, B, C, D]
    points = list(map(lambda x: x.location, points_list))

    # 路径数据注入点类
    for point in points_list:
        for data in datas:
            if point.location == data[0]:
                point.mesg.append(data)

    find_path = []
    current = A
    visited = [A.location]
    print('起点为：{}，坐标为{}'.format(A.name, A.location))

    cost = 0
    charge_total = 0
    while True:
        min_dis = 999
        min_location = None
        min_path = None

        for i in current.mesg:
            tem_next = i[1]
            tem_dis = i[2]
            tem_path = i[3]

            if tem_dis < min_dis and tem_next not in visited:
                min_dis = tem_dis
                min_location = tem_next
                min_path = tem_path
        visited.append(min_location)

        for point in points_list:
            if point.location == min_location:
                current = point
                # find_path.append([visited[-1],min_location,min_dis,min_path])

        print('下一个经过的充电点为：{}，坐标为{}，距离为{}'.format(current.name, min_location, min_dis))
        cost = cost + min_dis
        if len(visited) == 4:
            print('路径列表为：', visited)
            break

    print('在充电小车电量充足的情况下，贪心算法的总距离为：', cost)
    for k, i in enumerate(visited):
        for j in points_list:
            if i == j.location:
                charge_total = charge_total + j.charge
                print('经过第{}个点的总充电量为：{}个单位电池容量'.format(k + 1, charge_total))

    one_energy = 10800  # 10800焦耳
    total_energy = one_energy * charge_total
    print('小车充电的总能量为:', total_energy, 'J')
