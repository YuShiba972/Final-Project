from matplotlib import pyplot as plt
from .Base_Package import *
from .Methods import *


def threshold(points_list, dis_datas, dis_mat, va_list, num_iterations=50, alpha=5.0, beta=2.0, rho=0.5, Q=1.0,
              va_name='传感器节点休眠门限', times=30, filename='休眠门限变化'):
    # 启发式算法参数
    omiga = 1.0
    gama = 1.0

    # 默认模型参数
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2

    # # 默认蚁群参数
    # alpha = 5.0
    # beta = 2.0
    # rho = 0.5
    # Q = 1.0
    # num_iterations = 50

    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        print('执行门限变量测试')
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):

            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list=points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, thred=va,
                                             max_battery=max_battery, consume=consume, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, thred=va,
                                           max_battery=max_battery, consume=consume, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, thred=va,
                                            max_battery=max_battery, consume=consume, v=v, eff=eff, heu_mat=heu_mat,
                                            num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho, Q=Q))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    # 绘图显示参数定义
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(12, 5))

    # 数据字典
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    # 子图1
    plt.subplot(131)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    # 子图2
    plt.subplot(132)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    # 子图3
    plt.subplot(133)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
    plt.ylim()
    plt.savefig(filename)
    plt.show()


def max_batteryx(points_list, dis_datas, dis_mat, va_list, va_name='传感器节点最大电池容量', times=30, filename='电池容量变化'):
    # 启发式算法参数
    omiga = 1.0
    gama = 1.0

    # 默认模型参数
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2

    # 默认蚁群参数
    alpha = 5.0
    beta = 2.0
    rho = 0.5
    Q = 1.0
    num_iterations = 50

    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        print('执行电量变量测试')
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list=points_list, max_battery=max_battery,
                                                                       thred=thred)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, max_battery=va,
                                             thred=thred, consume=consume, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, max_battery=va,
                                           thred=thred, consume=consume, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, max_battery=va,
                                            thred=thred, consume=consume, v=v, eff=eff, heu_mat=heu_mat,
                                            num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho, Q=Q))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    # 绘图显示参数定义
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(12, 5))
    plt.ion()

    # 数据字典
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    # 子图1
    plt.subplot(131)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    # 子图2
    plt.subplot(132)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    # 子图3
    plt.subplot(133)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
    plt.ylim()
    plt.savefig(filename)
    plt.show()


def consumex(points_list, dis_datas, dis_mat, va_list, va_name='传感器节点工作功率', times=30, filename='功率变化'):
    # 启发式算法参数
    omiga = 1.0
    gama = 1.0

    # 默认模型参数
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2

    # 默认蚁群参数
    alpha = 5.0
    beta = 2.0
    rho = 0.5
    Q = 1.0
    num_iterations = 50

    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        print('执行功率变量测试')
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list=points_list, max_battery=max_battery,
                                                                       thred=thred)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, consume=va,
                                             max_battery=max_battery, thred=thred, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, consume=va,
                                           max_battery=max_battery, thred=thred, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, consume=va,
                                            max_battery=max_battery, thred=thred, v=v, eff=eff, heu_mat=heu_mat,
                                            num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho, Q=Q))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    # 绘图显示参数定义
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(12, 5))
    plt.ion()

    # 数据字典
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    # 子图1
    plt.subplot(131)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    # 子图2
    plt.subplot(132)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    # 子图3
    plt.subplot(133)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
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
