"""
************************
***  author:Yeller   ***
***  date:2023/03/21 ***
************************
"""
from Source_Package.Tools import *

if __name__ == "__main__":
    bar_data_file = 'Source_Package/map10.txt'
    # points = list(map(lambda x: x.location, Point.points6_bar10()))
    points = [[0, 0], [1, 18], [18, 1], [8, 3], [6, 10], [15, 15]]
    #   TODO:   展示栅格图模型.
    Bar_Surf = plot_Bar(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区建模图10.jpg')

    #   TODO:   根据禁行区文件和目标点生成：栅格类和Surface.
    # BarGoal_fig存储栅格类，BarGoal_Surf存储绘图Surface
    BarGoal_fig, BarGoal_Surf = plot_BarGoal(bar_data_file=bar_data_file, Imgname='Result_Package/禁行区+目标点.jpg',
                                             points_location_list=points)

    #   TODO:   根据禁行区文件和目标点，生成单点最短路径文件；如已存在文件则忽略.
    cycle_run(bar_data_file=bar_data_file, out_file='Result_Package/单点路径列表_tem.txt',
              points_location_list=points)  # 生成单点数据并保存文件

    #   TODO:   根据单点最短路径文件，画出图片并保存.
    plot_OneToAll(Bg_fig=BarGoal_fig, Surface=BarGoal_Surf, input_file='Result_Package/单点路径列表_tem.txt',
                  out_file='Result_Package/单点路径展示图.jpg')
