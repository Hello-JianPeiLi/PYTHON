import threading
import time

g_num = 0


def test1(num):
    global g_num
    for i in range(num):
        g_num += 1
    print("---test1---%d" % g_num)


def test2(num):
    global g_num
    for i in range(num):
        g_num += 1
    print("---test2---%d" % g_num)


def main():
    t1 = threading.Thread(target=test1, args=(200000,))
    t2 = threading.Thread(target=test2, args=(200000,))
    t1.start()
    t2.start()
    time.sleep(5) 
    print("---main---%d" % g_num)


if __name__ == '__main__':
    main()
