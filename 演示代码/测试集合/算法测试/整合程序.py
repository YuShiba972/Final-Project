"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
from matplotlib import pyplot as plt

from ArcRouting import Point
import random
import numpy as np


def read_dis(filename, points_list):
    """
    @filename: 带有location和distance的文件 @points_list: 点的列表
    """
    datas = []
    dis_l = []
    n = len(points_list)
    # 按顺序读取数据存入列表
    with open(filename, 'r') as f:
        for line in f:
            datas.append(eval(line))
    # 按顺序存入距离列表
    for data in datas:
        dis_l.append(data[2])

    # 建立距离矩阵(含起点)
    dis_origin = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:  # 左对角线元素为0
                dis_origin[i][j] = 0
            else:  # 其他元素填入列表中的元素
                if dis_l:
                    dis_origin[i][j] = dis_l.pop(0)
                else:
                    dis_origin[i][j] = 0
    # 优化距离矩阵(不含起点)
    dis_mat = dis_origin[1:n, 1:n]
    return dis_mat


def read_battery(points_list, max_battery=10800, consume=200, thred=0.2, v=1):
    goals_l = points_list[1::]
    origin_energy = []
    n = len(goals_l)
    # 随机生成能量
    for i in range(len(goals_l)):
        origin_energy.append(random.randint(int(thred * max_battery), max_battery))
    # 能量、消耗数据注入点类
    for k, point in enumerate(goals_l):
        point.battery = origin_energy[k]
        point.consume = consume
    # 生成电量列表
    bat_l = list(map(lambda x: x.battery, goals_l))
    # 生成电量矩阵
    bat_mat = np.repeat([bat_l], 3, axis=0)
    # 优化电量矩阵，将左对角线元素替换至超大值
    np.fill_diagonal(bat_mat, max_battery * 20)
    return bat_mat


