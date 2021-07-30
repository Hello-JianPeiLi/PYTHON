# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/26 11:36
class Teacher:

    def __init__(self, name):
        self.__name = name

    @property
    def get_name(self):
        return self.__name

    @get_name.setter
    def set_name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("请输入字符串")


tc = Teacher('李白')
print(tc.get_name)
tc.set_name = "万不该"
print(tc.get_name)
