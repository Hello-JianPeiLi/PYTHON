import os
import multiprocessing
from icecream import ic
import time

copy_file_num = list()


def copy_file(q, file_name, old_folder, new_folder):
    old_f = open(old_folder + "/" + file_name, "rb")
    content = old_f.read()
    old_f.close()

    new_f = open(new_folder + "/" + file_name, "wb")
    new_f.write(content)
    new_f.close()

    q.put(file_name)
    # ic("从[%s]的文件夹的[%s]文件复制到新文件夹---%s" % (old_folder, file_name, new_folder))


def main():
    start_time = time.time()
    # old_folder = input("请输入要复制的文件夹名：")
    old_folder = "test"
    try:
        new_folder = old_folder + "[复件]"
        os.mkdir(new_folder)
    except:
        pass
    file_names = os.listdir(old_folder)
    po = multiprocessing.Pool(5)
    q = multiprocessing.Manager().Queue()
    for file_name in file_names:
        po.apply_async(copy_file, args=(q, file_name, old_folder, new_folder,))
    po.close()
    # po.join()
    all_files = len(file_names)
    copy_ok_num = 0
    file_list = list()
    while True:
        file_name = q.get()
        file_list.append(file_name)
        # ic("已完成第---%d---%s的复制" % (copy_ok_num, file_name))
        copy_ok_num += 1
        # ic(copy_ok_num)
        # ic(all_files)
        # ic(len(file_list))
        print("\r完成进度%.f%%" % ((copy_ok_num / all_files) * 100), end="")
        if copy_ok_num >= all_files:
            break
    end_time = time.time()
    print("耗时%d" % (end_time - start_time))


if __name__ == '__main__':
    main()
