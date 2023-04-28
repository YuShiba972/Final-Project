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
    bar_file = 'map15.txt'
    dis_file = 'distance15.txt'
    # points_list = generate_points(bar_file, 10)
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    # dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    points_list = Point.points5_bar10()
    dis_datas, dis_mat = Map.get_dis_datas_and_mat('distance1.txt')

    # 绘图参数
    threds = [x / 10 for x in range(5)]
    consumes = [50, 100, 150, 200, 250]
    max_batteries = list(range(3000, 10001, 1000))
    times = 20
    # 绘图内容
    threshold(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=threds, va_name='门限', times=times)
    consume(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=consumes, va_name='消耗', times=times)
    max_battery(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat, va_list=max_batteries, va_name='最大电量',
                times=times)
