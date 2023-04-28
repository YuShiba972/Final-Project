"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import matplotlib.pyplot as plt
from Source_Package.Draw_Package import *
from Source_Package.Base_Package import *

if __name__ == "__main__":
    # 点列表，距离文件
    bar_file_5 = 'Source_Package/Map_In5.txt'
    bar_file_10 = 'Source_Package/Map_In10.txt'
    bar_file_15 = 'Source_Package/Map_In15.txt'
    bar_file_20 = 'Source_Package/Map_In20.txt'
    bar_file_25 = 'Source_Package/Map_In25.txt'

    dis_file_5 = 'Source_Package/Distance_5Points_In10.txt'  # 若已生成可复用
    dis_file_10 = 'Source_Package/Distance_10Points_In10.txt'  # 若已生成可复用
    dis_file_15 = 'Source_Package/Distance_15Points_In10.txt'  # 若已生成可复用
    dis_file_20 = 'Source_Package/Distance_20Points_In10.txt'  # 若已生成可复用
    dis_file_25 = 'Source_Package/Distance_25Points_In10.txt'  # 若已生成可复用
    dis_file_30 = 'Source_Package/Distance_30Points_In10.txt'  # 若已生成可复用

    points_list5 = Point.points5_bar10()
    points_list10 = Point.points10_bar10()
    points_list15 = Point.points15_bar10()
    points_list20 = Point.points20_bar10()
    # import multiprocessing
    #
    # # 定义需要并行运行的参数列表
    # params_list = [(points_list5, dis_file_5),
    #                (points_list10, dis_file_10),
    #                (points_list15, dis_file_15),
    #                (points_list20, dis_file_20),
    #                (points_list25, dis_file_25)]
    # # 创建多个进程，并将需要并行运行的函数作为进程的target传入
    # processes = [multiprocessing.Process(
    #     target=lambda args: ACO_Generate_distance(bar_data_file=Map(fp=bar_file_10).data, points_list=args[0],
    #                                               newtxt=args[1]), args=params) for params in params_list]
    # # 启动所有的进程
    # for process in processes:
    #     process.start()
    # # 等待所有进程运行结束
    # for process in processes:
    #     process.join()
    #
    dis_datas5, dis_mat5 = Map.get_dis_datas_and_mat(dis_file_5)
    dis_datas10, dis_mat10 = Map.get_dis_datas_and_mat(dis_file_10)
    # dis_datas15, dis_mat15 = Map.get_dis_datas_and_mat(dis_file_15)
    # dis_datas20, dis_mat20 = Map.get_dis_datas_and_mat(dis_file_20)
    # dis_datas25, dis_mat25 = Map.get_dis_datas_and_mat(dis_file_25)
    # dis_datas30, dis_mat30 = Map.get_dis_datas_and_mat(dis_file_30)

    # # 绘图参数
    threds = [x / 10 for x in range(1, 6)]
    consumes = [5, 10, 15, 20, 25]
    max_batteries = list(range(7000, 15001, 1000))
    # velocity = [x / 10 for x in range(10, 15)]
    times = 1
    # # # # 绘图内容
    thresholdx(points_list=points_list5, dis_datas=dis_datas5, dis_mat=dis_mat5,
               va_list=threds, va_name='门限', times=times, filename='Result_Package/门限5')
    # thresholdx(points_list=points_list10, dis_datas=dis_datas10, dis_mat=dis_mat10,
    #            va_list=threds, va_name='门限', times=times, filename='Result_Package/门限10')
    # thresholdx(points_list=points_list15, dis_datas=dis_datas15, dis_mat=dis_mat15,
    #            va_list=threds, va_name='门限', times=times, filename='Result_Package/门限15')
    # thresholdx(points_list=points_list20, dis_datas=dis_datas20, dis_mat=dis_mat20,
    #            va_list=threds, va_name='门限', times=times, filename='Result_Package/门限20')
    # thresholdx(points_list=points_list25, dis_datas=dis_datas25, dis_mat=dis_mat25,
    #            va_list=threds, va_name='门限', times=times, filename='Result_Package/门限25')

    # max_batteryx(points_list=points_list5, dis_datas=dis_datas5, dis_mat=dis_mat5,
    #              va_list=threds, va_name='最大电量', times=times, filename='Result_Package/最大电量5')
    # max_batteryx(points_list=points_list10, dis_datas=dis_datas10, dis_mat=dis_mat10,
    #              va_list=threds, va_name='最大电量', times=times, filename='Result_Package/最大电量10')
    # max_batteryx(points_list=points_list15, dis_datas=dis_datas15, dis_mat=dis_mat15,
    #              va_list=threds, va_name='最大电量', times=times, filename='Result_Package/最大电量15')
    # max_batteryx(points_list=points_list20, dis_datas=dis_datas20, dis_mat=dis_mat20,
    #              va_list=threds, va_name='最大电量', times=times, filename='Result_Package/最大电量20')
    # max_batteryx(points_list=points_list25, dis_datas=dis_datas25, dis_mat=dis_mat25,
    #              va_list=threds, va_name='最大电量', times=times, filename='Result_Package/最大电量25')

    # max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #              va_list=max_batteries, va_name='电量', times=times, filename='Result_Package/电量')
    # consumex(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #          va_list=consumes, va_name='消耗', times=times, filename='Result_Package/消耗')
