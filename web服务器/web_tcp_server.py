# -*- coding:utf-8 -*-
# Author: JianPei
# @Time : 2021/07/12 10:03
import socket
import re


def send_msg(new_socket):
    request = new_socket.recv(1024).decode('utf-8')
    # print(request.decode('utf-8'))
    request_lines = request.splitlines()
    ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
    if ret:
        file_name = ret.group(1)
        print("")
        print('->' * 20, file_name)
        if file_name == "/":
            file_name = '/index.html'

    try:
        f = open('./html' + file_name, 'rb')
        html_content = f.read()
        f.close()
    except:

        response = "HTTP/1.1 404 NO FOUND\r\n"
        response += "\r\n"
        response += '<h1>---NOT FOUND PAGE---</h1>'
        new_socket.send(response.encode('utf-8'))
    else:
        response = "HTTP/1.1 200 OK\r\n"
        response += "\r\n"
        # response += "<h1>hahah</h2>"
        # print(html_content)
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

        send_msg(new_socket)


if __name__ == '__main__':
    main()
