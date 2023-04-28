from .Tools import charge_and_get_bat_mat
from .Ant import AntColony


def plot_ite(args, out_file, num_iterations=50):
    # 启发式算法参数
    omiga = 1.0
    gama = 1.0

    # 默认蚁群参数
    alpha = 5.0
    beta = 2.0
    rho = 0.1

    draw_list = []
    for arg in args:
        print('----执行传感器节点数量为({})的测试----'.format(len(arg[0]) - 1))
        active_points_list, bat_mat = charge_and_get_bat_mat(arg[0])
        heu_mat = gama * arg[1] * 1000 + omiga * bat_mat
        ant = AntColony(heu_mat, num_iterations=num_iterations, alpha=alpha, beta=beta, rho=rho,
                        num_ants=int(heu_mat.shape[0] * 1.5))
        ant.run()

        draw_list.append(
            (len(arg[0]) - 1, list(range(len(ant.iteration_best))), ant.iteration_avgbest, ant.iteration_best))
    print('----绘制蚁群迭代图如下----')

    import matplotlib.pyplot as plt
    plt.rc("font", family='FangSong')
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    plt.figure(figsize=(8, 8))
    linestyle = '-'
    color = 'C1'
    linewidth = 2

    plt.subplot(221)
    plt.plot(draw_list[0][1], draw_list[0][3], label='最优平衡因子', linestyle=linestyle, color=color, linewidth=linewidth)
    plt.legend()
    plt.xlabel('迭代次数')
    plt.ylabel('平衡因子')
    plt.title('传感器节点数量为({})的蚁群迭代图'.format(draw_list[0][0]))

    plt.subplot(222)
    plt.plot(draw_list[1][1], draw_list[1][3], label='最优平衡因子', linestyle=linestyle, color=color, linewidth=linewidth)
    plt.legend()
    plt.xlabel('迭代次数')
    plt.ylabel('平衡因子')
    plt.title('传感器节点数量为({})的蚁群迭代图'.format(draw_list[1][0]))

    plt.subplot(223)
    plt.plot(draw_list[2][1], draw_list[2][3], label='最优平衡因子', linestyle=linestyle, color=color, linewidth=linewidth)
    plt.legend()
    plt.xlabel('迭代次数')
    plt.ylabel('平衡因子')
    plt.title('传感器节点数量为({})的蚁群迭代图'.format(draw_list[2][0]))

    plt.subplot(224)
    plt.plot(draw_list[3][1], draw_list[3][3], label='最优平衡因子', linestyle=linestyle, color=color, linewidth=linewidth)
    plt.legend()
    plt.xlabel('迭代次数')
    plt.ylabel('平衡因子')
    plt.title('传感器节点数量为({})的蚁群迭代图'.format(draw_list[3][0]))

    plt.savefig(out_file)
    plt.show()
