import socket


def main():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(("10.211.55.2", 7890))
    file_name = input("请输入要下载的文件：")
    tcp_client.send(file_name.encode("utf-8"))
    recv_msg = tcp_client.recv(1024)
    if recv_msg:
        with open("[new]" + file_name + ".txt", "wb") as f:
            f.write(recv_msg + "----我是下载的".encode("utf-8"))

    tcp_client.close()


if __name__ == '__main__':
    main()
