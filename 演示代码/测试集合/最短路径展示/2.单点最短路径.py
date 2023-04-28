"""
************************
***  author:Yeller   ***
***  date:2023/02/16 ***
************************
"""
from lddya.Algorithm import ACO  # 导入ACO算法
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块


def cycle_run(map_data, points):  # 获取单个目标点到所有点的最短距离集合
    best_path_l = []
    distance_l = []
    for k, i in enumerate(points):
        try:
            j = points[k + 1]
        except:
            break
        aco = ACO(map_data=map_data, start=points[0], end=j)
        aco.run()
        best_path_l.append(aco.way_data_best)  # 存储最优路径列表，形式为[(0,0),(1,2)...]
        distance_l.append(aco.way_len_best)  # 存储对应的距离列表，形式为[l1,l2...]
    return best_path_l, distance_l


def plot_one_to_more_path(Surface):
    way_picture = None
    for k, i in enumerate(best_path_l):
        if way_picture:
            way_picture = result_figure.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = result_figure.draw_way(way_data=i, Surface=Surface, color=route_color[k])
    return way_picture


def cycle_and_plot(map_data, points, Surface, route_colors, plot_path=True):
    best_path_l = []
    distance_l = []
    way_picture = None

    for k, i in enumerate(points[:-1]):  # 遍历目标点
        j = points[k + 1]
        aco = ACO(map_data=map_data, start=i, end=j)
        aco.run()
        best_path_l.append(aco.way_data_best)
        distance_l.append(aco.way_len_best)

        if plot_path:  # 绘制路径图
            if way_picture:
                way_picture = result_figure.draw_way(way_data=aco.way_data_best, Surface=way_picture,
                                                     color=route_colors[k])
            else:
                way_picture = result_figure.draw_way(way_data=aco.way_data_best, Surface=Surface, color=route_colors[k])

    if plot_path:  # 保存路径图
        result_figure.save(Surface=way_picture)

    print('出发点为{}，目标点的集合为：{}'.format(points[0], points[1:]))
    for i in points[1:]:  # 输出距离信息
        print('{}到点{}的距离为：{}'.format(points[0], i, distance_l[points.index(i) - 1]))
    print('{}最近的点为：{}，距离为：{}'.format(points[0], points[distance_l.index(min(distance_l)) + 1], min(distance_l)))
    return best_path_l, distance_l


if __name__ == "__main__":
    ###################################################################################
    # 参数导入与获取
    m = Map()
    m.load_map_file('Map_In10.txt')
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据

    points = [[0, 0], [4, 9], [16, 10], [10, 11]]
    route_color = [[60, 155, 60], [255, 255, 0], [255, 0, 0], [0, 255, 255], [0, 255, 255]]

    ###################################################################################

    ###################################################################################
    # 背景选择
    blank = result_figure.white_BG()  # 空白背景
    shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=shangetu)
    shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)

    best_path_l, distance_l = cycle_and_plot(map_data, points, shangetu_bar_goal, route_color)

    # ###################################################################################

    ###################################################################################
    # 画一对多的路径图
    # way_picture = plot_one_to_more_path(Surface=shangetu_bar_goal)
    # result_figure.save(Surface=way_picture)
    ###################################################################################

    ###################################################################################
    # 控制台打印
    # print('出发点为{}，目标点的集合为：{}'.format(points[0], points[1::]))
    # for i in points[1::]:
    #     print('{}到点{}的距离为：{}'.format(
    #         points[0], i, distance_l[points.index(i) - 1]))
    # print('{}最近的点为：{}，距离为：{}'.format(
    #     points[0], points[distance_l.index(min(distance_l)) + 1], min(distance_l)))
    ###################################################################################
