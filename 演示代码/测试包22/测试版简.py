"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""

from Source_Package.Draw_Package import *
from Source_Package.Base_Package import *

if __name__ == "__main__":
    # 点列表，距离文件
    bar_file = 'Source_Package/map10.txt'
    dis_file = 'Source_Package/distance10.txt'  # 若已生成可复用

    # 随机产生点
    # points_list = generate_points(bar_file, 6)
    # draw_map(points_list, bar_file)
    #
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    # dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    # 预先定位点
    points_list = Point.points_ori()
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    draw_map(points_list, bar_file)


    # 绘图参数
    threds = [x / 10 for x in range(5)]
    consumes = [2, 4, 6, 8, 10]
    max_batteries = list(range(3000, 20001, 1000))
    times = 10
    # 绘图内容
    thresholdx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/门限')
    max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/电量')
    consumex(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/消耗')