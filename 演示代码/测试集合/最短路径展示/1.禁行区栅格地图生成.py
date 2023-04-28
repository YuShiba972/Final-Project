"""
************************
***  author:Yeller   ***
***  date:2023/02/16 ***
************************
"""

from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块


def draw_map(points=[], filename='map.txt'):
    ###################################################################################
    points = map(lambda x: x.location, points)
    m = Map()
    m.load_map_file(filename)
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据
    # points = [[0, 0], [4, 9], [16, 10], [10, 11]]
    ###################################################################################

    ###################################################################################
    # blank = result_figure.white_BG()  # 空白背景
    shangetu = result_figure.shangetu_BG()  # 栅格背景
    ##################################################################################

    # shangetu_bar = result_figure.barrier(Surface=shangetu)  # 修改Surface参数以修改背景
    # shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    result_figure.save(Surface=shangetu, filename='map.jpg')
    ###################################################################################

draw_map()