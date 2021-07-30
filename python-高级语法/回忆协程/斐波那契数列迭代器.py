# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/19 16:39
from collections.abc import Iterable
from collections.abc import Iterator
import time


class Fibs(object):
    def __init__(self, num):
        self.a = 0
        self.b = 1
        self.fibs_list = list()
        self.current_num = 1
        self.num = num

    def __iter__(self):
        return self

    def __next__(self):
        if self.num >= self.current_num:
            self.a, self.b = self.b, self.a + self.b
            ret = self.fibs_list.append(self.a)
            self.current_num += 1
            return self.a
        else:
            raise StopIteration


class ClassIterable(object):
    def __init__(self):
        self.names = list()
        self.num = 0

    def add(self, name):
        self.names.append(name)

    def __iter__(self):
        return self

    def __next__(self):
        if self.num >= len(self.names):
            raise StopIteration
        else:
            ret = self.names[self.num]
            self.num += 1
            return ret


fb = Fibs(10)
ci = ClassIterable()
ci.add("张三")
ci.add("李四")
ci.add("王五")
# for i in ci:
#     print(i)

for i in fb:
    print(i)
print(isinstance(fb, Iterator))


def fibs(num):
    fibs_list = [0, 1]
    for i in range(num - 2):
        print(i)
        fibs_list.append(fibs_list[-2] + fibs_list[-1])
    return fibs_list


print(fibs(10))
