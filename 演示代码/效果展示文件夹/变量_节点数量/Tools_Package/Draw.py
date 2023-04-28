"""
************************
***  author:Yeller   ***
***  date:2023/04/21 ***
************************
"""
import numpy as np
from .Tools import charge_and_get_bat_mat
from .Ant import ACO_first
from .Ant import AntColony


def plot_result(arg_l, times=10, shows='single'):
    # 节点数量变化
    points_num = [arg[0] for arg in arg_l]
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
    num_iterations = 50

    def ACO_Gain():
        dis_mat = arg[1]
        dis_datas = arg[2]
        active_points_list, bat_mat = charge_and_get_bat_mat(arg[3], max_battery=max_battery, thred=thred)
        heu_mat = 1000 * gama * dis_mat + omiga * bat_mat
        tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                   max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                   heu_mat=heu_mat, alpha=alpha, beta=beta, rho=rho, num_iterations=num_iterations))

    y_lab = []
    for arg in arg_l:
        tem_Gains = []
        # 设置模拟充电周期数
        from multiprocessing import Pool
        with Pool() as pool:
            results = pool.starmap(ACO_Gain, range(times+1))
        tem_Gains.append()
        for i in range(times):
            dis_mat = arg[1]
            dis_datas = arg[2]
            active_points_list, bat_mat = charge_and_get_bat_mat(arg[3], max_battery=max_battery, thred=thred)
            heu_mat = 1000 * gama * dis_mat + omiga * bat_mat
            tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                       max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                       heu_mat=heu_mat, alpha=alpha, beta=beta, rho=rho, num_iterations=num_iterations))
        # 平均增益
        tem_Gains = np.mean(np.array(tem_Gains), axis=0)
        y_lab.append(tem_Gains)

    if shows == 'single':
        # 画图环境设置
        import matplotlib.pyplot as plt
        plt.rc("font", family='FangSong')
        plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
        # 画布/画布背景色
        plt.figure(figsize=(6, 6)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))

        ###################################################################################
        plt.subplot(311)
        # 柱状图绘画
        plt.bar(points_num, [Gain[0] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        # 折线图绘画
        plt.plot(points_num, [Gain[0] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='*', markersize=6, linewidth=1, label='传感器节点数量')
        # 子图背景色
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))
        # 网格显示
        # plt.grid(linestyle='--', linewidth=0.5, color=(166 / 255, 208 / 255, 221 / 255))
        # 网格显示
        plt.grid(axis='y')
        plt.title('收益比与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('收益比')
        # 坐标轴范围限制
        plt.xlim([0, 45])
        plt.ylim()
        # 显示数值标签
        for x, y in zip(points_num, [Gain[0] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=10)
        ###################################################################################
        plt.subplot(312)
        plt.bar(points_num, [Gain[1] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        plt.plot(points_num, [Gain[1] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='o', markersize=6, linewidth=1, label='传感器节点数量')
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))  # 设置背景色
        plt.grid(axis='y')
        plt.title('网络效益与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('网络效益')
        plt.ylim()
        for x, y in zip(points_num, [Gain[1] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(round(y, 2)), ha='center', va='bottom', fontsize=10)

        ###################################################################################
        plt.subplot(313)
        plt.bar(points_num, [Gain[3] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        plt.plot(points_num, [Gain[3] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='o', markersize=6, linewidth=1, label='传感器节点数量')
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))  # 设置背景色
        plt.grid(axis='y')
        plt.title('节点能量方差与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('节点能量方差')
        plt.ylim()
        for x, y in zip(points_num, [Gain[3] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=10)

        # 保存图片
        plt.savefig('Result_Package/节点数量_充电收益_总')
        # 展示图片
        plt.show()

    else:
        # 画图环境设置
        import matplotlib.pyplot as plt
        plt.rc("font", family='FangSong')  # 中文正常显示
        plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
        plt.ion()  # 开启交互窗口，展示图像不停止程序运行
        # 画布/画布背景色
        plt.figure(figsize=(6, 6)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))
        # 柱状图绘画
        plt.bar(points_num, [Gain[0] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        # 折线图绘画
        plt.plot(points_num, [Gain[0] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='*', markersize=6, linewidth=1, label='传感器节点数量')
        # 子图背景色
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))
        # 网格显示
        # plt.grid(linestyle='--', linewidth=0.5, color=(166 / 255, 208 / 255, 221 / 255))
        # 网格显示
        plt.grid(axis='y')
        plt.title('收益比与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('收益比')
        # 坐标轴范围限制
        plt.xlim([0, 45])
        plt.ylim()
        # 显示数值标签
        for x, y in zip(points_num, [Gain[0] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=10)
        # 保存图片
        plt.savefig('Result_Package/节点数量_充电效益比')
        # 展示图片
        plt.show()
        ###################################################################################
        plt.figure(figsize=(6, 6)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))
        plt.bar(points_num, [Gain[1] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        plt.plot(points_num, [Gain[1] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='o', markersize=6, linewidth=1, label='传感器节点数量')
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))  # 设置背景色
        plt.grid(axis='y')
        plt.title('网络效益与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('网络效益')
        plt.ylim()
        for x, y in zip(points_num, [Gain[1] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(round(y, 2)), ha='center', va='bottom', fontsize=10)
        # 保存图片
        plt.savefig('Result_Package/节点数量_网络效益')
        # 展示图片
        plt.show()
        ###################################################################################
        plt.figure(figsize=(6, 6)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))
        plt.bar(points_num, [Gain[3] for Gain in y_lab],
                color=(58 / 255, 152 / 255, 185 / 255), width=1.5)
        plt.plot(points_num, [Gain[3] for Gain in y_lab], linestyle='--',
                 color=(255 / 255, 105 / 255, 105 / 255), marker='o', markersize=6, linewidth=1, label='传感器节点数量')
        plt.gca().set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))  # 设置背景色
        plt.grid(axis='y')
        plt.title('节点能量方差与传感器节点数量关系图')
        plt.xlabel('传感器节点数量')
        plt.ylabel('节点能量方差')
        plt.ylim()
        for x, y in zip(points_num, [Gain[3] for Gain in y_lab]):
            plt.text(x, y + 0.1, str(int(y)), ha='center', va='bottom', fontsize=10)

        # 保存图片
        plt.savefig('Result_Package/节点数量_节点能量方差')
        # 展示图片
        plt.show()

        # 设置键盘键入任意键后关闭图像窗口
        plt.waitforbuttonpress()
        plt.close()


def plot_iteration(arg_l):
    # 节点数量变化
    points_num = [arg[0] for arg in arg_l]
    # 启发式算法参数
    omiga = 1.0
    gama = 1.0
    # 默认模型参数
    max_battery = 10800
    thred = 0.2
    # 默认蚁群参数
    alpha = 5.0  # 信息素重要性
    beta = 2.0  # 启发函数重要性
    rho = 0.1
    num_iterations = 10

    y_lab = []
    for arg in arg_l:
        # 设置模拟充电周期数
        dis_mat = arg[1]
        active_points_list, bat_mat = charge_and_get_bat_mat(arg[3], max_battery=max_battery, thred=thred)
        heu_mat = 1000 * gama * dis_mat + omiga * bat_mat
        ant = AntColony(heu_mat, num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho,
                        num_ants=int(heu_mat.shape[0] * 1.5))
        ant.run()
        iteration_avgbest, iteration_best = ant.iteration_avgbest, ant.iteration_best
        y_lab.append((iteration_avgbest, iteration_best))

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    # 画布/画布背景色
    plt.figure(figsize=(6, 6)).set_facecolor(color=(255 / 255, 255 / 255, 255 / 255))

    ###################################################################################
    plt.subplot(411)
    # 折线图绘画
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[0][0], label='当代平均最优解')
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[0][1], label='当代最优解')

    plt.title('节点数量{}-蚁群迭代图'.format(points_num[0]))
    plt.legend()
    plt.xlabel('蚁群代数')
    plt.ylabel('节点优先级评定参数')
    # 坐标轴范围限制
    plt.xlim()
    plt.ylim()

    plt.subplot(412)
    # 折线图绘画
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[1][0], label='当代平均最优解')
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[1][1], label='当代最优解')

    plt.title('节点数量{}-蚁群迭代图'.format(points_num[1]))
    plt.legend()
    plt.xlabel('蚁群代数')
    plt.ylabel('节点优先级评定参数')
    # 坐标轴范围限制
    plt.xlim()
    plt.ylim()

    plt.subplot(413)
    # 折线图绘画
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[2][0], label='当代平均最优解')
    plt.plot([i for i in range(1, num_iterations + 1)], y_lab[2][1], label='当代最优解')

    plt.title('节点数量{}-蚁群迭代图'.format(points_num[2]))
    plt.legend()
    plt.xlabel('蚁群代数')
    plt.ylabel('节点优先级评定参数')
    # 坐标轴范围限制
    plt.xlim()
    plt.ylim()

    plt.show()
