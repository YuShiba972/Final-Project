"""
************************
***  author:Yeller   ***
***  date:2023/03/21 ***
************************
"""
"""
    1.展示栅格地图
    2.展示基站、传感器节点
    3.展示1对1避障路径
    4.展示1对多避障路径
    5.展示多图1对多避障路径
    6.生成避障路径文件
"""

from Source_Package.Tools import *

if __name__ == "__main__":
    # 文件输入
    bar_data_file = 'Source_Package/map10.txt'
    points = Point.points6_bar10()

    ###############################################################
    #   TODO:   展示栅格地图模型.
    # shows表示是否打开图片
    # Bar_Surf = plot_Bar(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区建模图10.jpg', shows='True')
    ###############################################################

    ###############################################################
    #   TODO:   展示基站和节点建模.
    # BarGoal_fig存储栅格类，BarGoal_Surf存储绘图Surface
    # BarGoal_fig, BarGoal_Surf = plot_BarGoal(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区+目标点.jpg',
    #                                          points=points, shows='True')
    # ###############################################################

    ###############################################################
    #   TODO:   展示一对一避障最短路径
    # # 根据禁行区文件和目标点，生成单点最短路径文件；如已存在文件则忽略.
    # cycle_run_one(bar_data_file=bar_data_file, out_file='Result_Package/单点对单点路径列表_tem.txt',
    #               points=points)  # 生成单点数据并保存文件

    # BarGoal_fig, BarGoal_Surf = plot_BarGoal(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区+目标点.jpg',
    #                                          points=points, shows='False')
    # # 根据单点最短路径文件，画出图片并保存.
    # plot_OneToOne(Bg_fig=BarGoal_fig, Surface=BarGoal_Surf, input_file='Result_Package/单点对单点路径列表_tem.txt',
    #               out_file='Result_Package/单点对单点路径展示图.jpg', shows='True')
    ###############################################################

    ###############################################################
    # #   TODO:   展示一对多避障最短路径
    # cycle_run(bar_data_file=bar_data_file, out_file='Result_Package/单点对多点路径列表_tem.txt',
    #           points=points)  # 生成单点数据并保存文件
    # BarGoal_fig, BarGoal_Surf = plot_BarGoal(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区+目标点.jpg',
    #                                          points=points, shows='False')
    # plot_OneToAll(Bg_fig=BarGoal_fig, Surface=BarGoal_Surf, input_file='Result_Package/单点对多点路径列表_tem.txt',
    #               out_file='Result_Package/单点对多点路径展示图.jpg', shows='True')
    ###############################################################

    # #   TODO:   距离文件生成
    # ACO_Generate(bar_data_file=bar_data_file,points=points,filename='Result_Package/节点避障路径文件.txt')

