"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import multiprocessing

from Tools_Package.Draw_Package import *
from Tools_Package.Base_Package import *

# 点列表，距离文件
bar_file = 'Source_Package/Map_In10.txt'  # 禁行区文件
points_list = Point.points15_bar10()  # 目标点列表
dis_file = 'Source_Package/Distance_15Points_In10.txt'  # 路径文件

if __name__ == "__main__":
    # 绘制实验节点分布图
    # draw_map(bar_data_file=bar_file, points=points_list, filename='Result_Package/测试节点分布图.jpg')

    # 路径文件生成函数，已生成可直接复用
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    # 读取路径文件获取路径数据
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)

    # 绘图变量
    threds = [x / 10 for x in range(1, 6)]
    consumes = [5, 10, 15, 20, 25]
    max_batteries = list(range(7000, 15001, 1000))
    times = 10

    threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,va_list=threds, times=times,
              out_file='Result_Package/门限变量')

    # # 绘图内容
    # p1 = multiprocessing.Process(
    #     threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #               va_list=threds, times=times, filename='Result_Package/门限变量'))
    # p2 = multiprocessing.Process(
    #     max_battery(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #                  va_list=max_batteries, times=times, filename='Result_Package/电量变量'))
    # p3 = multiprocessing.Process(
    #     consume(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #              va_list=consumes, times=times, filename='Result_Package/消耗变量'))
    #
    # # 启动进程
    # p1.start()
    # p2.start()
    # p3.start()
    #
    # # 等待进程结束
    # p1.join()
    # p2.join()
    # p3.join()
