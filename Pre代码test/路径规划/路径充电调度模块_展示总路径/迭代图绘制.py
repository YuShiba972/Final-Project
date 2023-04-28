"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""

from Tools_Package.Draw_Package import *
from Tools_Package.Base_Package import *

# 输入文件
bar_file = '../蚁群避障模块_展示多图一对多/Source_Package/map10.txt'  # 禁行区文件
dis_file = 'Tools_Package/Distance_40Points_In10.txt'  # 路径文件
points_list = Point.points40_bar10()

# 启发矩阵参数
omiga, gama = 1.0, 1000.0
# 迭代次数
num_iterations = 200

if __name__ == "__main__":

    ##########################################################
    # 读取路径文件获取路径数据
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    # 生成节点初始能量矩阵
    active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
    # 启发式矩阵构建
    heu_mat = gama * dis_mat + omiga * bat_mat

    print('------路径规划开始------')
    best_path_points = []
    # 蚁群类初始化
    ant = AntColony_ite(heu_mat, num_iterations=num_iterations, num_ants=int(1.5 * heu_mat.shape[0]))

    # 蚂蚁执行
    best_path_index = ant.run()[0]
    print('------路径规划结束------')

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    num_iterations = len(ant.iteration_best)
    x = list(range(num_iterations))
    plt.plot(x, ant.iteration_best, label='最优平衡因子')
    plt.legend()
    plt.xlabel('迭代次数')
    plt.ylabel('平衡因子')
    plt.title('蚁群迭代图-充电调度')
    plt.savefig('Result_Package/蚁群充电调度迭代图')
    plt.show()




