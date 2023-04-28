"""
************************
***  author:Yeller   ***
***  date:2023/04/21 ***
************************
"""
import time

import numpy as np
from .Tools import charge_and_get_bat_mat
from .Ant import ACO_first


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
    rho = 0.1
    num_iterations = 100

    y_lab = []
    for arg in arg_l:
        start = time.time()
        tem_Gains = []
        # 设置模拟充电周期数
        for i in range(times):
            dis_mat = arg[1]
            dis_datas = arg[2]
            active_points_list, bat_mat = charge_and_get_bat_mat(arg[3], max_battery=max_battery, thred=thred)
            heu_mat = 1000 * gama * dis_mat + omiga * bat_mat
            tem_Gains.append(ACO_first(points_list=active_points_list, datas=dis_datas,
                                       max_battery=max_battery, consume=consume, v=v, eff=eff, thred=thred,
                                       heu_mat=heu_mat, alpha=alpha, beta=beta, rho=rho, num_iterations=num_iterations))
        end = time.time()
        print('单次变量的执行时间为:{}'.format(end-start))
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

