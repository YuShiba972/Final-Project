from matplotlib import pyplot as plt

from 演示代码.测试包66.Source_Package.Base_Package import *
from 演示代码.测试包66.Source_Package.Methods import *


def thresholdx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='门限'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    gama = 1.0

    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30

    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, thred=va,
                                             max_battery=max_battery, consume=consume, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, thred=va,
                                           max_battery=max_battery, consume=consume, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, thred=va,
                                            max_battery=max_battery, consume=consume, v=v, eff=eff,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(15, 15))
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    plt.subplot(331)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(332)
    bottom = [0] * len(va_list)  # 初始底部高度
    for name, y_data in data.items():
        plt.fill_between(va_list, bottom, [Gain[0] for Gain in y_data], alpha=0.5, label=name)
        bottom = [Gain[0] for Gain in y_data]  # 更新底部高度
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim(bottom=0)  # y轴下限设为0

    plt.subplot(333)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[0] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[0] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    ##############################################

    plt.subplot(334)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(335)
    bottom = [0] * len(va_list)  # 初始底部高度
    for name, y_data in data.items():
        plt.fill_between(va_list, bottom, [Gain[1] for Gain in y_data], alpha=0.5, label=name)
        bottom = [Gain[1] for Gain in y_data]  # 更新底部高度
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim(bottom=0)  # y轴下限设为0

    plt.subplot(336)
    opacity, bar_width, index = 0.8, 0.25 * 0.1, np.arange(len(va_list)) * 0.1
    plt.bar(index, [Gain[1] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[1] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[1] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    ##############################################

    plt.subplot(337)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[3] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
    plt.ylim()

    plt.subplot(338)
    bottom = [0] * len(va_list)  # 初始底部高度
    for name, y_data in data.items():
        plt.fill_between(va_list, bottom, [Gain[3] for Gain in y_data], alpha=0.5, label=name)
        bottom = [Gain[3] for Gain in y_data]  # 更新底部高度
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
    plt.ylim(bottom=0)  # y轴下限设为0

    plt.subplot(339)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点能量方差')
    plt.ylim()

    plt.savefig(filename)

    # 绘制饼图
    # 设置饼图中每个扇形的颜色
    colors = ['blue', 'green', 'red']

    # 创建子图，共len(va_list)个子图
    fig, axs = plt.subplots(1, len(va_list), figsize=(12, 4))

    # 循环绘制每个子图
    for i, va_value in enumerate(va_list):
        # 获取对应x值下C_ylabs，P_ylabs，ACO_ylabs的值
        values = [C_ylabs[i][0], P_ylabs[i][0], ACO_ylabs[i][0]]
        # 绘制饼图
        axs[i].pie(values, colors=colors, labels=data.keys(), autopct='%1.1f%%', startangle=90)
        axs[i].axis('equal')
        axs[i].set_title(f'{va_name}={va_value}')
    plt.suptitle('节点能量方差占比')
    plt.savefig(filename + 'PIE')
    # plt.show()

    # # 设置饼图中每个扇形的颜色
    # colors = ['blue', 'green', 'red']
    #
    # # 创建子图，共3个子图，每行3个
    # fig, axs = plt.subplots(3, 3, figsize=(12, 12))
    #
    # # 循环绘制每个子图
    # for i, va_value in enumerate(va_list):
    #     # 获取对应x值下C_ylabs，P_ylabs，ACO_ylabs的值
    #     values = [C_ylabs[i][0], P_ylabs[i][0], ACO_ylabs[i][0]]
    #     # 绘制饼图
    #     axs[i // 3, i % 3].pie(values, colors=colors, labels=data.keys(), autopct='%1.1f%%', startangle=90)
    #     axs[i // 3, i % 3].axis('equal')
    #     axs[i // 3, i % 3].set_title(f'{va_name}={va_value}')
    #
    # # 调整子图间距和整体布局
    # plt.subplots_adjust(wspace=0.4, hspace=0.4, left=0.1, right=0.9, top=0.9, bottom=0.1)
    #
    # # 显示图形
    # plt.show()


def max_batteryx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='电量'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    omi = 1.0

    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2

    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = omi * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, max_battery=va,
                                             thred=thred, consume=consume, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, max_battery=va,
                                           thred=thred, consume=consume, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, max_battery=va,
                                            thred=thred, consume=consume, v=v, eff=eff,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.figure(figsize=(12, 5))

    plt.subplot(131)
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)

    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(132)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(133)
    opacity, bar_width, index = 0.8, 0.25 * (va_list[1] - va_list[0]), np.arange(len(va_list)) * (
            va_list[1] - va_list[0])
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点剩余能量方差')
    plt.ylim()

    plt.savefig(filename)


def consumex(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='消耗', ):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    omiga = 1.0
    omi = 1.0

    max_battery = 10800
    v = 0.5
    eff = 30
    thred = 0.2

    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
            active_points_list1 = copy.deepcopy(active_points_list)
            active_points_list2 = copy.deepcopy(active_points_list)
            active_points_list3 = copy.deepcopy(active_points_list)

            heu_mat = omi * dis_mat * 1000 + omiga * bat_mat

            tem_C_Gain_l.append(charge_first(points_list=active_points_list1, datas=dis_datas, consume=va,
                                             thred=thred, max_battery=max_battery, v=v, eff=eff))

            tem_P_Gain_l.append(path_first(points_list=active_points_list2, datas=dis_datas, consume=va,
                                           thred=thred, max_battery=max_battery, v=v, eff=eff))

            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list3, datas=dis_datas, consume=va,
                                            thred=thred, max_battery=max_battery, v=v, eff=eff,
                                            heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.figure(figsize=(12, 5))

    plt.subplot(131)
    data = {'AS-CM': C_ylabs, 'NJNP': P_ylabs, 'AS-CNP': ACO_ylabs}

    for name, y_data in data.items():
        plt.plot(va_list, [Gain[0] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)

    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('收益比')
    plt.ylim()

    plt.subplot(132)
    for name, y_data in data.items():
        plt.plot(va_list, [Gain[1] for Gain in y_data], 'o--', alpha=0.5, linewidth=1, label=name)
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('网络效益')
    plt.ylim()

    plt.subplot(133)
    opacity, bar_width, index = 0.8, 0.25, np.arange(len(va_list))
    plt.bar(index, [Gain[3] for Gain in C_ylabs], bar_width, alpha=opacity, color='b', label='AS-CM')
    plt.bar(index + bar_width, [Gain[3] for Gain in P_ylabs], bar_width, alpha=opacity, color='g', label='NJNP')
    plt.bar(index + 2 * bar_width, [Gain[3] for Gain in ACO_ylabs], bar_width, alpha=opacity, color='r', label='AS-CNP')
    plt.legend()
    plt.xlabel(va_name)
    plt.ylabel('节点剩余能量方差')
    plt.ylim()

    plt.savefig(filename)
    plt.show(block=False)


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


def single_shouyibi(arg_l, times=1):
    points_num = [arg[0] for arg in arg_l]
    omiga = 1.0
    gama = 1.0
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2
    y_lab = []

    for arg in arg_l:
        tem_Gains = []
        for i in range(times):
            dis_mat = arg[1]
            dis_datas = arg[2]
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(arg[3])
            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat
            tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                       max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                       heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))
        tem_Gains = np.mean(np.array(tem_Gains), axis=0)
        y_lab.append(tem_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(10, 10)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))

    plt.subplot(111)
    plt.bar(points_num, [Gain[0] for Gain in y_lab],
            color=(255 / 255, 211 / 255, 176 / 255), width=1.5)
    plt.plot(points_num, [Gain[0] for Gain in y_lab],
             color=(255 / 255, 105 / 255, 105 / 255), marker='*', markersize=6, linewidth=1, label='传感器节点数量')

    plt.gca().set_facecolor(color=(255 / 255, 249 / 255, 245 / 255))  # 设置背景色
    # plt.grid(linestyle='--', linewidth=0.5, color=(166 / 255, 208 / 255, 221 / 255))
    plt.grid(axis='y')
    plt.title('收益比与传感器节点数量关系图')
    plt.xlabel('传感器节点数量')
    plt.ylabel('收益比')
    plt.xlim([0, 45])
    plt.ylim()
    # 显示数值标签
    for x, y in zip(points_num, [Gain[0] for Gain in y_lab]):
        plt.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=10)

    plt.show()
    plt.savefig('收益比随节点数量变化趋势图')


