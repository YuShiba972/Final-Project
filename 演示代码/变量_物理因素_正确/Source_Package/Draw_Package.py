from matplotlib import pyplot as plt

from 演示代码.测试包66.Source_Package.Base_Package import *
from 演示代码.测试包66.Source_Package.Methods import *


def thresholdx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='门限'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    gama = 1.0
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, thred=va))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, thred=va))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, thred=va,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.figure(figsize=(50,50))


    plt.subplot(222)
    opacity = 0.5
    bar_width = 0.25
    index = np.arange(len(va_list))
    # for name, y_data in data.items():
    #     plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    name = 'NJNP'
    plt.plot(va_list, [Gain[1] for Gain in P_ylabs], 'o--', alpha=0.5, linewidth=1, label=name)
    # plt.bar(index, [Gain[1] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='Variable 1')
    # plt.bar(index + bar_width, [Gain[1] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='Variable 2')
    # plt.bar(index + 2 * bar_width, [Gain[1] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r',
    #         label='Variable 3')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    # plt.xticks(index + bar_width, va_list)
    plt.ylim()

    plt.subplot(223)
    # for name, y_data in data.items():
    #     plt.plot(va_list, [Gain[2] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    name = 'NJNP'
    plt.plot(va_list, [Gain[2] for Gain in P_ylabs], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('休眠比')
    plt.ylim()

    plt.subplot(224)
    opacity = 0.8
    bar_width = 0.25
    index = np.arange(len(va_list))
    # for name, y_data in data.items():
    #     plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    name = 'NJNP'
    plt.plot(va_list, [Gain[3] for Gain in P_ylabs], 'o--', alpha=0.5, linewidth=1, label=name)
    # plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    # plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    # plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r',
    #         label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点剩余能量方差')

    # for i in range(len(va_list)):
    #     plt.text(x=i, y=[Gain[3] for Gain in C_ylabs][i] + 0.1, s=str(int([Gain[3] for Gain in C_ylabs][i])))
    #     plt.text(x=i+bar_width/2, y=[Gain[3] for Gain in P_ylabs][i] + 0.1, s=str(int([Gain[3] for Gain in P_ylabs][i])))
    #     plt.text(x=i+2*bar_width/2, y=[Gain[3] for Gain in ACO_ylabs][i] + 0.1, s=str(int([Gain[3] for Gain in ACO_ylabs][i])))

    plt.xticks(index + bar_width, va_list)
    plt.ylim()

    plt.show()


def max_batteryx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='电量'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    omi = 1.0
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = omi * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, max_battery=va))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, max_battery=va))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, max_battery=va,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)
        # C_Gains,  ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
        #                               np.mean(np.array(tem_ACO_Gain_l), axis=0)
        # C_ylabs.append(C_Gains),  ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.figure()

    plt.subplot(221)
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}
    # data = {'AS-CM': C_ylabs,  'AS-NJNP': ACO_ylabs}

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
    # plt.show()


def consumex(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='消耗'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    omi = 1.0
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = omi * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, consume=va))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, consume=va))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, consume=va,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)
        # C_Gains,  ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
        #                               np.mean(np.array(tem_ACO_Gain_l), axis=0)
        # C_ylabs.append(C_Gains),  ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.figure()

    plt.subplot(221)
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}
    # data = {'AS-CM': C_ylabs,  'AS-NJNP': ACO_ylabs}

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
    plt.show()

def draw_ant_path(points, ant_path, title):
    """
    绘制蚂蚁迭代过程路径图
    :param points: 各城市坐标点
    :param ant_path: 蚂蚁迭代过程中产生的路径
    :param title: 图像标题
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # 绘制各城市坐标点
    xs = [i[0] for i in points]
    ys = [i[1] for i in points]
    ax.scatter(xs, ys)

    # 绘制蚂蚁路径
    for j in range(1, len(ant_path)):
        city_i = ant_path[j - 1]
        city_j = ant_path[j]
        x = [points[city_i][0], points[city_j][0]]
        y = [points[city_i][1], points[city_j][1]]
        ax.plot(x, y, 'r')

    # 添加标题和坐标轴标签
    plt.rcParams['text.usetex'] = True  # 启用LaTeX渲染器
    plt.rcParams['font.family'] = ['SimHei']
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()