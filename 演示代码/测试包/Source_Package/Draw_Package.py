from 演示代码.测试包.Source_Package.Base_Package import *
from 演示代码.测试包.Source_Package.Methods import *

def threshold(points_list, dis_datas, dis_mat, va_list, va_name, times=30, name='门限'):
    C_ylab1 = []
    C_ylab2 = []
    C_ylab3 = []
    C_ylab4 = []
    P_ylab1 = []
    P_ylab2 = []
    P_ylab3 = []
    P_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []
    for va in va_list:
        # 取100次的平均
        tem_C_Gain1_l, tem_C_Gain2_l, tem_C_Gain3_l, tem_C_Gain4_l = [], [], [], []
        tem_P_Gain1_l, tem_P_Gain2_l, tem_P_Gain3_l, tem_P_Gain4_l = [], [], [], []
        tem_ACO_Gain1_l, tem_ACO_Gain2_l, tem_ACO_Gain3_l, tem_ACO_Gain4_l = [], [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)  # 充电并返回新列表，和电量矩阵
            # 电量优先
            C_Gain1, C_Gain2, C_Gain3, C_Gain4 = charge_first(points_list=active_points_list, datas=dis_datas, thred=va)
            tem_C_Gain1_l.append(C_Gain1)
            tem_C_Gain2_l.append(C_Gain2)
            tem_C_Gain3_l.append(C_Gain3)
            tem_C_Gain4_l.append(C_Gain4)
            # 距离优先
            P_Gain1, P_Gain2, P_Gain3, P_Gain4 = path_first(points_list=active_points_list, datas=dis_datas, thred=va)
            tem_P_Gain1_l.append(P_Gain1)
            tem_P_Gain2_l.append(P_Gain2)
            tem_P_Gain3_l.append(P_Gain3)
            tem_P_Gain4_l.append(P_Gain4)
            # ACO优先
            heu_mat = get_heu_mat(bat_mat, dis_mat)
            # aco = AntColony(heu_mat)  # 蚁群算法初始化
            # best_path, best_distance = aco.run()
            best_path, best_distance = AntColony(heu_mat).run()
            best_points = list(map(lambda x: x, [points_list[i] for i in best_path]))
            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = ACO_first(points_list=best_points, datas=dis_datas, thred=va)
            tem_ACO_Gain1_l.append(ACO_Gain1)
            tem_ACO_Gain2_l.append(ACO_Gain2)
            tem_ACO_Gain3_l.append(ACO_Gain3)
            tem_ACO_Gain4_l.append(ACO_Gain4)

        # 平均值获取
        C_Gain1_avg = np.mean(np.array(tem_C_Gain1_l))
        C_Gain2_avg = np.mean(np.array(tem_C_Gain2_l))
        C_Gain3_avg = np.mean(np.array(tem_C_Gain3_l))
        C_Gain4_avg = np.mean(np.array(tem_C_Gain4_l))

        P_Gain1_avg = np.mean(np.array(tem_P_Gain1_l))
        P_Gain2_avg = np.mean(np.array(tem_P_Gain2_l))
        P_Gain3_avg = np.mean(np.array(tem_P_Gain3_l))
        P_Gain4_avg = np.mean(np.array(tem_P_Gain4_l))

        ACO_Gain1_avg = np.mean(np.array(tem_ACO_Gain1_l))
        ACO_Gain2_avg = np.mean(np.array(tem_ACO_Gain2_l))
        ACO_Gain3_avg = np.mean(np.array(tem_ACO_Gain3_l))
        ACO_Gain4_avg = np.mean(np.array(tem_ACO_Gain4_l))

        # 绘图X、Y
        C_ylab1.append(C_Gain1_avg)
        C_ylab2.append(C_Gain2_avg)
        C_ylab3.append(C_Gain3_avg)
        C_ylab4.append(C_Gain4_avg)

        P_ylab1.append(P_Gain1_avg)
        P_ylab2.append(P_Gain2_avg)
        P_ylab3.append(P_Gain3_avg)
        P_ylab4.append(P_Gain4_avg)

        ACO_ylab1.append(ACO_Gain1_avg)
        ACO_ylab2.append(ACO_Gain2_avg)
        ACO_ylab3.append(ACO_Gain3_avg)
        ACO_ylab4.append(ACO_Gain4_avg)

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, C_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, C_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, C_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, C_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围
    plt.savefig(name)


