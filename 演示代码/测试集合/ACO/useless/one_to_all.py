"""
************************
***  author:Yeller   ***
***  date:2023/02/13 ***
************************
"""
from lddya.Algorithm import ACO  # 导入ACO算法
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块
import numpy as np
import random
import one_to_all_shorter


def cycle_run(map_data, points):  # 获取单个目标点到所有点的最短距离集合
    l = []
    # points = [[0, 0], [4, 9], [16, 10], [10, 11], [12, 15], [6, 19], [1, 1], [16, 4]]
    for k, i in enumerate(points):
        try:
            j = points[k + 1]
        except:
            break
        aco = ACO(map_data=map_data, start=[0, 0], end=j)
        aco.run()
        l.append(aco.way_data_best)
    return l


if __name__ == "__main__":
    ###################################################################################
    m = Map()
    m.load_map_file('Map_In10.txt')
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据
    points = [[0, 0], [4, 9], [16, 10], [10, 11]]
    ###################################################################################

    ###################################################################################
    blank = result_figure.white_BG()  # 空白背景
    # shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=blank)  #
    shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    ###################################################################################

    ###################################################################################
    # aco = ACO(map_data=map_data, start=[1, 1], end=[10, 11])  # 坐标格式[y,x]
    # aco.run()  # 迭代运行
    ll = cycle_run(map_data=map_data, points=points)
    way_picture = []
    route_color = [[60, 155, 60], [255, 255, 0], [255, 0, 0], [0, 255, 255], [0, 255, 255]]
    for k, i in enumerate(ll):
        if way_picture:
            way_picture = result_figure.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = result_figure.draw_way(way_data=i, Surface=shangetu_bar, color=route_color[k])
    result_figure.save(Surface=way_picture)
