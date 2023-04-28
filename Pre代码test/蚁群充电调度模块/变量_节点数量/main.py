"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
from Tools_Package.Points import *
from Tools_Package.Draw import *
from Tools_Package.Tools import *

if __name__ == "__main__":
    # 文件列表
    bar_file_10 = 'Source_Package/Map_In10.txt'

    dis_file_5 = 'Source_Package/Distance_5Points_In10.txt'  # 若已生成可复用
    dis_file_10 = 'Source_Package/Distance_10Points_In10.txt'  # 若已生成可复用
    dis_file_15 = 'Source_Package/Distance_15Points_In10.txt'  # 若已生成可复用
    dis_file_20 = 'Source_Package/Distance_20Points_In10.txt'  # 若已生成可复用
    dis_file_25 = 'Source_Package/Distance_25Points_In10.txt'  # 若已生成可复用
    dis_file_30 = 'Source_Package/Distance_30Points_In10.txt'  # 若已生成可复用
    dis_file_35 = 'Source_Package/Distance_35Points_In10.txt'  # 若已生成可复用
    dis_file_40 = 'Source_Package/Distance_40Points_In10.txt'  # 若已生成可复用

    points_list5 = Point.points5_bar10()
    points_list10 = Point.points10_bar10()
    points_list15 = Point.points15_bar10()
    points_list20 = Point.points20_bar10()
    points_list25 = Point.points25_bar10()
    points_list30 = Point.points30_bar10()
    points_list35 = Point.points35_bar10()
    points_list40 = Point.points40_bar10()

    dis_datas5, dis_mat5 = get_dis_datas_and_mat(dis_file_5)
    dis_datas10, dis_mat10 = get_dis_datas_and_mat(dis_file_10)
    dis_datas15, dis_mat15 = get_dis_datas_and_mat(dis_file_15)
    dis_datas20, dis_mat20 = get_dis_datas_and_mat(dis_file_20)
    dis_datas25, dis_mat25 = get_dis_datas_and_mat(dis_file_25)
    dis_datas30, dis_mat30 = get_dis_datas_and_mat(dis_file_30)
    dis_datas35, dis_mat35 = get_dis_datas_and_mat(dis_file_35)
    dis_datas40, dis_mat40 = get_dis_datas_and_mat(dis_file_40)

    # 参数列表(节点数量，距离矩阵，距离数据，节点坐标)
    arg_l = [(5, dis_mat5, dis_datas5, points_list5), (10, dis_mat10, dis_datas10, points_list10),
             (15, dis_mat15, dis_datas15, points_list15), (20, dis_mat20, dis_datas20, points_list20),
             (25, dis_mat25, dis_datas25, points_list25), (30, dis_mat30, dis_datas30, points_list30),
             (35, dis_mat35, dis_datas35, points_list35), (40, dis_mat40, dis_datas40, points_list40)]

    #################################################################################

    # 设置循环次数
    times = 3
    plot_result(arg_l, times, shows='multi')   # 关键字参数：shows = 'single'为单图显示，'multi'为多图显示

    #################################################################################


