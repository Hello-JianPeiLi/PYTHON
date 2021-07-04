from multiprocessing import Process
from time import sleep


def test1(msg):
    for i in range(5):
        print("---进程1---%s" % msg)
        sleep(1)


def test2(msg):
    for i in range(5):
        print("---进程2---%s" % msg)
        sleep(1)


def main():
    p1 = Process(target=test1, args=("Nihao",))
    p2 = Process(target=test2, args=("libai",))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
