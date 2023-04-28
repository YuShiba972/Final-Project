
from 演示代码.测试包66.Source_Package.Base_Package import *
from 演示代码.测试包66.Source_Package.Methods import *

def thresholdx(points_list, dis_datas, dis_mat, va_list, va_name, times=30, filename='门限'):
    C_ylabs, P_ylabs, ACO_ylabs = [], [], []
    for va in va_list:
        tem_C_Gain_l, tem_P_Gain_l, tem_ACO_Gain_l = [], [], []
        for i in range(times):
            active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)

            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, thred=va))
            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list, datas=dis_datas, thred=va,
                                            bat_mat=bat_mat, dis_mat=dis_mat))
        # print("*"*100)
        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

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

            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, max_battery=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, max_battery=va))
            tem_ACO_Gain_l.append(ACO_first(points_list=active_points_list, datas=dis_datas, max_battery=va,
                                            bat_mat=bat_mat, dis_mat=dis_mat))

        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)
        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

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
            tem_C_Gain_l.append(charge_first(points_list=active_points_list, datas=dis_datas, consume=va))
            tem_P_Gain_l.append(path_first(points_list=active_points_list, datas=dis_datas, consume=va))
            tem_ACO_Gain_l.append(
                ACO_first(points_list=active_points_list, datas=dis_datas, consume=va, bat_mat=bat_mat, dis_mat=dis_mat))
        C_Gains, P_Gains, ACO_Gains = np.mean(np.array(tem_C_Gain_l), axis=0), \
                                      np.mean(np.array(tem_P_Gain_l), axis=0), \
                                      np.mean(np.array(tem_ACO_Gain_l), axis=0)

        C_ylabs.append(C_Gains), P_ylabs.append(P_Gains), ACO_ylabs.append(ACO_Gains)

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

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