def single_wangluoxiaoyi(arg_l, times=1):
    points_num = [arg[0] for arg in arg_l]
    omiga = 1.0
    gama = 1.0
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2
    y_lab = []

    for arg in arg_l:
        tem_Gains = []
        for i in range(times):
            dis_mat = arg[1]
            dis_datas = arg[2]
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(arg[3])
            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat
            tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                       max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                       heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))
        tem_Gains = np.mean(np.array(tem_Gains), axis=0)
        y_lab.append(tem_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(10, 10))
    plt.subplot(111)
    plt.plot(points_num, [Gain[1] for Gain in y_lab], 'o--', alpha=0.5, linewidth=1)
    plt.xlabel('传感器节点数量')
    plt.ylabel('网络效益')
    plt.ylim()
    plt.savefig('网络效益随节点数量变化趋势图')


def single_fangcha(arg_l, times=1):
    points_num = [arg[0] for arg in arg_l]
    omiga = 1.0
    gama = 1.0
    max_battery = 10800
    consume = 5
    v = 0.5
    eff = 30
    thred = 0.2
    y_lab = []

    for arg in arg_l:
        tem_Gains = []
        for i in range(times):
            dis_mat = arg[1]
            dis_datas = arg[2]
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(arg[3])
            heu_mat = gama * dis_mat * 1000 + omiga * bat_mat
            tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                       max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                       heu_mat=heu_mat, alpha=5.0, beta=2.0, rho=0.5))
        tem_Gains = np.mean(np.array(tem_Gains), axis=0)
        y_lab.append(tem_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(10, 10))
    plt.subplot(111)
    plt.plot(points_num, [Gain[3] for Gain in y_lab], 'o--', alpha=0.5, linewidth=1)
    plt.xlabel('传感器节点数量')
    plt.ylabel('节点能量方差')
    plt.ylim()
    plt.savefig('能量方差随节点数量变化趋势图')
