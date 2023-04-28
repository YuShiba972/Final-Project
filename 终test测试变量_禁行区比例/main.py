"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
from Tools_Package.Points import *
from Tools_Package.Draw import *
from Tools_Package.Tools import *
import multiprocessing


def run_multi_ACO_Generate_distance(points_list, num_list=None):
    if num_list is None:
        num_list = [5, 10, 15, 20, 25]

    pool = multiprocessing.Pool(processes=len(num_list))
    for i in num_list:
        bar_file = f'Source_Package/Map_In{i}.txt'
        dis_file = f'Source_Package/Distance_10Points_In{i}.txt'
        # pool.apply_async(run_ACO_Generate_distance, args=(bar_file, dis_file))
        pool.apply_async(
            ACO_Generate_distance(bar_data_file=Map(fp=bar_file).data, points_list=points_list, newtxt=dis_file))

    pool.close()
    pool.join()


# 文件列表
bar_file_5 = 'Source_Package/Map_In5.txt'
bar_file_10 = 'Source_Package/Map_In10.txt'
bar_file_15 = 'Source_Package/Map_In15.txt'
bar_file_20 = 'Source_Package/Map_In20.txt'
bar_file_25 = 'Source_Package/Map_In25.txt'

dis_file_5 = 'Source_Package/Distance_10Points_In5.txt'  # 若已生成可复用
dis_file_10 = 'Source_Package/Distance_10Points_In10.txt'  # 若已生成可复用
dis_file_15 = 'Source_Package/Distance_10Points_In15.txt'  # 若已生成可复用
dis_file_20 = 'Source_Package/Distance_10Points_In20.txt'  # 若已生成可复用
dis_file_25 = 'Source_Package/Distance_10Points_In25.txt'  # 若已生成可复用

points_list15 = Point.points15_bar10()

if __name__ == "__main__":
    run_multi_ACO_Generate_distance(points_list15)

    dis_datas5, dis_mat5 = get_dis_datas_and_mat(dis_file_5)
    dis_datas10, dis_mat10 = get_dis_datas_and_mat(dis_file_10)
    dis_datas15, dis_mat15 = get_dis_datas_and_mat(dis_file_15)
    dis_datas20, dis_mat20 = get_dis_datas_and_mat(dis_file_20)
    dis_datas25, dis_mat25 = get_dis_datas_and_mat(dis_file_25)

    # 参数列表(节点数量，距离矩阵，距离数据，节点坐标)
    arg_l = [(5, dis_mat5, dis_datas5, points_list15), (10, dis_mat10, dis_datas10, points_list15),
             (15, dis_mat15, dis_datas15, points_list15), (20, dis_mat20, dis_datas20, points_list15),
             (25, dis_mat25, dis_datas25, points_list15), ]
    # #################################################################################
    times = 10
    plot_result(arg_l, times)
    #################################################################################

    with multiprocessing.Pool(processes=2) as pool:  # 创建一个最大进程数为2的进程池对象
        pool.apply_async(plot_result, args=(arg_l, times, 'single'))  # 异步提交任务
        pool.apply_async(plot_result, args=(arg_l, times, 'multi'))  # 执行plot_result函数，并传入对应参数
        pool.close()  # 禁止进一步向进程池中提交新任务
        pool.join()  # 阻塞主进程直到所有任务执行完毕
