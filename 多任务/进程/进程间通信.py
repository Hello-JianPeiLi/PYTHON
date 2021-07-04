import multiprocessing


def download_data(q):
    data = [11, 22, 33, 44]
    for temp in data:
        q.put(temp)
    print("数据已存入队列中")


def analysis_data(q):
    waiting_data_list = list()
    while True:
        data = q.get()
        waiting_data_list.append(data)
        if q.empty():
            break
    print(waiting_data_list)


def main():
    multiprocessing.set_start_method('fork')
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=download_data, args=(q,))
    p2 = multiprocessing.Process(target=analysis_data, args=(q,))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
