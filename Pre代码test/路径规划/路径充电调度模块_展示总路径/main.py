"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""

from Tools_Package.Draw_Package import *
from Tools_Package.Base_Package import *

# 输入文件
bar_file = '../蚁群避障模块_展示多图一对多/Source_Package/map10.txt'  # 禁行区文件
dis_file = '../蚁群避障模块_展示多图一对多/Result_Package/节点避障路径文件.txt'  # 路径文件
points_list = Point.points6_bar10()  # 目标点列表,测试点:5个传感器节点
# 启发矩阵参数
omiga, gama = 1.0, 1000.0
# 迭代次数
num_iterations = 200

if __name__ == "__main__":

    #   TODO: 绘制实验节点分布图
    # draw_map(bar_data_file=bar_file, points=points_list,
    #          shows='True', filename='Result_Package/测试节点分布图.jpg')

    ##########################################################
    # 读取路径文件获取路径数据
    dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)
    # 生成节点初始能量矩阵
    active_points_list, bat_mat = Point.charge_and_get_bat_mat(points_list)
    # 启发式矩阵构建
    heu_mat = gama * dis_mat + omiga * bat_mat

    print('------路径规划开始------')
    best_path_points = []
    # 蚁群类初始化
    ant = AntColony(heu_mat, num_iterations=num_iterations, num_ants=int(1.5 * heu_mat.shape[0]))

    # 蚂蚁执行
    best_path_index = ant.run()[0]
    print('------路径规划结束------')
    # ant.plot_iteration_distances()
    for i in best_path_index:
        best_path_points.append(points_list[i])
    best_path_name = list(map(lambda x: x.name, best_path_points))
    best_path_location = list(map(lambda x: x.location, best_path_points))
    print('本次AS-CNP算法规划的最优遍历次序为(节点标识)：', best_path_name)
    print('本次AS-CNP算法规划的最优遍历次序为(节点坐标)：', best_path_location)
    ##########################################################

    ##########################################################
    # 绘图模块 #
    draw_datas = []
    dis_list = []
    # best_path_location.append(points_list[0].location)  # 返回基站路径绘制与否
    print('------开始读取绘图数据------')
    for i in range(len(best_path_location)):
        start = best_path_location[i]
        try:
            end = best_path_location[i + 1]
            for datas in dis_datas:
                if datas[0] == start and datas[1] == end:
                    dis_list.append(datas[2])
                    draw_datas.append(datas[3])
        except:
            print('------结束读取绘图数据------')
    dis_list = [round(i, 2) for i in dis_list]
    print('充电小车行走的单步距离为:{}'.format(dis_list))
    print('充电小车行走的总距离为:{}'.format(round(sum(dis_list), 2)))
    BarGoal_fig, BarGoal_Surf = draw_map(bar_data_file=bar_file, points=points_list,
                                         filename='Result_Package/测试节点分布图.jpg')
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [0, 0, 0]]
    way_picture = None
    for k, i in enumerate(draw_datas):
        if way_picture:
            way_picture = BarGoal_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = BarGoal_fig.draw_way(way_data=i, Surface=BarGoal_Surf, color=route_color[k])
    BarGoal_fig.save(Surface=way_picture, filename='Result_Package/移动充电小车游行图_不含返回基站的路径.jpg')
    image = Image.open('Result_Package/移动充电小车游行图_不含返回基站的路径.jpg')
    image.show()

    ##########################################################################
    # 绘制返回基站的路径
    draw_datas = []
    dis_list = []
    final_location = best_path_location[-1]
    start_location = points_list[0].location
    back_path_location = [final_location, start_location]  # 返回基站路径绘制与否
    print(back_path_location)

    print('------开始读取返回路径绘图数据------')
    start = back_path_location[0]
    end = back_path_location[1]
    for datas in dis_datas:
        if datas[0] == start and datas[1] == end:
            draw_datas = datas[3]
    print('------结束读取返回路径绘图数据------')
    BarGoal_fig, BarGoal_Surf = draw_map(bar_data_file=bar_file, points=points_list, save='False')
    print('移动充电小车游行的返回路径为:', draw_datas)
    way_picture = BarGoal_fig.draw_way(way_data=draw_datas, Surface=BarGoal_Surf, color=[0, 0, 0])
    BarGoal_fig.save(Surface=way_picture, filename='Result_Package/移动充电小车游行图_返回基站的路径.jpg')
    image = Image.open('Result_Package/移动充电小车游行图_返回基站的路径.jpg')
    image.show()

    ###########################################################
    #  绘制带返回基站的路径图
    draw_datas = []
    dis_list = []
    best_path_location.append(points_list[0].location)  # 返回基站路径绘制与否
    print('------开始读取绘图数据------')
    for i in range(len(best_path_location)):
        start = best_path_location[i]
        try:
            end = best_path_location[i + 1]
            for datas in dis_datas:
                if datas[0] == start and datas[1] == end:
                    dis_list.append(datas[2])
                    draw_datas.append(datas[3])
        except:
            print('------结束读取绘图数据------')
    dis_list = [round(i, 2) for i in dis_list]
    BarGoal_fig, BarGoal_Surf = draw_map(bar_data_file=bar_file, points=points_list,
                                         filename='Result_Package/测试节点分布图.jpg')
    route_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [0, 0, 0]]
    way_picture = None
    for k, i in enumerate(draw_datas):
        if way_picture:
            way_picture = BarGoal_fig.draw_way(way_data=i, Surface=way_picture, color=route_color[k])
        else:
            way_picture = BarGoal_fig.draw_way(way_data=i, Surface=BarGoal_Surf, color=route_color[k])
    BarGoal_fig.save(Surface=way_picture, filename='Result_Package/移动充电小车游行图_含返回基站的路径.jpg')
    image = Image.open('Result_Package/移动充电小车游行图_含返回基站的路径.jpg')
    image.show()