def aco(points_list, Eta):
    cities = list(map(lambda x: x.location, points_list[1::]))  # 城市坐标矩阵

    n = len(cities)  # 城市数量
    m = int(n * 1.5)  # 蚂蚁数量，取城市数的1.5倍
    NC = 0  # 迭代计数器，从0开始，表示第NC+1次迭代
    NC_MAX = 10  # 最大迭代次数，取100~500之间
    ALPHA = 1  # 常数，α，信息素启发式因子
    BETA = 5  # 常数，β，期望启发因子
    RHO = 0.1  # 常数，ρ，信息素蒸发系数
    Q = 100  # 常数，信息素强度
    Best_Path = np.zeros((NC_MAX, n))  # NC_MAX*n矩阵，记录NC_MAX次迭代的所求最佳路径，每条记录表示一次迭代所的最优路径
    Best_Path_Len = np.zeros((NC_MAX, 1))  # NC_MAX*1矩阵，记录每次的最佳路径长度
    Best_Path_Len[:, :] = np.inf  # 所有元素暂时赋值为inf
    Best_Path_Len_Average = np.zeros((NC_MAX, 1))  # 最优路径长度平均
    Table_Phe = np.ones((n, n))  # n * n 信息素矩阵，初始值都为1
    Table_Path = np.zeros((m, n))  # m * n 路径记录表

    Distance = Eta

    # 2.迭代寻找最佳路径
    while NC < NC_MAX:
        print(f"第{NC + 1}次迭代")
        # 2.1 m只蚂蚁随机选取出生点
        Start = np.zeros((m, 1))  # 蚂蚁随机出生点矩阵，m行
        for i in range(0, m):
            Start[i] = random.randint(0, n - 1)  # 生成随机城市，m个    ###生成m个蚂蚁随机降落的城市
        Table_Path[:, 0] = Start[:, 0]  # 将各蚂蚁放到各自起始城市

        # 2.2 m只蚂蚁逐个选择路径
        Cities_Index = np.array(range(0, n))  # 记录各个城市的索引
        for i in range(0, m):  # m只蚂蚁循环
            for j in range(1, n):  # 每只蚂蚁对n个城市逐个访问
                Visited = Table_Path[i, 0:j]  # 将该只访问过的城市保存到矩阵Visited中
                Unvisited = np.zeros((1, n - j))  # 创建未访问城市的记录矩阵Unvisited
                P = np.zeros((1, n - j))  # 创建未访问城市的访问概率矩阵P
                count = 0  # 计数器
                # 逐个城市检索，将未访问的城市放到Unvisited表中
                for k in range(0, n):
                    if k not in Visited:
                        Unvisited[:, count] = k
                        count += 1
                    if len(Visited)==len(cities):
                        return 0
                # 根据公式计算概率
                for z in range(0, Unvisited.size):
                    tao_x = Visited[Visited.size - 1]
                    tao_y = Unvisited[:, z]
                    tao = np.power(Table_Phe[int(tao_x), int(tao_y)], ALPHA)
                    eta_x = Visited[Visited.size - 1]
                    eta_y = Unvisited[:, z]
                    eta = np.power(Eta[int(eta_x), int(eta_y)], BETA)
                    P[0, z] = tao * eta
                P = P / (np.sum(P))
                # 轮盘赌法，按概率选择下一个城市
                Pcum = np.cumsum(P)
                Select = np.argwhere(Pcum > random.random())
                to_visit = Unvisited[:, int(Select[0])]
                Table_Path[i, j] = to_visit  # 将代访问城市加入Table_Path矩阵，代表该城市被访问

        # 2.3.记录本次迭代最佳路线
        Length = np.zeros((m, 1))  # m*1矩阵，记录每只蚂蚁的路径长度
        for i in range(0, m):  # 计算每只蚂蚁的路径长度
            Route = Table_Path[i, :]  # 在Table_Path表中找到该蚂蚁的路径行，将整行赋给Route
            for j in range(0, n - 1):  # 对路径长度求和
                Length[i] = Length[i] + Distance[int(Route[j]), int(Route[j + 1])]
            Length[i] = Length[i] + Distance[int(Route[0]), int(Route[n - 1])]  # 从最后一个节点回到起点的距离

        if NC == 0:  # 第一次迭代
            min_length = np.min(Length)  # m只蚂蚁路径长度最小值
            min_index = np.argmin(Length)  # 最小值索引
            Best_Path[NC, :] = Table_Path[min_index, :]  # 最优路径表
            Best_Path_Len[NC, :] = min_length  # 最优路径长度为最小值
            Best_Path_Len_Average[NC, :] = np.mean(Length)  # 求平均
            print(f"最短路径：{Best_Path_Len[NC, :]}")
        else:  # 第NC次迭代
            min_length = np.min(Length)
            min_index = np.argmin(Length)
            Best_Path_Len[NC, :] = min(Best_Path_Len[NC - 1], min_length)
            Best_Path_Len_Average[NC, :] = np.mean(Length)
            if Best_Path_Len[NC, :] == min_length:
                Best_Path[NC, :] = Table_Path[min_index, :]
            else:
                Best_Path[NC, :] = Best_Path[NC - 1, :]
            print(f"最短路径：{Best_Path_Len[NC, :]}")

        # 2.4.更新信息素
        Delta_Table_Phe = np.zeros((n, n))  # 信息素变化量矩阵
        for i in range(0, m):
            for j in range(0, n - 2):
                Delta_Table_Phe[int(Table_Path[i, j]), int(Table_Path[i, j + 1])] \
                    = Delta_Table_Phe[int(Table_Path[i, j]), int(Table_Path[i, j + 1])] + Q / Length[i, :]
            Delta_Table_Phe[int(Table_Path[i, n - 2]), int(Table_Path[i, 0])] \
                = Delta_Table_Phe[int(Table_Path[i, n - 2]), int(Table_Path[i, 0])] + Q / Length[i, :]
        Table_Phe = (1 - RHO) * Table_Phe + Delta_Table_Phe

        # 2.5. 禁忌表清零
        Table_Path = np.zeros((m, n))
        print("*" * 100)
        NC = NC + 1  # 进入下一次迭代

    # 3. 迭代结束，结果输出
    shortest_length = np.min(Best_Path_Len)  # 在Best_Path_Len中找出最短长度
    shortest_index = np.argmin(Best_Path_Len)  # 取得该最短长的的路径在Best_Path_Len中的位置
    print(Best_Path)
    Shortest_Route = Best_Path[shortest_index, :]  # 根据位置在bast_path中找到该路径
    print(f"最短路径：{Shortest_Route + 1}")
    print(f"最短路径长度：{shortest_length}")

    # 4.可视化输出
    # 4.1 最短路径可视化
    # 创建窗口
    fig1 = plt.figure(figsize=(10, 8), dpi=120)  # 这只图片大小 figsize(len,width),dpi设置像素值

    # 准备数据
    x = []  # 存放各城市横坐标
    y = []  # 存放各城市纵坐标
    for i in range(0, len(cities)):  # 取值
        route = cities[int(Shortest_Route[i])]
        x.append(route[0])
        y.append(route[1])

    # 绘制坐标
    plt.xticks(np.arange(0, 5000, 500))
    plt.yticks(np.arange(0, 5000, 500))

    plt.xlabel("x")
    plt.ylabel("y")

    plt.title("最优路径图")
    c = 0
    for i, j in zip(x, y):  # 给各个点标注
        plt.text(i + 0.1, j + 0.3, str(int(Shortest_Route[c] + 1)), ha='center', va='bottom',
                 fontsize=10.5)
        c += 1

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 解决matplotlib不显示中文
    plt.grid(alpha=0.2)  # 绘制网格,alpha=0.2表示透明度

    # 画图
    plt.plot(x, y, color='orange')
    plt.scatter(x, y, c='black', marker='o')

    end2Start_x = [x[len(x) - 1], x[0]]
    end2Start_y = [y[len(y) - 1], y[0]]
    plt.plot(end2Start_x, end2Start_y, color='orange')  # 连接终点和起点，形成回路

    # 展示
    plt.show()

    # 4.2 各代最短路径和平均距离可视化
    fig2 = plt.figure(figsize=(10, 8), dpi=120)  # 这只图片大小 figsize(len,width),dpi设置像素值
    it = range(0, NC_MAX)  # 迭代次数
    d = Best_Path_Len.tolist()  # 距离
    a_ave = Best_Path_Len_Average.tolist()  # 平均距离
    plt.xticks(np.arange(0, NC_MAX, 20))
    plt.yticks(np.arange(1.5e+4, 2.2e+4, 1000))
    plt.xlabel("迭代次数")
    plt.ylabel("距离")
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 解决matplotlib不显示中文
    plt.grid(alpha=0.2)  # 绘制网格,alpha=0.2表示透明度
    plt.plot(it, d, color='b', ls='-', label="各代最大收益比")
    plt.plot(it, a_ave, color='y', ls='-', label="各代平均收益比")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    ###########################################################
    # 节点类初始化
    A = Point.Point(name='A', location=[0, 0])
    # 初始化目标点
    B = Point.Point(name='B', location=[16, 10])
    C = Point.Point(name='C', location=[4, 9])
    D = Point.Point(name='D', location=[10, 11])
    points_list = [A, B, C, D]
    ###########################################################
    dis_mat = read_dis('mapss.txt', points_list)
    bat_mat = read_battery(points_list)
    # "目标点"的启发函数矩阵，
    heu_mat = dis_mat / bat_mat
    print(heu_mat)
    aco(points_list, heu_mat)
