"""
************************
***  author:Yeller   ***
***  date:2023/02/16 ***
************************
"""
import copy


class Ant():
    def __init__(self, start, end) -> None:
        self.start = start  # 蚂蚁初始位置[y,x] = [0,0],考虑到列表索引的特殊性，先定y，后定x
        self.destination = end  # 默认的终点节点(在run方法中会重新定义该值)
        self.successful = True  # 标志蚂蚁是否成功抵达终点
        self.record_way = [start]  # 路径节点信息记录

    def run(self, map_data, pher_data):
        self.position = copy.deepcopy(self.start)
        # Step 1:不断找下一节点，直到走到终点或者力竭
        for i in range(self.max_step):
            r = self.select_next_node(map_data, pher_data)
            if r == False:
                self.successful = False
                break
            else:
                if self.position == self.destination:
                    break
        else:
            self.successful = False

    def select_next_node(self, map_data, pher_data):
        '''
        Function:
        ---------
        选择下一节点，结果直接存入self.postion，仅返回一个状态码True/False标志选择的成功与否。
        '''
        y_1 = self.position[0]
        x_1 = self.position[1]
        # Step 1:计算理论上的周围节点
        node_be_selected = [[y_1 - 1, x_1 - 1], [y_1 - 1, x_1], [y_1 - 1, x_1 + 1],  # 上一层
                            [y_1, x_1 - 1], [y_1, x_1 + 1],  # 同层
                            [y_1 + 1, x_1 - 1], [y_1 + 1, x_1], [y_1 + 1, x_1 + 1],  # 下一层
                            ]
        # Step 2:排除非法以及障碍物节点
        node_be_selected_1 = []
        for i in node_be_selected:
            if i[0] < 0 or i[1] < 0:
                continue
            if i[0] >= len(map_data) or i[1] >= len(map_data):
                continue
            if map_data[i[0]][i[1]] == 0:
                node_be_selected_1.append(i)
        if len(node_be_selected_1) == 0:  # 如果无合法节点，则直接终止节点的选择
            return False
        if self.destination in node_be_selected_1:  # 如果到达终点旁，则直接选中终点
            self.position = self.destination
            self.record_way.append(copy.deepcopy(self.position))
            map_data[self.position[0]][self.position[1]] = 1
            return True
        # Step 3:计算节点与终点之间的距离，构建距离启发因子
        dis_1 = []  # 距离启发因子
        for i in node_be_selected_1:
            dis_1.append(((self.destination[0] - i[0]) ** 2 + (self.destination[1] - i[1]) ** 2) ** 0.5)
        # Step 3.1:倒数反转
        for j in range(len(dis_1)):
            dis_1[j] = 1 / dis_1[j]

        # Step 4:计算节点被选中的概率
        prob = []
        for i in range(len(node_be_selected_1)):
            p = (dis_1[i] ** self.dis_imp) * (pher_data[y_1 * len(map_data) + x_1][
                                                  node_be_selected_1[i][0] * len(map_data) + node_be_selected_1[i][
                                                      1]] ** self.pher_imp)
            prob.append(p)
        # Step 5:轮盘赌选择某节点
        prob_sum = sum(prob)
        for i in range(len(prob)):
            prob[i] = prob[i] / prob_sum
        rand_key = np.random.rand()
        for k, i in enumerate(prob):
            if rand_key <= i:
                break
            else:
                rand_key -= i
        # Step 6:更新当前位置，并记录新的位置，将之前的位置标记为不可通过
        self.position = copy.deepcopy(node_be_selected_1[k])
        self.record_way.append(copy.deepcopy(self.position))
        map_data[self.position[0]][self.position[1]] = 1
        return True