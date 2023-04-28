# """
# ************************
# ***  author:Yeller   ***
# ***  date:2023/02/20 ***
# ************************
# """
# # 必须可哈希不可变的数据结构：str tuple
# # and和or惰性求值
# # and和or并不一定会返回True或False，而是得到最后一个被计算的表达式的值
# # 运算符not一定会返回True或False
#
#
# test1 = list({'a': 3, 'b': 9, 'c': 78}.items())
# print('test1:', test1, '元组形式')
#
# test2 = list({'a': 3, 'b': 9, 'c': 78}.keys())
# print('test2:', test2)
#
# test3 = list({'a': 3, 'b': 9, 'c': 78}.values())
# print('test3:', test3)
#
# test4 = [x * x * x for x in range(4)]
# print('test4:', test4)
#
# keys, values = ['a', 'b', 'c', 'd'], [1, 2, 3, 4]
# test5 = dict(zip(keys, values))  # zip(函数，映射序列)
# print('test5:', test5)
#
# test6 = 3 and 5
# print('test6:', test6)
#
# test7 = 3 and 5 > 2
# print('test7:', test7)
#
# test8 = isinstance(3.0, int)
# print('test8:', test8)
#
# test9 = isinstance(3.0, (int, float))  # 或
# print('test9:', test9)
#
# test10 = eval('3+5')
# print('test10:', test10)
#
# test11 = eval(str([1, 2, 3, 4]))
# print('test11:', test11)
#
# test12 = list(enumerate(['Python', 'Greate']))  # 元素索引枚举
# print('test12:', test12)
#
# test13 = list(filter(lambda x: x.isalnum(), ['foo', 'x41', '?!', '***']))
# print('test13:', test13)
#
# test14 = list(range(9, 0, -3))
# print('test14:', test14)
#
# test14 = list(zip('123', 'abc', ',.!'))  # 序列映射
# print('test14:', test14)
#
# test15 = list(zip(['a', 'b', 'c'], [1, 2]))
# print('test15:', test15)
#
# # strip() 删除两侧空格
#
# test16 = [i for elem in [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12]] if len(elem) == 3
#           for i in elem if i % 3 == 0]
# print('test16:', test16)
#
# test17 = [3, 5, 7, 9][0:3]  # 切片，不包括最后一位
# print('test17:', test17)
#
# test18 = [7, 8, 9][0:-1]  # -1表示最后一位
# print('test18:', test18)
#
# x = map(str, range(20))
# print(list(x))
# # print()
#
# print({1, 2, 3, 4} > {1, 2, 3})
#
# print([1, 2, 3] < [1, 2, 2, 5])
#
# print(3 and 5 and 5 > 2)  # 最后一个计算的表达式的值作为整个表达式的值
#
# print(max(['a23555', '111']))

# def test(head,feet):
#     rabbit = feet//2-head
#     hen = head - rabbit
#     return rabbit, hen
#
# rabbit,hen =test(4,10)
# print('兔子有{}，鸡有{}'.format(rabbit,hen))

# total = 1
# a = 5
# for i in range(1,a+1):
#     total = total*i
# print(total)

a = input('输入：')
c = list(map(int, a))
sum = 0
for i in c:
    sum = sum +i
print(sum)