"""
************************
***  author:Yeller   ***
***  date:2023/02/12 ***
************************
"""
from lddya.Algorithm import ACO  # 导入ACO算法
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块
import numpy as np
import random

m = Map()
m.load_map_file('Map_In10.txt')  # 读取地图文件
# l = [[1,0,1,0],[0,1,0,0],[0,0,0,0],[1,1,0,0]]

# 点坐标映射到栅格图位置需要加1，点是从0开始，栅格图编码从1开始
point = [[0, 0], [4, 9], [16, 10], [10, 11], [12, 15], [6, 19], [1, 1], [16, 4]]
# map_data = np.array(l)
# point = [[0,0],[0,1]]
map_data = m.data

# 障碍物数组
# number1 = -1
# number2 = -1
# l = []
# for i in map_data:
#     number1 = number1 + 1
#     for j in i:
#         number2 = number2 + 1
#         if j == 1:
#             l.append([number1, number2])
# print(l)
# point = np.zeros(1, 5)
# for i in range(int(point.shape[0])):
#     for j in range(int(point.shape[1])):
#         point[i][j] = random.randint(0, 1)
# print(point)

# 随机充电点产生
# a = [[random.randint(0,20) for j in range(2)] for i in range(5)]
# print((a))


# aco = ACO(map_data=map_data, start=[0, 0],
#           end=[10, 10])  # 初始化ACO，不调整任何参数的情况下，仅提供地图数据即可，本行中数据由Map.data提供，start跟end都是[y,x]格式，默认[0,0],[19,19]。
# aco.run()  # 迭代运行

###################  地形建模函数
best_list = []
sfig = ShanGeTu(map_data=map_data)  # 初始化栅格图绘制模块
sfig.goal(point,background)
aco = ACO(map_data=map_data, start=[0,0],
          end=[4, 9])  # 初始化ACO，不调整任何参数的情况下，仅提供地图数据即可，本行中数据由Map.data提供，start跟end都是[y,x]格式，默认[0,0],[19,19]。
best_list.append(aco.run())  # 迭代运行
# print(best_list)
sfig.draw_way(best_list)  # 绘制路径信息，路径数据由ACO.way_data_best提供。

aco = ACO(map_data=map_data, start=[0,0],
          end=[16, 10])  # 初始化ACO，不调整任何参数的情况下，仅提供地图数据即可，本行中数据由Map.data提供，start跟end都是[y,x]格式，默认[0,0],[19,19]。
aco.run()  # 迭代运行
sfig.draw_way(aco.way_data_best)  # 绘制路径信息，路径数据由ACO.way_data_best提供。

# sfig.draw_way()
sfig.save('123.jpg')  # 保存栅格图数据为'123.jpg'


def plot_best_line(start, end):
    aco = ACO(map_data=map_data, start=start,
              end=end)  # 初始化ACO，不调整任何参数的情况下，仅提供地图数据即可，本行中数据由Map.data提供，start跟end都是[y,x]格式，默认[0,0],[19,19]。
    aco.run()  # 迭代运行
    sfig.draw_way(aco.way_data_best)


start = [0, 0]

# for i in point:
#     plot_best_line(start, i)

sfig.save('123.jpg')  # 保存栅格图数据为'123.jpg'
# dfig = IterationGraph(data_list=[aco.generation_aver, aco.generation_best],  # 绘制数据: 每代平均、每代最优路径信息
#                       style_list=['--r', '-.g'],  # 线型 (规则同plt.plot()中的线型规则)
#                       legend_list=['每代平均', '每代最优'],  # 图例 (可选参数，可以不写)
#                       xlabel='迭代次数',  # x轴标签，默认“x”
#                       ylabel='路径长度'  # y轴标签，默认“y”
#                       )  # 初始化迭代图绘制模块
# dfig.save('321.jpg')                     #迭代图保存为321.jpg
