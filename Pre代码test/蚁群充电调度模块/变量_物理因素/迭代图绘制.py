"""
************************
***  author:Yeller   ***
***  date:2023/03/09 ***
************************
"""
import multiprocessing

from Tools_Package.Draw_Package import *
from Tools_Package.Base_Package import *

# 文件输入
dis_file = 'Source_Package/Distance_15Points_In10.txt'  # 路径文件
dis_datas, dis_mat = Map.get_dis_datas_and_mat(dis_file)  # 读取路径文件获取路径数据
points_list = Point.points15_bar10()  # 目标点列表,测试点:15个传感器节点

# 绘图变量
threds = [0.1, 0.2, 0.3, 0.4]
consumes = [5, 10, 15, 20]
max_batteries = [5000, 10000, 15000, 20000]

if __name__ == "__main__":
    # 绘图内容，指定变量列表，指定输出文件名称
    threshold_ite(points_list=points_list, dis_mat=dis_mat,
                  va_list=threds, out_file='Result_Package/蚁群迭代图-门限变量')
    # max_batteries_ite(points_list=points_list, dis_mat=dis_mat,
    #                   va_list=max_batteries, out_file='Result_Package/蚁群迭代图-最大电量变量')
    # consume_ite(points_list=points_list, dis_mat=dis_mat,
    #             va_list=consumes, out_file='Result_Package/蚁群迭代图-节点工作功率变量')

    # with multiprocessing.Pool(processes=3) as pool:
    #     result1 = pool.apply_async(
    #         threshold_ite(points_list=points_list, dis_mat=dis_mat,
    #                       va_list=threds, out_file='Result_Package/蚁群迭代图-门限变量'))
    #     result2 = pool.apply_async(
    #         max_batteries_ite(points_list=points_list, dis_mat=dis_mat,
    #                           va_list=max_batteries, out_file='Result_Package/蚁群迭代图-最大电量变量'))
    #     result3 = pool.apply_async(
    #         consume_ite(points_list=points_list, dis_mat=dis_mat,
    #                     va_list=consumes, out_file='Result_Package/蚁群迭代图-节点工作功率变量'))
