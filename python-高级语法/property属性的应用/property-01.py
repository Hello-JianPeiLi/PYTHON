# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/26 11:25
class Teacher:
    """
    使用property升级getter和setter方法
    """

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("请输入字符串")

    name = property(get_name, set_name)


class Teacher2:
    def __init__(self, age):
        self.age = age


######### 没加property ##########
# tc = Teacher('李白')
# tc2 = Teacher2(19)
# print(tc2.age)
# print(tc.get_name())

######### 加property ##########
tc = Teacher('李黑')
print(tc.name)
# tc.name = "李彩色"
# print(tc.name)
