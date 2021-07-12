# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/05 10:54
import os
import multiprocessing


def copy_file(queue, file_name, old_folder, new_folder):
    with open(old_folder + '/' + file_name, "rb") as f:
        content = f.read()
    with open(new_folder + '/' + file_name, "wb") as f:
        f.write(content)
    # print("从%s的文件夹中的文件%s复制到---%s", (old_folder, new_folder, file_name))
    queue.put(file_name)


def main():
    old_folder = input("请输入要复制的文件名：")
    file_names = os.listdir(old_folder)
    try:
        new_folder = old_folder + '[复件]'
        os.mkdir(new_folder)
    except:
        pass
    queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(5)
    for file_name in file_names:
        pool.apply_async(copy_file, (queue, file_name, old_folder, new_folder))
    pool.close()
    # pool.join()
    all_file_num = len(file_names)
    copy_ok_num = 0
    while True:
        copy_ok_num += 1
        print("\r复制进度为:%0.2f%%" % (copy_ok_num * 100 / all_file_num), end="")
        if copy_ok_num >= all_file_num:
            break


if __name__ == '__main__':
    main()
