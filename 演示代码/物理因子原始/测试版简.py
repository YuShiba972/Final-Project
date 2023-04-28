"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import matplotlib.pyplot as plt
from Source_Package.Draw_Package import *
from Source_Package.Base_Package import *

bar_file = 'Source_Package/Map_In10.txt'
dis_file = 'Source_Package/Distance_15Points_In10.txt'  # 若已生成可复用
points_list = Point.points15_bar10()
if __name__ == "__main__":
    # 绘制实验节点分布图
    # draw_map(bar_data_file=bar_file, points=points_list, filename='Result_Package/测试节点分布图.jpg')
    # 路径文件生成函数，已生成可直接复用
    # ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file)
    # 通过路径文件获取路径信息
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)

    # 绘图参数
    threds = [x / 10 for x in range(1, 6)]
    consumes = [5, 10, 15, 20, 25]
    max_batteries = list(range(7000, 15001, 1000))

    times = 5
    # 绘图内容
    thresholdx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/门限')
    # max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #              va_list=max_batteries, va_name='电量', times=times, filename='Result_Package/电量')
    # consumex(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #          va_list=consumes, va_name='消耗', times=times, filename='Result_Package/消耗')
