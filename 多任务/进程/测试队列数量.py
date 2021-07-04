import multiprocessing
from icecream import ic
import os


def download_file(q):
    data = [11, 22, 33, 44, 55, 66, 77]
    file_names = os.listdir("test")
    data_num = len(file_names)
    for temp in file_names:
        q.put((temp, data_num))


def analysis_data(q):
    num = 0
    while True:
        data, data_num = q.get()
        num += 1
        ic(num)
        ic(data)
        ic(data_num)
        if num >= data_num:
            break


def main():
    multiprocessing.set_start_method('fork')
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=download_file, args=(q,))
    p2 = multiprocessing.Process(target=analysis_data, args=(q,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
