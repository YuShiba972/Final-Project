"""
************************
***  author:Yeller   ***
***  date:2023/03/22 ***
************************
"""
import random
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块
import numpy as np
from PIL import Image


def add_points(in_file, out_file, num):
    # 指定生成数量
    num_of_twos = num
    # 读取数据文件并转换为列表形式
    with open(in_file, 'r') as f:
        data_list = [line.strip() for line in f]
    # 统计 1 的个数
    count = sum(line.count('1') for line in data_list)
    print('输入文件的障碍物比例:', '%', count / 400)

    # 获取数据矩阵的行数和列数
    num_rows, num_cols = len(data_list), len(data_list[0])

    # 将值为 0 的位置加入列表中
    zero_indices = [(i, j) for i in range(num_rows) for j in range(num_cols) if data_list[i][j] == '0']
    # 在列表中随机选择指定数量的位置，并将其值改为 1
    for i, j in random.sample(zero_indices[1::], num_of_twos):
        data_list[i] = data_list[i][:j] + '1' + data_list[i][j + 1:]

    # 将新生成的矩阵写入文件
    with open(out_file, 'w') as f:
        for i, line in enumerate(data_list):
            f.write(line + ('\n' if (i + 1) % 20 != 0 and i != num_rows - 1 else '\n'))

    with open(out_file, 'r') as f:
        data_list = [line.strip() for line in f]

    # 统计 1 的个数
    count = sum(line.count('1') for line in data_list)
    print('禁行区面积比例:', '%', count / 400)


def plot_Bar(bar_data_file, Imgname, shows='False'):
    m = Map()
    m.load_map_file(bar_data_file)
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 构造栅格图片类

    shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=shangetu)  # 修改Surface参数以修改背景
    # shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    result_figure.save(Surface=shangetu_bar, filename=Imgname)
    if shows == 'True':
        from PIL import Image
        Image.open(Imgname).show()
    with open(bar_data_file, 'r') as f:
        data_list = [line.strip() for line in f]
    # 统计 1 的个数
    count = sum(line.count('1') for line in data_list)
    print('禁行区的面积比例为:', '%', count / 4)

    return shangetu_bar


def plot_BarGoal(bar_data_file, points, Imgname='禁行区+目标点.jpg', shows='False'):
    points_location_list = list(map(lambda x: x.location, points))
    m = Map()
    m.load_map_file(bar_data_file)
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 构造栅格图片类

    shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=shangetu)

    shangetu_bar_goal = result_figure.goal_point(points_location_list, Surface=shangetu_bar)
    result_figure.save(Surface=shangetu_bar_goal, filename=Imgname)
    if shows == 'True':
        from PIL import Image
        Image.open(Imgname).show()
    return result_figure, shangetu_bar_goal


def cycle_run(bar_data_file, points, out_file='单点路径列表_tem.txt'):  # 获取单个目标点到所有点的最短距离集合
    points_location_list = list(map(lambda x: x.location, points))

    m = Map()
    m.load_map_file(bar_data_file)
    map_data = m.data  # map_data为numpy数组
    best_path_l = []
    distance_l = []
    start = points_location_list[2]
    points_location_list.remove(points_location_list[2])
    while points_location_list:
        aco = ACO(map_data=map_data, start=start, end=points_location_list[-1],
                  max_iter=50, ant_num=400, pher_imp=1, dis_imp=5, evaporate=0.1, pher_init=8)
        points_location_list.remove(points_location_list[-1])
        aco.run()
        # aco.plot_iteration_path()
        best_path_l.append(aco.way_data_best)  # 存储最优路径列表，形式为[(0,0),(1,2)...]
        distance_l.append(aco.way_len_best)  # 存储对应的距离列表，形式为[l1,l2...]
    with open(out_file, 'w') as f:
        f.write(str(best_path_l))
    return best_path_l, distance_l


def cycle_run_one(bar_data_file, points, out_file='单点路径列表_tem.txt'):  # 获取单个目标点到所有点的最短距离集合
    points_location_list = list(map(lambda x: x.location, points))

    m = Map()
    m.load_map_file(bar_data_file)
    map_data = m.data  # map_data为numpy数组
    best_path_l = []
    distance_l = []
    points_location_list = points_location_list[0:2:]
    for k, i in enumerate(points_location_list):
        try:
            j = points_location_list[k + 1]
        except:
            break
        aco = ACO(map_data=map_data, start=points_location_list[0], end=j,
                  max_iter=100, ant_num=400, pher_imp=1, dis_imp=5, evaporate=0.1, pher_init=8)
        aco.run()
        aco.plot_iteration_path()
        best_path_l.append(aco.way_data_best)  # 存储最优路径列表，形式为[(0,0),(1,2)...]
        distance_l.append(aco.way_len_best)  # 存储对应的距离列表，形式为[l1,l2...]
    with open(out_file, 'w') as f:
        f.write(str(best_path_l))
    return best_path_l, distance_l


