import socket


def send_to_content(new_socket, client_address):
    download_name = new_socket.recv(1024).decode("utf-8")
    print("客户端(%s)要下载的文件是：%s" % (str(client_address), (download_name + ".txt")))
    file_content = None
    try:
        f = open(download_name + ".txt", "rb")
        file_content = f.read()
        print("内容是：", file_content)
        f.close()
    except Exception as ret:
        print("error ---", ret)
        print("没有这个文件")
    if file_content:
        new_socket.send(file_content)


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", 7890))
    tcp_socket.listen(128)
    while True:
        print("---等待客户端连接---")
        new_socket, client_address = tcp_socket.accept()
        send_to_content(new_socket, client_address)
        new_socket.close()
    tcp_socket.close()


if __name__ == '__main__':
    main()