def max_battery(points_list, dis_datas, dis_mat, va_list, va_name, times=30):
    C_ylab1 = []
    C_ylab2 = []
    C_ylab3 = []
    C_ylab4 = []
    P_ylab1 = []
    P_ylab2 = []
    P_ylab3 = []
    P_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []
    for va in va_list:
        # 取100次的平均
        tem_C_Gain1_l, tem_C_Gain2_l, tem_C_Gain3_l, tem_C_Gain4_l = [], [], [], []
        tem_P_Gain1_l, tem_P_Gain2_l, tem_P_Gain3_l, tem_P_Gain4_l = [], [], [], []
        tem_ACO_Gain1_l, tem_ACO_Gain2_l, tem_ACO_Gain3_l, tem_ACO_Gain4_l = [], [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)  # 充电并返回新列表，和电量矩阵
            # 电量优先
            C_Gain1, C_Gain2, C_Gain3, C_Gain4 = charge_first(points_list=active_points_list, datas=dis_datas,
                                                              max_battery=va)
            tem_C_Gain1_l.append(C_Gain1)
            tem_C_Gain2_l.append(C_Gain2)
            tem_C_Gain3_l.append(C_Gain3)
            tem_C_Gain4_l.append(C_Gain4)
            # 距离优先
            P_Gain1, P_Gain2, P_Gain3, P_Gain4 = path_first(points_list=active_points_list, datas=dis_datas,
                                                            max_battery=va)
            tem_P_Gain1_l.append(P_Gain1)
            tem_P_Gain2_l.append(P_Gain2)
            tem_P_Gain3_l.append(P_Gain3)
            tem_P_Gain4_l.append(P_Gain4)
            # ACO优先
            heu_mat = get_heu_mat(bat_mat, dis_mat)
            aco = AntColony(heu_mat)  # 蚁群算法初始化
            best_path, best_distance = aco.run()
            best_points = list(map(lambda x: x, [points_list[i] for i in best_path]))
            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = ACO_first(points_list=best_points, datas=dis_datas,
                                                                   max_battery=va)
            tem_ACO_Gain1_l.append(ACO_Gain1)
            tem_ACO_Gain2_l.append(ACO_Gain2)
            tem_ACO_Gain3_l.append(ACO_Gain3)
            tem_ACO_Gain4_l.append(ACO_Gain4)

        # 平均值获取
        C_Gain1_avg = np.mean(np.array(tem_C_Gain1_l))
        C_Gain2_avg = np.mean(np.array(tem_C_Gain2_l))
        C_Gain3_avg = np.mean(np.array(tem_C_Gain3_l))
        C_Gain4_avg = np.mean(np.array(tem_C_Gain4_l))

        P_Gain1_avg = np.mean(np.array(tem_P_Gain1_l))
        P_Gain2_avg = np.mean(np.array(tem_P_Gain2_l))
        P_Gain3_avg = np.mean(np.array(tem_P_Gain3_l))
        P_Gain4_avg = np.mean(np.array(tem_P_Gain4_l))

        ACO_Gain1_avg = np.mean(np.array(tem_ACO_Gain1_l))
        ACO_Gain2_avg = np.mean(np.array(tem_ACO_Gain2_l))
        ACO_Gain3_avg = np.mean(np.array(tem_ACO_Gain3_l))
        ACO_Gain4_avg = np.mean(np.array(tem_ACO_Gain4_l))

        # 绘图X、Y
        C_ylab1.append(C_Gain1_avg)
        C_ylab2.append(C_Gain2_avg)
        C_ylab3.append(C_Gain3_avg)
        C_ylab4.append(C_Gain4_avg)

        P_ylab1.append(P_Gain1_avg)
        P_ylab2.append(P_Gain2_avg)
        P_ylab3.append(P_Gain3_avg)
        P_ylab4.append(P_Gain4_avg)

        ACO_ylab1.append(ACO_Gain1_avg)
        ACO_ylab2.append(ACO_Gain2_avg)
        ACO_ylab3.append(ACO_Gain3_avg)
        ACO_ylab4.append(ACO_Gain4_avg)

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, C_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, C_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, C_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, C_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围
    plt.savefig('电量')


