import threading
from time import sleep


def song():
    for i in range(5):
        sleep(1)
        print("---我在唱歌---")


def dance():
    for i in range(5):
        sleep(1)
        print("---我在跳舞---")


def main():
    t1 = threading.Thread(target=song)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()
    while True:
        # print(threading.enumerate())
        sleep(1)
        if len(threading.enumerate()) <= 1:
            break


if __name__ == '__main__':
    main()
