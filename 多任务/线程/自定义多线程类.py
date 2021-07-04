import threading
from time import sleep


class MyThread(threading.Thread):
    def __init__(self, name="Python"):
        super(MyThread, self).__init__()
        self.name = name

    def run(self) -> None:
        t1 = threading.Thread(target=self.song)
        t2 = threading.Thread(target=self.dance)
        t1.start()
        t2.start()

    def song(self):
        for i in range(3):
            sleep(1)
            print("---我在唱歌---")

    def dance(self):
        for i in range(3):
            sleep(1)
            print("---我在跳舞---")

    def test(self):
        self.song()
        self.dance()


if __name__ == '__main__':
    t = MyThread()
    t.start()
    sleep(1)
    print("---1---")
    t.test()
