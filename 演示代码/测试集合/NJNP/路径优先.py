"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
************************
"""
import random


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
    datas = read_path_map('../../方法库/新建/mapss.txt')

    A = Point(name='A', location=[0, 0], color=[255, 0, 0], charge=0.1)
    B = Point(name='B', location=[4, 9], color=[0, 255, 0], charge=0.3)
    C = Point(name='C', location=[16, 10], color=[0, 0, 255], charge=0.4)
    D = Point(name='D', location=[10, 11], color=[255, 255, 0], charge=0.5)
    E = Point(name='E', location=[7, 5], color=[255, 0, 255], charge=0.5)
    F = Point(name='E', location=[8, 8], color=[255, 0, 255], charge=0.5)
    G = Point(name='G', location=[9, 12], color=[255, 0, 255], charge=0.5)
    points_list = [A, B, C, D, E, F, G]
    points = list(map(lambda x: x.location, points_list))

    result = []
    for num in range(1,20):
        # 随机生成节点初始能量(0,10800J)和消耗速率(100J/s),休眠阈值为:3000J
        orgin_energy = []
        consume = []
        for i in range(len(points_list) - 1):
            orgin_energy.append(random.randint(4000, 10800))
            consume.append(random.randint(300, 500))

        # 路径数据注入点类
        for point in points_list:
            for data in datas:
                if point.location == data[0]:
                    point.mesg.append(data)
        # 能量数据注入点类
        for k, point in enumerate(points_list[1::]):
            point.battery = orgin_energy[k]

            # consume[k] = point.consume

        #################################################################
        # NJNP算法，距离最近优先
        find_path = []
        current = A
        visited = [A.location]
        print('起点为：{}，坐标为{}'.format(A.name, A.location))

        cost = 0  # 行驶距离
        eff = 0  # 有效充电电量
        charge_total = 0
        eff_one = 0
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
                    eff_one = 10800 - point.battery
                    current = point
                    # find_path.append([visited[-1],min_location,min_dis,min_path])
            print('下一个经过的充电点为：{}，坐标为{}，距离为{}，充电电量为{}'.format(current.name, min_location, min_dis, eff_one))
            cost = cost + min_dis
            eff = eff + eff_one
            if len(visited) == len(points_list)-1:
                print('在充电小车电量充足的情况下，NJNP算法的总距离为：', cost)
                print('路径列表为：', visited)
                print('有效电量为：', eff)
                print('收益比，有效充电电量与行驶距离比为：', eff / cost)
                break
        result.append((num, eff/cost))
    print(result)



    # 画图函数
    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')  # 中文正常显示

    x, y = [], []
    for data in result:
        x.append(data[0])
        y.append(data[1])

    plt.plot(x, y, 'b*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.legend()  # 显示上面的label
    plt.xlabel('充电周期')  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim(100, 2000)  # 仅设置y轴坐标范围
    # plt.ylim(-1,1)#仅设置y轴坐标范围
    plt.show()
