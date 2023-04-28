"""
************************
***  author:Yeller   ***
***  date:2023/02/211 ***
************************
"""
from lddya.Algorithm import ACO  # 导入ACO算法
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块
import taichi as ti

# 生成单点最短路径，需要的参数为(地图数据，充电点的集合)
def cycle_run(map_data, points):  # 获取单个目标点到所有点的最短距离集合
    datas = []
    for point in points:
        tem = points.copy()  # 新分配内存区域
        tem.remove(point)
        for goal_point in tem:
            aco = ACO(map_data=map_data, start=point, end=goal_point)
            aco.run()
            datas.append([point, goal_point, aco.way_len_best, aco.way_data_best])
    return datas


if __name__ == "__main__":
    ###################################################################################
    # 参数导入与获取
    m = Map()
    m.load_map_file('Map_In10.txt')
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据

    points = [[0, 0], [4, 9], [16, 10], [10, 11], [7, 5], [8, 8], [9, 12]]

    ###################################################################################
    # 背景选择
    m, n = 0, 0
    for i in map_data:
        for j in i:
            if j == 1:
                n = n + 1
            m = m + 1
    print('禁行区的比例为：%{}'.format(m/n))
    result_figure = ShanGeTu(map_data)  # 加载地图数据
    blank = result_figure.white_BG()  # 空白背景
    shangetu_bar = result_figure.barrier(Surface=blank)  # 修改Surface参数以修改背景
    shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    result_figure.save(Surface=shangetu_bar_goal)
    ###################################################################################

    datas = cycle_run(map_data=map_data, points=points)

    with open('mapss.txt', mode='w') as f:
        # path_data依次为，起点，终点，路径长度，路径列表
        for data in datas:
            f.writelines(str(data) + '\n')