def plot_OneToOne(Bg_fig, Surface, input_file, out_file='单点对单点路径展示图.jpg', shows='False'):
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255],
                   [255, 255, 0], [0, 47, 167], [47, 0, 167], [167, 47, 0], [160, 255, 255],
                   [100, 100, 255], [255, 100, 255], [47, 100, 167], [167, 47, 100], [40, 255, 255], ]
    with open(input_file) as f:
        best_path_l = eval(f.readline())
    way_picture = None
    for k, i in enumerate(best_path_l):
        if way_picture:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=Surface, color=route_color[k])
    Bg_fig.save(Surface=way_picture, filename=out_file)
    if shows == 'True':
        from PIL import Image
        Image.open(out_file).show()


def plot_OneToAll(Bg_fig, Surface, input_file, out_file='单点对多点路径展示图.jpg', shows='False'):
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255],
                   [255, 255, 0], [0, 47, 167], [47, 0, 167], [167, 47, 0], [160, 255, 255],
                   [100, 100, 255], [255, 100, 255], [47, 100, 167], [167, 47, 100], [40, 255, 255], ]
    with open(input_file) as f:
        best_path_l = eval(f.readline())
    way_picture = None
    for k, i in enumerate(best_path_l):
        if way_picture:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=Surface, color=route_color[k])
    Bg_fig.save(Surface=way_picture, filename=out_file)
    if shows == 'True':
        from PIL import Image
        Image.open(out_file).show()


def plot_AllToAll(Bg_fig, Surface, input_file, out_file='单点对多点路径展示图集合.jpg', shows='False'):
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255],
                   [255, 255, 0], [0, 47, 167], [47, 0, 167], [167, 47, 0], [160, 255, 255],
                   [100, 100, 255], [255, 100, 255], [47, 100, 167], [167, 47, 100], [40, 255, 255], ]
    with open(input_file) as f:
        best_path_l = eval(f.readline())
    way_picture = None
    for k, i in enumerate(best_path_l):
        if way_picture:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=Surface, color=route_color[k])
    Bg_fig.save(Surface=way_picture, filename=out_file)
    if shows == 'True':
        from PIL import Image
        Image.open(out_file).show()


class Point:
    def __init__(self, name='', location=None, battery=0, consume=0,
                 max_battery=10800, threshold=0.2, velocity=1):
        self.name = name
        self.location = location
        self.battery = battery
        self.max_battery = max_battery
        self.consume = consume
        self.threshold = threshold
        self.velocity = velocity

    @staticmethod
    def points6_bar10():
        A = Point(name='A', location=[0, 0])
        B = Point(name='B', location=[1, 18])
        C = Point(name='C', location=[19, 2])
        D = Point(name='D', location=[8, 4])
        E = Point(name='E', location=[4, 8])
        F = Point(name='F', location=[15, 15])
        points_list = [A, B, C, D, E, F]
        return points_list


import pandas as pd
import copy


################################################## 1 蚁群算法路径规划 ###########################################
# 参数α和β反映了信息素与启发信息的相对重要性，用来调节信息素与距离的重要程度。
# 其中如果令α=0，β!=0该算法则成了贪婪启发式算法。
# 单只蚂蚁仅根据距离来选择下一城市。如果令α!=0，β=0，则单只蚂蚁仅根据信息素来选择下一城市。

