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
    times = 5

    omiga = 1.0
    gama = 1.0

    active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list=points_list)
    heu_mat = (gama * dis_mat * 1000 + omiga * bat_mat)

    # 绘图内容
    ACO_first(points_list=points_list, datas=dis_datas, heu_mat=heu_mat,
              max_battery=10800, consume=20, thred=0.2, v=0.5, eff=30,
              num_iterations=200, alpha=1.5, beta=0.2, rho=0.5, Q=1500.0, iteration_fig='True'
              )
    # alpha: 信息素
    # beta: 启发式距离
    # Q: 每代更新因子 * 启发式距离
