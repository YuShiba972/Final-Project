"""
************************
***  author:Yeller   ***
***  date:2023/02/28 ***
************************
"""
from lddya.Draw import ShanGeTu, IterationGraph  # 导入栅格图、迭代图的绘制模块
from lddya.Map import Map  # 导入地图文件读取模块

###################################################################################
m = Map()
m.load_map_file('Map_In10.txt')
map_data = m.data  # map_data为numpy数组
print(map_data)
m, n = 0, 0
for i in map_data:
    for j in i:
        if j == 1:
            n = n + 1
        m = m + 1
print(m, n)
result_figure = ShanGeTu(map_data)  # 加载地图数据
points = [[0, 0], [4, 9], [16, 10], [10, 11]]
blank = result_figure.white_BG()  # 空白背景
shangetu_bar = result_figure.barrier(Surface=blank)  # 修改Surface参数以修改背景
shangetu_bar_goal = result_figure.goal_point(points, Surface=shangetu_bar)  # 画目标点

result_figure.save(Surface=shangetu_bar_goal)
