"""
************************
***  author:Yeller   ***
***  date:2023/02/16 ***
************************
"""
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
        aco = ACO(map_data=map_data, start=[0, 0], end=j)
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


def find_cloest_points(points):
    best_path_l, distance_l = cycle_run(map_data=map_data, points=points)
    print('出发点为{}，目标点的集合为：{}'.format(points[0], points[1::]))
    for i in points[1::]:
        print('{}到点{}的距离为：{}'.format(
            points[0], i, distance_l[points.index(i) - 1]))
    print('{}最近的点为：{}，距离为：{}'.format(
        points[0], points[distance_l.index(min(distance_l)) + 1], min(distance_l)))
    print('________________________________')

    # points[0], points[distance_l.index(min(distance_l)) + 1]


if __name__ == "__main__":
    ###################################################################################
    # 参数导入与获取
    m = Map()
    m.load_map_file('Map_In10.txt')
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据

    # points = [[0, 0], [4, 9]]
    points = [[0, 0], [4, 9], [16, 10], [10, 11]]
    route_color = [[60, 155, 60], [255, 255, 0], [255, 0, 0], [0, 255, 255], [0, 255, 255]]
    # best_path_l, distance_l = cycle_run(map_data=map_data, points=points)
    ###################################################################################

    ###################################################################################
    # 背景选择
    blank = result_figure.white_BG()  # 空白背景
    # shangetu = result_figure.shangetu_BG()  # 栅格背景
    # shangetu_bar = result_figure.barrier(Surface=shangetu)  #
    shangetu_bar_goal = result_figure.goal_point(points, Surface=blank)  # 画目标点
    ###################################################################################

    ###################################################################################
    # 画一对多的路径图
    # way_picture = plot_one_to_more_path(Surface=shangetu_bar_goal)
    # result_figure.save(Surface=way_picture)
    ###################################################################################

    # 每循环一次就找到一条最短路径
    # for i in range(len(points) - 1):
    best_path_l, distance_l = cycle_run(map_data=map_data, points=points)
    print(best_path_l[distance_l.index(min(distance_l))])

    # points = points[1::]

