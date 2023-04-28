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
    for k, i in enumerate(points):
        try:
            j = points[k + 1]
        except:
            break
        aco = ACO(map_data=map_data, start=points[0], end=j)
        aco.run()
        # print('点{}到{}的最短距离为：{}，路径为：{}'.format(points[0], j, aco.way_len_best, aco.way_data_best))
        path_data_l.append([points[0], j, aco.way_len_best, aco.way_data_best])
    return path_data_l


if __name__ == "__main__":
    ###################################################################################
    # 参数导入与获取
    m = Map()
    m.load_map_file('map.txt')
    map_data = m.data  # map_data为numpy数组
    result_figure = ShanGeTu(map_data)  # 加载地图数据

    points = [[0, 0], [16, 10], [4, 9], [10, 11]]
    ###################################################################################

    ###################################################################################
    # 背景选择
    blank = result_figure.white_BG()  # 空白背景
    shangetu = result_figure.shangetu_BG()  # 栅格背景
    shangetu_bar = result_figure.barrier(Surface=blank)  #
    shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点
    ###################################################################################

    ###################################################################################
    # 控制台打印
    path_data_l = []
    for i in range(len(points) - 1):
        path_data_l = cycle_run(map_data=map_data, points=points)
        points = points[1::]
    # print(path_data_l)
    with open('path_data.txt', mode='w') as f:
        # path_data依次为，起点，终点，路径长度，路径列表
        for path_data in path_data_l:
            f.write(str(path_data[0]) + ' ' + str(path_data[1]) + ' '
                    + str(path_data[2]) + ' ' + str(path_data[3]) + '\n')

    # f.write(str(points[0]) + '' + str(i) + '' + str(distance_l[points.index(i) - 1])
    #             + '\n')
    # print('{}最近的点为：{}，距离为：{}'.format(
    #     points[0], points[distance_l.index(min(distance_l)) + 1], min(distance_l)))

    # path_list.append(best_path_l[distance_l.index(min(distance_l))])

    # 实际的路径
    # print(path_list)
    ###################################################################################
    way_picture = plot_total_path(Surface=shangetu_bar_goal, path_list=path_list)  # 形式[[路径1],[路径2]]
    result_figure.save(Surface=way_picture)
    ###################################################################################