def consume(points_list, dis_datas, dis_mat, va_list, va_name, times=30):
    C_ylab1 = []
    C_ylab2 = []
    C_ylab3 = []
    C_ylab4 = []
    P_ylab1 = []
    P_ylab2 = []
    P_ylab3 = []
    P_ylab4 = []
    ACO_ylab1 = []
    ACO_ylab2 = []
    ACO_ylab3 = []
    ACO_ylab4 = []
    for va in va_list:
        # 取100次的平均
        tem_C_Gain1_l, tem_C_Gain2_l, tem_C_Gain3_l, tem_C_Gain4_l = [], [], [], []
        tem_P_Gain1_l, tem_P_Gain2_l, tem_P_Gain3_l, tem_P_Gain4_l = [], [], [], []
        tem_ACO_Gain1_l, tem_ACO_Gain2_l, tem_ACO_Gain3_l, tem_ACO_Gain4_l = [], [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)  # 充电并返回新列表，和电量矩阵
            # 电量优先
            C_Gain1, C_Gain2, C_Gain3, C_Gain4 = charge_first(points_list=active_points_list, datas=dis_datas,
                                                              consume=va)
            tem_C_Gain1_l.append(C_Gain1)
            tem_C_Gain2_l.append(C_Gain2)
            tem_C_Gain3_l.append(C_Gain3)
            tem_C_Gain4_l.append(C_Gain4)
            # 距离优先
            P_Gain1, P_Gain2, P_Gain3, P_Gain4 = path_first(points_list=active_points_list, datas=dis_datas, consume=va)
            tem_P_Gain1_l.append(P_Gain1)
            tem_P_Gain2_l.append(P_Gain2)
            tem_P_Gain3_l.append(P_Gain3)
            tem_P_Gain4_l.append(P_Gain4)
            # ACO优先
            heu_mat = get_heu_mat(bat_mat, dis_mat)
            aco = AntColony(heu_mat)  # 蚁群算法初始化
            best_path, best_distance = aco.run()
            best_points = list(map(lambda x: x, [points_list[i] for i in best_path]))
            ACO_Gain1, ACO_Gain2, ACO_Gain3, ACO_Gain4 = ACO_first(points_list=best_points, datas=dis_datas, consume=va)
            tem_ACO_Gain1_l.append(ACO_Gain1)
            tem_ACO_Gain2_l.append(ACO_Gain2)
            tem_ACO_Gain3_l.append(ACO_Gain3)
            tem_ACO_Gain4_l.append(ACO_Gain4)

        # 平均值获取
        C_Gain1_avg = np.mean(np.array(tem_C_Gain1_l))
        C_Gain2_avg = np.mean(np.array(tem_C_Gain2_l))
        C_Gain3_avg = np.mean(np.array(tem_C_Gain3_l))
        C_Gain4_avg = np.mean(np.array(tem_C_Gain4_l))

        P_Gain1_avg = np.mean(np.array(tem_P_Gain1_l))
        P_Gain2_avg = np.mean(np.array(tem_P_Gain2_l))
        P_Gain3_avg = np.mean(np.array(tem_P_Gain3_l))
        P_Gain4_avg = np.mean(np.array(tem_P_Gain4_l))

        ACO_Gain1_avg = np.mean(np.array(tem_ACO_Gain1_l))
        ACO_Gain2_avg = np.mean(np.array(tem_ACO_Gain2_l))
        ACO_Gain3_avg = np.mean(np.array(tem_ACO_Gain3_l))
        ACO_Gain4_avg = np.mean(np.array(tem_ACO_Gain4_l))

        # 绘图X、Y
        C_ylab1.append(C_Gain1_avg)
        C_ylab2.append(C_Gain2_avg)
        C_ylab3.append(C_Gain3_avg)
        C_ylab4.append(C_Gain4_avg)

        P_ylab1.append(P_Gain1_avg)
        P_ylab2.append(P_Gain2_avg)
        P_ylab3.append(P_Gain3_avg)
        P_ylab4.append(P_Gain4_avg)

        ACO_ylab1.append(ACO_Gain1_avg)
        ACO_ylab2.append(ACO_Gain2_avg)
        ACO_ylab3.append(ACO_Gain3_avg)
        ACO_ylab4.append(ACO_Gain4_avg)

    import matplotlib.pyplot as plt

    plt.rc("font", family='FangSong')  # 中文正常显示
    plt.figure()

    plt.subplot(221)
    plt.plot(va_list, C_ylab1, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab1, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab1, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('收益比')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(222)
    plt.plot(va_list, C_ylab2, '*--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab2, '*--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab2, '*--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('网络效益')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(223)
    plt.plot(va_list, C_ylab3, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab3, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab3, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点休眠比率')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围

    plt.subplot(224)
    plt.plot(va_list, C_ylab4, 'o--', alpha=0.5, linewidth=1, label='MMAS-CM')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, P_ylab4, 'o--', alpha=0.5, linewidth=1, label='NJNP')  # 'bo-'表示蓝色实线，数据点实心原点标注
    plt.plot(va_list, ACO_ylab4, 'o--', alpha=0.5, linewidth=1, label='ACO')  # 'bo-'表示蓝色实线，数据点实心原点标注

    plt.legend()  # 显示上面的label
    plt.xlabel(va_name)  # x_label
    plt.ylabel('节点遍历电量方差')  # y_label
    plt.ylim()  # 仅设置y轴坐标范围
    plt.savefig('消耗')


def thresholdx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='门限'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)

            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list, datas=dis_datas, thred=va,bat_mat=bat_mat,dis_mat=dis_mat))
        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)

        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.figure()

    plt.subplot(221)
    data = {'MMAS-CM': C_ylabs, 'NJNP': P_ylabs, 'ACO': ACO_ylabs}
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(222)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(223)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[2] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('休眠比')
    plt.ylim()

    plt.subplot(224)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[3] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('方差')
    plt.ylim()
    plt.savefig(filename)

def max_batteryx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='电量'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)

            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list, datas=dis_datas, thred=va,bat_mat=bat_mat,dis_mat=dis_mat))
        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)

        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.figure()

    plt.subplot(221)
    data = {'MMAS-CM': C_ylabs, 'NJNP': P_ylabs, 'ACO': ACO_ylabs}
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(222)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(223)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[2] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('休眠比')
    plt.ylim()

    plt.subplot(224)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[3] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('方差')
    plt.ylim()
    plt.savefig(filename)


def consumex(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='消耗'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)

            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list, datas=dis_datas, thred=va,bat_mat=bat_mat,dis_mat=dis_mat))
        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)

        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.figure()

    plt.subplot(221)
    data = {'MMAS-CM': C_ylabs, 'NJNP': P_ylabs, 'ACO': ACO_ylabs}
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(222)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(223)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[2] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('休眠比')
    plt.ylim()

    plt.subplot(224)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[3] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('方差')
    plt.ylim()
    plt.savefig(filename)
