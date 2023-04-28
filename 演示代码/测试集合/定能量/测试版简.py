"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""

from Draw_Package import *
from Base_Package import *

if __name__ == "__main__":
    # 点列表，距离文件
    bar_file = 'testmap.txt'
    dis_file = 'testdistance.txt'
    # points_list = generate_points(bar_file, 6)
    points_list = Point.points5_bar10()
    # draw_map(points_list, bar_file)
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    # points_list = Point.points5_bar10()
    # draw_map(points_list, bar_file)

    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    # dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)

    # 绘图参数
    threds = [x / 10 for x in range(5)]
    # consumes = [0]
    max_batteries = list(range(3000, 10001, 1000))
    times = 1
    # 绘图内容
    threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=threds,
              va_name='门限', times=times, battery=6000, name='门限8000')
    threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=threds,
              va_name='门限', times=times, battery=9000, name='门限9000')
    threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=threds,
              va_name='门限', times=times, battery=10000, name='门限10000')

    # consume(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=consumes,
    #         va_name='消耗', times=times, battery=6000, name='消耗8000')
    # consume(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=consumes,
    #         va_name='消耗', times=times, battery=9000, name='消耗9000')
    # consume(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=consumes,
    #         va_name='消耗', times=times, battery=10000)

    # max_battery(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=max_batteries,
    #             va_name='最大电量', times=times, battery=6000, name='电量8000')
    # max_battery(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=max_batteries,
    #             va_name='最大电量', times=times, battery=9000, name='电量9000')
    # max_battery(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=max_batteries,
    #             va_name='最大电量', times=times, battery=10000, name='电量10000')
