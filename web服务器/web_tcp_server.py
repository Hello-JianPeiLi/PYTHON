# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/12 10:03

import socket


def recv_msg(new_socket):
    recv_req = new_socket.recv(1024)
    print(recv_req.decode('utf-8'))


def send_msg(new_socket):
    response = "HTTP/1.1 200 OK\n\r\n\r"
    # with open('./html/index.html', 'rb') as f:
    #     html_content = f.read()
    f = open('./html/index.html', 'rb')
    html_content = f.read()
    f.close()
    # response += "\n\r"
    # response += "<h1>hahah</h2>"
    print(response)
    # print(html_content)
    print('123')
    print(html_content.decode('utf-8'))
    new_socket.send(response.encode('utf-8'))
    new_socket.send(html_content)

    new_socket.close()


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind(("", 7890))
    tcp_socket.listen(128)
    print("---等待客户端连接---")
    while True:
        new_socket, client_addr = tcp_socket.accept()
        recv_msg(new_socket)
        send_msg(new_socket)


if __name__ == '__main__':
    main()
