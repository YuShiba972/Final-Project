"""
************************
***  author:Yeller   ***
***  date:2023/02/20 ***
************************
"""
"""
************************
***  author:Yeller   ***
***  date:2023/02/17 ***
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

    points = [[0, 0], [16, 10], [4, 9], [10, 11]]

    ###################################################################################
    # 背景选择
    # blank = result_figure.white_BG()  # 空白背景
    # shangetu = result_figure.shangetu_BG()  # 栅格背景
    # shangetu_bar = result_figure.barrier(Surface=blank)  #
    # shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    ###################################################################################

    ###################################################################################
    # 控制台打印
    # path_data_l = []
    # distance_l = []

    # for i in range(len(points) - 1):
    datas = cycle_run(map_data=map_data, points=points)
    for data in datas:
        print(data)
    # with open('maps.txt', mode='w') as f:
    #     # datas依次为，起点，终点，路径长度，路径列表
    #     for data in datas:
    #         f.write(str(path_data[0]) + '/' + str(path_data[1]) + '/'
    #                 + str(path_data[2]) + '/' + str(path_data[3]) + '\n')
    # b = []

    with open('maps.txt', mode='w') as f:
        # path_data依次为，起点，终点，路径长度，路径列表
        for data in datas:
            f.writelines(str(data)+'\n')

