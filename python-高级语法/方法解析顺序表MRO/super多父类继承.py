# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/19 14:34

"""
使用  父类.__init__()可以调用指定父类，但是如果孙子继承了多个父类，多个父类也都继承了同一个父类，那么就会多次调用父类
"""


class Parent(object):
    def __init__(self, name, *args, **kwargs):
        print("调用父类方法---Parent---init方法")
        self.name = name
        print('我是---Parent---的属性：%s' % self.name)


class Son1(Parent):
    def __init__(self, name, age, *args, **kwargs):
        print("调用---Son1---init方法")
        super().__init__(name, *args, **kwargs)
        self.age = age
        print('我是---Son1---的属性：%s' % self.age)


class Son2(Parent):
    def __init__(self, name, gender, *args, **kwargs):
        print("调用---Son2---init方法")
        # Parent.__init__(self, name)
        super().__init__(name, *args, **kwargs)
        self.gender = gender
        print('我是---Son2---的属性：%s' % self.gender)


class Grandson(Son1, Son2):
    def __init__(self, name, age, gender):
        print("调用---Grandson---init方法")
        # Son1.__init__(self, name, age)
        # Son2.__init__(self, name, gender)
        super().__init__(name, age, gender)


gs = Grandson('grandson', 18, '男')
print(Grandson.__mro__)
