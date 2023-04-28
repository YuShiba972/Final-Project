# -*- coding: utf-8 -*-
"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""

# "Console.OutputEncoding = Encoding.UTF8"

import matplotlib.pyplot as plt
# # import sys
# # sys.stdout.encoding = 'utf-8'
# from Source_Package.Draw_Package import *
# from Source_Package.Base_Package import *

if __name__ == "__main__":
    # 点列表，距离文件
    bar_file = 'Source_Package/Map_In10.txt'
    dis_file = 'Source_Package/Distance_15Points_In10.txt'  # 若已生成可复用
    points_list = Point.points15_bar10()
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)

    # 绘图参数
    threds = [x / 10 for x in range(1, 6)]
    consumes = [5, 10, 15, 20, 25]
    max_batteries = list(range(7000, 15001, 1000))
    # velocity = [x / 10 for x in range(10, 15)]
    times = 1
    # 绘图内容
    thresholdx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/门限')

    # max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #              va_list=max_batteries, va_name='电量', times=times, filename='Result_Package/电量')
    # consumex(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #          va_list=consumes, va_name='消耗', times=times, filename='Result_Package/消耗')
