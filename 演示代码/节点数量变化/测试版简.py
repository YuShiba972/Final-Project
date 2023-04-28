"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import matplotlib.pyplot as plt
from Source_Package.Draw_Package import *
from Source_Package.Base_Package import *


def generate_distance_helper(args):
    bar_file_10 = 'Source_Package/Map_In10.txt'
    points_list, dis_file = args
    ACO_Generate_distance(bar_data_file=Map(fp=bar_file_10).data, points_list=points_list, newtxt=dis_file)


def run_max_batteries(args):
    times = 1
    max_batteries = list(range(7000, 15001, 1000))
    points_list, dis_datas, dis_mat, filename_prefix = args
    max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
                 va_list=max_batteries, va_name='传感器节点最大电池容量', times=times,
                 filename=f'Result_Package/电池容量{filename_prefix}')


def run_thresholdx(args):
    times = 1
    threads = [x / 10 for x in range(1, 6)]
    points_list, dis_datas, dis_mat, filename_prefix = args
    thresholdx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
               va_list=threads, va_name='门限', times=times, filename=f'Result_Package/门限{filename_prefix}')

    # tem_points = generate_points(bar_file_10, 30)
    # draw_map(points_list40, bar_file_10)

    import multiprocessing

    params_list = [(points_list30, dis_file_30),
                   (points_list35, dis_file_35),
                   (points_list40, dis_file_40)]

    processes = [multiprocessing.Process(target=generate_distance_helper, args=(params,)) for params in params_list]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    # 文件列表
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

    dis_datas5, dis_mat5 = Map.get_dis_datas_and_mat(dis_file_5)
    dis_datas10, dis_mat10 = Map.get_dis_datas_and_mat(dis_file_10)
    dis_datas15, dis_mat15 = Map.get_dis_datas_and_mat(dis_file_15)
    dis_datas20, dis_mat20 = Map.get_dis_datas_and_mat(dis_file_20)
    dis_datas25, dis_mat25 = Map.get_dis_datas_and_mat(dis_file_25)
    dis_datas30, dis_mat30 = Map.get_dis_datas_and_mat(dis_file_30)
    dis_datas35, dis_mat35 = Map.get_dis_datas_and_mat(dis_file_35)
    dis_datas40, dis_mat40 = Map.get_dis_datas_and_mat(dis_file_40)

    from multiprocessing import Pool

    threads = [x / 10 for x in range(1, 6)]
    consumes = [5, 10, 15, 20, 25]
    max_batteries = list(range(7000, 15001, 1000))
    # velocity = [x / 10 for x in range(10, 15)]
    # times = 5

    points_list = [points_list20, points_list25, points_list30, points_list35, points_list40]
    dis_datas = [dis_datas20, dis_datas25, dis_datas30, dis_datas35, dis_datas40]
    dis_mat = [dis_mat20, dis_mat25, dis_mat30, dis_mat35, dis_mat40]
    filename_prefix = ['20', '25', '30', '35', '40']

    # args_list = zip(points_list, dis_datas, dis_mat, filename_prefix)
    #
    # with Pool(processes=len(points_list)) as pool:
    #     pool.map(run_thresholdx, args_list)

    arg_l = [(5, dis_mat5, dis_datas5, points_list5), (10, dis_mat10, dis_datas10, points_list10),
             (15, dis_mat15, dis_datas15, points_list15), (20, dis_mat20, dis_datas20, points_list20),
             (25, dis_mat25, dis_datas25, points_list25), (30, dis_mat30, dis_datas30, points_list30),
             (35, dis_mat35, dis_datas35, points_list35), (40, dis_mat40, dis_datas40, points_list40)]
    single_shouyibi(arg_l, 1)
    # single_wangluoxiaoyi(arg_l)
    # single_fangcha(arg_l)
    # import multiprocessing
    # times = 10
    # with multiprocessing.Pool(processes=3) as pool:  # 使用进程池并行执行三个函数
    #     pool.apply_async(single_shouyibi, args=(arg_l, times))
    #     pool.apply_async(single_wangluoxiaoyi, args=(arg_l, times))
    #     pool.apply_async(single_fangcha, args=(arg_l, times))
    #     # 等待所有进程完成
    #     pool.close()
    #     pool.join()

    # thresholdx(points_list=points_list20, dis_datas=dis_datas20, dis_mat=dis_mat20,
    #            va_list=[0.2], va_name='门限', times=times, filename='Result_Package/门限20')
    # max_batteryx(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #              va_list=max_batteries, va_name='电量', times=times, filename='Result_Package/电量')
    # consumex(points_list=points_list, dis_datas=dis_datas, dis_mat=dis_mat,
    #          va_list=consumes, va_name='消耗', times=times, filename='Result_Package/消耗')
