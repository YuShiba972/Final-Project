"""
************************
***  author:Yeller   ***
***  date:2023/02/16 ***
************************
"""
import copy
import random


def a_star(start, end, raw_map_point_dict, calculate_count=1):
    # 计算次数
    calculate_count = max(calculate_count, 1)
    for _ in range(calculate_count):
        pass
    map_point_dict = copy.deepcopy(raw_map_point_dict)
    # 建立open集合和close集合
    open_dict = {}
    close_dict = {}
    # 初始化地图起点
    map_point_dict[start].G = 0
    map_point_dict[start].H = get_H(start, end)
    map_point_dict[start].F = map_point_dict[start].G + map_point_dict[start].H
    # 把起点加紧open集合里
    open_dict[start] = map_point_dict[start].F
    # open为空时退结束循环
    is_find_end = False
    while open_dict and not is_find_end:
        # 找出F代价最小的作为基点
        base_point = list(list(open_dict.items())[0])
        ''' 随机找法 '''
        equal_list = []
        for key, value in open_dict.items():
            if value < base_point[1]:
                base_point[0] = key
                base_point[1] = value

                equal_list = [base_point]
            elif value == base_point[1]:
                equal_list.append((key, value))
        if equal_list:
            random.shuffle(equal_list)
            base_point = equal_list[0]
        ''' 固定顺序找法 '''
        # for key, value in open_dict.items():
        #     if value < base_point[1]:
        #         base_point[0] = key
        #         base_point[1] = value

        # print(base_point)
        # 把选出来的基点从open集合里去掉
        del open_dict[base_point[0]]
        # 获取基点相邻点坐标
        neighbor_list = []
        neighbor_list.append(('up', (base_point[0][0], base_point[0][1] - 1)))
        neighbor_list.append(('down', (base_point[0][0], base_point[0][1] + 1)))
        neighbor_list.append(('left', (base_point[0][0] - 1, base_point[0][1])))
        neighbor_list.append(('right', (base_point[0][0] + 1, base_point[0][1])))

        # 遍历相邻点（即处理相邻点）
        for key, value in neighbor_list:
            # 超出限定值
            if value[0] < 0 or value[0] > 24 or value[1] < 0 or value[1] > 24:
                continue
            # 判定为障碍物
            if map_point_dict[value].is_obstacle:
                continue
            # 判定该点是否已经在close里，即已经计算过的点
            if value in close_dict:
                continue
            # 判定该点是否已经在open里
            elif value in open_dict:
                new_G = map_point_dict[value].G + map_point_dict[value].neighbor_cost[key]
                if map_point_dict[value].G > new_G:
                    map_point_dict[value].parent_point.append(base_point[0])
                    map_point_dict[value].G = new_G
                    map_point_dict[value].F = new_G + map_point_dict[value].H
            else:
                map_point_dict[value].parent_point.append(base_point[0])
                map_point_dict[value].G = 0 + map_point_dict[value].neighbor_cost[key]
                map_point_dict[value].H = get_H(value, end)
                map_point_dict[value].F = map_point_dict[value].G + map_point_dict[value].H
                open_dict[value] = map_point_dict[value].F
                # 判定是否找到终点
                if value == end:
                    is_find_end = True

        close_dict[base_point[0]] = base_point[1]

    if is_find_end:
        result_path = get_path(start, end, map_point_dict)
        return result_path
    else:
        return []

# 计算终点代价
def get_H(start, end):
    # 计算两点间的距离
    distance = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
    return distance

# 获取路径列表
def get_path(start, end, map_point_dict):
    result_path = []
    result_path.append(end)
    current_point = map_point_dict[end].get_parent()
    while current_point != start:
        result_path.append(current_point)
        current_point = map_point_dict[current_point].get_parent()

    result_path.reverse()
    return result_path


if __name__ == '__main__':
    # 建立地图点25 * 25 (0 ~ 24)
    map_point_dict = {}
    for x in range(25):
        for y in range(25):
            map_point_dict[(x, y)] = MapPoint(x=x, y=y)
    # 输入起点和终点
    start = (0, 0)
    end = (22, 9)
    print(a_star(start, end, map_point_dict))




