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
    points = Point.points6_bar10()
    bar_data_file = 'Source_Package/map10.txt'
    Imgname = 'Source_Package/禁行区+目标点.jpg'
    input_file = 'Result_Package/节点避障路径文件.txt'

    #  TODO:   距离文件生成,优化后的生成函数
    # ACO_Generate(bar_data_file=bar_data_file, points=points, filename='Result_Package/节点避障路径文件.txt')

    BarGoal_fig1, BarGoal_Surf1 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')
    BarGoal_fig2, BarGoal_Surf2 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')
    BarGoal_fig3, BarGoal_Surf3 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')
    BarGoal_fig4, BarGoal_Surf4 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')
    BarGoal_fig5, BarGoal_Surf5 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')
    BarGoal_fig6, BarGoal_Surf6 = plot_BarGoal(bar_data_file=bar_data_file, Imgname=Imgname, points=points,
                                               shows='False')

    read(Bg_fig=BarGoal_fig1, Surface=BarGoal_Surf1, po_index=1, input_file=input_file, shows='True')
    read(Bg_fig=BarGoal_fig2, Surface=BarGoal_Surf2, po_index=2, input_file=input_file, shows='True')
    read(Bg_fig=BarGoal_fig3, Surface=BarGoal_Surf3, po_index=3, input_file=input_file, shows='True')
    read(Bg_fig=BarGoal_fig4, Surface=BarGoal_Surf4, po_index=4, input_file=input_file, shows='True')
    read(Bg_fig=BarGoal_fig5, Surface=BarGoal_Surf5, po_index=5, input_file=input_file, shows='True')
    read(Bg_fig=BarGoal_fig6, Surface=BarGoal_Surf6, po_index=6, input_file=input_file, shows='True')
