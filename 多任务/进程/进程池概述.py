import multiprocessing
import os
import time
import random


def worker(msg):
    start_time = time.time()
    print("---%s进程开始执行,进程id为---%d" % (msg, os.getpid()))
    time.sleep(random.random())
    end_time = time.time()
    # print(msg, "---进程执行完毕，所耗时间为---%0.2f" % (end_time - start_time))


if __name__ == '__main__':
    po = multiprocessing.Pool(3)
    for i in range(10):
        po.apply_async(worker, (i,))
    print("---start---")
    po.close()
    po.join()
    print("---end---")
