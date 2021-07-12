# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/05 14:13
import time


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


classmate = ClassIterable()
classmate.add("张三")
classmate.add("李四")
classmate.add("王五")
for i in classmate:
    print(i)
    time.sleep(1)