class ACO:
    def __init__(self, map_data, start, end, max_iter=500, ant_num=600, pher_imp=1.0, dis_imp=5, evaporate=0.1,
                 pher_init=8) -> None:
        '''
            Params:
            --------
                pher_imp : 信息素重要性系数
                dis_imp  : 距离重要性系数
                evaporate: 信息素挥发系数(指保留的部分)
                pher_init: 初始信息素浓度
        '''

        # Step 0: 参数定义及赋值
        self.max_iter = max_iter  # 最大迭代次数
        self.ant_num = ant_num  # 蚂蚁数量
        self.ant_gener_pher = 1  # 每只蚂蚁携带的最大信息素总量
        self.pher_init = pher_init  # 初始信息素浓度
        self.ant_params = {  # 生成蚂蚁时所需的参数
            'dis_imp': dis_imp,
            'pher_imp': pher_imp,
            'start': start,
            'end': end
        }
        self.map_data = map_data.copy()  # 地图数据
        self.map_lenght = self.map_data.shape[0]  # 地图尺寸,用来标定蚂蚁的最大体力
        self.pher_data = pher_init * np.ones(shape=[self.map_lenght * self.map_lenght,
                                                    self.map_lenght * self.map_lenght])  # 信息素矩阵
        self.evaporate = evaporate  # 信息素挥发系数
        self.way_len_best = 999999
        self.way_data_best = []  # 最短路径对应的节点信息，画路线用

        self.generation_aver = []  # 每代的平均路径(大小)，绘迭代图用
        self.generation_best = []  # 每代的最短路径(大小)，绘迭代图用

    def run(self):
        # 总迭代开始
        for i in range(self.max_iter):
            success_way_list = []
            # print('第',i,'代: ',end = '')
            # Step 1:当代若干蚂蚁依次行动
            for j in range(self.ant_num):
                ant = Ant(start=self.ant_params['start'], end=self.ant_params['end'], max_step=self.map_lenght * 3,
                          pher_imp=self.ant_params['pher_imp'], dis_imp=self.ant_params['dis_imp'])
                ant.run(map_data=self.map_data.copy(), pher_data=self.pher_data)
                if ant.successful == True:  # 若成功，则记录路径信息
                    success_way_list.append(ant.record_way)
            # print(' 成功率:',len(success_way_list),end= '')
            # Step 2:计算每条路径对应的长度，后用于信息素的生成量
            way_lenght_list = []
            # way就是在成功列表里面的
            for j in success_way_list:
                way_lenght_list.append(self.calc_total_lenght(j))
            # Step 3:更新信息素浓度
            #  step 3.1: 挥发
            self.pher_data = self.evaporate * self.pher_data
            #  step 3.2: 叠加新增信息素
            for k, j in enumerate(success_way_list):
                j_2 = np.array(j)
                j_3 = j_2[:, 0] * self.map_lenght + j_2[:, 1]
                for t in range(len(j_3) - 1):
                    self.pher_data[j_3[t]][j_3[t + 1]] += self.ant_gener_pher / way_lenght_list[k]
            # Step 4: 当代的首尾总总结工作
            if not way_lenght_list:
                continue

            # 当代寻路数据
            self.generation_aver.append(np.average(way_lenght_list))
            self.generation_best.append(min(way_lenght_list))

            if self.way_len_best > min(way_lenght_list):
                a_1 = way_lenght_list.index(min(way_lenght_list))
                self.way_len_best = way_lenght_list[a_1]
                self.way_data_best = copy.deepcopy(success_way_list[a_1])
            # print('平均长度:', np.average(way_lenght_list), '最短:', np.min(way_lenght_list))

    def calc_total_lenght(self, way):  # 每次的way在成功列表里面
        lenght = 0
        for j1 in range(len(way) - 1):
            a1 = abs(way[j1][0] - way[j1 + 1][0]) + abs(way[j1][1] - way[j1 + 1][1])
            if a1 == 2:
                lenght += 1.41421
            else:
                lenght += 1
        return lenght

    def plot_iteration_path(self):
        import matplotlib.pyplot as plt
        num_iterations = len(self.generation_aver)
        x = list(range(num_iterations))

        plt.rcParams['font.family'] = ['SimHei']
        plt.plot(x, self.generation_aver, label='每代平均路径长度')
        plt.plot(x, self.generation_best, label='每代最优路径长度')
        plt.legend()
        plt.xlabel('蚂蚁迭代数')
        plt.ylabel('路径长度')
        plt.title('蚁群算法迭代图')
        plt.show()


