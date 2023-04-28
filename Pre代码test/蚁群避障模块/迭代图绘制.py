"""
************************
***  author:Yeller   ***
***  date:2023/04/26 ***
************************
"""
from Source_Package.Tools import *

if __name__ == "__main__":
    # 文件输入
    bar_data_file = 'Source_Package/map10.txt'
    out_file = 'Result_Package/蚁群避障迭代图.jpg'
    points = Point.points_ite()

    points_location_list = list(map(lambda x: x.location, points))
    m = Map()
    m.load_map_file(bar_data_file)
    map_data = m.data  # map_data为numpy数组
    draw_datas = []
    for k, i in enumerate(points_location_list):
        try:
            j = points_location_list[k + 1]
        except:
            break
        aco = ACO(map_data=map_data, start=points_location_list[0], end=j,
                  max_iter=50, ant_num=200)
        aco.run()
        draw_datas.append(aco.current_best)

    x = list(range(len(draw_datas[0])))
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示

    plt.subplot(221)
    plt.plot(x, draw_datas[0], label='最优路径长度')
    plt.legend()
    plt.xlabel('蚂蚁迭代次数')
    plt.ylabel('避障路径长度')
    plt.title('蚁群算法迭代图(基站到点(1,18))')

    plt.subplot(222)
    plt.plot(x, draw_datas[1], label='最优路径长度')
    plt.legend()
    plt.xlabel('蚂蚁迭代次数')
    plt.ylabel('避障路径长度')
    plt.title('蚁群算法迭代图(基站到点(19,2))')

    plt.subplot(223)
    plt.plot(x, draw_datas[2], label='最优路径长度')
    plt.legend()
    plt.xlabel('蚂蚁迭代次数')
    plt.ylabel('避障路径长度')
    plt.title('蚁群算法迭代图(基站到点(2,16))')

    plt.subplot(224)
    plt.plot(x, draw_datas[3], label='最优路径长度')
    plt.legend()
    plt.xlabel('蚂蚁迭代数')
    plt.ylabel('路径长度')
    plt.title('蚁群算法迭代图(基站到点(17,5))')

    plt.savefig(out_file)
    plt.show()