########################################################################################################################
# Ant只管通过地图数据以及信息素数据，输出一条路径。
class Ant():
    def __init__(self, start, end, max_step, pher_imp, dis_imp) -> None:
        self.max_step = max_step  # 蚂蚁最大行动力
        self.pher_imp = pher_imp  # 信息素重要性系数
        self.dis_imp = dis_imp  # 距离重要性系数
        self.start = start  # 蚂蚁初始位置[y,x] = [0,0],考虑到列表索引的特殊性，先定y，后定x
        self.destination = end  # 默认的终点节点(在run方法中会重新定义该值)
        self.successful = True  # 标志蚂蚁是否成功抵达终点
        self.record_way = [start]  # 路径节点信息记录

    def run(self, map_data, pher_data):
        self.position = copy.deepcopy(self.start)
        # Step 1:不断找下一节点，直到走到终点或者力竭
        for i in range(self.max_step):
            r = self.select_next_node(map_data, pher_data)
            if r == False:
                self.successful = False
                break
            else:
                if self.position == self.destination:
                    break
        else:
            self.successful = False

    def select_next_node(self, map_data, pher_data):
        '''
        Function:
        ---------
        选择下一节点，结果直接存入self.postion，仅返回一个状态码True/False标志选择的成功与否。
        '''
        y_1 = self.position[0]
        x_1 = self.position[1]
        # Step 1:计算理论上的周围节点
        node_be_selected = [[y_1 - 1, x_1 - 1], [y_1 - 1, x_1], [y_1 - 1, x_1 + 1],  # 上一层
                            [y_1, x_1 - 1], [y_1, x_1 + 1],  # 同层
                            [y_1 + 1, x_1 - 1], [y_1 + 1, x_1], [y_1 + 1, x_1 + 1],  # 下一层
                            ]
        # Step 2:排除非法以及障碍物节点
        node_be_selected_1 = []
        for i in node_be_selected:
            if i[0] < 0 or i[1] < 0:
                continue
            if i[0] >= len(map_data) or i[1] >= len(map_data):
                continue
            if map_data[i[0]][i[1]] == 0:
                node_be_selected_1.append(i)
        if len(node_be_selected_1) == 0:  # 如果无合法节点，则直接终止节点的选择
            return False
        if self.destination in node_be_selected_1:  # 如果到达终点旁，则直接选中终点
            self.position = self.destination
            self.record_way.append(copy.deepcopy(self.position))
            map_data[self.position[0]][self.position[1]] = 1
            return True
        # Step 3:计算节点与终点之间的距离，构建距离启发因子
        dis_1 = []  # 距离启发因子
        for i in node_be_selected_1:
            dis_1.append(((self.destination[0] - i[0]) ** 2 + (self.destination[1] - i[1]) ** 2) ** 0.5)
        # Step 3.1:倒数反转
        for j in range(len(dis_1)):
            dis_1[j] = 1 / dis_1[j]

        # Step 4:计算节点被选中的概率
        prob = []
        for i in range(len(node_be_selected_1)):
            p = (dis_1[i] ** self.dis_imp) * (pher_data[y_1 * len(map_data) + x_1][
                                                  node_be_selected_1[i][0] * len(map_data) + node_be_selected_1[i][
                                                      1]] ** self.pher_imp)
            prob.append(p)
        # Step 5:轮盘赌选择某节点
        prob_sum = sum(prob)
        for i in range(len(prob)):
            prob[i] = prob[i] / prob_sum
        rand_key = np.random.rand()
        for k, i in enumerate(prob):
            if rand_key <= i:
                break
            else:
                rand_key -= i
        # Step 6:更新当前位置，并记录新的位置，将之前的位置标记为不可通过
        self.position = copy.deepcopy(node_be_selected_1[k])
        self.record_way.append(copy.deepcopy(self.position))
        map_data[self.position[0]][self.position[1]] = 1
        return True


def ACO_Generate(bar_data_file, points, filename):
    datas = []
    points_location_list = list(map(lambda x: x.location, points))
    with open(bar_data_file, 'r') as f:
        data = [list(line.strip('\n')) for line in f.readlines()]
    npdata = np.array(data, dtype=np.int64)
    for point in points_location_list:
        tem = points_location_list.copy()  # 新分配内存区域
        tem.remove(point)
        for goal_point in tem:
            aco = ACO(map_data=npdata, start=point, end=goal_point, max_iter=300, ant_num=400)
            aco.run()
            datas.append([point, goal_point, aco.way_len_best, aco.way_data_best])
    for data in datas:
        print(data)
    with open(filename, mode='w') as f:
        # path_data依次为，起点，终点，路径长度，路径列表
        for data in datas:
            f.writelines(str(data) + '\n')


def read(Bg_fig, Surface, po_index, input_file='Result_Package/节点避障距离文件.txt', ):
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255],
                   [255, 255, 0], [0, 47, 167], [47, 0, 167], [167, 47, 0], [160, 255, 255],
                   [100, 100, 255], [255, 100, 255], [47, 100, 167], [167, 47, 100], [40, 255, 255]]
    with open(input_file, 'r') as f:
        # 初始化结果列表
        datas = []
        # 逐行读取文件中的文本数据
        for line in f:
            # 去除每行文本两端的空格和换行符
            line = line.strip()
            # 将文本转换为列表对象，并添加到结果列表中
            datas.append(eval(line))

    datas_piece = [datas[i:i + 5] for i in range(0, len(datas), 5)]
    draw_datas = []  # 绘图的路径列表
    # 遍历每个子列表
    for piece in datas_piece:
        sub_piece = []
        # 遍历每个元素
        for item in piece:
            # 将第三个元素（即嵌套列表）中的元素取出来添加到新的子列表中
            sub_piece.append(item[3])
        # 将新的子列表添加到结果列表中
        draw_datas.append(sub_piece)

    way_picture = None
    for k, i in enumerate(draw_datas[po_index - 1]):
        if way_picture:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = Bg_fig.draw_way(way_data=i, Surface=Surface, color=route_color[k])
    Bg_fig.save(Surface=way_picture, filename='Result_Package/单点对多点路径展示图{}.jpg'.format(po_index))
